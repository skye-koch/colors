import os
import uuid
from urllib.parse import unquote_plus
import boto3
from PIL import Image

SOURCE_BUCKET = ''
DESTINATION_BUCKET = ''

s3_client = boto3.client('s3')

def get_colors(download_path):
    with Image.open(download_path) as image:
        image_colors = image.getcolors(maxcolors=1000000)
    return image_colors

def color_file(image_colors, destination_path):
    text_colors = "\n".join((f"{color[0]},{color[1]}" for color in image_colors))
    with open(destination_path, 'w') as color_file:
        color_file.write(text_colors)

def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    name, extension = os.path.splitext(key.replace('/', ''))
    download_path = f"/tmp/{name}"
    text_file = f"{name}.txt"
    save_path = f"/tmp/{text_file}"

    s3_client.download_file(bucket, key, download_path)

    image_colors = get_colors(download_path)
    if image_colors is not None:
        color_file(image_colors, save_path)
        s3_client.upload_file(save_path, DESTINATION_BUCKET, f"{uuid.uuid4()}-{text_file}")
        return True
    else:
        return False
