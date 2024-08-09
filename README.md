# HRNET on AWS Lambda

## Download models

HRNET (ONNX)

https://github.com/PINTO0309/PINTO_model_zoo/tree/main/268_Lite-HRNet

Lite HRNET (ONNX)
https://github.com/PINTO0309/PINTO_model_zoo/tree/main/271_HRNet

YoloV5 (ONNX)
https://colab.research.google.com/drive/1V-F3erKkPun-vNn28BoOc6ENKmfo8kDh?usp=sharing

YoloV6 (ONNX)
https://colab.research.google.com/drive/1pke1ffMeI2dXkIAbzp6IHWdQ0u8S6I0n?usp=sharing

Input example:
````
{
    "queryStringParameters":
        {
            "image": encoded_string,
        },
}
```

Output example:
```
{
  "statusCode": 200,
  "body": "{\"poses\": [[-1.3835058055282164e+20, -1.844674407370955e+20], [780.0, 780.0], [810.0, 780.0], [795.0, 800.0], [870.0, 800.0], [765.0, 880.0], [930.0, 860.0], [660.0, 920.0], [1050.0, 880.0], [615.0, 940.0], [1035.0, 820.0], [795.0, 1120.0], [900.0, 1140.0], [690.0, 1260.0], [795.0, 1280.0], [720.0, 1460.0], [765.0, 1480.0]]}"
}
```