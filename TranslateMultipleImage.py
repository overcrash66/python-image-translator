"""
This script processes images by performing OCR (Optical Character Recognition) to extract text,
translates the extracted text to a target language, and replaces the original text in the images
with the translated text. The processed images are saved in a specified output folder.

Usage:
1. Ensure the 'ExportedImages' folder contains the images to be processed.
2. Ensure the 'TranslatedImages' folder is empty or contains no conflicting filenames.
3. Run the script and follow the prompts.

Dependencies:
- deep_translator
- easyocr
- concurrent.futures
"""

print("[INFO] Starting the image processing...")

from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator
import os
import easyocr
import warnings
from concurrent.futures import ThreadPoolExecutor
import time
warnings.filterwarnings("ignore", category=RuntimeWarning, module="easyocr.utils")

print("[INFO] Please make sure ExportedImages folder is empty!")
print("[INFO] Please make sure TranslatedImages folder is empty!")
print("[Warning] please make sure TranslatedImages folder is empty !")

#add command line pause or ask user to press enter
input("Press Enter to continue...")
def process_image(filename, input_folder, output_folder, reader, translator):
    print(f"[INFO] Processing {filename}...")

    image_path = os.path.join(input_folder, filename)
    extracted_text_boxes = perform_ocr(image_path, reader)

    translated_texts = []
    for box in extracted_text_boxes:
        text = box[1]
        try:
            translated_texts.append(translator.translate(text))
        except Exception as e:
            print(f"[WARNING] Translation error for '{text}': {e}")
            print(f"[WARNING] No translation found for: {text}")
            translated_texts.append(None)

    image = overlay_translated_text(image_path, translated_texts, extracted_text_boxes)

    output_path = os.path.join(output_folder, filename)
    image.save(output_path)
    print(f"[INFO] Saved {filename} to {output_folder}.")

print("[INFO] Loading the OCR and translation models...")
source_lang = "en"
target_lang = "fr"
reader = easyocr.Reader([source_lang, target_lang], model_storage_directory='model')
translator = GoogleTranslator(source="en", target="fr")

def main():
    input_folder = "ExportedImages"
    output_folder = "TranslatedImages"
    choice = input("Do you want to process images one by one or process multiple images? (Enter 1 for one by one or 2 for multiple files same time): ").strip().lower()
    if choice not in ["1", "2"]:
        print("[ERROR] Invalid choice. Please Enter 1 for one by one or 2 for multiple for multiple files same time.")
        return

    if choice == "1":
        for filename in os.listdir(input_folder):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                process_image(filename, input_folder, output_folder, reader, translator)
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    if choice == "2":
        num_workers = os.cpu_count() or 1
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(process_image, filename, input_folder, output_folder, reader, translator)
                    for filename in os.listdir(input_folder)
                    if filename.lower().endswith((".jpg", ".jpeg", ".png"))]

            total_files = len(futures)
            for i, future in enumerate(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"[ERROR] Failed to process {futures[i].filename}: {e}")
                # Uncomment the following lines to show progress
                # progress = (i + 1) / total_files * 100
                # print(f"[INFO] Progress: {progress:.2f}%")

def perform_ocr(image_path, reader):
    # Perform OCR on the image
    result = reader.readtext(image_path, width_ths = 0.8,  decoder = 'wordbeamsearch')

    # Extract text and bounding boxes from the OCR result
    extracted_text_boxes = [(entry[0], entry[1]) for entry in result if entry[2] > 0.4]

    return extracted_text_boxes

def get_font(image, text, width, height):

    # Default values at start
    font_size = None  # For font size
    font = None  # For object truetype with correct font size
    box = None  # For version 8.0.0
    x = 0
    y = 0

    draw = ImageDraw.Draw(image)  # Create a draw object

    # Test for different font sizes
    for size in range(1, 500):

        # Create new font
        new_font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=size)

        # Calculate bbox for version 8.0.0
        new_box = draw.textbbox((0, 0), text, font=new_font)

        # Calculate width and height
        new_w = new_box[2] - new_box[0]  # Bottom - Top
        new_h = new_box[3] - new_box[1]  # Right - Left

        # If too big then exit with previous values
        if new_w > width or new_h > height:
            break

        # Set new current values as current values
        font_size = size
        font = new_font
        box = new_box
        w = new_w
        h = new_h

        # Calculate position (minus margins in box)
        x = (width - w) // 2 - box[0]  # Minus left margin
        y = (height - h) // 2 - box[1]  # Minus top margin

    return font, x, y

def adjust_color_brightness(color, strength):
    r, g, b = color
    r = max(0, min(255, r + strength))
    g = max(0, min(255, g + strength))
    b = max(0, min(255, b + strength))
    return (r, g, b)

def extract_background_color(image, x_min, y_min, x_max, y_max):
    margin = 10
    region = image.crop((
        max(x_min - margin, 0),
        max(y_min - margin, 0),
        min(x_max + margin, image.width),
        min(y_max + margin, image.height),
    ))
    edge_colors = region.getcolors(region.size[0] * region.size[1])
    background_color = max(edge_colors, key=lambda x: x[0])[1]
    return adjust_color_brightness(background_color, 40)

def determine_text_color(background_color):
    # Calculate the luminance of the background color
    luminance = (
        0.299 * background_color[0]
        + 0.587 * background_color[1]
        + 0.114 * background_color[2]
    ) / 255

    # Determine the text color based on the background luminance
    if luminance > 0.5:
        return "black"  # Use black text for light backgrounds
    else:
        return "white"  # Use white text for dark backgrounds

def overlay_translated_text(image_path, translated_texts, text_boxes):
    # Open the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Load a font that supports French accent marks
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=20)
    
    # Replace each text box with translated text
    for text_box, translated in zip(text_boxes, translated_texts):

        if translated is None:
            continue

        # Set initial values
        x_min, y_min = text_box[0][0][0], text_box[0][0][1]
        x_max, y_max = text_box[0][0][0], text_box[0][0][1]

        for coordinate in text_box[0]:

            x, y = coordinate

            if x < x_min:
                x_min = x
            elif x > x_max:
                x_max = x
            if y < y_min:
                y_min = y
            elif y > y_max:
                y_max = y

        # Find the most common color in the text region
        background_color = extract_background_color(image, x_min, y_min, x_max, y_max)

        # Draw a rectangle to cover the text region with the original background color
        draw.rectangle(((x_min, y_min), (x_max, y_max)), fill=background_color)

        # Calculate font size, box
        font, x, y = get_font(image, translated, x_max - x_min, y_max - y_min)

        # Draw the translated text within the box
        draw.text(
            (x_min + x, y_min + y),
            translated,
            fill=determine_text_color(background_color),
            font=font,
        )

    return image

start_time = time.time()

if __name__ == "__main__":
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_minutes = elapsed_time / 60
    print(f"[INFO] Image processing completed in {elapsed_minutes:.2f} minutes.")
    print("[INFO] Please check the 'TranslatedImages' folder for the processed images.")
    print("[INFO] Thank you for using the image processing script!")

