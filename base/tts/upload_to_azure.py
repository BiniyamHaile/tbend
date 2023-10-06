import os
import requests
from urllib.parse import quote

async def upload_to_azure(file_path):
    
    sas_url = "https://testanews.blob.core.windows.net/testanewsvoice"
    sas_token = "?sp=racwl&st=2023-10-01T17:09:35Z&se=2024-10-02T01:09:35Z&spr=https&sv=2022-11-02&sr=c&sig=2tY4%2FWnSEhQZq4b%2Fna3TGJIJCw0q99hBbY%2FQ7TdGMtE%3D"
    
    blob_name = os.path.basename(file_path)
    headers = {
        'x-ms-blob-type': 'BlockBlob'
    }
    print("uploading to azure ... ", file_path)

    try:
        with open(os.path.join(file_path), 'rb') as data:
            response = requests.put(f"{sas_url}/{blob_name}{sas_token}", headers=headers, data=data)
        
            if response.status_code == 201:
                
                
                return True
            else:
               
                print(f"Error uploading file: {response.status_code} - {response.text}")
                return False
    except Exception as ex:
        print(f"Error uploading file: {ex}")
        return False