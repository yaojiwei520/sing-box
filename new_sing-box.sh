#!/bin/sh

# 定义要下载的 GitHub 版本页面链接
base_url="https://github.com/yaojiwei520/sing-box/releases/download/v1.0"

# 定义要下载的文件名
files=(
    "luci-app-homeproxy_git-24.238.29320-de2cf6f_all.ipk"
    "chinadns-ng_2023.10.28-1_x86_64.ipk"
    "luci-i18n-homeproxy-zh-cn_git-24.238.29320-de2cf6f_all.ipk"
)

# 下载每个文件
for file in "${files[@]}"; do
    url="$base_url/$file"
    echo "正在下载: $url"
    output_file="$(basename "$file")"
    wget -q -O "$output_file" "$url"
done

# 删除不带 .ipk 后缀的文件
for f in *; do
    if [[ "$f" != *.ipk ]]; then
        echo "删除文件: $f"
        rm -f "$f"
    fi
done

# 更新 opkg
echo "正在更新 opkg..."
opkg update

# 分次安装 ipk 文件
for ipk in *.ipk; do
    echo "正在安装: $ipk"
    opkg install "$ipk"
done

echo "所有操作完成！"
