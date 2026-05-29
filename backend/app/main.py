from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.analytics.router import router as analytics_router
from app.auth.router import router as auth_router
from app.crypto.router import router as crypto_router
from app.plaid.router import router as plaid_router
from app.splitwise.router import router as splitwise_router
from app.database import Base, engine


app = FastAPI(title="OpenLedger API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(plaid_router, prefix="/plaid", tags=["plaid"])
app.include_router(splitwise_router, prefix="/splitwise", tags=["splitwise"])
app.include_router(crypto_router, prefix="/crypto", tags=["crypto"])
app.include_router(analytics_router, prefix="/analytics", tags=["analytics"])


@app.on_event("startup")
def startup() -> None:
    # MVP bootstrap: create known tables on startup.
    from app.analytics import models as analytics_models  # noqa: F401
    from app.auth import models as auth_models  # noqa: F401
    from app.crypto import models as crypto_models  # noqa: F401
    from app.plaid import models as plaid_models  # noqa: F401
    from app.splitwise import models as splitwise_models  # noqa: F401

    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
