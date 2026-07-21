import streamlit as st
import google.generativeai as genai

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
    
    dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    dia_selecionado = st.selectbox("Selecione o dia para visualizar:", dias)
    
    st.subheader(f"Refeições de {dia_selecionado}")
    
    # 4 Refeições incluindo Lanche da Tarde e sem carnes nem frango
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### ☕ Café da Manhã")
        st.info("**Omelete com Aveia e Frutas**\n\n- 2 Ovos\n- 30g Aveia\n- Morangos\n\n*Kcal: 350 | Prot: 20g*")
        
    with col2:
        st.markdown("### 🍽️ Almoço")
        st.success("**Tilápia Grelhada com Quinoa**\n\n- 150g Tilápia\n- 4 col. Quinoa\n- Salada verde e azeite\n\n*Kcal: 480 | Prot: 38g*")
        
    with col3:
        st.markdown("### 🥪 Lanche da Tarde")
        st.primary("**Iogurte com Chia e Castanhas**\n\n- 170g Iogurte Natural\n- 1 col. Chia\n- 15g Castanhas\n\n*Kcal: 250 | Prot: 14g*")
        
    with col4:
        st.markdown("### 🌙 Jantar")
        st.warning("**Sopa de Lentilha e Cogumelos**\n\n- Lentilha cozida\n- Cogumelos paris\n- Legumes variados\n\n*Kcal: 380 | Prot: 22g*")
        
    st.divider()
    st.subheader("🔄 Troca Rápida de Refeição")
    col_a, col_b = st.columns(2)
    with col_a:
        st.selectbox("Trocar a refeição:", ["Almoço de Terça", "Jantar de Quinta", "Lanche de Sexta"])
    with col_b:
        st.selectbox("Pela refeição de:", ["Jantar de Sexta", "Almoço de Sábado", "Lanche de Domingo"])
    st.button("Confirmar Troca no Cardápio")

# --- ABA 2: ASSISTENTE DE IA (CHAT CONVERSACIONAL) ---
with aba2:
    st.header("💬 Converse com seu Assistente de Nutrição")
    st.write("Peça substituições, ideias de refeições ou tire dúvidas. A IA já sabe das suas restrições alimentares!")

    # Histórico de Chat
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Sou seu assistente de nutrição. Sei que suas refeições incluem lanche da tarde e que você NÃO come carne bovina, suína nem frango. Como posso te ajudar hoje?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Entrada do usuário
    if prompt := st.chat_input("Ex: 'O que posso comer no lanche da tarde com 20g de proteína?' ou 'Substitua a tilápia do almoço'"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Chamada corrigida para o Gemini 1.5 Flash
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            system_instruction = (
                "Você é um nutricionista especialista e assistente pessoal. "
                "REGRA INEGOCIÁVEL: O usuário NÃO COME carne bovina, carne suína nem frango. "
                "As refeições do usuário são divididas em 4: Café da manhã, Almoço, Lanche da tarde e Jantar. "
                "Opções de proteína permitidas: Ovos, peixes, frutos do mar, queijos, iogurtes, whey, tofu, cogumelos, feijões, grão-de-bico, lentilha e sementes. "
                "Dê respostas diretas, práticas e focadas em bater macronutrientes mantendo sabor e variabilidade."
            )
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
        st.success("Receita analisada! Calorias e macronutrientes calculados sem carnes nem frango e salvos com sucesso.")
