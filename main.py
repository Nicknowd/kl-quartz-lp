from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import os

app = FastAPI(title="KL-Quartz App")

# Configurar diretórios estáticos e de templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configurar banco de dados SQLite
DATABASE = "database.db"

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                cnpj TEXT,
                phone TEXT,
                produto TEXT,
                funcionarios TEXT,
                message TEXT,
                captation_means TEXT,
                customer_domain TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Inicializar o banco
init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, name="landing.html"
    )

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request):
    form_data = await request.form()
    
    # Salvar lead no banco de dados
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO leads (name, email, cnpj, phone, produto, funcionarios, message, captation_means, customer_domain)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                form_data.get('name', ''),
                form_data.get('email', ''),
                form_data.get('data__cnpj__1', ''),
                form_data.get('phone', ''),
                form_data.get('data__produto__0', ''),
                form_data.get('data__funcionarios__1', ''),
                form_data.get('message', ''),
                form_data.get('captation_means', ''),
                form_data.get('customer_domain', ''),
            ))
            conn.commit()
    except Exception as e:
        print(f"Erro ao salvar lead: {e}")
    
    # Retornar página de confirmação
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Obrigado! - KL Quartz</title>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Poppins:wght@700&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Montserrat', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background: linear-gradient(135deg, #6865A8, #2a285e);
                color: #fff;
            }
            .container {
                text-align: center;
                padding: 40px;
            }
            .container img {
                max-width: 193px;
                margin-bottom: 30px;
            }
            h1 {
                font-family: 'Poppins', sans-serif;
                font-size: 36px;
                margin-bottom: 15px;
            }
            p {
                font-size: 18px;
                margin-bottom: 30px;
                opacity: 0.9;
            }
            a {
                display: inline-block;
                padding: 12px 30px;
                background: #1CAF13;
                color: #fff;
                text-decoration: none;
                border-radius: 25px;
                font-weight: 700;
                transition: background 0.3s;
            }
            a:hover {
                background: #16a60e;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img src="https://image-service.unbounce.com/https%3A%2F%2Fapp.unbouncepreview.com%2Fpublish%2Fassets%2F33df825f-ae98-42ff-b628-4074ef14c41b%2Ff581ec59-logo-kl_1000000000000000000028.png?png8=true" alt="KL Quartz">
            <h1>Obrigado!</h1>
            <p>Logo entraremos em contato!</p>
            <a href="/">Voltar ao início</a>
        </div>
    </body>
    </html>
    """
