from src.api import app  # ✅ Import FastAPI app from src/api

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
