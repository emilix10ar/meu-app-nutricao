import streamlit as st
import pandas as pd

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
        ["Onívora (com carne)", "Ovolactovegetariana", "Pescetariana", "Vegana", "Flexitariana", "Sem Glúten", "Sem Lactose"],
        index=4 # Deixando Flexitariana como padrão
    )
    
    st.subheader("2. Restrições Médicas e Alergias")
    alergias = st.multiselect(
        "Selecione se houver (Filtro Estrito):",
        ["Sem Laticínios", "Restrição Estrita a Glúten", "Sem Frutos do Mar", "Alergia a Oleaginosas", "Alergia a Ovo", "Alergia a Soja", "Diabética / Baixo IG"]
    )
    
    st.subheader("3. Alimentos Excluídos 🚫")
    st.write("Digite um alimento para excluí-lo de todas as receitas.")
    
    # Lógica para gerenciar a lista de aversões
    if "lista_odios" not in st.session_state:
        st.session_state.lista_odios = []

    novo_odio = st.text_input("Ex: Coentro, Berinjela, Uva Passa...")
    if st.button("Bloquear alimento"):
        if novo_odio and novo_odio.lower() not in [item.lower() for item in st.session_state.lista_odios]:
            st.session_state.lista_odios.append(novo_odio.title())
            st.rerun()
            
    # Exibir a lista de alimentos odiados
    if st.session_state.lista_odios:
        st.markdown("**Meus itens excluídos:**")
        for item in st.session_state.lista_odios:
            st.markdown(f"- ❌ {item}")
        
        if st.button("Limpar Lista"):
            st.session_state.lista_odios = []
            st.rerun()

# --- FUNÇÕES AUXILIARES ---
# Dicionário mock de receitas para substituir as letras pelos nomes
receitas_mock = {
    "Café da Manhã": {"A": "Panqueca de Aveia", "B": "Ovos Mexidos", "C": "Iogurte c/ Granola", "D": "Vitamina de Banana", "C1": "Panqueca de Aveia", "C2": "Ovos Mexidos", "C3": "Iogurte c/ Granola", "C4": "Vitamina de Banana", "C5": "Tapioca Fit", "C6": "Crepioca", "C7": "Pão de Queijo"},
    "Almoço": {"A": "Bowl de Quinoa", "B": "Salada Grão de Bico", "C": "Macarrão Abobrinha", "D": "Escondidinho Fit", "A1": "Bowl de Quinoa", "A2": "Salada Grão de Bico", "A3": "Macarrão Abobrinha", "A4": "Escondidinho Fit", "A5": "Estrogonofe Veg", "A6": "Risoto Leve", "A7": "Feijoada Vegana"},
    "Lanche da Tarde": {"A": "Iogurte com Frutas", "B": "Mix de Castanhas", "C": "Biscoito de Arroz", "D": "Smoothie Verde", "L1": "Iogurte com Frutas", "L2": "Mix de Castanhas", "L3": "Biscoito de Arroz", "L4": "Smoothie Verde", "L5": "Muffin de Banana", "L6": "Torrada c/ Pasta", "L7": "Palitos de Cenoura"},
    "Jantar": {"A": "Sopa de Lentilha", "B": "Omelete de Espinafre", "C": "Creme de Abóbora", "D": "Salada Caprese", "J1": "Sopa de Lentilha", "J2": "Omelete de Espinafre", "J3": "Creme de Abóbora", "J4": "Salada Caprese", "J5": "Torta de Vegetais", "J6": "Yakisoba Leve", "J7": "Pizza Low Carb"}
}

# Função para gerar a matriz da semana baseada no nível de variação
def gerar_matriz_semana(modo):
    if "Baixa" in modo:
        df = pd.DataFrame({
            "Refeição": ["Café da Manhã", "Almoço", "Lanche da Tarde", "Jantar"],
            "Segunda": ["A", "A", "A", "A"],
            "Terça": ["A", "A", "A", "A"],
            "Quarta": ["A", "A", "A", "A"],
            "Quinta": ["A", "A", "A", "A"],
            "Sexta": ["B", "B", "B", "B"],
            "Sábado": ["B", "B", "B", "B"],
            "Domingo": ["B", "B", "B", "B"]
        })
    elif "Média" in modo:
        df = pd.DataFrame({
            "Refeição": ["Café da Manhã", "Almoço", "Lanche da Tarde", "Jantar"],
            "Segunda": ["A", "A", "A", "B"],
            "Terça": ["A", "A", "B", "B"],
            "Quarta": ["A", "B", "A", "C"],
            "Quinta": ["B", "B", "B", "C"],
            "Sexta": ["B", "C", "A", "D"],
            "Sábado": ["B", "C", "B", "D"],
            "Domingo": ["C", "D", "C", "A"]
        })
    else:
        df = pd.DataFrame({
            "Refeição": ["Café da Manhã", "Almoço", "Lanche da Tarde", "Jantar"],
            "Segunda": ["C1", "A1", "L1", "J1"],
            "Terça": ["C2", "A2", "L2", "J2"],
            "Quarta": ["C3", "A3", "L3", "J3"],
            "Quinta": ["C4", "A4", "L4", "J4"],
            "Sexta": ["C5", "A5", "L5", "J5"],
            "Sábado": ["C6", "A6", "L6", "J6"],
            "Domingo": ["C7", "A7", "L7", "J7"]
        })
        
    # Substitui as letras (códigos) pelos nomes reais das receitas
    for index, row in df.iterrows():
        refeicao = row["Refeição"]
        for col in df.columns[1:]:
            codigo = df.at[index, col]
            df.at[index, col] = receitas_mock[refeicao].get(codigo, codigo)
            
    return df

# --- ÁREA PRINCIPAL DO APP ---
st.title("🥗 NutriIA: Seu Planejador Personalizado")

aba1, aba2, aba3 = st.tabs(["📅 Cardápio da Semana", "💬 Assistente & Substituições", "📖 Livro de Receitas"])

with aba1:
    st.header("Seu Planejamento Semanal")
    
    st.info(f"**Filtros Ativos:** Dieta {estilo_dieta} | Alergias: {', '.join(alergias) if alergias else 'Nenhuma'} | Itens excluídos: {len(st.session_state.lista_odios)}")
    
    st.subheader("1. Nível de Variação da Semana")
    modo_variacao = st.radio(
        "Escolha como quer cozinhar nesta semana:",
        ["Baixa Variação (Modo Marmita - 8 receitas)", 
         "Média Variação (Modo Equilíbrio - 14 receitas)", 
         "Alta Variação (Modo Chef - 28 receitas)"],
        horizontal=True
    )
    
    # Exibir a Tabela da Matriz
    st.markdown("**Visão Geral da Semana (Matriz de Receitas):**")
    df_semana = gerar_matriz_semana(modo_variacao)
    # Configurando o Pandas para não mostrar o índice numérico
    st.dataframe(df_semana, hide_index=True, use_container_width=True)
    
    st.divider()
    
    # Menu do Dia Selecionado
    st.subheader("2. Cardápio Detalhado do Dia")
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    dia_selecionado = st.selectbox("Visualizar ingredientes e preparo de:", dias)
    
    # Pegar as letras/códigos da matriz para o dia selecionado
    refeicoes_do_dia = df_semana[dia_selecionado].tolist()
    
    st.markdown(f"### Menu de {dia_selecionado}")
    
    # Criar 4 colunas para as refeições
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"#### ☕ Café da Manhã")
        st.markdown(f"**{refeicoes_do_dia[0]}**")
        st.caption("320 kcal | 15g Proteína")
        with st.expander("Ver Receita Completa"):
            st.markdown("**Ingredientes:**")
            st.markdown("- 40g de aveia em flocos\n- 1 ovo inteiro\n- 1 banana nanica amassada\n- 1 pitada de canela em pó\n- 1 colher de chá de óleo de coco (para untar)")
            st.markdown("**Modo de Preparo:**")
            st.markdown("1. Amasse bem a banana com um garfo.\n2. Misture o ovo, a aveia e a canela até formar uma massa homogênea.\n3. Unte uma frigideira antiaderente com o óleo de coco e aqueça.\n4. Despeje a massa e doure dos dois lados.")
            st.button("Salvar Receita", key="save_cafe")

    with col2:
        st.markdown(f"#### 🥗 Almoço")
        st.markdown(f"**{refeicoes_do_dia[1]}**")
        st.caption("450 kcal | 22g Proteína")
        with st.expander("Ver Receita Completa"):
            st.markdown("**Ingredientes (Pesados Crus):**")
            st.markdown("- 60g de quinoa em grãos crua\n- 100g de brócolis ninja\n- 80g de cenoura picada\n- 1 colher de sopa (15ml) de azeite extra virgem\n- Sal, pimenta-do-reino e páprica defumada a gosto\n- Suco de meio limão")
            st.markdown("**Modo de Preparo:**")
            st.markdown("1. Lave a quinoa e cozinhe em 120ml de água fervente com uma pitada de sal por 15 min.\n2. Cozinhe o brócolis e a cenoura no vapor até ficarem *al dente*.\n3. Em uma tigela, misture a quinoa cozida e os vegetais.\n4. Tempere com azeite, limão, sal, pimenta e páprica defumada.")
            st.button("Salvar Receita", key="save_almoco")

    with col3:
        st.markdown(f"#### 🍎 Lanche da Tarde")
        st.markdown(f"**{refeicoes_do_dia[2]}**")
        st.caption("200 kcal | 12g Proteína")
        with st.expander("Ver Receita Completa"):
            st.markdown("**Ingredientes:**")
            st.markdown("- 1 pote (170g) de iogurte natural desnatado\n- 80g de morangos frescos picados\n- 1 colher de sopa (10g) de semente de chia\n- Gotas de extrato de baunilha (opcional)")
            st.markdown("**Modo de Preparo:**")
            st.markdown("1. Em uma taça, despeje o iogurte natural e misture a baunilha se desejar.\n2. Cubra com os morangos picados.\n3. Finalize salpicando as sementes de chia por cima. Sirva gelado.")
            st.button("Salvar Receita", key="save_lanche")

    with col4:
        st.markdown(f"#### 🍲 Jantar")
        st.markdown(f"**{refeicoes_do_dia[3]}**")
        st.caption("380 kcal | 18g Proteína")
        with st.expander("Ver Receita Completa"):
            st.markdown("**Ingredientes (Pesados Crus):**")
            st.markdown("- 50g de lentilha crua\n- 1/2 cebola média picada\n- 2 dentes de alho amassados\n- 100g de abóbora cabotiá em cubos\n- 1 colher de chá de azeite\n- 1 folha de louro, cominho e coentro fresco a gosto")
            st.markdown("**Modo de Preparo:**")
            st.markdown("1. Deixe a lentilha de molho por 2 horas. Escorra.\n2. Refogue a cebola e o alho no azeite até dourarem.\n3. Adicione a abóbora, a lentilha, o louro e o cominho. Cubra com água (aprox. 400ml).\n4. Cozinhe na pressão por 15 min ou até amolecer. Finalize com coentro fresco picado.")
            st.button("Salvar Receita", key="save_jantar")

with aba2:
    st.header("💬 Converse com seu Assistente")
    st.write("O chat já saberá que você está na dieta **{}** e excluiu: **{}**!".format(
        estilo_dieta, 
        ', '.join(st.session_state.lista_odios) if st.session_state.lista_odios else 'nenhum alimento'
    ))

with aba3:
    st.header("📖 Livro de Receitas")
    st.write("Suas receitas salvas aparecerão aqui.")
