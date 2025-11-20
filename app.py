from flask import Flask, send_file
import os
import subprocess

app = Flask("NR-CODEX")

SSH_DIR = "/tmp/.ssh"
PRIVATE_KEY = f"{SSH_DIR}/id_ed25519"
PUBLIC_KEY = f"{SSH_DIR}/id_ed25519.pub"

# Create SSH directory & Keys if missing
def create_ssh_key():
    if not os.path.exists(SSH_DIR):
        os.makedirs(SSH_DIR, exist_ok=True)

    if not os.path.exists(PRIVATE_KEY):
        subprocess.run([
            "ssh-keygen", "-t", "ed25519",
            "-N", "", "-f", PRIVATE_KEY
        ])

@app.route("/")
def home():
    create_ssh_key()

    with open(PUBLIC_KEY, "r") as f:
        pub = f.read()

    return f"""
    <h1>🔐 NR-CODEX SSH Key Generator</h1>

    <h3>Your Public Key:</h3>
    <pre>{pub}</pre>

    <p>Put this key in your VPS:</p>
    <pre>~/.ssh/authorized_keys</pre>

    <a href="/download">
        <button style="padding:10px 20px;font-size:16px;background:black;color:white;border-radius:10px;">
            Download Private Key
        </button>
    </a>
    """

@app.route("/download")
def download_key():
    create_ssh_key()
    return send_file(PRIVATE_KEY, as_attachment=True)

if __name__ == "__main__":
    create_ssh_key()
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
