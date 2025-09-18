# src/app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}

def run():
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
# from fastapi import FastAPI
# from app.config import settings
# from interfaces.api.user_api import router as user_router

# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     version="1.0.0",
#     description="DDD Clean Architecture Playground API"
# )

# # APIルーターを登録
# app.include_router(user_router, prefix=settings.API_V1_STR)

# @app.get("/")
# def read_root():
#     return {
#         "message": "DDD Clean Architecture Playground API",
#         "version": "1.0.0",
#         "docs": "/docs"
#     }

# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}

# def run():
#     import uvicorn
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

# if __name__ == "__main__":
#     run()
