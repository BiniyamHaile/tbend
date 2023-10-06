import requests

def get_blob_data(newsId):
    sas_url = "https://testanews.blob.core.windows.net/testanewsvoice"
    sas_token = "?sp=racwl&st=2023-10-01T17:09:35Z&se=2024-10-02T01:09:35Z&spr=https&sv=2022-11-02&sr=c&sig=2tY4%2FWnSEhQZq4b%2Fna3TGJIJCw0q99hBbY%2FQ7TdGMtE%3D"
    blob_url_with_sas = f"{sas_url}/{newsId}.wav{sas_token}"
    """
    Fetches the blob data from Azure Blob Storage using the provided URL with SAS token.

    :param blob_url_with_sas: The full URL to the blob, including the SAS token.
    :return: The blob's content.
    """
    response = requests.get(blob_url_with_sas)

    if response.status_code == 200:
        return response.content
    else:
        response.raise_for_status()
        return False

