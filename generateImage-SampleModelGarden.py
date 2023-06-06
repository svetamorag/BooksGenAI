from typing import Dict, List, Union

from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from google.cloud import storage
import base64
import glob
import os
from datetime import datetime
from io import BytesIO
from PIL import Image

def predict_custom_trained_model_sample(
    pn: float,
    project: str,
    endpoint_id: str,
    instances: Union[Dict, List[Dict]],
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
    
):
    """
    `instances` can be either single instance of type dict or a list
    of instances.
    """
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # The format of each instance should conform to the deployed model's prediction input schema.
    instances = instances if type(instances) == list else [instances]
    instances = [
        json_format.ParseDict(instance_dict, Value()) for instance_dict in instances
    ]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # The predictions are a google.protobuf.Value representation of the model's predictions.
    predictions = response.predictions
    for prediction in predictions:
        #print(" prediction:", prediction)
        fileName="pagen{pn}.jpg".format(pn=pn)
        print(fileName)
        save_image(base64_to_image(prediction),"svetasproject-generalcontent",fileName)
       
def generateImageFromPrompt(text,page_num):   
    predict_custom_trained_model_sample(
        project="000000", #Change it with the code suggested by Vertex Endpoint
        endpoint_id="000000",
        location="us-central1",
        instances=[{ "prompt": text}],
        pn=page_num,
    )



