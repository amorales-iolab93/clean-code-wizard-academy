import uvicorn
from fastapi import FastAPI

from app.core.bootstrap.app import create_app

app: FastAPI = create_app()

# if __name__ == "__main__":
#     uvicorn.run(
#         "main:create_app",
#         host="0.0.0.0",
#         port=8080,
#         factory=True,
#         log_config="/src/app/log.json"
#     )
