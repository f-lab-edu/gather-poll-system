from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import votes, results
import logging

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("api")

app = FastAPI(title="투표 시스템 API", debug=True)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시에는 특정 도메인으로 제한해야 합니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 요청 로깅 미들웨어
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug(f"Request path: {request.url.path}")
    logger.debug(f"Request method: {request.method}")
    
    # 요청 본문 로깅 (읽은 후 다시 설정)
    body = await request.body()
    logger.debug(f"Request body: {body}")
    
    # 원래 요청 본문 복원
    async def receive():
        return {"type": "http.request", "body": body}
    
    request._receive = receive
    
    response = await call_next(request)
    return response

# 라우터 등록
app.include_router(votes.router)
app.include_router(results.router)

@app.get("/")
async def root():
    return {"message": "투표 시스템 API에 오신 것을 환영합니다!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
