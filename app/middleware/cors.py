from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 도메인을 지정해야 합니다
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )