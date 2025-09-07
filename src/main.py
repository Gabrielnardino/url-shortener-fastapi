from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, SessionLocal
# --- FIM DO BLOCO DE IMPORTAÇÃO ---


# Cria as tabelas do banco de dados na inicialização
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Encurtador de URLs Profissional")

# --- Configuração dos Arquivos Estáticos ---
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/encurtar", response_model=schemas.URLResponse)
def encurtar_url(url_request: schemas.URLRequest, db: Session = Depends(get_db)):
    try:
        return crud.create_short_url(db=db, url_request=url_request)
    except ValueError as e:
        # Captura o erro do CRUD e retorna uma resposta HTTP 400
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/{short_code}")
def redirecionar(short_code: str, db: Session = Depends(get_db)):
    # Certifique-se de que SessionLocal está definido. Se você o moveu para database.py, importe-o.
    from .database import SessionLocal 
    db_url = crud.get_url_by_short_code(db, short_code=short_code)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL não encontrada")
    return RedirectResponse(url=db_url.long_url)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

