from typing import Annotated
from fastapi import Depends, FastAPI
from dapr.clients import DaprClient  , DaprInternalError

def get_dapr():
    with DaprClient() as dapr:
        yield dapr

app = FastAPI()


@app.get("/")
def read_root():
    return {"message" :"Ok"}


@app.get('/healthz')
def healthz_route(dapr : Annotated[DaprClient , Depends(get_dapr)]):
    try:
        metadata = dapr.get_metadata()
        if metadata:
            return {"dapr_status": "Dapr is up and running", "details": metadata}
        else:
            return {"dapr_status": "Dapr returned no metadata"}
    except DaprInternalError as de:
        return {"dapr_status": "Failed to interact with Dapr", "error": str(de)}