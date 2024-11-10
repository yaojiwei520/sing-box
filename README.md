# downlaod-sing-box of shell


---
# uploads.sh 
# 脚本说明
## 1.版本管理：

* 脚本使用 version.txt 文件来跟踪当前版本号。
* 每次运行脚本时，版本号会自动增加，例如从 v1.0 到 v1.1，依此类推。
## 2.下载文件：

* 脚本会下载指定的 .ipk 文件。
## 3.创建 GitHub Release：

* 使用 GitHub API 创建新的 Release，并将版本说明设置为更新次数。
## 4.上传文件：

* 将下载的 .ipk 文件上传到刚创建的 Release。
