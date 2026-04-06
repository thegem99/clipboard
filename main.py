from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

API_BASE = "https://clipboardserver-production.up.railway.app/"  # 👈 change this

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Data Share Client</title>
    <style>
        body {
            font-family: Arial;
            max-width: 600px;
            margin: 40px auto;
        }
        textarea, input {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
        }
        button {
            padding: 10px;
            margin-top: 10px;
            width: 100%;
        }
        .box {
            border: 1px solid #ccc;
            padding: 20px;
            margin-bottom: 30px;
        }
    </style>
</head>
<body>

<h2>📤 Send Data</h2>
<div class="box">
    <form method="POST" action="/send">
        <textarea name="data" placeholder="Enter data..."></textarea>
        <button type="submit">Send</button>
    </form>
    <p>{{ code }}</p>
</div>

<h2>📥 Receive Data</h2>
<div class="box">
    <form method="POST" action="/get">
        <input name="code" placeholder="Enter code"/>
        <button type="submit">Get Data</button>
    </form>
    <pre>{{ received }}</pre>
</div>

</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE)


@app.route("/send", methods=["POST"])
def send():
    data = request.form.get("data")

    res = requests.post(
        f"{API_BASE}/api/send",
        json={"data": data}
    )

    result = res.json()
    return render_template_string(HTML_PAGE, code=result.get("code", result))


@app.route("/get", methods=["POST"])
def get():
    code = request.form.get("code")

    res = requests.get(f"{API_BASE}/api/get/{code}")
    result = res.json()

    return render_template_string(
        HTML_PAGE,
        received=result.get("data", result.get("error"))
    )


if __name__ == "__main__":
    app.run(debug=True)
