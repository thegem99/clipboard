from flask import Flask, request, render_template_string, send_file
import requests
import io

app = Flask(__name__)

API_BASE = "https://clipboardserver-production.up.railway.app"  # replace with your API

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Clipboard Share</title>
<style>
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin:0; background:#f4f4f9; }
header { background:#4A90E2; color:white; padding:15px; text-align:center; font-size:24px; }
nav { display:flex; justify-content:center; background:#357ABD; }
nav button { background:none; border:none; color:white; padding:15px 30px; cursor:pointer; font-size:16px; transition:0.3s; }
nav button:hover { background:#285A8F; }
nav button.active { background:#1D3B66; }
.container { max-width:700px; margin:30px auto; padding:20px; background:white; box-shadow:0 0 15px rgba(0,0,0,0.1); border-radius:10px; }
textarea, input { width:100%; padding:12px; margin-top:10px; border-radius:5px; border:1px solid #ccc; font-size:16px; }
button.send { background:#4A90E2; color:white; border:none; padding:12px; margin-top:10px; cursor:pointer; width:100%; font-size:16px; border-radius:5px; transition:0.3s; }
button.send:hover { background:#357ABD; }
pre { background:#f0f0f0; padding:15px; border-radius:5px; overflow-x:auto; }
img.preview { max-width:100%; margin-top:10px; border-radius:5px; }
.download-btn { background:#28a745; color:white; padding:10px; margin-top:10px; display:inline-block; border-radius:5px; text-decoration:none; transition:0.3s; }
.download-btn:hover { background:#218838; }
.section { display:none; }
.section.active { display:block; }
</style>
<script>
function showSection(name){
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(name).classList.add('active');
    document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
    document.getElementById(name+'-btn').classList.add('active');
}
window.onload = function(){ showSection('text'); }
</script>
</head>
<body>

<header>📋 Clipboard Share</header>
<nav>
    <button id="text-btn" onclick="showSection('text')">Text</button>
    <button id="image-btn" onclick="showSection('image')">Image</button>
</nav>

<div class="container">

<!-- Text Section -->
<div id="text" class="section">
    <h2>📤 Send Text</h2>
    <form method="POST" action="/send_text">
        <textarea name="data" placeholder="Enter your text..."></textarea>
        <button class="send" type="submit">Send Text</button>
    </form>
    <p>{{ code }}</p>

    <h2>📥 Receive Text</h2>
    <form method="POST" action="/get">
        <input name="code" placeholder="Enter code"/>
        <button class="send" type="submit">Get Data</button>
    </form>
    <pre>{{ received }}</pre>
</div>

<!-- Image Section -->
<div id="image" class="section">
    <h2>📤 Send Image</h2>
    <form method="POST" action="/send_file" enctype="multipart/form-data">
        <input type="file" name="file"/>
        <button class="send" type="submit">Upload Image</button>
    </form>
    <p>{{ file_code }}</p>

    <h2>📥 Receive Image</h2>
    <form method="POST" action="/get">
        <input name="code" placeholder="Enter code"/>
        <button class="send" type="submit">Get Image</button>
    </form>

    {% if image %}
        <img class="preview" src="/image/{{ image_code }}">
        <a class="download-btn" href="/image/{{ image_code }}" download="image">Download Image</a>
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
        result = res.json()
        code = result.get("code", "Error")
    except:
        code = "Upload failed"
    return render_template_string(HTML_PAGE, code=code)

@app.route("/send_file", methods=["POST"])
def send_file_route():
    file = request.files.get("file")
    if not file:
        return render_template_string(HTML_PAGE, file_code="No file selected")
    res = requests.post(f"{API_BASE}/api/send", files={"file": file})
    try:
        result = res.json()
        code = result.get("code", "Error")
    except:
        print("API RESPONSE:", res.text)
        code = "Upload failed"
    return render_template_string(HTML_PAGE, file_code=code)

@app.route("/get", methods=["POST"])
def get():
    code = request.form.get("code")
    res = requests.get(f"{API_BASE}/api/get/{code}")
    if "application/json" not in res.headers.get("Content-Type", ""):
        return render_template_string(HTML_PAGE, image=True, image_code=code)
    result = res.json()
    return render_template_string(HTML_PAGE, received=result.get("data", result.get("error")))

@app.route("/image/<code>")
def get_image(code):
    res = requests.get(f"{API_BASE}/api/get/{code}")
    return send_file(io.BytesIO(res.content), mimetype=res.headers.get("Content-Type", "image/png"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
