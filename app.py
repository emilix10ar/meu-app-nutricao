import streamlit as st

# Configuração da página do aplicativo
st.set_page_config(
    page_title="NutriIA - Sua Dieta Inteligente",
    page_icon="🥗",
    layout="wide"
)

# --- MENU LATERAL: CONFIGURAÇÕES E PREFERÊNCIAS ---
with st.sidebar:
    st.header("⚙️ Suas Preferências")
    
    st.subheader("1. Estilo de Vida Alimentar")
    estilo_dieta = st.selectbox(
        "Selecione sua base alimentar:",
        ["Onívora (com carne)", "Ovolactovegetariana", "Pescetariana", "Vegana", "Flexitariana", "Sem Glúten", "Sem Lactose"]
    )
    
    st.subheader("2. Restrições Médicas e Alergias")
    alergias = st.multiselect(
        "Selecione se houver (Filtro Estrito):",
        ["Sem Laticínios", "Restrição Estrita a Glúten", "Sem Frutos do Mar", "Alergia a Oleaginosas", "Alergia a Ovo", "Alergia a Soja", "Diabética / Baixo IG"]
    )
    
    st.subheader("3. Alimentos que eu odeio 🚫")
    st.write("Digite um alimento para excluí-lo de todas as receitas.")
    
    # Lógica para gerenciar a lista de aversões
    if "lista_odios" not in st.session_state:
        st.session_state.lista_odios = []

    novo_odio = st.text_input("Ex: Coentro, Berinjela, Uva Passa...")
    if st.button("Adicionar à lista negra"):
        if novo_odio and novo_odio.lower() not in [item.lower() for item in st.session_state.lista_odios]:
            st.session_state.lista_odios.append(novo_odio.title())
            st.rerun()
            
    # Exibir a lista de alimentos odiados
    if st.session_state.lista_odios:
        st.markdown("**Meus itens bloqueados:**")
        for item in st.session_state.lista_odios:
            st.markdown(f"- ❌ {item}")
        
        if st.button("Limpar Lista"):
            st.session_state.lista_odios = []
            st.rerun()

# --- ÁREA PRINCIPAL DO APP ---
st.title("🥗 NutriIA: Seu Planejador Personalizado")

aba1, aba2, aba3 = st.tabs(["📅 Cardápio da Semana", "💬 Assistente & Substituições", "📖 Livro de Receitas"])

with aba1:
    st.header("Seu Planejamento Semanal")
    
    st.info(f"**Filtros Ativos:** Dieta {estilo_dieta} | Alergias: {', '.join(alergias) if alergias else 'Nenhuma'} | Itens bloqueados: {len(st.session_state.lista_odios)}")
    
    st.write("Nesta etapa, o app filtrará as receitas do Google Sheets com base nas configurações do menu lateral antes de montar as matrizes de variação.")
    
    st.subheader("Nível de Variação da Semana")
    modo_variacao = st.radio(
        "Escolha como quer cozinhar nesta semana:",
        ["Baixa Variação (Modo Marmita - 8 receitas)", 
         "Média Variação (Modo Equilíbrio - 14 receitas)", 
         "Alta Variação (Modo Chef - 28 receitas)"],
        horizontal=True
    )
    
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    dia_selecionado = st.selectbox("Visualizar receitas de:", dias)
    
    st.success("O visual do cardápio e das matrizes (A, B, C...) entrará aqui e respeitará 100% dos filtros laterais escolhidos!")

with aba2:
    st.header("💬 Converse com seu Assistente")
    st.write("O chat já saberá que você está na dieta **{}** e odeia **{}**!".format(
        estilo_dieta, 
        ', '.join(st.session_state.lista_odios) if st.session_state.lista_odios else 'nada'
    ))

with aba3:
    st.header("📖 Livro de Receitas")
    st.write("Adicione receitas novas aqui.")
