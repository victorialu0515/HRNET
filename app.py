import boto3
import botocore
import os
from HRNET import HRNET, ModelType
import base64
from datetime import datetime
from tempfile import TemporaryDirectory
import cv2
import json
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
    with TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)
        s3 = boto3.client('s3')
        model_key = "hrnet_coco_w48_384x288.onnx"

        model_path = "hrnet_coco_w48_384x288.onnx"
        try:
            s3.download_file("model1234", model_key, model_path)
        except Exception as e:
            print("Error:", e)
            return

        # model_path = "models/hrnet_coco_w48_384x288.onnx"
        model_type = ModelType.COCO
        hrnet = HRNET(model_path, model_type, conf_thres=0.5)

        querystring = event.get('queryStringParameters', event)
        image_b64 = querystring.get("image")

        image_path = 'decode.jpg'
        decodeString(image_b64, image_path)

        img = cv2.imread(image_path)

        total_heatmap, peaks = hrnet(img)
        output_img = hrnet.draw_pose(img)
        cv2.imwrite(image_path, output_img)

        upload_file(image_path, "model1234", f"hrnet-{datetime.now().strftime('%Y, %m, %d, %H, %M, %S')}.jpg")


        print(f'boto3 version: {boto3.__version__}')
        print(f'botocore version: {botocore.__version__}')
        return {
            'statusCode': 200,
            'body': json.dumps({
                "poses": hrnet.poses.tolist()
            })

        }


if __name__ == '__main__':
    with open("/Users/victorialu/Downloads/IMG_2264_time_19.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    with open("imageString.txt", "w") as f:
        f.write(encoded_string)

    event = {
        "queryStringParameters":
            {
                "image": encoded_string,
            },
    }
    lambda_handler(event, None)
