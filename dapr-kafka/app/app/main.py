from typing import Annotated
from fastapi import Depends, FastAPI
from dapr.ext.fastapi import DaprApp
from dapr.clients import DaprClient
from pydantic import BaseModel


class Message(BaseModel):
    id : int
    value:str
    

class CloudEventModel(BaseModel):
    data: Message
    datacontenttype: str
    id: str
    pubsubname: str
    source: str
    specversion: str
    topic: str
    traceid: str
    traceparent: str
    tracestate: str
    type: str

app = FastAPI()

dapr_app = DaprApp(app)

def get_dapr():
    with DaprClient() as dapr:
        yield dapr

@app.get('/')
def read_root():
    return {'status' : "Ok"}


@app.post('/publish')
def publish_dapr(message:Message , dapr:Annotated[DaprClient , Depends(get_dapr)]):
    dapr.publish_event(pubsub_name="pubsub" ,topic_name="dapr" , data = message.model_dump_json() , data_content_type="application/json")
    return  message



@dapr_app.subscribe(pubsub='pubsub', topic='dapr')
def event_handler(event_data: CloudEventModel):
    print(event_data)