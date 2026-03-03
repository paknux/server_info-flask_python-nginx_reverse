from flask import Flask, render_template_string
import socket
import psutil
import platform
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Mengambil informasi server
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_info = f"{platform.system()} {platform.release()}"
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_info = psutil.virtual_memory()
    
    # Template HTML sederhana (Inline)
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Server Monitor</title>
        <style>
            body { font-family: sans-serif; background: #f4f4f9; padding: 50px; }
            .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-width: 500px; margin: auto; }
            h2 { color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }
            .info { margin: 15px 0; font-size: 1.1em; }
            .label { font-weight: bold; color: #555; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🖥️ Server Information</h2>
            <div class="info"><span class="label">Server Name:</span> {{ hostname }}</div>
            <div class="info"><span class="label">IP Address:</span> {{ ip_address }}</div>
            <div class="info"><span class="label">OS:</span> {{ os_info }}</div>
            <hr>
            <h3>📊 Live Stats</h3>
            <div class="info"><span class="label">CPU Usage:</span> {{ cpu_usage }}%</div>
            <div class="info"><span class="label">RAM Usage:</span> {{ ram_percent }}% ({{ ram_used }}GB / {{ ram_total }}GB)</div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(
        html_template, 
        hostname=hostname, 
        ip_address=ip_address, 
        os_info=os_info,
        cpu_usage=cpu_usage,
        ram_percent=ram_info.percent,
        ram_used=round(ram_info.used / (1024**3), 2),
        ram_total=round(ram_info.total / (1024**3), 2)
    )

if __name__ == '__main__':
    # Jalankan di host 0.0.0.0 agar bisa diakses dari jaringan lain
    app.run(host='0.0.0.0', port=5000, debug=True)