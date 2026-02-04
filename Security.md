# Seguridad de la API - Autenticación y Autorización

Este documento detalla paso a paso cómo se implementó la seguridad en la API `BookCircle`, cubriendo desde el registro de usuarios hasta la protección de rutas mediante JWT (JSON Web Tokens).

## 1. Configuración del Entorno y Dependencias

Para manejar la seguridad, se utilizan las siguientes librerías clave:
- **Passlib[bcrypt]**: Para el hasheo seguro de contraseñas.
- **Python-Jose**: Para la generación y validación de tokens JWT.
- **FastAPI Security**: Herramientas integradas para manejar OAuth2 y esquemas de seguridad.

La configuración central se encuentra en `app/core/security.py`:
- **SECRET_KEY**: Clave utilizada para firmar los tokens.
- **ALGORITHM**: Algoritmo de firma (HS256).
- **ACCESS_TOKEN_EXPIRE_MINUTES**: Tiempo de vida del token (30 minutos por defecto).

## 2. Autenticación (Authentication)

La autenticación es el proceso de verificar la identidad del usuario.

### 2.1. Registro de Usuario (`/auth/register`)
- **Entrada**: El usuario envía datos (email, username, password).
- **Validación**: Se verifica que el email y username no existan ya en la base de datos.
- **Hasheo**: La contraseña **nunca** se guarda en texto plano. Se utiliza `get_password_hash` (usando bcrypt) para transformarla en un hash seguro.
- **Almacenamiento**: Se guarda el usuario con la contraseña hasheada.

### 2.2. Inicio de Sesión y Obtención de Token (`/token`)
- **Entrada**: El usuario envía sus credenciales (username y password) mediante `OAuth2PasswordRequestForm`.
- **Verificación**:
    1. Se busca al usuario por `username`.
    2. Se compara la contraseña enviada con el hash guardado usando `verify_password`.
- **Generación de Token**: Si las credenciales son válidas, se llama a `create_access_token`.
    - Se crea un payload con el `sub` (subject) igual al username.
    - Se añade la fecha de expiración (`exp`).
    - Se firma el token con la `SECRET_KEY` y el algoritmo `HS256`.
- **Salida**: Se devuelve el `access_token` y el tipo `bearer`.

## 3. Autorización (Authorization)

La autorización controla el acceso a los recursos protegidos.

### 3.1. Dependencia `get_current_user`
Esta función es el "guardián" de las rutas protegidas.
1. **Extracción**: `OAuth2PasswordBearer` extrae el token del encabezado `Authorization: Bearer <token>`.
2. **Decodificación**: Se intenta decodificar el token usando la misma clave y algoritmo.
3. **Validación**:
    - Si el token es inválido o expiró, lanza una excepción `HTTP_401_UNAUTHORIZED`.
    - Se extrae el `username` del payload.
    - Se verifica que el usuario exista en la base de datos.
4. **Retorno**: Si todo es correcto, devuelve el objeto `user`, que se inyecta en la función de la ruta.

### 3.2. Protección de Rutas
Cualquier endpoint que requiera autenticación declara una dependencia del usuario actual:

```python
@app.get("/clubs", ...)
def clubs(..., current_user: models.User = Depends(get_current_user)):
    # ... código ...
```

Si el usuario no envía un token válido, FastAPI rechazará la petición automáticamente con un error 401 antes de que se ejecute el código de la función.
