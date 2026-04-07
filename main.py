from flask import Flask, request, render_template_string, send_file
import requests
import io

app = Flask(__name__)

API_BASE = "https://clipboardserver-production.up.railway.app"

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Clipboard Share</title>
<style>
body { font-family: 'Segoe UI'; margin:0; background:#f4f4f9; }
header { background:#4A90E2; color:white; padding:15px; text-align:center; font-size:24px; }
nav { display:flex; justify-content:center; background:#357ABD; }
nav button { background:none; border:none; color:white; padding:15px 30px; cursor:pointer; }
nav button.active { background:#1D3B66; }
.container { max-width:700px; margin:30px auto; padding:20px; background:white; border-radius:10px; }
textarea, input { width:100%; padding:10px; margin-top:10px; }
button.send { background:#4A90E2; color:white; border:none; padding:10px; margin-top:10px; width:100%; }
pre { background:#eee; padding:10px; }
img.preview { max-width:100%; margin-top:10px; }
.section { display:none; }
.section.active { display:block; }
.download-btn { display:inline-block; margin-top:10px; padding:10px; background:#28a745; color:white; text-decoration:none; }
</style>

<script>
function showSection(name){
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(name).classList.add('active');

    document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
    document.getElementById(name+'-btn').classList.add('active');
}

window.onload = function() {
    let section = "{{ section or 'text' }}";
    showSection(section);
};
</script>
</head>
<body>

<header>📋 Clipboard Share</header>

<nav>
    <button id="text-btn" onclick="showSection('text')">Text</button>
    <button id="file-btn" onclick="showSection('file')">File</button>
</nav>

<div class="container">

<!-- TEXT -->
<div id="text" class="section">
    <h2>Send Text</h2>
    <form method="POST" action="/send_text">
        <textarea name="data">{{ text_value or "" }}</textarea>
        <button class="send">Send</button>
    </form>
    <p>{{ code }}</p>

    <h2>Receive Text</h2>
    <form method="POST" action="/get">
        <input name="code" value="{{ code_value or '' }}">
        <button class="send">Get</button>
    </form>
    <pre>{{ received }}</pre>
</div>

<!-- FILE -->
<div id="file" class="section">
    <h2>Send File</h2>
    <form method="POST" action="/send_file" enctype="multipart/form-data">
        <input type="file" name="file">
        <button class="send">Upload</button>
    </form>
    <p>{{ file_code }}</p>

    <h2>Receive File</h2>
    <form method="POST" action="/get">
        <input name="code" value="{{ file_code_value or '' }}">
        <button class="send">Get</button>
    </form>

    {% if file %}
        {% if is_image %}
            <img class="preview" src="/file/{{ file_code }}">
        {% endif %}
        <br>
        <a class="download-btn" href="/file/{{ file_code }}">Download File</a>
    {% endif %}
</div>

</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/send_text", methods=["POST"])
def send_text():
    data = request.form.get("data")

    res = requests.post(f"{API_BASE}/api/send", json={"data": data})

    try:
        code = res.json().get("code")
    except:
        code = "Error"

    return render_template_string(
        HTML_PAGE,
        code=code,
        text_value=data,
        section="text"
    )


@app.route("/send_file", methods=["POST"])
def send_file_route():
    file = request.files.get("file")

    if not file:
        return render_template_string(
            HTML_PAGE,
            file_code="No file selected",
            section="file"
        )

    res = requests.post(
        f"{API_BASE}/api/send",
        files={"file": (file.filename, file.stream, file.content_type)}
    )

    try:
        code = res.json().get("code")
    except:
        code = "Upload failed"

    return render_template_string(
        HTML_PAGE,
        file_code=code,
        file=True,
        is_image=file.content_type.startswith("image"),
        section="file"
    )


@app.route("/get", methods=["POST"])
def get():
    code = request.form.get("code")

    res = requests.get(f"{API_BASE}/api/get/{code}")

    content_type = res.headers.get("Content-Type", "")

    # FILE
    if "application/json" not in content_type:
        return render_template_string(
            HTML_PAGE,
            file=True,
            file_code=code,
            file_code_value=code,
            is_image=content_type.startswith("image"),
            section="file"
        )

    # TEXT
    result = res.json()
    return render_template_string(
        HTML_PAGE,
        received=result.get("data", result.get("error")),
        code_value=code,
        text_value=result.get("data"),
        section="text"
    )


@app.route("/file/<code>")
def get_file(code):
    res = requests.get(f"{API_BASE}/api/get/{code}")

    return send_file(
        io.BytesIO(res.content),
        mimetype=res.headers.get("Content-Type", "application/octet-stream"),
        download_name=code
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
