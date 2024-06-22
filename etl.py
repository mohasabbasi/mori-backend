import json
from PIL import Image
import requests
from io import BytesIO
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client import models
import encoder
import logging

logging.basicConfig(filename='error.log',
                    level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(message)s')

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "mori_collection"
EMBEDDING_SIZE = 512

def collection_exists(collection_name):
    response = requests.get(f"{QDRANT_URL}/collections/{collection_name}")
    return response.status_code == 200


client = QdrantClient(url=QDRANT_URL)

if not collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBEDDING_SIZE , distance=Distance.COSINE ),
    )


images_default_path = 'server/data/images'
if not os.path.exists(images_default_path):
    os.mkdir(images_default_path)

def fetch_products_data():
    with open('server/data/data_lake/products.json','r') as f:
        data = json.loads(f.read())

    return data

def download_and_save_img(url , save_path):
    try:

        response = requests.get(url)


        # response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        img.save(save_path)
    except (IOError, SyntaxError) as e:
        print(f"Skipping corrupted image: {url}")
        logging.error("An error occurred: %s", e)


products_list = fetch_products_data()

current_path = os.getcwd()

# Print the current working directory
print("Current Working Directory:", current_path)


for product in products_list[0:10]:
    #Step first get and clean data
    # print(product )
    save_dir = f"server/data/images/{product['id']}"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)


    for idx , img_url in enumerate(product['images']):

        file_name = f"{idx}.jpg"
        save_path = os.path.join(save_dir , file_name)

        try:
            download_and_save_img(img_url, save_path)

            img_encoded_vector = encoder.encode_image(save_path).cpu().numpy().tolist()[0]
            print(len(img_encoded_vector))
            client.upload_points(
                collection_name="mori_collection",
                points=[
                    models.PointStruct(
                        id=product["id"], vector=img_encoded_vector , payload=product
                    )
                ],
            )

        except Exception as e:
            logging.error("An error occurred: %s", e)


