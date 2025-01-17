import os
import sys
import logging
import datetime
from fastapi import FastAPI, Request
from router import hcl

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(hcl.router)
app.router.redirect_slashes = False


# 미들웨어로 작업 완료 시점 기록
@app.middleware("http")
async def log_completion_time(request: Request, call_next):
    response = await call_next(request)  # 요청을 처리하고 응답 생성
    completion_time = datetime.datetime.now().isoformat()  # 작업 완료 시점 기록
    logger.info(
        f"Request: {request.method} {request.url} - Completed at {completion_time}"
    )
    return response


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping")
async def ping():
    return {"message": "PONG"}
