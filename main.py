from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="API de Clubes de Lectura",
    description="API REST para gestionar clubes de lectura",
    version="1.0.0"
)

# ============= MODELOS (Schemas) =============

class Club(BaseModel):
    """Model representing a reading club"""
    id: int
    name: str
    description: str
    created_date: str
    favorite_genre: str
    members: int

class ClubCreate(BaseModel):
    """Model for creating a new club (without ID)"""
    name: str
    description: str
    favorite_genre: str
    members: int = 0

class ClubUpdate(BaseModel):
    """Model for updating a club (all fields optional)"""
    name: str | None = None
    description: str | None = None
    favorite_genre: str | None = None
    members: int | None = None

# --- Modelos para Miembros ---
class Member(BaseModel):
    """Model representing a club member"""
    id: int
    name: str
    email: str
    joined_date: str

class MemberCreate(BaseModel):
    """Model for adding a new member"""
    name: str
    email: str
# ============= DATOS ESTÁTICOS (Simulación de BD) =============

clubs_db = {
    1: {
        "id": 1,
        "name": "Lectores Nocturnos",
        "description": "Club para amantes de la lectura nocturna",
        "created_date": "2024-01-15",
        "favorite_genre": "Misterio",
        "members": 25
    },
    2: {
        "id": 2,
        "name": "Fantasía y Más",
        "description": "Dedicado a la literatura fantástica",
        "created_date": "2024-02-20",
        "favorite_genre": "Fantasía",
        "members": 40
    },
    3: {
        "id": 3,
        "name": "Clásicos Eternos",
        "description": "Explorando la literatura clásica",
        "created_date": "2024-03-10",
        "favorite_genre": "Clásicos",
        "members": 15
    }
}

# Simulación de tabla de miembros
# ============= DATOS ESTÁTICOS DE MIEMBROS =============

# Estructura: Clave = club_id, Valor = Lista de diccionarios (miembros)
members_db = {
    1: [ # Miembros del Club 1 (Lectores Nocturnos)
        {
            "id": 101, 
            "name": "Ana García", 
            "email": "ana@correo.com", 
            "joined_date": "2024-01-20"
        },
        {
            "id": 102, 
            "name": "Carlos Ruiz", 
            "email": "carlos@correo.com", 
            "joined_date": "2024-02-15"
        }
    ],
    2: [ # Miembros del Club 2 (Fantasía y Más)
        {
            "id": 201, 
            "name": "Elena Torres", 
            "email": "elena@correo.com", 
            "joined_date": "2024-03-01"
        }
    ],
    # El club 3 no tiene miembros definidos, devolverá lista vacía automáticamente
}

# Variable para generar IDs únicos
next_id = 4


# ============= ENDPOINTS =============

@app.get("/")
def root():
    """Endpoint raíz - Bienvenida"""
    return {
        "mensaje": "Bienvenido a la API de Clubes de Lectura",
        "documentacion": "/docs"
    }


@app.get("/clubs", response_model=list[Club], tags=["Clubs"])
def get_clubs():
    """
    Obtener todos los clubes de lectura
    
    Retorna una lista con todos los clubes registrados.
    """
    return list(clubs_db.values())


@app.post("/clubs", tags=["Clubs"])
def create_clubs(club: ClubCreate):
    return club


@app.get("/clubs/{clubId}", tags=["Clubs"])
def get_clubs(clubId: int) -> Club:
    return Club()


@app.put("/clubs/{clubId}", tags=["Clubs"])
def get_clubs(clubId: int) -> Club:
    return Club()


@app.delete("/clubs/{clubId}", tags=["Clubs"])
def get_clubs(clubId: int) -> int:
    return 204

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
# ============= ENDPOINTS MIEMBROS =============

# GET MEMBERS
@app.get("/clubs/{clubId}/members", response_model=list[Member], tags=["Members"])
def get_members(clubId: int):
    """
    Obtener los miembros de un club.
    Busca en la BD simulada y si el club no existe o no tiene miembros,
    devuelve una lista vacía [].
    """
    return members_db.get(clubId, [])

# POST MEMBERS
@app.post("/clubs/{clubId}/members", tags=["Members"])
def create_member(clubId: int, member: MemberCreate):
    """
    Agregar un miembro al club
    """
    # Retorna el mismo objeto recibido para cumplir con el esquema
    return member

# DELETE MEMBERS
@app.delete("/clubs/{clubId}/members/{userId}", tags=["Members"])
def delete_member(clubId: int, userId: int) -> int:
    """
    Eliminar un miembro del club
    """
    return 204