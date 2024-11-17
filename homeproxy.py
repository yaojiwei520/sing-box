import requests
from bs4 import BeautifulSoup

# 自定义 URL
BASE_URL = "https://github.com/qichiyuhub/rule/tree/master/config/singbox"

def download_file(url, filename):
    print(f"正在下载 {filename}...")
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"{filename} 下载成功")
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")

def fetch_files(url):
    print("正在获取文件列表...")
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return []

    # 解析 HTML 内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有文件链接
    files = {}
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/qichiyuhub/rule/blob/master/config/singbox/'):
            filename = href.split('/')[-1]
            files[filename] = href  # 保存文件名和对应的 blob 链接
            print(f"找到文件链接: {filename} - {href}")  # 打印文件链接

    return files

if __name__ == "__main__":
    # 获取文件列表
    files = fetch_files(BASE_URL)

    # 打印所有文件
    print("\n所有文件:")
    for file in files.keys():
        print(file)

    # 检查是否存在 homeproxy 文件
    if "homeproxy" in files:
        print("找到 homeproxy 文件。")

        # 构造原始文件的 URL
        blob_url = files["homeproxy"]
        file_url = f"https://raw.githubusercontent.com{blob_url.replace('/blob', '')}"
        download_file(file_url, "homeproxy")
    else:
        print("未找到 homeproxy 文件。")
