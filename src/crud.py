import secrets
import string
from sqlalchemy.orm import Session
from . import models, schemas

def generate_short_code(db: Session, length: int = 6) -> str:
    """Gera um código aleatório e garante que ele seja único no banco de dados."""
    characters = string.ascii_letters + string.digits
    while True:
        short_code = "".join(secrets.choice(characters) for _ in range(length))
        # Verifica se o código gerado já não existe no banco
        if not get_url_by_short_code(db, short_code):
            return short_code

def get_url_by_short_code(db: Session, short_code: str):
    """Busca uma URL no banco de dados pelo seu código curto."""
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()

def create_short_url(db: Session, url_request: schemas.URLRequest) -> models.URL:
    """Cria uma nova URL curta no banco de dados."""
    if url_request.custom_code:
        # Se um código customizado foi fornecido
        if get_url_by_short_code(db, url_request.custom_code):
            # Levanta um erro se o código já existir
            raise ValueError("Código customizado já em uso.")
        short_code = url_request.custom_code
    else:
        # Se nenhum código foi fornecido, gera um aleatório
        short_code = generate_short_code(db)
    
    db_url = models.URL(
        long_url=url_request.long_url, 
        short_code=short_code
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url