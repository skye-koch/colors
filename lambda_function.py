import csv
import boto3
from io import StringIO, BytesIO
from itertools import batched
from PIL import Image

s3 = boto3.client('s3')
DESTINATION = "skyekoch-images-output"

def get_image_colors(bucket, key):
    resp = s3.get_object(Bucket=bucket, Key=key)
    with Image.open(BytesIO(resp['Body'].read())) as img:
        return img.getcolors(maxcolors=img.size[0] * img.size[1])

def create_csv_payload(data):
    buf = StringIO()
    writer = csv.writer(buf)
    for batch in batched(data, 20000):
        writer.writerows([(x[0], *x[1]) for x in batch])
    return buf.getvalue()

def lambda_handler(event, context):
    src_bucket = event['Records'][0]['s3']['bucket']['name']
    src_key = event['Records'][0]['s3']['object']['key']
    
    #no infinite loops allowed
    if src_bucket == DESTINATION:
        return False

    colors = get_image_colors(src_bucket, src_key)
    csv_data = create_csv_payload(colors)
    
    out_key = src_key.rsplit('.', 1)[0] + ".csv"
    s3.put_object(Bucket=DESTINATION, Key=out_key, Body=csv_data)
    
    return True
