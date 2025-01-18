# Image Translator

This project utilizes optical character recognition (OCR) and translation to translate text within images from one language to another. It performs the following steps:

1. **OCR Processing:** The project extracts text and its bounding boxes from input images using the EasyOCR library.
2. **Translation:** It translates the extracted text using the Google Translator API.
3. **Text Replacement:** The translated text is then overlaid onto the image, replacing the original text while maintaining its position and style.
4. **Output:** Finally, the modified image with translated text is saved to an output folder.


## Usage

1. Place your input images in the `input` folder.
2. Run the script `main.py`.
3. Translated images will be saved in the `output` folder.

## The goal of this update / tools, is to be able to translate from a video to video with the combination of [OpenTranslator](https://github.com/overcrash66/OpenTranslator).

[![Demo - Translation Example](https://img.youtube.com/vi/ebviBPenkfI/0.jpg)](https://www.youtube.com/watch?v=ebviBPenkfI)

# Setup

## Installation

Clone this repository to your local machine.

```
Install the required Python dependencies using pip install pipenv && pipenv install.
```

or

```
py -3.10 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

If you like to use torch with cuda:

```
pip uninstall torch torchvision
pip install torch==2.5.1+cu118 torchaudio==2.5.1+cu118 torchvision==0.20.1+cu118 --index-url https://download.pytorch.org/whl/cu118
```

## Notes

- Supported languages for OCR can be seen [here](https://www.jaided.ai/easyocr/)
- Supported languages for Google Translate can be obtained using the following code:

    ```python
    from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES
    print(GOOGLE_LANGUAGES_TO_CODES)
    ```

- Adjustments to text languages, recognition thresholds, translation services, or image processing parameters can be made within the script.

## Examples

![image-1](./input/Untitled.png)
![image-1-translated](output/Untitled-translated.png)

## Acknowledgments

- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - For OCR processing.
- [Google Translator](https://pypi.org/project/deep-translator/) - For text translation.
- [Pillow (PIL Fork)](https://python-pillow.org/) - For image manipulation.