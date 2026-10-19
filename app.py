import os
import re
import sys
import io
import zipfile
import webbrowser
import threading

import barcode
from barcode.writer import SVGWriter
from flask import Flask, render_template, request, send_file, jsonify

MAX_BATCH = 5000
INVALID_FILENAME = re.compile(r'[\\/:*?"<>|\r\n\t]')


def resource_path(rel):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=None,
)


def clean_sn(raw):
    return re.sub(r"\s+", "", str(raw or ""))


def safe_name(sn):
    return INVALID_FILENAME.sub("_", sn)


def make_svg(sn, opts):
    code = barcode.get("code128", sn, writer=SVGWriter())
    buf = io.BytesIO()
    code.write(
        buf,
        options={
            "write_text": True,
            "module_height": opts["module_height"],
            "module_width": opts["module_width"],
            "font_size": opts["font_size"],
            "quiet_zone": opts["quiet_zone"],
            "text_distance": opts["text_distance"],
            "background": "white",
            "foreground": "black",
        },
        text="SN:" + sn,
    )
    return buf.getvalue()


SIZE_RE = re.compile(r'width="([\d.]+)mm"\s+height="([\d.]+)mm"')


def svg_dimensions(sn, opts):
    match = SIZE_RE.search(make_svg(sn, opts).decode("utf-8"))
    if not match:
        return None
    return round(float(match.group(1)), 2), round(float(match.group(2)), 2)



def parse_sns(payload):
    result = []
    seen = set()
    dup = []
    for item in payload:
        sn = clean_sn(item)
        if not sn:
            continue
        if not re.fullmatch(r"[0-9A-Za-z]+", sn):
            continue
        if sn in seen:
            dup.append(sn)
            continue
        seen.add(sn)
        result.append(sn)
    return result, dup


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/preview")
def preview():
    sn = clean_sn(request.args.get("sn", ""))
    if not re.fullmatch(r"[0-9A-Za-z]+", sn or ""):
        return jsonify({"error": "SN 只能包含数字或字母"}), 400
    opts = read_options(request.args)
    svg = make_svg(sn, opts).decode("utf-8")
    return svg, 200, {"Content-Type": "image/svg+xml; charset=utf-8"}


@app.route("/api/size")
def size():
    sn = clean_sn(request.args.get("sn", ""))
    if not re.fullmatch(r"[0-9A-Za-z]+", sn or ""):
        return jsonify({"error": "SN 只能包含数字或字母"}), 400
    opts = read_options(request.args)
    dims = svg_dimensions(sn, opts)
    if not dims:
        return jsonify({"error": "无法计算尺寸"}), 500
    return jsonify({"sn": sn, "width_mm": dims[0], "height_mm": dims[1]})


def read_options(src):
    def num(key, default, lo, hi):
        try:
            v = float(src.get(key, default))
        except (TypeError, ValueError):
            v = default
        return max(lo, min(hi, v))

    return {
        "quiet_zone": num("quiet_zone", 2.0, 2.0, 20.0),
        "module_height": num("module_height", 15.0, 5.0, 60.0),
        "module_width": num("module_width", 0.3, 0.1, 2.0),
        "font_size": num("font_size", 10.0, 4.0, 40.0),
        "text_distance": num("text_distance", 1.5, 0.5, 10.0),
    }


@app.route("/api/generate", methods=["POST"])
def generate():
    if request.is_json:
        data = request.get_json(force=True, silent=True) or {}
    else:
        data = request.form.to_dict()
    raw = data.get("sns", "")
    if isinstance(raw, str):
        items = re.split(r"[\s,;]+", raw)
    else:
        items = raw

    sns, dup = parse_sns(items)
    if not sns:
        return jsonify({"error": "没有解析到有效的 SN"}), 400
    if len(sns) > MAX_BATCH:
        return jsonify({"error": f"一次最多生成 {MAX_BATCH} 个"}), 400

    opts = read_options(data)
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as zf:
        for sn in sns:
            zf.writestr(safe_name(sn) + ".svg", make_svg(sn, opts))
        zf.writestr(
            "SN列表.txt",
            "SN:\n" + "\n".join(sns) + "\n",
        )
    mem.seek(0)
    resp = send_file(
        mem,
        mimetype="application/zip",
        as_attachment=True,
        download_name="sn-barcodes.zip",
    )
    resp.headers["X-Count"] = str(len(sns))
    resp.headers["X-Duplicate"] = str(len(dup))
    return resp


def open_browser(port):
    webbrowser.open(f"http://127.0.0.1:{port}")


def main():
    port = int(os.environ.get("PORT", "5000"))
    if getattr(sys, "frozen", False):
        threading.Timer(1.0, open_browser, args=(port,)).start()
    app.run(host="127.0.0.1", port=port, debug=False, threaded=True)


if __name__ == "__main__":
    main()
