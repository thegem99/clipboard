from flask import Flask, request, render_template_string, send_file
import requests
import io

app = Flask(__name__)

# Replace this with your deployed API URL
API_BASE = "https://clipboardserver-production.up.railway.app"  

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Data Share Client</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 40px auto; }
        textarea, input { width: 100%; padding: 10px; margin-top: 10px; }
        button { padding: 10px; margin-top: 10px; width: 100%; }
        .box { border: 1px solid #ccc; padding: 20px; margin-bottom: 30px; }
        img { max-width: 100%; margin-top: 10px; }
    </style>
</head>
<body>

<h2>📤 Send Text</h2>
<div class="box">
    <form method="POST" action="/send_text">
        <textarea name="data" placeholder="Enter text..."></textarea>
        <button type="submit">Send Text</button>
    </form>
    <p>{{ code }}</p>
</div>

<h2>📤 Send Image</h2>
<div class="box">
    <form method="POST" action="/send_file" enctype="multipart/form-data">
        <input type="file" name="file"/>
        <button type="submit">Upload Image</button>
    </form>
    <p>{{ file_code }}</p>
</div>

<h2>📥 Receive</h2>
<div class="box">
    <form method="POST" action="/get">
        <input name="code" placeholder="Enter code"/>
        <button type="submit">Get Data</button>
    </form>

    <pre>{{ received }}</pre>

    {% if image %}
        <img src="/image/{{ image_code }}">
    {% endif %}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

# Send text
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

# Send file
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

# Get data
@app.route("/get", methods=["POST"])
def get():
    code = request.form.get("code")
    res = requests.get(f"{API_BASE}/api/get/{code}")

    if "application/json" not in res.headers.get("Content-Type", ""):
        # It's a file
        return render_template_string(HTML_PAGE, image=True, image_code=code)

    result = res.json()
    return render_template_string(HTML_PAGE, received=result.get("data", result.get("error")))

# Serve image from API
@app.route("/image/<code>")
def get_image(code):
    res = requests.get(f"{API_BASE}/api/get/{code}")
    return send_file(io.BytesIO(res.content), mimetype=res.headers.get("Content-Type", "image/png"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
