import os
import bcrypt
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (local) ou das Settings da Vercel
load_dotenv()

# --- Conexão Adaptada para Backend ---
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def hash_senha(senha: str):
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_senha(senha: str, senha_hash: str):
    return bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8'))

def buscar_usuario_por_email(email: str):
    # Mantendo sua lógica exata de busca
    res = supabase.table("users").select("*").eq("email", email).execute()
    return res.data[0] if res.data else None

def cadastrar_usuario(username, email, senha_limpa, org_name, role, org_id):
    """
    Nota: org_id agora vem como parâmetro, 
    pois no FastAPI não existe st.session_state.
    """
    try:
        senha_protegida = hash_senha(senha_limpa)
        
        user_payload = {
            "username": username,
            "email": email,
            "password_hash": senha_protegida,
            "org_name": org_name,
            "org_id": org_id,
            "role": role
        }
        supabase.table("users").insert(user_payload).execute()
        return True, "Cadastro realizado com sucesso!"
    except Exception as e:
        return False, f"Erro: {str(e)}"

def excluir_usuario_por_id(id_usuario: int):
    try:
        supabase.table("users").delete().eq("id", id_usuario).execute()
        return True, "Membro removido com sucesso."
    except Exception as e:
        return False, f"Erro ao remover: {str(e)}"
