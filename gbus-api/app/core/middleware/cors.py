from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

def set_cors(app: FastAPI) -> None:
    origins = [
        "http://localhost", 
        "http://localhost:8080", 
        "http://localhost:3000", 
        "http://gbus-front.s3-website.ap-northeast-2.amazonaws.com", 
        "http://jarih.net"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
