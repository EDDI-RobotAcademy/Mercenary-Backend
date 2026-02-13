from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import load_env

load_env()

app = FastAPI(
    title="FastAPI Backend",
    description="FastAPI 백엔드 프로젝트",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용하도록 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=33333)
