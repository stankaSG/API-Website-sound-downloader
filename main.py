from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap5
from api_functions import find_sounds, download_sound, get_download_url, clean_audio_folder

app = Flask(__name__)
Bootstrap5(app)

@app.route('/')
def home():


    return render_template("index.html")

@app.route('/search', methods=['POST'])
def search_sound():
    clean_audio_folder()
    name = request.form.get('name')

    if name:
        data = find_sounds(name)
        sound_list = []
        for i in range(len(data["results"][:5])):
            sound_name = data["results"][i]["name"]
            sound_id = data["results"][i]["id"]
            download_url = get_download_url(sound_id)

            filepath = f"static/audio/{sound_name}"
            download_sound(download_url, filepath)

            sound_list.append((sound_name, filepath))

        return render_template("index.html", sound_list=sound_list )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)