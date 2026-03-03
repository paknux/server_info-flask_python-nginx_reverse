from flask import Flask, render_template_string
import socket
import psutil
import platform

app = Flask(__name__)

@app.route('/')
def index():
    # Mengambil informasi server
    hostname = socket.gethostname()
    # Mengambil IP Privat (untuk info di balik reverse proxy)
    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "127.0.0.1"
        
    os_info = f"{platform.system()} {platform.release()}"
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_info = psutil.virtual_memory()
    
    # Template HTML dengan fitur Dark Mode & Header
    html_template = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Server Monitor</title>
        <style>
            :root {
                --bg-color: #f4f4f9;
                --card-bg: #ffffff;
                --text-color: #333333;
                --label-color: #555555;
                --border-color: #eeeeee;
                --header-bg: #333333;
                --header-text: #ffffff;
            }

            /* Variabel Warna Dark Mode */
            [data-theme="dark"] {
                --bg-color: #121212;
                --card-bg: #1e1e1e;
                --text-color: #e0e0e0;
                --label-color: #bbbbbb;
                --border-color: #333333;
                --header-bg: #000000;
                --header-text: #00ff00; /* Hijau terminal */
            }

            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: var(--bg-color); 
                color: var(--text-color);
                margin: 0;
                transition: background 0.3s, color 0.3s;
            }

            header {
                background: var(--header-bg);
                color: var(--header-text);
                padding: 1rem 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }

            .container { padding: 50px 20px; }

            .card { 
                background: var(--card-bg); 
                padding: 25px; 
                border-radius: 12px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
                max-width: 500px; 
                margin: auto; 
                transition: background 0.3s;
            }

            h2 { margin-top: 0; color: var(--text-color); border-bottom: 2px solid var(--border-color); padding-bottom: 10px; }
            .info { margin: 15px 0; font-size: 1.1em; }
            .label { font-weight: bold; color: var(--label-color); }
            
            .btn-toggle {
                background: #444;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 0.9em;
                transition: 0.2s;
            }
            .btn-toggle:hover { background: #666; }

            hr { border: 0; border-top: 1px solid var(--border-color); }
        </style>

        <script>
            // Script ini diletakkan di head agar tema langsung diterapkan sebelum halaman muncul (mencegah flash putih)
            const savedTheme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', savedTheme);
        </script>
    </head>
    <body>

        <header>
            <div style="font-weight: bold; font-size: 1.2em;">🚀 ServerInfo Pro</div>
            <button class="btn-toggle" onclick="toggleTheme()" id="theme-btn">
                🌓 Ganti Mode
            </button>
        </header>

        <div class="container">
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
        </div>

        <script>
            function toggleTheme() {
                const currentTheme = document.documentElement.getAttribute('data-theme');
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                
                document.documentElement.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
            }
        </script>
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
    app.run(host='0.0.0.0', port=5000, debug=True)