from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from middlewares.error_hendler import ErrorHandler
from login_router import router as login_router
from auth import decode_token, verify_token
from routers import citas_router, consultas_router, municipio, paciente_router, pandas, uisau_router, usuarios_router, medicos_router, cie10_router, cons_nac_router
from routers import procedimientos_medicos_router
import jwt
import logging




async def check_jwt_token(request: Request, token: str = Depends(decode_token)):
    if token is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    roles = token.get("roles", [])

    request.state.roles = roles  # Almacena los roles en el estado del request

    return token


app = FastAPI()
app.add_middleware(ErrorHandler)

allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye las rutas del módulo login_router
app.include_router(login_router, tags=["login"])

# Importación de routers y aplicación de middleware de verificación de token JWT
app.include_router(citas_router.router, dependencies=[Depends(check_jwt_token)])
app.include_router(paciente_router.router, dependencies=[Depends(check_jwt_token)])
app.include_router(municipio.router, dependencies=[Depends(check_jwt_token)])
app.include_router(consultas_router.router, dependencies=[Depends(check_jwt_token)])
app.include_router(pandas.router, dependencies=[Depends(check_jwt_token)])
app.include_router(uisau_router.router, dependencies=[Depends(check_jwt_token)])
app.include_router(usuarios_router.router, dependencies=[Depends(check_jwt_token)])
app.include_router(medicos_router.router, dependencies=[Depends(check_jwt_token)])
app.include_router(cie10_router.router, dependencies=[Depends(check_jwt_token)])
app.include_router(cons_nac_router.router, dependencies=[Depends(check_jwt_token)])
app.include_router(procedimientos_medicos_router.router, dependencies=[Depends(check_jwt_token)])


# # Define una ruta protegida
# @app.get("/ruta-protegida", tags=["ruta protegida"], dependencies=[Depends(check_jwt_token)])
# async def ruta_protegida():
#     return {"mensaje": "¡Has accedido a una ruta protegida!"}


# Redirecciona la ruta principal a la documentación ("/docs")
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


# Configura el logger de FastAPI
log = logging.getLogger("uvicorn.access")
log = logging.getLogger(__name__)
# log.setLevel(logging.INFO)

# Crea un manejador de registros que formatee la información como deseas
log_handler = logging.StreamHandler()
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - IP: %(client_ip)s - PORT: %(client_port)s')
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)

@app.middleware("http")
async def custom_logging(request: Request, call_next):
    try:
        # Agrega información adicional al registro (en este caso, la IP y el puerto)
        request.state.client_ip = request.client.host
        request.state.client_port = request.client.port

        response = await call_next(request)

        # Extrae la información adicional del estado del request
        client_ip = request.state.client_ip
        client_port = request.state.client_port

        # Loggea la información
        log.info("", extra={"client_ip": client_ip, "client_port": client_port})

        return response
    except HTTPException as e:
        log.info(f"IP: {request.client.host} - {e}")
        raise e