import streamlit as st
import pandas as pd
from dados_receitas import carregar_dados_planilha
from logica_compras import consolidar_lista_compras, buscar_opcoes_troca, gerar_texto_google_keep

st.set_page_config(
    page_title="NutriIA - Sua Dieta Inteligente",
    page_icon="🥗",
    layout="wide"
)

RECEITAS_DB, CATEGORIAS_COMPRAS, todos_ingredientes = carregar_dados_planilha()

with st.sidebar:
    st.header("⚙️ Suas Preferências")
    
    st.subheader("1. Estilo de Vida Alimentar")
    estilo_dieta = st.selectbox(
        "Selecione sua base alimentar:",
        ["Flexitariana", "Onívora (com carne)", "Ovolactovegetariana", "Pescetariana", "Vegana", "Sem Glúten", "Sem Lactose"]
    )
    
    st.subheader("2. Restrições Médicas e Alergias")
    alergias = st.multiselect(
        "Selecione se houver (Filtro Estrito):",
        ["Sem Laticínios", "Restrição Estrita a Glúten", "Sem Frutos do Mar", "Alergia a Oleaginosas", "Alergia a Ovo", "Alergia a Soja", "Diabética / Baixo IG"]
    )
    
    st.subheader("3. Alimentos Excluídos 🚫")
    st.write("Pesquise e selecione um alimento para excluí-lo.")
    
    if "lista_odios" not in st.session_state:
        st.session_state.lista_odios = []

    opcoes_disponiveis = [ing for ing in todos_ingredientes if ing not in st.session_state.lista_odios]

    alimento_selecionado = st.selectbox(
        "Digite para buscar na lista:",
        options=[""] + opcoes_disponiveis,
        index=0,
        key="select_odio_input"
    )
    
    if st.button("Bloquear alimento"):
        if alimento_selecionado and alimento_selecionado not in st.session_state.lista_odios:
            st.session_state.lista_odios.append(alimento_selecionado)
            st.rerun()
            
    if st.session_state.lista_odios:
        st.markdown("**Meus itens excluídos:**")
        for item in list(st.session_state.lista_odios):
            col_text, col_del = st.columns([3, 1])
            with col_text:
                st.write(f"❌ {item}")
            with col_del:
                if st.button("🗑️", key=f"del_{item}"):
                    st.session_state.lista_odios.remove(item)
                    st.rerun()
        
        if st.button("Limpar Toda a Lista"):
            st.session_state.lista_odios = []
            st.rerun()

if "trocas_usuario" not in st.session_state:
    st.session_state.trocas_usuario = {}

# Matriz base focada nas refeições cadastradas no Sheets/Mock
MATRIZ_BASE = {
    "Segunda": ["Panqueca de Aveia", "Tilápia Grelhada com Quinoa", "Panqueca de Aveia", "Tilápia Grelhada com Quinoa"],
    "Terça": ["Panqueca de Aveia", "Tilápia Grelhada com Quinoa", "Panqueca de Aveia", "Tilápia Grelhada com Quinoa"],
    "Quarta": ["Panqueca de Aveia", "Tilápia Grelhada com Quinoa", "Panqueca de Aveia", "Tilápia Grelhada com Quinoa"],
    "Quinta": ["Panqueca de Aveia", "Tilápia Grelhada com Quinoa", "Panqueca de Aveia", "Tilápia Grelhada com Quinoa"],
    "Sexta": ["Panqueca de Aveia", "Tilápia Grelhada com Quinoa", "Panqueca de Aveia", "Tilápia Grelhada com Quinoa"],
    "Sábado": ["Panqueca de Aveia", "Tilápia Grelhada com Quinoa", "Panqueca de Aveia", "Tilápia Grelhada com Quinoa"],
    "Domingo": ["Panqueca de Aveia", "Tilápia Grelhada com Quinoa", "Panqueca de Aveia", "Tilápia Grelhada com Quinoa"]
}

st.title("🥗 NutriIA: Seu Planejador Personalizado")

aba1, aba2, aba3, aba4 = st.tabs([
    "📅 Cardápio da Semana", 
    "🛒 Montar Lista & Compras", 
    "💬 Assistente & Substituições", 
    "📖 Livro de Receitas"
])

with aba1:
    st.header("Seu Planejamento Semanal")
    st.info(f"**Filtros Ativos:** Dieta {estilo_dieta} | Alergias: {', '.join(alergias) if alergias else 'Nenhuma'}")
    
    st.subheader("1. Nível de Variação da Semana")
    modo_variacao = st.radio(
        "Escolha como quer cozinhar nesta semana:",
        ["Baixa Variação (Modo Marmita)", "Média Variação (Modo Equilíbrio)", "Alta Variação (Modo Chef)"],
        horizontal=True
    )
    
    st.markdown("**Visão Geral da Semana:**")
    
    df_semana = pd.DataFrame(MATRIZ_BASE)
    df_semana.insert(0, "Refeição", ["Café da Manhã", "Almoço", "Lanche da Tarde", "Jantar"])
    st.dataframe(df_semana, hide_index=True, use_container_width=True)
    
    st.divider()
    st.subheader("2. Cardápio Detalhado do Dia")
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    dia_sel = st.selectbox("Visualizar ingredientes e preparo de:", dias)
    
    refeicoes_dia = MATRIZ_BASE[dia_sel]
    cols = st.columns(4)
    titulos = ["☕ Café da Manhã", "🥗 Almoço", "🍎 Lanche da Tarde", "🍲 Jantar"]
    
    for idx, col in enumerate(cols):
        rec_nome = refeicoes_dia[idx]
        # .get seguro caso o usuário adicione um prato na planilha que não exista na matriz
        rec_info = RECEITAS_DB.get(rec_nome, {"kcal": 0, "proteina": 0, "ingredientes": [], "preparo": "Receita não encontrada."})
        with col:
            st.markdown(f"#### {titulos[idx]}")
            st.markdown(f"**{rec_nome}**")
            st.caption(f"{rec_info.get('kcal', 0)} kcal | {rec_info.get('proteina', 0)}g Proteína")
            with st.expander("Ver Receita Completa"):
                st.markdown("**Ingredientes:**")
                for ing in rec_info.get("ingredientes", []):
                    st.markdown(f"- {ing['qtd']}{ing['unidade']} de {ing['item']}")
                st.markdown("**Modo de Preparo:**")
                st.write(rec_info.get("preparo", "Instruções indisponíveis."))

with aba2:
    st.header("🛒 Seleção de Refeições & Lista de Compras Inteligente")
    st.write("Marque as refeições que fará em casa. Desmarque as que comer fora para economizar!")
    
    col_check, col_lista = st.columns([1, 1])
    refeicoes_aprovadas = []
    
    with col_check:
        st.subheader("1. Confirmar Cardápio Semanal")
        
        for dia in dias:
            with st.expander(f"📌 Refeições de {dia}", expanded=(dia == "Segunda")):
                refeicoes_dia = MATRIZ_BASE[dia]
                refeicao_tipos = ["Café da Manhã", "Almoço", "Lanche da Tarde", "Jantar"]
                
                for idx, tipo in enumerate(refeicao_tipos):
                    rec_padrao = refeicoes_dia[idx]
                    chave_troca = f"{dia}_{tipo}"
                    rec_atual = st.session_state.trocas_usuario.get(chave_troca, rec_padrao)
                    
                    fara_refeicao = st.checkbox(
                        f"{tipo}: **{rec_atual}**", 
                        value=True, 
                        key=f"check_{chave_troca}"
                    )
                    
                    if fara_refeicao:
                        refeicoes_aprovadas.append(rec_atual)
                        
                    opcoes = buscar_opcoes_troca(rec_atual, RECEITAS_DB)
                    if opcoes:
                        sub_cols = st.columns([1, 2])
                        with sub_cols[0]:
                            st.caption("Trocar por:")
                        with sub_cols[1]:
                            for opc in opcoes:
                                if st.button(f"🔄 {opc['nome']} ({opc['kcal']}kcal)", key=f"btn_{chave_troca}_{opc['nome']}"):
                                    st.session_state.trocas_usuario[chave_troca] = opc['nome']
                                    st.rerun()

    with col_lista:
        st.subheader("2. Sua Lista de Compras Consolidada")
        
        if not refeicoes_aprovadas:
            st.warning("Nenhuma refeição foi marcada à esquerda para gerar a lista.")
        else:
            lista_consolidada = consolidar_lista_compras(refeicoes_aprovadas, RECEITAS_DB, CATEGORIAS_COMPRAS)
            
            for categoria, itens in lista_consolidada.items():
                if itens:
                    st.markdown(f"### {categoria}")
                    for (nome_ing, unidade), dados in itens.items():
                        chave_base = f"base_{nome_ing}_{categoria}"
                        chave_qtd = f"qtd_{nome_ing}_{categoria}"
                        
                        if chave_qtd not in st.session_state:
                            st.session_state[chave_qtd] = dados["qtd"]
                            st.session_state[chave_base] = dados["qtd"]
                        elif st.session_state.get(chave_base) != dados["qtd"]:
                            st.session_state[chave_base] = dados["qtd"]
                            st.session_state[chave_qtd] = dados["qtd"]

                        qtd_atual = float(st.session_state.get(chave_qtd, dados["qtd"]))

                        c_qtd, c_ing, c_sub = st.columns([1, 2.5, 1])
                        with c_qtd:
                            nova_qtd = st.number_input(
                                f"Qtd ({unidade})",
                                min_value=0.0,
                                value=qtd_atual,
                                step=1.0,
                                key=chave_qtd,
                                label_visibility="collapsed"
                            )
                            dados["qtd"] = nova_qtd

                        with c_ing:
                            if nova_qtd > 0:
                                st.checkbox(f"**{nova_qtd} {unidade}** de {nome_ing}", value=False, key=f"ing_{nome_ing}_{categoria}")
                            else:
                                st.caption(f"~~{nome_ing} (Possuo em casa)~~")

                        with c_sub:
                            if dados["substitutos"]:
                                with st.popover("🔄 Substituir"):
                                    st.caption(f"Não achou {nome_ing}?")
                                    for sub in dados["substitutos"]:
                                        st.write(f"- Opção: **{sub}**")
            
            st.divider()
            
            st.subheader("3. Exportar para o Google Keep")
            texto_keep = gerar_texto_google_keep(lista_consolidada)
            st.text_area("Copie o texto abaixo e cole no Google Keep:", value=texto_keep, height=200)

with aba3:
    st.header("💬 Converse com seu Assistente de Nutrição")
    st.write("Em breve conectaremos a Inteligência Artificial ao vivo aqui!")

with aba4:
    st.header("📖 Seu Livro de Receitas")
    st.write("Sua biblioteca de receitas conectada automaticamente ao Google Sheets.")
