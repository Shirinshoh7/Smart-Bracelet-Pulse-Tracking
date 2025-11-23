from flask import Flask, Response, jsonify
import random
import time

app = Flask(__name__)

pulse_history = []  # храним историю (время, пульс)


@app.route("/")
def index():
    html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Монитор браслета</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #e9f5ff, #ffffff);
                text-align: center;
                padding: 40px;
                color: #2c3e50;
            }
            h1 {
                font-size: 36px;
                margin-bottom: 20px;
            }
            .pulse {
                font-size: 70px;
                font-weight: bold;
                color: #e74c3c;
                margin-bottom: 15px;
            }
            .status {
                font-size: 28px;
                margin-top: 10px;
                font-weight: 600;
            }
            .normal { color: #27ae60; }
            .high { color: #e67e22; }
            .critical { color: #c0392b; }

            .controls {
                margin-top: 40px;
            }
            button {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                margin: 5px;
            }
            button:hover {
                background-color: #2980b9;
            }

            canvas {
                margin-top: 40px;
                width: 90%%;
                max-width: 800px;
                height: 400px;
            }

            .footer {
                margin-top: 40px;
                font-size: 14px;
                color: #7f8c8d;
            }
        </style>
    </head>
    <body>
        <h1>📟 Smart Bracelet Monitor</h1>
        <div id="pulse" class="pulse">--</div>
        <div id="status" class="status">Загрузка...</div>

        <div class="controls">
            <button onclick="updatePulse()">🔄 Обновить сейчас</button>
            <button onclick="showAverage()">📊 Средний пульс за час</button>
        </div>

        <canvas id="pulseChart"></canvas>

        <div class="footer">⏱ Обновляется автоматически каждую секунду</div>

        <script>
            let chart;
            const maxPoints = 30; // показываем последние 30 секунд

            async function updatePulse() {
                const response = await fetch('/data');
                const data = await response.json();
                const pulse = data.pulse;
                const timeLabel = new Date().toLocaleTimeString();

                document.getElementById('pulse').innerText = pulse + " bpm";
                const status = document.getElementById('status');

                if (pulse < 60) {
                    status.innerText = "Пониженный пульс ❄️";
                    status.className = "status high";
                } else if (pulse <= 90) {
                    status.innerText = "Норма ❤️";
                    status.className = "status normal";
                } else if (pulse <= 110) {
                    status.innerText = "Повышенный пульс ⚠️";
                    status.className = "status high";
                } else {
                    status.innerText = "Опасно! Очень высокий пульс 🚨";
                    status.className = "status critical";
                }

                // Добавляем данные в график
                if (chart) {
                    chart.data.labels.push(timeLabel);
                    chart.data.datasets[0].data.push(pulse);
                    if (chart.data.labels.length > maxPoints) {
                        chart.data.labels.shift();
                        chart.data.datasets[0].data.shift();
                    }
                    chart.update();
                }
            }

            async function showAverage() {
                const response = await fetch('/average');
                const data = await response.json();
                alert("📊 Средний пульс за последний час: " + data.average + " bpm");
            }

            function createChart() {
                const ctx = document.getElementById('pulseChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: [],
                        datasets: [{
                            label: 'Изменение пульса (bpm)',
                            data: [],
                            borderColor: '#e74c3c',
                            borderWidth: 3,
                            fill: false,
                            tension: 0.3
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: false,
                                min: 40,
                                max: 140
                            }
                        }
                    }
                });
            }

            createChart();
            setInterval(updatePulse, 1000);
            updatePulse();
        </script>
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")


@app.route("/data")
def get_data():
    pulse = random.randint(55, 130)
    pulse_history.append((time.time(), pulse))
    if len(pulse_history) > 3600:
        pulse_history.pop(0)
    return jsonify({"pulse": pulse})


@app.route("/average")
def get_average():
    current_time = time.time()
    last_hour = [p for t, p in pulse_history if current_time - t <= 3600]
    avg = round(sum(last_hour) / len(last_hour), 1) if last_hour else 0
    return jsonify({"average": avg})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
