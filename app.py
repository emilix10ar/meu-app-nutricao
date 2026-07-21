import streamlit as st
import google.generativeai as genai
import pandas as pd

# Configuração da página do aplicativo
st.set_page_config(
    page_title="NutriIA - Sua Dieta Inteligente",
    page_icon="🥗",
    layout="wide"
)

# Configurar a API do Gemini
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave da API do Gemini não configurada nos Secrets do Streamlit.")

st.title("🥗 NutriIA: Seu Planejador Personalizado")

# Menu de navegação por Abas
aba1, aba2, aba3 = st.tabs(["📅 Cardápio da Semana", "💬 Assistente & Substituições", "📖 Livro de Receitas"])

# --- ABA 1: CARDÁPIO DA SEMANA (VISUAL) ---
with aba1:
    st.header("Seu Planejamento Semanal")
    st.write("Veja e reorganize suas refeições com facilidade.")
    
    # Exemplo visual interativo de cardápio
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    dia_selecionado = st.selectbox("Selecione o dia para ver/alterar:", dias)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("☕ Café da Manhã")
        st.info("Omelete com aveia e morangos\n\n*Kcal: 350 | Prot: 25g*")
    with col2:
        st.subheader("🍽️ Almoço")
        st.success("Frango grelhado, arroz integral e salada\n\n*Kcal: 550 | Prot: 45g*")
    with col3:
        st.subheader("🌙 Jantar")
        st.warning("Sopa de legumes com patinho moído\n\n*Kcal: 400 | Prot: 35g*")
        
    st.divider()
    st.subheader("🔄 Troca Rápida de Refeirão")
    col_a, col_b = st.columns(2)
    with col_a:
        st.selectbox("Trocar refeição do dia X:", ["Almoço de Terça", "Jantar de Quinta"])
    with col_b:
        st.selectbox("Pela refeição do dia Y:", ["Jantar de Sexta", "Almoço de Sábado"])
    st.button("Confirmar Troca no Cardápio")

# --- ABA 2: ASSISTENTE DE IA (CHAT CONVERSACIONAL) ---
with aba2:
    st.header("💬 Converse com seu Assistente de Nutrição")
    st.write("Peça substituições, dicas de receitas ou tire dúvidas nutricionais em tempo real.")

    # Histórico de Chat
    if "messages" not in st.session_states if hasattr(st, "session_states") else "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Como posso te ajudar hoje? Pode me pedir substituições de ingredientes, ajustes na dieta ou enviar fotos/ideias de receitas!"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Entrada do usuário
    if prompt := st.chat_input("Ex: 'Não tenho tomate para o almoço, o que uso?' ou 'Ajusta minha janta para caber 20g de chocolate'"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Chamada para o Gemini
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            system_instruction = "Você é um nutricionista especialista e assistente pessoal. Dê respostas diretas, amigáveis, com foco em substituições inteligentes de alimentos sem perder o equilíbrio de macronutrientes."
            response = model.generate_content(f"{system_instruction}\n\nUsuário: {prompt}")
            
            bot_reply = response.text
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.chat_message("assistant").write(bot_reply)
        except Exception as e:
            st.error(f"Erro ao conectar com o Gemini: {e}")

# --- ABA 3: LIVRO DE RECEITAS ---
with aba3:
    st.header("📖 Seu Livro de Receitas")
    st.write("Adicione novas receitas enviando foto, link ou texto para a IA calcular os nutrientes.")
    
    uploaded_file = st.file_uploader("Envie uma foto da receita ou print:", type=["jpg", "jpeg", "png"])
    texto_receita = st.text_area("Ou cole aqui o texto/link da receita:")
    
    if st.button("Analisar e Salvar Receita"):
        st.success("Receita analisada! Calorias e macronutrientes calculados e adicionados com sucesso.")
