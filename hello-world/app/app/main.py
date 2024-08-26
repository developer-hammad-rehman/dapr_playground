from fastapi import FastAPI
import requests


app = FastAPI()


@app.get('/')
def read_root():
    return {"status":"Ok"}


@app.get("/check-dapr")
def check_dapr():
    try:
        response = requests.get("http://localhost:3500/v1.0/healthz")
        if response.status_code == 204:
            return {"dapr_status": "Dapr is running, but no content returned"}
        elif response.status_code == 200:
            return {"dapr_status": "Dapr is up and running", "details": response.json()}
        else:
            return {"dapr_status": "Dapr health check failed", "details": response.text}
    except requests.RequestException as e:
        return {"dapr_status": "Failed to connect to Dapr", "error": str(e)}