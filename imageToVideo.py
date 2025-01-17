'''
This script is used to convert a list of images to a video respecting the order by image name / number
'''

import cv2
import os
import re
import numpy as np
from datetime import datetime

def images_to_video(image_folder, output_video, frame_rate=30):
    """
    Converts all images in a folder to a video file, adapting invalid frames when necessary.

    Args:
        image_folder (str): Path to the folder containing images.
        output_video (str): Path to save the output video file.
        frame_rate (int): Frame rate of the output video.

    Returns:
        None
    """
    # Get all image files in the folder
    images = [img for img in os.listdir(image_folder) if img.endswith((".png", ".jpg", ".jpeg"))]
    
    # Extract and sort by numeric index in filenames
    images.sort(key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else float('inf'))
    
    if not images:
        print("No images found in the folder.")
        return

    # Read the first image to determine video dimensions
    first_image_path = os.path.join(image_folder, images[0])
    first_image = cv2.imread(first_image_path)
    if first_image is None:
        print(f"Error: Unable to read the first image: {first_image_path}")
        return
    height, width, _ = first_image.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 format
    video_writer = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

    # Placeholder frame for invalid images (black frame)
    placeholder_frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Process each image
    for image_file in images:
        image_path = os.path.join(image_folder, image_file)
        frame = cv2.imread(image_path)

        if frame is None:
            print(f"Warning: Couldn't read image {image_path}. Using placeholder frame.")
            frame = placeholder_frame.copy()  # Use the placeholder frame
        else:
            # Resize frame to match the video dimensions
            frame = cv2.resize(frame, (width, height))
        
        video_writer.write(frame)

    # Release the VideoWriter object
    video_writer.release()
    print(f"Video saved at {output_video}")

# Example usage
if __name__ == "__main__":
    image_folder_path = "TranslatedImages"  # Replace with your folder path
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_video_path = f"output_video_{current_datetime}.mp4"  # Replace with your desired output file name
    frame_rate = 12  # Optional: Adjust the frame rate as needed

    images_to_video(image_folder_path, output_video_path, frame_rate)
