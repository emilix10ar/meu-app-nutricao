import streamlit as st

# Configuração inicial da página
st.set_page_config(
    page_title="NutriIA - Sua Dieta Inteligente",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 NutriIA: Seu Planejador Personalizado")

# Criando as 3 abas, mas vamos preencher só a primeira por enquanto
aba1, aba2, aba3 = st.tabs(["📅 Cardápio da Semana", "💬 Assistente & Substituições", "📖 Livro de Receitas"])

# --- FASE 1: APENAS O CARDÁPIO VISUAL ---
with aba1:
    st.header("Seu Planejamento Semanal")
    st.write("Veja e reorganize suas refeições com facilidade.")
    
    dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    dia_selecionado = st.selectbox("Selecione o dia para visualizar:", dias)
    
    st.subheader(f"Refeições de {dia_selecionado}")
    
    # Dividindo a tela em 4 colunas para as 4 refeições
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### ☕ Café da Manhã")
        # Usando st.info (azul)
        st.info("**Omelete com Aveia e Frutas**\n\n- 2 Ovos\n- 30g Aveia\n- Morangos\n\n*Kcal: 350 | Prot: 20g*")
        
    with col2:
        st.markdown("### 🍽️ Almoço")
        # Usando st.success (verde)
        st.success("**Tilápia Grelhada com Quinoa**\n\n- 150g Tilápia\n- 4 col. Quinoa\n- Salada verde e azeite\n\n*Kcal: 480 | Prot: 38g*")
        
    with col3:
        st.markdown("### 🥪 Lanche da Tarde")
        # Usando st.warning (amarelo) - O ERRO ANTERIOR ESTAVA AQUI!
        st.warning("**Iogurte com Chia e Castanhas**\n\n- 170g Iogurte Natural\n- 1 col. Chia\n- 15g Castanhas\n\n*Kcal: 250 | Prot: 14g*")
        
    with col4:
        st.markdown("### 🌙 Jantar")
        # Usando st.error (vermelho/rosa)
        st.error("**Sopa de Lentilha e Cogumelos**\n\n- Lentilha cozida\n- Cogumelos paris\n- Legumes variados\n\n*Kcal: 380 | Prot: 22g*")

with aba2:
    st.info("O Chat com a Inteligência Artificial será construído aqui na Fase 2.")

with aba3:
    st.info("O Leitor de Receitas será construído aqui na Fase 3.")
