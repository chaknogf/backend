from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import logging
import os

from middlewares.error_hendler import ErrorHandler
from login_router import router as login_router
from auth import decode_token
from routers import (
    citas_router,
    consultas_router,
    municipio,
    paciente_router,
    pandas,
    uisau_router,
    usuarios_router,
    medicos_router,
    cie10_router,
    cons_nac_router,
    procedimientos_medicos_router,
)

# =========================
# JWT Dependency
# =========================

async def check_jwt_token(request: Request, token: dict = Depends(decode_token)):
    if token is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    request.state.roles = token.get("roles", [])
    return token


# =========================
# App
# =========================

app = FastAPI(
    title="Hospital API",
    version="1.0.0",
    description="API para gestión hospitalaria",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# =========================
# CORS Configuration
# =========================

# Define allowed origins
origins = [
    "http://localhost:4200",
    "http://localhost:4201",
    "https://hosptecpan.space",
    "https://www.hosptecpan.space",
    ["*"]
]

# Add environment variable for additional origins if needed
if os.getenv("ADDITIONAL_ORIGINS"):
    origins.extend(os.getenv("ADDITIONAL_ORIGINS").split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
    max_age=3600,
)

# =========================
# Other Middlewares
# =========================

app.add_middleware(ErrorHandler)

# =========================
# Routers públicos
# =========================

app.include_router(login_router, prefix="/auth", tags=["Autenticación"])

# =========================
# Routers protegidos con JWT
# =========================

protected_dependencies = [Depends(check_jwt_token)]

app.include_router(citas_router.router, dependencies=protected_dependencies)
app.include_router(paciente_router.router, dependencies=protected_dependencies)
app.include_router(municipio.router, dependencies=protected_dependencies)
app.include_router(consultas_router.router, dependencies=protected_dependencies)
app.include_router(pandas.router, dependencies=protected_dependencies)
app.include_router(uisau_router.router, dependencies=protected_dependencies)
app.include_router(usuarios_router.router, dependencies=protected_dependencies)
app.include_router(medicos_router.router, dependencies=protected_dependencies)
app.include_router(cie10_router.router, dependencies=protected_dependencies)
app.include_router(cons_nac_router.router, dependencies=protected_dependencies)
app.include_router(procedimientos_medicos_router.router, dependencies=protected_dependencies)

# =========================
# Root → Docs
# =========================

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# =========================
# Logging
# =========================

log = logging.getLogger("backend")
log.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - IP: %(client_ip)s - PORT: %(client_port)s"
)
handler.setFormatter(formatter)
log.addHandler(handler)

@app.middleware("http")
async def custom_logging(request: Request, call_next):
    if request.url.path in ("/openapi.json", "/docs", "/redoc"):
        return await call_next(request)
    
    response = await call_next(request)
    
    client_ip = request.client.host if request.client else "unknown"
    client_port = request.client.port if request.client else "unknown"
    
    log.info(
        "request",
        extra={"client_ip": client_ip, "client_port": client_port}
    )
    
    return response