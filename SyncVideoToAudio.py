import subprocess
import os
import numpy as np
import librosa
from scipy.signal import correlate
if os.path.exists("temp_video_audio.wav"):
    os.remove("temp_video_audio.wav")
def sync_audio_to_video(video_path, audio_path, output_path, 
                        tolerance=1000, offset=0, debug=False):
    """
    Syncs audio to a video using advanced checks and features.

    Parameters:
    video_path (str): Path to the video file.
    audio_path (str): Path to the audio file.
    output_path (str): Path to save the output video file.
    tolerance (int): Maximum allowed duration mismatch in milliseconds (default is 1000).
    offset (int): Initial offset to apply to the audio (default is 0).
    debug (bool): If True, enables printing of debug information (default is False).
    """
    if not os.path.exists(video_path):
        raise ValueError(f"Video file not found: {video_path}")
    if not os.path.exists(audio_path):
        raise ValueError(f"Audio file not found: {audio_path}")

    # Get video and audio durations
    video_duration = get_media_duration(video_path)
    audio_duration = get_media_duration(audio_path)

    # Check for duration mismatch
    if abs(video_duration - audio_duration) > tolerance:
        raise ValueError(
            f"Duration mismatch: video ({video_duration:.2f}s), audio ({audio_duration:.2f}s)"
        )

    # Extract audio from the video (if available)
    video_audio_temp = "temp_video_audio.wav"
    extracted_audio = extract_audio_from_video(video_path, video_audio_temp, debug)

    if not extracted_audio:
        if debug:
            print("No audio stream found in video, generating silent audio...")
        generate_silent_audio(video_duration, video_audio_temp)

    # Align the audio and calculate offset
    calculated_offset = align_audio_cross_correlation(video_audio_temp, audio_path, debug)

    # Sync audio to video using FFmpeg
    sync_with_ffmpeg(video_path, audio_path, output_path, offset + calculated_offset, debug)

    print(f"Audio synced to video: {output_path}")

def get_media_duration(file_path):
    """Gets the duration of a video or audio file using FFprobe."""
    try:
        return float(subprocess.check_output(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
             '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
        ).decode('utf-8'))
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error getting file duration: {e}")

def extract_audio_from_video(video_path, output_audio_path, debug=False):
    """Extracts audio from video if it exists."""
    if os.path.exists(output_audio_path):
        if debug:
            print(f"Audio file already exists: {output_audio_path}")
        return output_audio_path

    try:
        output = subprocess.check_output(
            ['ffprobe', '-v', 'error', '-show_entries', 'stream=index,codec_type',
             '-select_streams', 'a', '-of', 'json', video_path]
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFprobe failed: {e}")

    if b'"codec_type": "audio"' not in output:
        if debug:
            print(f"No audio stream found in video: {video_path}")
        return None

    try:
        subprocess.run(
            ['ffmpeg', '-i', video_path, '-q:a', '0', '-map', 'a', output_audio_path],
            check=True
        )
        return output_audio_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg failed: {e}")

def generate_silent_audio(duration, output_path):
    """Generates a silent audio file of the specified duration."""
    try:
        subprocess.run(
            ['ffmpeg', '-f', 'lavfi', '-i', 
             f'anullsrc=channel_layout=mono:sample_rate=44100', 
             '-t', str(duration), output_path], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error generating silent audio: {e}")

def align_audio_cross_correlation(video_audio_path, external_audio_path, debug=False):
    """Aligns audio using cross-correlation."""
    video_audio, sr_video = librosa.load(video_audio_path, sr=44100)
    external_audio, sr_external = librosa.load(external_audio_path, sr=44100)

    # Use a smaller segment of the audio for cross-correlation
    segment_length = min(len(video_audio), len(external_audio), sr_video * 30)  # 30 seconds segment
    video_audio_segment = video_audio[:segment_length]
    external_audio_segment = external_audio[:segment_length]

    correlation = correlate(external_audio_segment, video_audio_segment, mode='full')
    lag = np.argmax(correlation) - len(video_audio_segment) + 1
    offset = lag / sr_video

    if debug:
        print(f"Calculated offset: {offset:.3f} seconds")
    return offset

def sync_with_ffmpeg(video_path, audio_path, output_path, offset, debug=False):
    """Syncs audio to video using FFmpeg."""
    command = [
        'ffmpeg', '-i', video_path, '-itsoffset', str(offset), '-i', audio_path,
        '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'copy', output_path
    ]
    if debug:
        print(f"Running command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error syncing audio: {e}")

if __name__ == "__main__":
    # Example usage
    video_file = "output_video_20250113_115654.mp4"
    audio_file = "translated-audio-file.mp3"
    output_file = "output_video.mp4"

    try:
        sync_audio_to_video(video_file, audio_file, output_file, debug=True)
    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}")
