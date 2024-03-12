import whisper
import ffmpeg
import requests
import os
import logging
import shutil
import argparse
from datetime import datetime

from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Declare timestamp once for consistent use across the script
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def download_media(url, filename):
    logging.info("Downloading media...")
    try:
        media_data = requests.get(url).content
        with open(filename, "wb") as file:
            file.write(media_data)
        logging.info("Download complete.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download media: {e}")
        raise


def transcribe_audio(audio_path):
    logging.info("Transcribing audio...")
    try:
        model = whisper.load_model("base.en")
        result = model.transcribe(audio_path)
        logging.info("Transcription complete.")
        return result["text"]
    except Exception as e:
        logging.error(f"Failed to transcribe audio: {e}")
        raise


def extract_audio(video_path, audio_path):
    logging.info("Extracting audio from video...")
    try:
        ffmpeg.input(video_path).output(audio_path).run()
        logging.info("Audio extraction complete.")
    except ffmpeg.Error as e:
        logging.error(f"Failed to extract audio: {e}")
        raise


def persist_data(url, transcription, folder_name):
    try:
        with open(f"{folder_name}/url.txt", "w") as url_file:
            url_file.write(url)
        with open(f"{folder_name}/transcription.txt", "w") as transcription_file:
            transcription_file.write(transcription)
        logging.info(f"Data persisted in folder: {folder_name}")
    except IOError as e:
        logging.error(f"Failed to persist data: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio or video files.")
    parser.add_argument(
        "source",
        type=str,
        nargs="?",
        default=None,
        help="URL or path of the video or audio to transcribe",
    )
    args = parser.parse_args()

    source = args.source
    if source is None:
        source = input(
            "Please enter the URL or path of the video or audio to transcribe: "
        )

    is_source_url = is_url(source)
    media_type = None

    folder_name = f"transcription/{timestamp}"
    os.makedirs(folder_name, exist_ok=True)

    if is_source_url:
        media_type = (
            "audio"
            if source.endswith((".mp3", ".wav", ".aac", ".m4a"))
            else "video" if source.endswith((".mp4", ".avi", ".mov")) else None
        )
        file_extension = source.split(".")[-1]
        filename = f"{folder_name}/downloaded_media.{file_extension}"
        download_media(source, filename)
    else:
        if os.path.exists(source):
            media_type = (
                "audio"
                if source.endswith((".mp3", ".wav", ".aac", ".m4a"))
                else "video" if source.endswith((".mp4", ".avi", ".mov")) else None
            )
            # Copy the local file to the transcription folder
            file_extension = source.split(".")[-1]
            filename = f"{folder_name}/{os.path.basename(source)}"
            shutil.copy(source, filename)
        else:
            logging.error("File does not exist.")
            return

    if not media_type:
        logging.error(
            "Unsupported media type. Please provide a video or audio URL or path."
        )
        return

    if media_type == "video":
        audio_path = f"{folder_name}/extracted_audio.wav"
        extract_audio(filename, audio_path)
        transcription = transcribe_audio(audio_path)
    else:
        transcription = transcribe_audio(filename)

    logging.info("Transcription:\n" + transcription)
    persist_data(source, transcription, folder_name)


if __name__ == "__main__":
    main()
