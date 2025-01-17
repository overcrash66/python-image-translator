## Usage

1. Place your input images in the `input` folder.
2. Run the script `main.py`.
3. Translated images will be saved in the `output` folder.

## New Features

### SyncVideoToAudio.py
This script syncs audio to a video file using advanced checks and features. It performs the following steps:
- **Duration Check:** Ensures that the video and audio durations are within a specified tolerance.
- **Audio Extraction:** Extracts audio from the video if available, or generates silent audio if not.
- **Audio Alignment:** Aligns the audio using cross-correlation to calculate the offset.
- **Synchronization:** Syncs the audio to the video using FFmpeg and saves the output.

### MultipleImageProcessing.py
This script processes multiple images by performing OCR to extract text, translating the text, and replacing the original text in the images with the translated text. It includes:
- **Batch Processing:** Allows processing images one by one or multiple images simultaneously using multithreading.
- **Error Handling:** Handles translation errors and missing translations gracefully.
- **Customization:** Supports custom source and target languages for OCR and translation.

### videoToImage.py
This script extracts frames from a video file and saves them as individual images. It features:
- **Frame Extraction:** Reads and saves each frame of the video as a separate image.
- **Output Management:** Ensures the output folder exists and manages the file naming for the frames.

### imageToVideo.py
This script converts a series of images into a video file. It includes:
- **Image-to-Video Conversion:** Reads images from a folder and combines them into a video file.
- **Frame Rate Customization:** Allows setting the frame rate for the output video.
- **Error Handling:** Uses a placeholder frame for any invalid or unreadable images.

## The goal of this update is to be able to translate video to video with the combination of [OpenTranslator](https://github.com/overcrash66/OpenTranslator).

## Notes

-   Supported languages for OCR can be seen [here](https://www.jaided.ai/easyocr/)
-   Supported languages for Google Translate can be obtained using the following code:
    ```python
    from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES
    print(GOOGLE_LANGUAGES_TO_CODES)
    ```
-   Adjustments to text languages, recognition thresholds, translation services, or image processing parameters can be made within the script.

## Examples

![image-1](https://github.com/boysugi20/python-image-translator/assets/53815726/cc2a52b3-2627-4f08-a428-c0dba4341bda)
![image-1-translated](https://github.com/boysugi20/python-image-translator/assets/53815726/3ecafe2e-df19-4ca2-aeff-b05cc89394db)

## Acknowledgments

-   [EasyOCR](https://github.com/JaidedAI/EasyOCR) - For OCR processing.
-   [Google Translator](https://pypi.org/project/deep-translator/) - For text translation.
-   [Pillow (PIL Fork)](https://python-pillow.org/) - For image manipulation.