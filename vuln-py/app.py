from flask import Flask, request, escape
import subprocess, yaml, base64, pickle, hashlib

app = Flask(__name__)

@app.route("/run")
def run():
    cmd = request.args.get("cmd", "echo hi")
    # ❌ shell=True with user input: command injection
    subprocess.Popen(cmd, shell=True)
    return "OK"

@app.route("/yaml")
def parse_yaml():
    s = request.args.get("data", "{}")
    # ❌ unsafe YAML load (no SafeLoader)
    data = yaml.load(s)
    return escape(str(data))

@app.route("/pickle")
def do_pickle():
    # ❌ insecure deserialization of untrusted data
    b64 = request.args.get("data", "")
    try:
      raw = base64.b64decode(b64)
      obj = pickle.loads(raw)
      return str(obj)
    except Exception as e:
      return "error: " + str(e), 400

@app.route("/md5")
def weak_hash():
    # ❌ weak hash algorithm
    pw = request.args.get("pw", "password")
    return hashlib.md5(pw.encode()).hexdigest()

if __name__ == "__main__":
    app.run(port=5000)
