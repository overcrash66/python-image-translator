'''
This script convert an input video to frames / a list of images
'''

import os
import cv2

def video_to_images(video_path, output_folder):
    # Check if the video file exists
    if not os.path.isfile(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if the video was opened successfully
    if not video.isOpened():
        print(f"Error: Unable to open video file '{video_path}'.")
        return

    frame_count = 0

    while True:
        # Read a frame from the video
        ret, frame = video.read()

        # If no frame is read, we reached the end of the video
        if not ret:
            break

        # Generate the file name for the frame image
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.png")

        # Save the frame as an image
        cv2.imwrite(frame_filename, frame)

        frame_count += 1

    # Release the video capture object
    video.release()

    print(f"Exported {frame_count} frames to '{output_folder}'.")

if __name__ == "__main__":
    # Input MP4 video file
    video_path = input("Enter the path to the MP4 video file: ")

    # Output folder
    output_folder = "ExportedImages"

    # Extract frames
    video_to_images(video_path, output_folder)
