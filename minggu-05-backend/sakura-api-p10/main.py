from fastapi import FastAPI

app = FastAPI(
    title = "Sakura Task API",
    version="0.1.0"
)

@app.get("/")
def beranda():
    return {
        "pesan": "Sakura Tasks API jalan",
        "dokumentasi": "/docs"
        }