#!/bin/sh

# 定义要下载的 GitHub 版本页面链接
base_url="https://ghp.ci/https://github.com/yaojiwei520/sing-box/releases/download/v1.0"

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

echo "下载完成！"
