from flask import Flask, make_response
import platform
import psutil
from datetime import datetime
import sys

app = Flask(__name__)

@app.route("/")
def index():
    data = {
        "platform": platform.platform(),
        "upSince": datetime.fromtimestamp(psutil.boot_time()).strftime('%d %B, %Y %H:%M:%S'),
        "diskUsage": psutil.disk_usage('/').percent,
        "memoryUsage": psutil.virtual_memory().percent,
        "memoryAvail": round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total, 1),
        "cpuUsage": psutil.cpu_percent(interval=None, percpu=False),
        "statusText": "Online",
        "online": True
    }
    return make_response(data)

if __name__ == "__main__":
    if(len(sys.argv) > 1 and sys.argv[1].isdigit()):
        print(f"Starting client on port {sys.argv[1]}")
        app.run(host="0.0.0.0", port=int(sys.argv[1]), debug=False)
    else:
        print(f"Starting client on port 8191")
        app.run(host="0.0.0.0", port=8191, debug=False)