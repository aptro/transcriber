## Setting Up the Environment

Follow these steps to set up your environment:

1. **Install Python 3.9.9 using pyenv:**
   Execute the following command to install Python 3.9.9:
   ```
   pyenv install 3.9.9
   ```

2. **Set the local Python version to 3.9.9:**
   Set your local environment to use Python 3.9.9 by running:
   ```
   pyenv local 3.9.9
   ```

3. **Install project dependencies using Poetry:**
   Install all necessary dependencies with Poetry using:
   ```
   poetry install
   ```

4. **Run the transcription script:**
   To transcribe an audio file, use the command below. Replace the path with the location of your file:
   ```
   poetry run python -m transcribe /Users/you/Desktop/transcribe.m4a
   ```

   Alternatively, to transcribe a video from a URL, use:
   ```
   poetry run python -m transcribe https://video.twimg.com/ext_tw_video/1767204649499549697/pu/vid/avc1/480x270/NFekR_0sz25y6GhS.mp4
   ```
