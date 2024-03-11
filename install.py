import os
import requests
import zipfile
import shutil
import subprocess


def check_folder(folder_name):
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, folder_name)
    return os.path.exists(folder_path)


def download_file(url, file_name, destination_folder="downloads\\"):
    os.makedirs(destination_folder, exist_ok=True)
    file_path = os.path.join(destination_folder, file_name)
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path
    else:
        print(f"Failed to download the file {url}. Status code: {response.status_code}")
        exit()


def unzip_file(zip_file, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(destination_folder)


def check_nodejs_version():
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        installed_version = result.stdout.strip()
        if installed_version.startswith("v18"):
            return True
        else:
            return False
    except FileNotFoundError:
        return False


def processNodeJS():
    if check_nodejs_version() == False:
        if check_folder("nodejs/node.exe") == False:
            filepath = download_file(
                "https://nodejs.org/download/release/v18.19.1/node-v18.19.1-win-x64.zip",
                "nodejs.zip",
            )
            unzip_file(filepath, "nodejs")
            source = "nodejs/node-v18.19.1-win-x64"
            destination = "nodejs"

            files = os.listdir(source)
            for file in files:
                file_name = os.path.join(source, file)
                shutil.move(file_name, destination)
    print("NodeJS ✅")


def processNginx():
    if check_folder("nginx/nginx.exe") == False:
        filepath = download_file(
            "https://drive.google.com/uc?export=download&id=1RwZj8hkIt-HVbI1ybrelK2I4uIZoTPEx",
            "nginx.zip",
        )
        unzip_file(filepath, "nginx")
    print("Nginx ✅")


def processRedis():
    if check_folder("redis/redis-server.exe") == False:
        filepath = download_file(
            "https://github.com/tporadowski/redis/releases/download/v5.0.14.1/Redis-x64-5.0.14.1.zip",
            "redis.zip",
        )
        unzip_file(filepath, "redis")
    print("Redis ✅")


def processPHP():
    if check_folder("php/php.exe") == False:
        filepath = download_file(
            "https://windows.php.net/downloads/releases/php-8.2.16-nts-Win32-vs16-x64.zip",
            "php.zip",
        )
        unzip_file(filepath, "php")
        download_file(
            "https://getcomposer.org/download/latest-stable/composer.phar",
            "composer.phar",
            "php\\",
        )
        download_file(
            "https://drive.google.com/uc?export=download&id=1ClAw9MnK4qEFyrDfY9KAVF5H-EaH1fYw",
            "php.ini",
            "php\\",
        )
    print("PHP ✅")


processNginx()
processRedis()
processPHP()
processNodeJS()
shutil.rmtree("downloads", ignore_errors=True)
shutil.rmtree("nodejs/node-v18.19.1-win-x64/", ignore_errors=True)

input("")