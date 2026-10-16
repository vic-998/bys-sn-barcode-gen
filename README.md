# SN 条码批量生成器

输入纯数字 SN，批量生成 Code128 条码，每个条码下方显示 `SN:xxxxxxxxxxxx`，
导出为 **SVG 矢量文本** 压缩包（长数字不会像 Excel 那样变科学计数法或丢精度）。

## 功能

- 网页界面：粘贴 / 从 Excel 复制一列 / 导入 TXT、CSV 文件
- 自动去重、过滤非法字符，单次最多 5000 个
- 条码下方按图显示 `SN:2241122660700591` 格式
- 左右静区 ≥ 2mm（可调），黑条白底，SVG 按比例缩放打印
- 一键下载 `sn-barcodes.zip`，内含每个 `SN.svg` + `SN列表.txt`

## 直接运行（开发模式）

双击 `run.bat`，或：

```bat
pip install -r requirements.txt
python app.py
```

浏览器访问 http://127.0.0.1:5000

## 打包成 EXE

双击 `build.bat`。完成后得到 `dist\sn-barcode-gen.exe`，
双击 exe 会自动打开浏览器，无需安装 Python。

> 参数说明（网页内可调）：静区、条码高度、线条宽度、文字大小。

## 目录结构

```
sn-barcode-generator/
├─ app.py            后端（Flask + python-barcode）
├─ templates/
│  └─ index.html     前端页面
├─ requirements.txt
├─ run.bat           开发运行
└─ build.bat         打包 EXE
```
