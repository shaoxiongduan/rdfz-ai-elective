import os
import subprocess
from pathlib import Path

def remove_audio(input_folder):
    # Ensure the input folder exists
    if not os.path.isdir(input_folder):
        print(f"Error: The folder '{input_folder}' does not exist.")
        return

    # Get all files in the input folder
    files = os.listdir(input_folder)

    # Supported video file extensions
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']

    for file in files:
        file_path = os.path.join(input_folder, file)
        file_extension = os.path.splitext(file)[1].lower()

        if file_extension in video_extensions:
            output_file = os.path.join(input_folder, f"temp_{file}")
            
            # FFmpeg command to remove audio
            command = [
                'ffmpeg',
                '-i', file_path,
                '-c:v', 'copy',
                '-an',
                output_file
            ]

            try:
                # Run FFmpeg command
                subprocess.run(command, check=True, stderr=subprocess.DEVNULL)
                
                # Remove original file and rename the new file
                os.remove(file_path)
                os.rename(output_file, file_path)
                print(f"Removed audio from: {file}")
            except subprocess.CalledProcessError:
                print(f"Error processing file: {file}")
            except Exception as e:
                print(f"An error occurred with file {file}: {str(e)}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing the video files: ")
    remove_audio(folder_path)