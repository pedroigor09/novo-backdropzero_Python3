import requests

def download_file_from_google_drive(url, destination):
    file_id = url.split('/')[5]
    base_url = 'https://drive.google.com/uc?export=download'
    session = requests.Session()
    response = session.get(base_url, params={'id': file_id}, stream=True)
    token = None

    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value

    if token:
        response = session.get(base_url, params={'id': file_id, 'confirm': token}, stream=True)

    with open(destination, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

if __name__ == "__main__":
    google_drive_url = 'hhttps://drive.google.com/file/d/1LfZbT05ftAThX1dKOy25U8J7_ma1rtiD/view?usp=sharing'
    destination = 'saved_models/u2net/u2net.pth'
    download_file_from_google_drive(google_drive_url, destination)
