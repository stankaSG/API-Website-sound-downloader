import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["APIKEY"]
headers = {"Authorization": f"Token {API_KEY}"}
URL = "https://freesound.org/apiv2/"


def clean_audio_folder():
    audio_folder = "static/audio"

    if os.path.exists(audio_folder):
        for filename in os.listdir(audio_folder):
            filepath = os.path.join(audio_folder, filename)

            if os.path.isfile(filepath):
                os.remove(filepath)
        print("Audio files cleaned")



def find_sounds(query):
    response = requests.get(f"{URL}search/text/?query={query}&token={API_KEY}")
    response.raise_for_status()

    data = response.json()


    return data


def get_download_url(sound_id):
    response = requests.get(f"{URL}sounds/{sound_id}/", headers=headers)

    response.raise_for_status()
    sound_data = response.json()

    return sound_data["previews"]["preview-hq-mp3"]


def download_sound(download_url,filepath):
    download_response = requests.get(download_url, headers=headers, stream=True)

    if download_response.status_code == 200:
        content_type = download_response.headers.get("Content-Type", "")
        print(f"Content-Type: {content_type}")
        if "audio" in content_type or ".wav" in download_url or ".mp3" in download_url:
            with open(f"{filepath}.mp3", "wb") as file:
                for chunk in download_response.iter_content(1024):
                    file.write(chunk)
            print(f"✅ Zvuk bol stiahnutý!")
        else:
            print(f"❌ Stiahnutý súbor nie je audio: {download_response.text}")
    else:
        print(f"❌ Chyba pri sťahovaní: {download_response.status_code} - {download_response.text}")




