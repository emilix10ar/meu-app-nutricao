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

# Barra Lateral (Filtros e Preferências)
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

# ----- ABA 1: CARDÁPIO DA SEMANA -----
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

# ----- ABA 2: LISTA DE COMPRAS -----
with aba2:
    st.header("🛒 Seleção de Refeições & Lista de Compras Inteligente")
    st.write("Marque as refeições que fará em casa. Desmarque as que comer fora para economizar!")
    
    col_check, col_lista = st.columns([1, 1])
    refeicoes_aprovadas = []
    
    with col_check:
        st.subheader("1. Confirmar Cardápio Semanal")
        dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        
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

# ----- ABA 3: ASSISTENTE GEMINI AI -----
with aba3:
    st.header("💬 Converse com seu Assistente de Nutrição (IA)")
    st.write("Tire dúvidas nutricionais, receba dicas de substituição e peça sugestões com base no seu banco de dados e preferências!")
    
    # Tenta obter a chave do Streamlit Secrets
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.warning("⚠️ **Chave do Gemini não configurada nos Secrets!**")
        st.info(
            "Para utilizar a IA gratuitamente:\n"
            "1. Acesse o [Google AI Studio](https://aistudio.google.com/) e crie sua API Key.\n"
            "2. No painel do Streamlit Cloud, vá em **Manage App** ➔ **Settings** ➔ **Secrets**.\n"
            "3. Adicione a linha: `GEMINI_API_KEY = \"sua_chave_aqui\"`"
        )
    else:
        try:
            from google import genai
            
            if "chat_messages" not in st.session_state:
                st.session_state.chat_messages = [
                    {"role": "assistant", "content": "Olá! Sou seu assistente do NutriIA. Como posso te ajudar com seu cardápio, receitas ou dúvidas de substituição hoje?"}
                ]

            for msg in st.session_state.chat_messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            prompt_usuario = st.chat_input("Ex: Não tenho tilápia para o almoço, o que posso substituir mantendo a proteína?")
            
            if prompt_usuario:
                st.session_state.chat_messages.append({"role": "user", "content": prompt_usuario})
                with st.chat_message("user"):
                    st.markdown(prompt_usuario)

                # Construção do Contexto das Receitas da Planilha
                contexto_receitas = "Receitas do usuário cadastradas na planilha:\n"
                for nome, rec in RECEITAS_DB.items():
                    contexto_receitas += f"- {nome} ({rec['tipo']} | {rec['kcal']} kcal, {rec['proteina']}g prot):\n"
                    for ing in rec.get("ingredientes", []):
                        contexto_receitas += f"   • {ing['qtd']}{ing['unidade']} {ing['item']}\n"

                system_prompt = f"""Você é o NutriIA, um assistente de nutrição virtual amigável, prático e objetivo.
                
                Informações do perfil do usuário:
                - Estilo de dieta: {estilo_dieta}
                - Alergias e Restrições: {', '.join(alergias) if alergias else 'Nenhuma'}
                - Alimentos bloqueados/odiados: {', '.join(st.session_state.lista_odios) if st.session_state.lista_odios else 'Nenhum'}
                
                {contexto_receitas}
                
                Instruções de resposta:
                1. Responda à dúvida do usuário levando em consideração o estilo de dieta, alergias e alimentos excluídos dele.
                2. Sempre que sugerir trocas de alimentos ou receitas, priorize manter o equilíbrio nutricional (calorias e proteínas).
                3. Se o usuário perguntar algo sobre as receitas dele, use os dados do banco de dados fornecido.
                4. Mantenha um tom encorajador, simples e direto ao ponto."""

                with st.chat_message("assistant"):
                    with st.spinner("NutriIA está pensando..."):
                        try:
                            client = genai.Client(api_key=api_key)
                            full_prompt = f"{system_prompt}\n\nPergunta do usuário: {prompt_usuario}"
                            
                            response = client.models.generate_content(
                                model='gemini-3.5-flash',
                                contents=full_prompt,
                            )
                            resposta_texto = response.text
                            st.markdown(resposta_texto)
                            st.session_state.chat_messages.append({"role": "assistant", "content": resposta_texto})
                        except Exception as e:
                            st.error(f"Erro ao comunicar com a inteligência artificial: {e}")
        except ImportError:
            st.error("Biblioteca `google-genai` não instalada. Verifique se atualizou o arquivo `requirements.txt` no GitHub.")

# ----- ABA 4: LIVRO DE RECEITAS -----
with aba4:
    st.header("📖 Seu Livro de Receitas")
    st.write("Todas as suas receitas cadastradas no Google Sheets visualizadas em formato de cards!")
    
    if not RECEITAS_DB:
        st.info("Nenhuma receita encontrada na planilha.")
    else:
        rec_cols = st.columns(2)
        for idx, (nome, dados) in enumerate(RECEITAS_DB.items()):
            col_target = rec_cols[idx % 2]
            with col_target:
                with st.container(border=True):
                    st.subheader(nome)
                    st.caption(f"🏷️ **Tipo:** {dados['tipo']} | 🔥 **{dados['kcal']} kcal** | 💪 **{dados['proteina']}g Proteína**")
                    st.markdown("**Ingredientes:**")
                    for ing in dados.get("ingredientes", []):
                        st.markdown(f"- {ing['qtd']}{ing['unidade']} de {ing['item']}")
                    
                    with st.expander("Modo de Preparo"):
                        st.write(dados.get("preparo", "Sem modo de preparo informado."))
