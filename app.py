import boto3
import botocore
import os
from HRNET import HRNET, ModelType, PersonDetector, filter_person_detections
import base64
from datetime import datetime
from tempfile import TemporaryDirectory
import cv2
import json
import numpy as np
import uuid
from decimal import *

# Loaded once per container (warm-start reuse) rather than per invocation. Paths are rooted at
# LAMBDA_TASK_ROOT (/var/task) since the handler later os.chdir()s into a scratch tmp dir.
_MODELS_DIR = os.path.join(os.environ.get("LAMBDA_TASK_ROOT", ".."), "models")
hrnet = HRNET(os.path.join(_MODELS_DIR, "hrnet_coco_w48_384x288.onnx"), ModelType.COCO, conf_thres=0.5)
person_detector = PersonDetector(os.path.join(_MODELS_DIR, "yolov6s.onnx"), conf_thres=0.4, iou_thres=0.5)
def drawPoses(
        img_path: str,
        hrnet: HRNET,
        display: bool = True,
) -> str:
    """Function for getting the data of the current move and next move in a dataframe

  Arguments:
    img_path: path to the input image with the person
    rock_json_path: path to json file with only rocks data
    hrnet: HRNET model object
    csv_path: path to save the csv result
    display: show detection result or not

  Return:
    csv path
  """
    # Read image from disk
    # img_path = "/Users/victorialu/Downloads/with person.jpg"



def decodeString(image_b64, imagePath):
    # Decode the base64 string
    image_data = base64.b64decode(image_b64)

    # Write the decoded data to a file
    with open(imagePath, 'wb') as image_file:
        image_file.write(image_data)

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def lambda_handler(event, context):

    # Initialize a session using Amazon DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

    # Replace 'your_table_name' with your DynamoDB table name
    table = dynamodb.Table('hrnet')


    body = event
    if event.get("httpMethod") == "POST":
        body = json.loads(event.get("body"))
    elif event.get("httpMethod") == "GET":
        body = event.get('queryStringParameters', event)

    image_b64 = body.get("image")

    with TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)
        try:
            image_path = 'decode.jpg'
            decodeString(image_b64, image_path)

            img = cv2.imread(image_path)

            # Crop to the detected person before running pose estimation -- HRNet's input is a fixed
            # 384x288, so on a full-frame photo where the climber is only part of the image, resizing the
            # whole frame down makes every joint too small to clear the confidence threshold. Falls back to
            # the whole-image estimate if no person is confidently detected (e.g. unusual climbing pose).
            boxes, scores, class_ids = person_detector(img)
            has_person, (p_boxes, p_scores, p_class_ids) = filter_person_detections((boxes, scores, class_ids))
            if has_person:
                best = int(np.argmax(p_scores))
                _, poses_list = hrnet.update_with_detections(img, ([p_boxes[best]], [p_scores[best]], [p_class_ids[best]]))
                pose = poses_list[0]
                hrnet.poses = pose  # so draw_pose renders this single skeleton, matching the no-crop response shape
            else:
                _, pose = hrnet.update(img)

            output_img = hrnet.draw_pose(img)
            cv2.imwrite(image_path, output_img)

            s3Key = f"hrnet-{datetime.now().strftime('%Y, %m, %d, %H, %M, %S')}.jpg"
            upload_file(image_path, "model1234", s3Key)

            poseList = pose.tolist()
            poses = [[Decimal(str(x)) for x in sublist] for sublist in poseList]
            data = {"time": datetime.now().strftime('%Y, %m, %d, %H, %M, %S'), "user_id": str(uuid.uuid4()),
                    "result": poses, "s3Key": s3Key}

            table.put_item(
                Item=data
            )

            return {
                'statusCode': 200,
                'body': json.dumps({
                    "poses": poseList,
                    "personDetected": has_person
                })
            }
        except Exception as e:
            print("Error:", e)
            return {
                'statusCode': 500,
                'body': json.dumps({"error": str(e)})
            }


if __name__ == '__main__':
    with open("/Users/victorialu/Downloads/IMG_2264_time_19.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    with open("imageString.txt", "w") as f:
        f.write(encoded_string)

    event = {
        "httpMethod": "GET",
        "queryStringParameters":
            {
                "image": encoded_string,
            },
    }
    lambda_handler(event, None)
