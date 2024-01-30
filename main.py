import uvicorn
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get('/')
def main():
    return "hello bro"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", port=port, log_level="info", reload=True)