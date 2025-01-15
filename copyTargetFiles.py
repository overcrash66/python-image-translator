import os
import shutil

def copy_files_in_range(source_folder, destination_folder, start_file, end_file):
    # Ensure the source folder exists
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

    # Ensure the destination folder exists or create it
    os.makedirs(destination_folder, exist_ok=True)

    # Extract starting and ending numbers from filenames
    start_number = int(start_file.split('_')[1].split('.')[0])
    end_number = int(end_file.split('_')[1].split('.')[0])

    for file_name in sorted(os.listdir(source_folder)):
        # Check if the file matches the frame_*.png format
        if file_name.startswith("frame_") and file_name.endswith(".png"):
            try:
                # Extract the numeric part of the file name
                file_number = int(file_name.split('_')[1].split('.')[0])

                # Check if the file number is within the range
                if start_number <= file_number <= end_number:
                    # Copy the file to the destination folder
                    source_path = os.path.join(source_folder, file_name)
                    destination_path = os.path.join(destination_folder, file_name)
                    shutil.copy2(source_path, destination_path)
                    print(f"Copied: {file_name}")
            except ValueError:
                # Skip files that don't follow the naming convention
                continue

if __name__ == "__main__":
    source_folder = "exportedImages33"
    destination_folder = "ExportedImages"
    start_file = "frame_7062.png"
    end_file = "frame_10000.png"

    copy_files_in_range(source_folder, destination_folder, start_file, end_file)
