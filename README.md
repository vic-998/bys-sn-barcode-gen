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

> 参数说明（网页内可调）：静区、条码高度、线条宽度、文字大小、文字间距。

## 打印尺寸（给别人描述用）

SVG 文件里 `width`/`height` 就是 100% 缩放时的**实际毫米尺寸**（在网页「效果预览」下方也会实时显示）。

Code128 单行条码的尺寸公式：

```
宽 W = 2 × 静区(quiet_zone) + 模块数 × 线条宽度(module_width)
高 H = 上边距(1) + 下边距(1) + 条码高度(module_height) + 文字高度/2 + 文字间距(text_distance)
```

- `模块数` 由 SN 长度决定（纯数字会自动用 Code128-C 压缩，16 位数字 = 123 个模块）。
- `文字高度/2 = font_size × 0.3528 ÷ 2`（pt 转 mm）。

**默认参数**（静区 2mm、线条 0.3mm、条码高 15mm、文字 10pt、间距 1.5mm）实测：

| SN 位数 | 宽 mm | 高 mm |
| --- | --- | --- |
| 8 位 | 27.70 | 20.26 |
| 16 位 | 40.90 | 20.26 |
| 22 位 | 50.80 | 20.26 |

> 高度只与高度/字号/间距有关，和 SN 长度无关；宽度随 SN 变长而变宽。
> 打印时选择「实际大小 / 100%」即可得到上表尺寸。

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
