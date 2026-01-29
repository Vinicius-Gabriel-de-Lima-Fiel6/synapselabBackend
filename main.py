import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import auth_db as db
from calculadora import calcular_analitica_fiel, calcular_termo_fiel #
from motores_quimicos import MotorCalculoAvancado #

app = FastAPI()

# --- CONFIGURAÇÃO DE SEGURANÇA (CORS) ---
# Isso permite que o seu site React fale com este código Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONEXÃO COM SUPABASE ---
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class LoginRequest(BaseModel):
    email: str
    password: str

# Rota para tirar o erro "Not Found" quando abrir o link no navegador
@app.get("/")
async def root():
    return {"message": "LabSmartAI API Online", "status": "running"}

# Rota de Login que o seu app.jsx chama
@app.post("/auth/login")
async def login(req: LoginRequest):
    user = db.buscar_usuario_por_email(req.email)
    if user and db.verificar_senha(req.password, user['password_hash']):
        return {
            "logado": True,
            "user_data": user
        }
    raise HTTPException(status_code=401, detail="Dados incorretos.")

# Rota de Métricas que o seu app.jsx chama
@app.get("/dashboard/metrics")
async def get_metrics(org_name: str):
    try:
        res_sub = supabase.table("substancias").select("quantidade").eq("org_name", org_name).execute()
        total_itens = sum([i['quantidade'] for i in res_sub.data]) if res_sub.data else 0
        
        res_eq = supabase.table("equipamentos").select("id", count="exact").eq("org_name", org_name).execute()
        total_equip = res_eq.count if res_eq.count else 0
        
        return {
            "total_itens": total_itens,
            "total_equipamentos": total_equip,
            "total_analises": len(res_sub.data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/api/calculadora")
async def processar_calculo(req: CalculoRequest):
    # Tenta na analítica, se não encontrar, tenta na termo
    res = calcular_analitica_fiel(req.operacao, req.dados)
    if res == 0.0:
        res = calcular_termo_fiel(req.operacao, req.dados)
    return {"resultado": res}

# ROTA DA IA (ESTEQUIOMETRIA)
@app.post("/api/ia_estequiometria")
async def processar_ia(req: dict):
    reac, prod = req.get("reagentes"), req.get("produtos")
    reac_bal, prod_bal, erro = motor_ia.balancear_e_resolver(reac, prod) #
    if erro: return {"erro": erro}
    
    eq_completa = f"{reac_bal} -> {prod_bal}"
    laudo = motor_ia.consultoria_ia(eq_completa, "N/A", "N/A") #
    return {"equacao": eq_completa, "laudo": laudo}
