import pandas as pd
import streamlit as st

SHEET_ID = "1_WrmhHlN5a0Wob0b_gNoWh9tQ26NLRZbGp7mdLr2hrU"
URL_BASE = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet="

@st.cache_data(ttl=60)
def carregar_dados_planilha():
    try:
        df_rec = pd.read_csv(URL_BASE + "Receitas")
        df_ing = pd.read_csv(URL_BASE + "Ingredientes_Linha")
        df_nut = pd.read_csv(URL_BASE + "Nutricao")
    except Exception:
        return _carregar_mock()
        
    if df_rec.empty or df_ing.empty:
        return _carregar_mock()

    receitas_db = {}
    categorias_set = set()
    todos_ingredientes = set()

    nutricao_dict = {}
    for _, row in df_nut.iterrows():
        nome = str(row.get('Nome_Alimento', '')).strip()
        nutricao_dict[nome] = {
            'kcal': float(row.get('Calorias_100g', 0) or 0),
            'prot': float(row.get('Proteinas_100g', 0) or 0)
        }

    for _, rec in df_rec.iterrows():
        ativo = str(rec.get('Ativo', 'Sim')).strip().lower()
        if ativo in ['nao', 'não', 'n']:
            continue
            
        id_rec = rec.get('ID_Receita')
        nome_rec = str(rec.get('Nome_Receita', '')).strip()
        
        if not nome_rec or pd.isna(id_rec):
            continue
        
        receitas_db[nome_rec] = {
            "tipo": str(rec.get('Tipo_Refeicao', 'Geral')),
            "preparo": str(rec.get('Modo_Preparo', 'Sem preparo cadastrado.')),
            "kcal": 0,
            "proteina": 0,
            "ingredientes": []
        }
        
        ings = df_ing[df_ing['ID_Receita'] == id_rec]
        kcal_total = 0
        prot_total = 0
        
        for _, ing in ings.iterrows():
            nome_ing = str(ing.get('Nome_Ingrediente', '')).strip()
            if not nome_ing or pd.isna(nome_ing):
                continue
                
            qtd = float(ing.get('Quantidade', 0) or 0)
            unidade = str(ing.get('Unidade', '')).strip()
            categoria = str(ing.get('Categoria_Compras', 'Outros')).strip()
            
            categorias_set.add(categoria)
            todos_ingredientes.add(nome_ing)
            
            if nome_ing in nutricao_dict:
                kcal_total += (nutricao_dict[nome_ing]['kcal'] / 100) * qtd
                prot_total += (nutricao_dict[nome_ing]['prot'] / 100) * qtd
            
            receitas_db[nome_rec]["ingredientes"].append({
                "item": nome_ing,
                "qtd": qtd,
                "unidade": unidade,
                "categoria": categoria,
                "substitutos": []
            })
            
        receitas_db[nome_rec]["kcal"] = round(kcal_total)
        receitas_db[nome_rec]["proteina"] = round(prot_total)

    categorias_compras = sorted(list(categorias_set)) if categorias_set else CATEGORIAS_COMPRAS
    ingredientes_lista = sorted(list(todos_ingredientes)) if todos_ingredientes else obter_todos_ingredientes()
    
    return receitas_db, categorias_compras, ingredientes_lista

def _carregar_mock():
    return RECEITAS_DB, CATEGORIAS_COMPRAS, obter_todos_ingredientes()

CATEGORIAS_COMPRAS = [
    "🥦 Hortifrúti (Horta, Pomar & Ervas)",
    "🥩 Açougue, Peixaria & Frios",
    "🌾 Mercearia Seca (Grãos, Massas & Farinhas)",
    "🫒 Condimentos, Óleos & Enlatados"
]

RECEITAS_DB = {
    "Panqueca de Aveia": {
        "tipo": "Café da Manhã",
        "kcal": 320,
        "proteina": 18,
        "ingredientes": [
            {"item": "Aveia em flocos", "qtd": 40, "unidade": "g", "categoria": "🌾 Mercearia Seca (Grãos, Massas & Farinhas)", "substitutos": ["Quinoa em flocos"]},
            {"item": "Ovo de galinha cru", "qtd": 2, "unidade": "unidades", "categoria": "🥩 Açougue, Peixaria & Frios", "substitutos": []},
            {"item": "Banana nanica", "qtd": 1, "unidade": "unidade", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": []}
        ],
        "preparo": "1. Amasse a banana.\n2. Misture os ovos crus e a aveia.\n3. Doure na frigideira."
    },
    "Tilápia Grelhada com Quinoa": {
        "tipo": "Almoço",
        "kcal": 480,
        "proteina": 38,
        "ingredientes": [
            {"item": "Filé de tilápia cru", "qtd": 150, "unidade": "g", "categoria": "🥩 Açougue, Peixaria & Frios", "substitutos": ["Peito de frango cru (150g)"]},
            {"item": "Quinoa em grãos crua", "qtd": 40, "unidade": "g", "categoria": "🌾 Mercearia Seca (Grãos, Massas & Farinhas)", "substitutos": ["Arroz integral cru (50g)"]}
        ],
        "preparo": "1. Pese 150g do filé de tilápia cru e tempere.\n2. Lave 40g de quinoa crua e cozinhe com água.\n3. Grelhe o peixe e sirva."
    }
}

def obter_todos_ingredientes():
    ingredientes = set()
    for receita in RECEITAS_DB.values():
        for ing in receita.get("ingredientes", []):
            ingredientes.add(ing["item"])
    return sorted(list(ingredientes))
