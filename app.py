import streamlit as st
import pandas as pd
from dados_receitas import RECEITAS_DB
from logica_compras import consolidar_lista_compras, buscar_opcoes_troca, gerar_texto_google_keep

# Configuração da página do aplicativo
st.set_page_config(
    page_title="NutriIA - Sua Dieta Inteligente",
    page_icon="🥗",
    layout="wide"
)

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
    st.write("Digite um alimento para excluí-lo de todas as receitas.")
    
    if "lista_odios" not in st.session_state:
        st.session_state.lista_odios = []

    novo_odio = st.text_input("Ex: Coentro, Berinjela, Uva Passa...")
    if st.button("Bloquear alimento"):
        if novo_odio and novo_odio.lower() not in [item.lower() for item in st.session_state.lista_odios]:
            st.session_state.lista_odios.append(novo_odio.title())
            st.rerun()
            
    if st.session_state.lista_odios:
        st.markdown("**Meus itens excluídos:**")
        for item in st.session_state.lista_odios:
            st.markdown(f"- ❌ {item}")
        
        if st.button("Limpar Lista"):
            st.session_state.lista_odios = []
            st.rerun()

if "trocas_usuario" not in st.session_state:
    st.session_state.trocas_usuario = {}

# Mapeamento do Cardápio Semanal Base
MATRIZ_BASE = {
    "Segunda": ["Panqueca de Aveia", "Tilápia Grelhada com Quinoa", "Iogurte com Chia e Castanhas", "Sopa de Lentilha e Cogumelos"],
    "Terça": ["Ovos Mexidos", "Bowl de Quinoa", "Mix de Castanhas", "Omelete de Espinafre"],
    "Quarta": ["Iogurte c/ Granola", "Salada Grão de Bico", "Iogurte com Chia e Castanhas", "Sopa de Lentilha e Cogumelos"],
    "Quinta": ["Vitamina de Banana", "Tilápia Grelhada com Quinoa", "Mix de Castanhas", "Omelete de Espinafre"],
    "Sexta": ["Panqueca de Aveia", "Bowl de Quinoa", "Iogurte com Chia e Castanhas", "Sopa de Lentilha e Cogumelos"],
    "Sábado": ["Ovos Mexidos", "Salada Grão de Bico", "Mix de Castanhas", "Omelete de Espinafre"],
    "Domingo": ["Iogurte c/ Granola", "Tilápia Grelhada com Quinoa", "Iogurte com Chia e Castanhas", "Sopa de Lentilha e Cogumelos"]
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
    st.info(f"**Filtros Ativos:** Dieta {estilo_dieta} | Alergias: {', '.join(alergias) if alergias else 'Nenhuma'} | Itens excluídos: {len(st.session_state.lista_odios)}")
    
    st.subheader("1. Nível de Variação da Semana")
    modo_variacao = st.radio(
        "Escolha como quer cozinhar nesta semana:",
        ["Baixa Variação (Modo Marmita)", "Média Variação (Modo Equilíbrio)", "Alta Variação (Modo Chef)"],
        horizontal=True
    )
    
    st.markdown("**Visão Geral da Semana (Nomes das Receitas):**")
    
    # Criar DataFrame para exibição
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
        rec_info = RECEITAS_DB.get(rec_nome, {})
        with col:
            st.markdown(f"#### {titulos[idx]}")
            st.markdown(f"**{rec_nome}**")
            st.caption(f"{rec_info.get('kcal', 300)} kcal | {rec_info.get('proteina', 15)}g Proteína")
            with st.expander("Ver Receita Completa"):
                st.markdown("**Ingredientes:**")
                for ing in rec_info.get("ingredientes", []):
                    st.markdown(f"- {ing['qtd']}{ing['unidade']} de {ing['item']}")
                st.markdown("**Modo de Preparo:**")
                st.write(rec_info.get("preparo", "Instruções indisponíveis."))

with aba2:
    st.header("🛒 Seleção de Refeições & Lista de Compras Inteligente")
    st.write("Marque as refeições que você fará em casa. Desmarque as que comer fora para economizar nas compras!")
    
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
                    
                    # Verificar se o usuário já realizou uma troca
                    chave_troca = f"{dia}_{tipo}"
                    rec_atual = st.session_state.trocas_usuario.get(chave_troca, rec_padrao)
                    
                    # Checkbox para aceitar a refeição na lista de compras
                    fara_refeicao = st.checkbox(
                        f"{tipo}: **{rec_atual}**", 
                        value=True, 
                        key=f"check_{chave_troca}"
                    )
                    
                    if fara_refeicao:
                        refeicoes_aprovadas.append(rec_atual)
                        
                    # Botão para trocar opção de refeição
                    opcoes = buscar_opcoes_troca(rec_atual)
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
            st.warning("Nenhuma refeição foi marcada. Marque ao menos uma refeição à esquerda para gerar sua lista.")
        else:
            lista_consolidada = consolidar_lista_compras(refeicoes_aprovadas)
            
            # Exibir categorias
            for categoria, itens in lista_consolidada.items():
                if itens:
                    st.markdown(f"### {categoria}")
                    for (nome_ing, unidade), dados in itens.items():
                        c_ing, c_sub = st.columns([2, 1])
                        with c_ing:
                            # Item com quantidade interativa e ajustável
                            st.checkbox(f"**{dados['qtd']}{unidade}** de {nome_ing}", value=False, key=f"ing_{nome_ing}_{categoria}")
                        with c_sub:
                            if dados["substitutos"]:
                                with st.popover("🔄 Substituir"):
                                    st.caption(f"Não achou {nome_ing}?")
                                    for sub in dados["substitutos"]:
                                        st.write(f"- Opção: **{sub}**")
            
            st.divider()
            
            # Botão de Exportação para o Google Keep
            st.subheader("3. Exportar para o Google Keep")
            texto_keep = gerar_texto_google_keep(lista_consolidada)
            
            st.text_area("Copie o texto abaixo e cole diretamente em uma nota do Google Keep:", value=texto_keep, height=200)

with aba3:
    st.header("💬 Converse com seu Assistente de Nutrição")
    st.write("Em breve conectaremos a Inteligência Artificial ao vivo aqui!")

with aba4:
    st.header("📖 Seu Livro de Receitas")
    st.write("Sua biblioteca de receitas personalizadas.")
