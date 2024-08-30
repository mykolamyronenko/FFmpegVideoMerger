import subprocess
import tempfile
import shutil
import customtkinter as ctk

def get_video_info(video_file):
    try:
        cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,time_base -of csv=s=x:p=0 "{video_file}"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')[0].split('x')
        width, height, fps, time_base = output[0], output[1], output[2], output[3].split('/')[1]
        cmd = f'ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate -of default=noprint_wrappers=1:nokey=1 "{video_file}"'
        audio_hz = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split('\n')[0]
        return int(width), int(height), fps, int(audio_hz), int(time_base)
    except Exception as e:
        print(f"Error in get_video_info {e}")
        return None, None, None, None, None

def get_aspect_ratios(width, height):
    aspect_ratios = {
        (720, 480): ('3/2', '4/3'),
        (1280, 720): ('1/1', '16/9')
    }
    
    for (w, h), (sar, dar) in aspect_ratios.items():
        if width <= w and height <= h:
            return sar, dar
    
    return '1/1', '16/9'

def create_temp_dir():
    return tempfile.mkdtemp()

def delete_temp_dir(temp_dir):
    shutil.rmtree(temp_dir)

def change_theme():
    theme = 'dark' if ctk.get_appearance_mode() == "Dark" else 'light'
    ctk.set_appearance_mode(theme)
