import requests
import zipfile
import os
import shutil
from pathlib import Path

def move_all_files_to_folder(src_folder, dst_folder):
    content_list = os.listdir(src_folder)

    for item in content_list:
        src = os.path.join(src_folder, item)
        dst = os.path.join(dst_folder, item)
        shutil.move(src, dst)

def remove_dir(dir_path):
    shutil.rmtree(dir_path)

def download_and_extract_zip(url, folder_path):
    response = requests.get(url)

    response.raise_for_status()

    if response.status_code == 200:
        zip_file_path = os.path.join(folder_path, "ffmpeg.zip")
        with open(zip_file_path, "wb+") as zip_file:
            zip_file.write(response.content)
        
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(folder_path)
        
        os.remove(zip_file_path)

def update_path(new_path_element):
    if type(new_path_element) != str:
        new_path_element = str(new_path_element)

    current_path = os.environ.get("PATH")

    if new_path_element not in current_path:
        # add to PATH
        if current_path[-1] != os.pathsep:
            current_path += os.pathsep
        updated_path = f"{current_path}{new_path_element}{os.pathsep}"
        os.environ["PATH"] = updated_path

def setup_ffmpeg(dir: Path, download_dependency: bool):
    print("Setting FFmpeg dependency up...")

    if download_dependency:
        print("Creating directory...")
        os.mkdir(dir)

        print("Downloading and extracting .zip...")
        download_and_extract_zip(
            "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
            dir,
        )
        
        print("Moving files from the folder created while extracting the .zip file to the root dependency folder...")
        folder_content_list = os.listdir(dir)
        for item in folder_content_list:
            if "ffmpeg" in item:
                move_all_files_to_folder(dir / item, dir)
                remove_dir(dir / item)
                break

    # add FMPEG to path
    bin_dir = dir / "bin"
    update_path(bin_dir)
