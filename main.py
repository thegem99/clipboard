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

/* Copy button */
.copy-btn {
    position:absolute;
    top:8px;
    right:8px;
    background:#4A90E2;
    color:white;
    border:none;
    border-radius:5px;
    padding:5px 10px;
    cursor:pointer;
}
.copy-btn:hover {
    background:#357ABD;
}
</style>

<script>
function showSection(name){
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(name).classList.add('active');
    document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
    document.getElementById(name+'-btn').classList.add('active');
}

// Copy function
function copyReceived(btn){
    let text = document.getElementById("received-text").innerText;

    navigator.clipboard.writeText(text).then(() => {
        btn.innerText = "✅";
        setTimeout(() => btn.innerText = "📋", 1500);
    }).catch(() => {
        btn.innerText = "❌";
    });
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
    <button id="image-btn" onclick="showSection('image')">Image</button>
</nav>

<div class="container">

<!-- Text Section -->
<div id="text" class="section">
    <h2>📤 Send Text</h2>
    <form method="POST" action="/send_text">
        <textarea name="data" placeholder="Enter your text...">{{ text_value or "" }}</textarea>
        <button class="send" type="submit">Send Text</button>
    </form>
    <p>{{ code }}</p>

    <h2>📥 Receive Text</h2>
    <form method="POST" action="/get">
        <input name="code" placeholder="Enter code" value="{{ code_value or '' }}"/>
        <button class="send" type="submit">Get Data</button>
    </form>

    <div style="position:relative; margin-top:10px;">
        <button class="copy-btn" onclick="copyReceived(this)">📋</button>
        <pre id="received-text">{{ received }}</pre>
    </div>
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
        <input name="code" placeholder="Enter code" value="{{ image_code_value or '' }}"/>
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
