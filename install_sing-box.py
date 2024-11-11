import requests
from bs4 import BeautifulSoup
import os
import subprocess
import sys

# 定义要爬取的 URL
BASE_URL = "https://fantastic-packages.github.io/packages/releases/23.05/packages/x86_64/luci/"
CHINADNS_BASE_URL = "https://fantastic-packages.github.io/packages/releases/23.05/packages/x86_64/packages/"

def download_file(url):
    filename = url.split('/')[-1]
    print(f"正在下载 {filename}...")
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"{filename} 下载成功")
        return filename
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")
        return None

def fetch_files(url, keyword):
    print(f"正在获取包含 '{keyword}' 的文件列表...")
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return []

    # 解析 HTML 内容
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有的包含指定关键字的链接
    file_list = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if keyword in href:
            file_list.append(href)

    return file_list

def install_package(package):
    print(f"正在安装 {package}...")
    result = subprocess.run(["opkg", "install", package], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{package} 安装成功！")
    else:
        print(f"{package} 安装失败: {result.stderr}")

def show_progress_bar(iteration, total, length=40):
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r|{bar}| {percent:.2f}% 完成')
    sys.stdout.flush()

if __name__ == "__main__":
    # 更新 opkg
    print("正在更新 opkg...")
    subprocess.run(["opkg", "update"])

    # 下载并安装 homeproxy 文件
    homeproxy_files = fetch_files(BASE_URL, 'homeproxy')
    total_files = len(homeproxy_files)

    for i, file in enumerate(homeproxy_files):
        full_url = os.path.join(BASE_URL, file)
        downloaded_file = download_file(full_url)
        if downloaded_file:
            install_package(downloaded_file)
            show_progress_bar(i + 1, total_files)

    print("\n")

    # 下载并安装 chinadns-ng 文件
    chinadns_files = fetch_files(CHINADNS_BASE_URL, 'chinadns-ng')
    total_files = len(chinadns_files)

    for i, file in enumerate(chinadns_files):
        full_url = os.path.join(CHINADNS_BASE_URL, file)
        downloaded_file = download_file(full_url)
        if downloaded_file:
            install_package(downloaded_file)
            show_progress_bar(i + 1, total_files)

    print("\n所有操作完成！")
