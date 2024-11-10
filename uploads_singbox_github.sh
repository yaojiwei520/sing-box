#!/bin/bash

# 配置部分
GITHUB_TOKEN="your_github_token"  # 请替换为你的 GitHub 令牌
REPO="yaojiwei520/sing-box"     # 请替换为你的 GitHub 仓库名
VERSION_FILE="version.txt"          # 用于存储当前版本号的文件

# 检查 version.txt 是否存在，如果不存在则初始化为 1.0
if [ ! -f "$VERSION_FILE" ]; then
    echo "1.0" > "$VERSION_FILE"
fi

# 读取当前版本号
CURRENT_VERSION=$(cat "$VERSION_FILE")
VERSION_NUMBER=$(echo "$CURRENT_VERSION" | awk -F. '{print $2}')
NEW_VERSION_NUMBER=$((VERSION_NUMBER + 1))
NEW_VERSION="v1.$NEW_VERSION_NUMBER"

# 更新版本文件
echo "$NEW_VERSION" > "$VERSION_FILE"

# 下载文件
echo "正在查找 homeproxy 的 ipk 文件..."
IPK_FILES=(
    "https://fantastic-packages.github.io/packages/releases/23.05/packages/x86_64/luci/luci-app-homeproxy_git-24.238.29320-de2cf6f_all.ipk"
    "https://fantastic-packages.github.io/packages/releases/23.05/packages/x86_64/luci/luci-i18n-homeproxy-zh-cn_git-24.238.29320-de2cf6f_all.ipk"
)

for URL in "${IPK_FILES[@]}"; do
    echo "正在下载: $URL"
    curl -O "$URL"
done

# 删除不带 .ipk 后缀的文件
echo "正在删除不带 .ipk 后缀的文件..."
rm -f upload.sh

# 创建 GitHub Release
echo "正在创建 GitHub Release..."
RELEASE_DATA=$(curl -X POST -H "Authorization: token $GITHUB_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"tag_name\": \"$NEW_VERSION\", \"name\": \"$NEW_VERSION\", \"body\": \"更新次数: $NEW_VERSION_NUMBER\"}" \
    "https://api.github.com/repos/$REPO/releases")

# 获取上传地址
UPLOAD_URL=$(echo "$RELEASE_DATA" | jq -r '.upload_url' | sed "s/{?name,label}//")

# 上传文件到 GitHub Releases
echo "正在上传到 GitHub Releases..."
for ipk in *.ipk; do
    echo "上传文件: $ipk"
    curl -X POST -H "Authorization: token $GITHUB_TOKEN" \
         -H "Content-Type: application/octet-stream" \
         -F "file=@$ipk" \
         "$UPLOAD_URL?name=$(basename "$ipk")"
done

echo "所有操作完成！"
