from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from middlewares.error_hendler import ErrorHandler
from login_router import router as login_router
from auth import decode_token, verify_token
from routers import citas_router, consultas_router, municipio, paciente_router, pandas, uisau_router, usuarios_router
import jwt


# Define un middleware para verificar el token JWT
async def check_jwt_token(token: str = Depends(decode_token)):
    if token is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


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

# # Define una ruta protegida
# @app.get("/ruta-protegida", tags=["ruta protegida"], dependencies=[Depends(check_jwt_token)])
# async def ruta_protegida():
#     return {"mensaje": "¡Has accedido a una ruta protegida!"}
