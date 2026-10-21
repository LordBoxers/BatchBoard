import datetime
import random
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config import settings

app = FastAPI()


@app.get("/api/batch/current")
def get_current_batch():
    now = datetime.datetime.now()
    # 24 datapunkter med 2 timers mellemrum (sidste 48 timer)
    timestamps = [now - datetime.timedelta(hours=i * 2) for i in reversed(range(24))]
    labels = [ts.strftime("%d/%m %H:%M") for ts in timestamps]

    # Graf 1: Temperatur (°C) - Faktisk temperatur svæver tæt omkring setpoint på 20.0°C
    temp_target = 20.0
    temp_actual = [
        round(temp_target + random.uniform(-0.4, 0.5), 1) for _ in range(24)
    ]

    # Graf 2: Vægtfylde (Specific Gravity) - Jævnt faldende kurve fra 1.050 mod 1.012
    gravity_values = [
        round(1.050 - (i * 0.0016) + random.uniform(-0.0004, 0.0004), 3)
        for i in range(24)
    ]

    # Graf 3: Tryk i tanken (PSI) - Stiger langsomt fra 0 til ca. 12 PSI
    pressure_values = [
        round(min(12.0, (i * 0.52) + random.uniform(-0.2, 0.3)), 1)
        for i in range(24)
    ]

    return {
        "metadata": {
            "batch_name": "Batch #42 - Hazy IPA",
            "recipe": "New England IPA",
            "status": "Aktiv Gæring (Dag 3)",
            "last_updated": now.strftime("%H:%M:%S"),
            "target_temp": temp_target,
            "original_gravity": 1.052,
            "target_final_gravity": 1.012,
        },
        "charts": {
            "temperature": {
                "title": "Gæringstemperatur",
                "unit": "°C",
                "labels": labels,
                "series": [
                    {
                        "name": "Aktuel Måling",
                        "data": temp_actual,
                        "color": "#f0883e",
                    },
                    {
                        "name": "Måltemperatur (Setpoint)",
                        "data": [temp_target] * 24,
                        "color": "#8b949e",
                    },
                ],
            },
            "gravity": {
                "title": "Massefylde (Specific Gravity)",
                "unit": "SG",
                "labels": labels,
                "series": [
                    {
                        "name": "Aktuel SG",
                        "data": gravity_values,
                        "color": "#58a6ff",
                    }
                ],
            },
            "pressure": {
                "title": "Tanktryk",
                "unit": "PSI",
                "labels": labels,
                "series": [
                    {
                        "name": "Aktuel PSI",
                        "data": pressure_values,
                        "color": "#3fb950",
                    }
                ],
            },
        },
    }


# Server statiske filer (HTML/JS)
app.mount("/", StaticFiles(directory="static", html=True), name="static")