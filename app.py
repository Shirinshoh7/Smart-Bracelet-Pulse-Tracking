import random
import time
from collections import deque
from flask import Flask, Response, jsonify

app = Flask(__name__)

# Используем deque для эффективного хранения истории (макс. 3600 записей)
# Это автоматически удаляет старые записи при добавлении новых
pulse_history = deque(maxlen=3600)

UI_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Bracelet Pro</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary: #e74c3c;
            --success: #27ae60;
            --warning: #e67e22;
            --bg: #f8f9fa;
            --card: #ffffff;
        }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg);
            color: #2c3e50;
            margin: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            background: var(--card);
            padding: 30px;
            border-radius: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            max-width: 800px;
            width: 100%;
            text-align: center;
        }

        h1 { font-weight: 800; letter-spacing: -1px; margin-bottom: 30px; }

        .pulse-display {
            padding: 20px;
            border-radius: 20px;
            background: rgba(231, 76, 60, 0.05);
            margin-bottom: 25px;
        }

        .pulse-value {
            font-size: 82px;
            font-weight: 900;
            color: var(--primary);
            line-height: 1;
        }

        .unit { font-size: 24px; color: #95a5a6; }

        .status-badge {
            display: inline-block;
            padding: 8px 20px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 18px;
            transition: all 0.3s ease;
        }

        .chart-container {
            margin-top: 30px;
            height: 350px;
            position: relative;
        }

        .btn-group {
            margin-top: 25px;
            display: flex;
            gap: 10px;
            justify-content: center;
        }

        button {
            padding: 12px 24px;
            border-radius: 12px;
            border: none;
            background: #2c3e50;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, background 0.2s;
        }

        button:hover { background: #34495e; transform: translateY(-2px); }
        button.secondary { background: #ecf0f1; color: #2c3e50; }

        /* Status Colors */
        .status-normal { background: #d4edda; color: var(--success); }
        .status-high { background: #fff3cd; color: var(--warning); }
        .status-danger { background: #f8d7da; color: var(--primary); }
    </style>
</head>
<body>
    <div class="container">
        <h1>Smart Bracelet <span style="color: var(--primary)">Pro</span></h1>
        
        <div class="pulse-display">
            <div id="pulse" class="pulse-value">--</div>
            <div class="unit">BPM</div>
            <div id="status" class="status-badge">Инициализация...</div>
        </div>

        <div class="chart-container">
            <canvas id="pulseChart"></canvas>
        </div>

        <div class="btn-group">
            <button onclick="updatePulse()">Обновить сейчас</button>
            <button class="secondary" onclick="showAverage()">Средний за час</button>
        </div>
    </div>

    <script>
        const UI = {
            pulse: document.getElementById('pulse'),
            status: document.getElementById('status'),
            ctx: document.getElementById('pulseChart').getContext('2d')
        };

        let pulseChart;
        const MAX_POINTS = 30;

        function initChart() {
            pulseChart = new Chart(UI.ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Пульс',
                        data: [],
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.1)',
                        borderWidth: 4,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { min: 40, max: 140, grid: { display: false } },
                        x: { grid: { display: false } }
                    }
                }
            });
        }

        async function updatePulse() {
            try {
                const response = await fetch('/data');
                const data = await response.json();
                const pulse = data.pulse;

                UI.pulse.innerText = pulse;
                updateStatus(pulse);
                updateChart(pulse);
            } catch (e) { console.error("Ошибка загрузки данных"); }
        }

        function updateStatus(pulse) {
            let text, className;
            if (pulse < 60) { text = "Пониженный ❄️"; className = "status-high"; }
            else if (pulse <= 90) { text = "Норма ❤️"; className = "status-normal"; }
            else if (pulse <= 110) { text = "Повышенный ⚠️"; className = "status-high"; }
            else { text = "Опасно! 🚨"; className = "status-danger"; }
            
            UI.status.innerText = text;
            UI.status.className = `status-badge ${className}`;
        }

        function updateChart(value) {
            const time = new Date().toLocaleTimeString([], { hour12: false, minute: '2min', second: '2min' });
            pulseChart.data.labels.push(time);
            pulseChart.data.datasets[0].data.push(value);

            if (pulseChart.data.labels.length > MAX_POINTS) {
                pulseChart.data.labels.shift();
                pulseChart.data.datasets[0].data.shift();
            }
            pulseChart.update('none'); // 'none' для плавной анимации
        }

        async function showAverage() {
            const res = await fetch('/average');
            const data = await res.json();
            alert(`📈 Средний пульс: ${data.average} BPM`);
        }

        initChart();
        setInterval(updatePulse, 1000);
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return Response(UI_HTML, mimetype="text/html")

@app.route("/data")
def get_data():
    pulse = random.randint(58, 125)
    pulse_history.append({"time": time.time(), "value": pulse})
    return jsonify({"pulse": pulse})

@app.route("/average")
def get_average():
    if not pulse_history:
        return jsonify({"average": 0})
    
    # Считаем среднее только по записям из deque
    values = [item["value"] for item in pulse_history]
    avg = round(sum(values) / len(values), 1)
    return jsonify({"average": avg})

if __name__ == "__main__":
    # debug=True поможет при разработке
    app.run(host="0.0.0.0", port=5000, debug=False)
