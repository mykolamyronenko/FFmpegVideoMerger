import os
import subprocess
import shutil
from CTkMessagebox import CTkMessagebox
import sys
from utils import get_video_info, get_aspect_ratios, create_temp_dir, delete_temp_dir

INITIAL_PROGRESS = 10
PROGRESS_INCREMENT = 80
END_PROGRESS = 100
AAC = 'aac'
H264 = 'libx264'
AUDIO = 2

class VideoProcessor:
    def __init__(self, ui):
        self.ui = ui
        self.temp_dir = create_temp_dir()

    def start_merge(self):
        try:
            self.check_requirements()
            self.get_video_specs()
            self.process_files()
            self.finalize_merge()
            self.cleanup_after_merge()
        except Exception as e:
            self.handle_merge_error(e)
            self.cleanup_after_merge()

    def check_requirements(self):
        if not (shutil.which('ffmpeg') and shutil.which('ffprobe')):
            raise Exception("ffmpeg and ffprobe are required but not installed or not in the PATH.")

    def get_video_specs(self):
        for video_file in self.ui.files:
            try:
                width, height, fps, audio_hz, time_base = get_video_info(video_file)
                if (width != "N/A" and height != "N/A" and fps != "N/A" and audio_hz != "N/A" and time_base != "N/A"):
                    SAR, DAR = get_aspect_ratios(width, height)
                    return int(width), int(height), fps, int(audio_hz), int(time_base), str(SAR), str(DAR)
            except Exception as e:
                self.handle_merge_error(e)
                print(f"Error in get_video_specs {e}")
        raise Exception("No valid video file found.")

    def process_files(self):
        width, height, fps, audio_hz, time_base, SAR, DAR = self.get_video_specs()
        self.ui.progress_bar.set(INITIAL_PROGRESS / 100)
        self.ui.progress.configure(text=f"Merging in process - {INITIAL_PROGRESS}%", font=("cursive", 16), text_color="#0070ff")
        for i, video_file in enumerate(self.ui.files, start=1):
            try:
                output_file = os.path.join(self.temp_dir, f"input{i}.mp4")
                self.convert_video(video_file, output_file, width, height, str(fps), audio_hz, time_base, str(SAR), str(DAR))
                self.ui.converted_files.append(output_file)
                print(f"File {output_file} was not skipped")
            except Exception as e:
                self.handle_merge_error(e)
                print(f"Error in process_files {e}")
            self.ui.progress_bar.set((INITIAL_PROGRESS + (PROGRESS_INCREMENT / len(self.ui.files) * i)) / 100)
            self.ui.progress.configure(text=f"Merging in process - {round(self.ui.progress_bar.get() * 100)}%", font=("cursive", 16), text_color="#0070ff")
            self.ui.app.after(0, self.ui.app.update_idletasks)

    def finalize_merge(self):
        try:
            list_file_path = os.path.join(self.temp_dir, 'list.txt')
            with open(list_file_path, 'w') as f:
                for video_file in self.ui.converted_files:
                    f.write(f"file '{video_file}'\n")

            self.merge_videos(self.ui.output, list_file_path)
            self.ui.progress_bar.set(1)
            self.ui.progress.configure(text=f"Merging done - 100%", font=("cursive", 16), text_color="#0070ff")
            self.ui.app.after(0, self.ui.app.update_idletasks)
            self.ui.progress.configure(text="Merging done ", text_color="#28b62c")
        except Exception as e:
            self.handle_merge_error(e)
            print(f"Error in finalize_merge {e}")

    def convert_video(self, input_file, output_file, width, height, fps, audio_hz, time_base, SAR, DAR):
        try:
            cmd = f'ffmpeg -y -i "{input_file}" -vf "scale={width}:{height}, setsar={SAR}, setdar={DAR}" -r {fps} -ar {audio_hz} -ac {AUDIO} -video_track_timescale {time_base} -c:v {H264} -c:a {AAC} -threads 1 "{output_file}"'
            subprocess.run(cmd, shell=True, check=True)
            print(f"Converted video file: {input_file}")
        except subprocess.CalledProcessError as e:
            self.handle_merge_error(e)
            print(f"Error in convert_video {e}")

    def merge_videos(self, output_file, list_file_path):
        try:
            cmd = f'ffmpeg -y -f concat -safe 0 -i "{list_file_path}" -c copy "{output_file}"'
            subprocess.check_output(cmd, shell=True)
            self.ui.app.after(0, self.ui.app.update_idletasks)
        except Exception as e:
            self.handle_merge_error(e)
            print(f"Error in merge_video {e}")

    def handle_merge_error(self, e):
        self.ui.app.after(0, lambda: CTkMessagebox(title="Error", message=f"Error: {str(e)}", icon="error"))
        print(f"Error: {str(e)}")
        self.ui.progress.configure(text="An error occurred during merging ", text_color="#ff0800")
        self.ui.progress_bar.set(1)
        sys.exit(1)

    def cleanup_after_merge(self):
        try:
            self.delete_converted_files()
            print("Files merged")
            self.ui.app.after(0, lambda: CTkMessagebox(title="Success", message=f"Files merged into:\n{self.ui.output}", icon="info"))
            self.ui.title.configure(text="Choose files to merge", font=("cursive", 20), text_color="#0070ff")
        except Exception as e:
            self.handle_merge_error(e)

    def delete_converted_files(self):
        try:
            for file in self.ui.converted_files:
                os.remove(file)
            if os.path.exists('list.txt'):
                os.remove('list.txt')
            self.ui.converted_files = []
        except Exception as e:
            print(f"Error in delete_converted_files {e}")
