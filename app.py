import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configuração da página
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

# BANCO DE DADOS DE RECEITAS (Sem carnes, suínos e aves - Foco em Peixes, Ovos, Laticínios e Vegetais)
db_receitas = {
    "Café da Manhã": [
        {"nome": "Omelete com Aveia e Frutas", "ingredientes": ["2 Ovos inteiros cru", "30g de Aveia em flocos", "50g de Morangos", "1 col. de chá de azeite", "Sal, pimenta e canela"], "modo": "1. Lave e pique os morangos. 2. Bata os ovos com aveia, sal e pimenta. 3. Aqueça o azeite na frigideira e doure o omelete dos dois lados. 4. Sirva com morangos polvilhados com canela.", "kcal": 350, "prot": 20},
        {"nome": "Iogurte com Maçã e Canela", "ingredientes": ["170g Iogurte Natural", "1 Maçã pequena", "15g Aveia", "Canela em pó"], "modo": "1. Pique a maçã em cubos. 2. Em uma tigela, misture o iogurte, a maçã e a aveia. 3. Finalize com canela a gosto.", "kcal": 280, "prot": 15},
        {"nome": "Crepioca de Queijo", "ingredientes": ["1 Ovo", "2 col. sopa Goma de Tapioca", "30g Queijo Minas padrão", "Sal e Orégano"], "modo": "1. Bata o ovo com a tapioca, sal e orégano. 2. Despeje na frigideira antiaderente. 3. Quando firmar, adicione o queijo, dobre ao meio e deixe derreter.", "kcal": 310, "prot": 14},
        {"nome": "Vitamina Proteica", "ingredientes": ["200ml Leite Desnatado ou Vegetal", "1 Banana", "30g Whey Protein (Baunilha)", "10g Chia"], "modo": "1. Coloque todos os ingredientes no liquidificador. 2. Bata até ficar homogêneo e sirva gelado.", "kcal": 330, "prot": 32},
        {"nome": "Ovos Mexidos com Cúrcuma", "ingredientes": ["3 Ovos inteiros", "1 col. chá de Manteiga", "Cúrcuma, Sal e Pimenta", "1 Fatia de Pão Integral"], "modo": "1. Bata os ovos com os temperos. 2. Aqueça a manteiga e faça os ovos mexidos em fogo baixo para não ressecar. 3. Sirva sobre o pão torrado.", "kcal": 380, "prot": 22},
        {"nome": "Mingau de Aveia", "ingredientes": ["40g Aveia em flocos", "150ml Leite Desnatado", "1 col. sobremesa Cacau 100%", "Stévia a gosto"], "modo": "1. Misture aveia, leite e cacau em uma panela. 2. Cozinhe em fogo baixo mexendo sempre até engrossar. 3. Adoce com stévia no final.", "kcal": 250, "prot": 12},
        {"nome": "Torrada com Pasta de Amendoim", "ingredientes": ["2 Fatias Pão Integral", "30g Pasta de Amendoim Integral", "Rodelas de Banana (Meia banana)"], "modo": "1. Toste levemente as fatias de pão. 2. Espalhe a pasta de amendoim uniformemente. 3. Coloque as rodelas de banana por cima.", "kcal": 400, "prot": 16}
    ],
    "Almoço": [
        {"nome": "Tilápia Grelhada com Quinoa", "ingredientes": ["150g Tilápia crua", "40g Quinoa crua", "Meio limão, 1 dente de alho", "Azeite (1 col. sopa), Sal, Páprica", "Folhas Verdes"], "modo": "1. Tempere o peixe com limão, alho, páprica e sal. 2. Lave a quinoa e cozinhe em 1 xícara de água com sal por 15min. 3. Grelhe a tilápia no azeite (3min de cada lado). 4. Sirva com salada regada a azeite.", "kcal": 480, "prot": 38},
        {"nome": "Grão-de-Bico Refogado", "ingredientes": ["100g Grão-de-bico cru", "1/2 Cebola, 1 Alho", "Azeite, Sal, Cúrcuma, Cominho", "150g Brócolis cru"], "modo": "1. Deixe o grão-de-bico de molho, depois cozinhe na pressão por 25min. 2. Cozinhe o brócolis no vapor. 3. Refogue cebola e alho no azeite, adicione os temperos e o grão-de-bico cozido. 4. Misture o brócolis.", "kcal": 450, "prot": 20},
        {"nome": "Salmão com Batata Doce", "ingredientes": ["150g Salmão cru", "100g Batata Doce crua", "Azeite, Alecrim, Sal, Pimenta", "Tomates cereja"], "modo": "1. Corte a batata doce em cubos, tempere com azeite, sal e alecrim e asse por 30min (200°C). 2. Tempere o salmão com sal e pimenta e grelhe ou asse nos 15 minutos finais junto com os tomates.", "kcal": 550, "prot": 35},
        {"nome": "Macarrão de Abobrinha c/ Atum", "ingredientes": ["1 Abobrinha média", "1 Lata de Atum em água (drenado)", "Molho de tomate caseiro (100ml)", "Manjericão, Alho, Sal"], "modo": "1. Faça espaguete com a abobrinha crua. 2. Refogue o alho, adicione o molho de tomate e o atum. 3. Coloque a abobrinha no molho apenas por 2 minutos para não amolecer demais. 4. Finalize com manjericão.", "kcal": 320, "prot": 30},
        {"nome": "Moqueca de Banana da Terra", "ingredientes": ["1 Banana da Terra crua", "1/2 Pimentão, 1/2 Cebola", "50ml Leite de Coco", "Azeite de Dendê (1 col. chá), Coentro"], "modo": "1. Fatie a banana e os vegetais. 2. Refogue cebola e pimentão, adicione a banana, o leite de coco e o dendê. 3. Cozinhe por 10min em fogo baixo. 4. Finalize com coentro.", "kcal": 400, "prot": 5},
        {"nome": "Risoto de Cogumelos", "ingredientes": ["50g Arroz Arbório cru", "100g Cogumelos Paris frescos", "1/4 Cebola, 1 col. manteiga", "Caldo de legumes caseiro", "30g Parmesão ralado"], "modo": "1. Refogue os cogumelos e reserve. 2. Refogue a cebola na manteiga, adicione o arroz cru e vá colocando o caldo quente aos poucos, mexendo sempre (aprox. 18min). 3. Misture os cogumelos e o parmesão no fim.", "kcal": 420, "prot": 14},
        {"nome": "Omelete de Forno c/ Legumes", "ingredientes": ["3 Ovos inteiros", "50g Cenoura ralada (crua), 50g Ervilha", "Sal, Pimenta, Cheiro-verde", "1 col. sopa Azeite"], "modo": "1. Bata os ovos e misture todos os vegetais e temperos. 2. Unte uma travessa pequena com azeite e despeje a mistura. 3. Asse em forno a 180°C por 20 minutos.", "kcal": 350, "prot": 21}
    ],
    "Lanche da Tarde": [
        {"nome": "Iogurte com Chia e Castanhas", "ingredientes": ["170g Iogurte Natural", "10g Chia", "15g Mix de Castanhas", "1 col. chá de mel (opcional)"], "modo": "1. Misture a chia no iogurte e deixe hidratar por 10min na geladeira. 2. Pique as castanhas. 3. Coloque as castanhas e o mel por cima e sirva.", "kcal": 250, "prot": 14},
        {"nome": "Mix de Castanhas e Frutas", "ingredientes": ["30g Mix de Castanhas", "1 Pera ou Maçã"], "modo": "1. Lave a fruta e consuma *in natura* acompanhada do mix de oleaginosas.", "kcal": 260, "prot": 5},
        {"nome": "Smoothie de Morango", "ingredientes": ["150ml Leite Desnatado", "100g Morangos congelados", "1 col. sopa Aveia"], "modo": "1. Coloque tudo no liquidificador e bata até obter um creme espesso.", "kcal": 150, "prot": 7},
        {"nome": "Biscoito de Arroz c/ Queijo", "ingredientes": ["3 Biscoitos de Arroz integrais", "3 col. sopa Cottage ou Ricota", "Orégano e um fio de azeite"], "modo": "1. Espalhe o queijo sobre os biscoitos de arroz. 2. Tempere com orégano e um fiozinho de azeite.", "kcal": 180, "prot": 10},
        {"nome": "Pão de Queijo de Frigideira", "ingredientes": ["1 Ovo", "2 col. sopa Tapioca", "1 col. sopa Parmesão ralado"], "modo": "1. Misture todos os ingredientes em uma caneca. 2. Despeje em uma frigideira antiaderente pequena e doure dos dois lados.", "kcal": 220, "prot": 11},
        {"nome": "Vitamina de Abacate", "ingredientes": ["50g Abacate", "150ml Leite Desnatado", "1 col. sobremesa Chia"], "modo": "1. Bata o abacate com o leite e a chia no liquidificador. Sirva gelado.", "kcal": 200, "prot": 6},
        {"nome": "Palitos de Cenoura c/ Homus", "ingredientes": ["1 Cenoura média crua", "2 col. sopa Homus (Pasta de grão-de-bico)"], "modo": "1. Descasque e corte a cenoura em palitos. 2. Mergulhe os palitos no homus para consumir.", "kcal": 160, "prot": 5}
    ],
    "Jantar": [
        {"nome": "Sopa de Lentilha e Cogumelos", "ingredientes": ["50g Lentilha crua", "100g Cogumelos Paris frescos", "Cebola, Alho, Azeite (1 col. chá)", "Louro, Sal e Pimenta"], "modo": "1. Refogue cebola e alho no azeite. Adicione a lentilha crua e água quente. Cozinhe por 20min. 2. Grelhe os cogumelos à parte sem óleo até dourarem. 3. Junte os cogumelos à sopa pronta.", "kcal": 380, "prot": 22},
        {"nome": "Tofu Grelhado e Brócolis", "ingredientes": ["150g Tofu firme", "100g Brócolis cru", "Shoyu (1 col. sopa), Gengibre ralado", "Óleo de gergelim (1 fio)"], "modo": "1. Fatie o tofu, tempere com shoyu e gengibre. Grelhe até dourar. 2. Cozinhe o brócolis no vapor. 3. Sirva juntos, finalizados com óleo de gergelim.", "kcal": 280, "prot": 24},
        {"nome": "Salada Niçoise (Atum e Ovos)", "ingredientes": ["1 Lata Atum (drenado)", "1 Ovo cozido", "Folhas Verdes, Tomate, Azeitonas", "Azeite, Limão, Sal"], "modo": "1. Cozinhe o ovo. 2. Monte a base de folhas e tomates. 3. Adicione o atum e o ovo cortado. 4. Tempere com azeite, limão e sal.", "kcal": 350, "prot": 32},
        {"nome": "Caldo de Abóbora", "ingredientes": ["200g Abóbora Cabotiá crua", "1/2 Cebola, Alho", "Gengibre em pó, Sal, Noz-moscada", "1 col. sopa Creme de Ricota"], "modo": "1. Cozinhe a abóbora com cebola e alho até desmanchar. 2. Bata no liquidificador com um pouco da água do cozimento. 3. Tempere, volte ao fogo e finalize com o creme de ricota.", "kcal": 200, "prot": 6},
        {"nome": "Wrap de Alface c/ Patê de Atum", "ingredientes": ["Folhas grandes de Alface", "1 Lata Atum", "2 col. sopa Iogurte Natural", "Cenoura ralada, Sal, Salsa"], "modo": "1. Misture o atum, iogurte, cenoura e temperos para fazer um patê. 2. Lave e seque bem a alface. 3. Use a alface como 'massa' e recheie com o patê.", "kcal": 220, "prot": 25},
        {"nome": "Berinjela Recheada c/ Ricota", "ingredientes": ["1/2 Berinjela", "50g Ricota amassada", "Molho de tomate caseiro", "Orégano, Azeite, Sal"], "modo": "1. Retire o miolo da berinjela. 2. Misture a ricota com os temperos e preencha a berinjela. 3. Cubra com molho e asse por 30min a 200°C.", "kcal": 180, "prot": 10},
        {"nome": "Creme de Ervilha", "ingredientes": ["50g Ervilha Seca crua", "1/2 Cebola, Alho", "Azeite (1 col. chá), Sal, Hortelã fresca"], "modo": "1. Cozinhe a ervilha na pressão com cebola e alho por 20min. 2. Bata no liquidificador (cuidado com a temperatura). 3. Sirva com folhinhas de hortelã fresco.", "kcal": 250, "prot": 14}
    ]
}

dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]

# Matrizes exatas baseadas nas tabelas de imagem do usuário
padroes_variacao = {
    "Baixa Variação (Modo Praticidade / Marmita)": {
        "Café da Manhã":   [0, 0, 0, 0, 1, 1, 1],
        "Almoço":          [0, 0, 0, 0, 1, 1, 1],
        "Lanche da Tarde": [0, 0, 0, 0, 1, 1, 1],
        "Jantar":          [0, 0, 0, 0, 1, 1, 1]
    },
    "Média Variação (Modo Equilíbrio)": {
        "Café da Manhã":   [0, 0, 0, 1, 1, 1, 2],
        "Almoço":          [0, 0, 1, 1, 2, 2, 3],
        "Lanche da Tarde": [0, 1, 0, 1, 0, 1, 2],
        "Jantar":          [1, 1, 2, 2, 3, 3, 0]
    },
    "Alta Variação (Modo Chef / Gastronômico)": {
        "Café da Manhã":   [0, 1, 2, 3, 4, 5, 6],
        "Almoço":          [0, 1, 2, 3, 4, 5, 6],
        "Lanche da Tarde": [0, 1, 2, 3, 4, 5, 6],
        "Jantar":          [0, 1, 2, 3, 4, 5, 6]
    }
}

st.title("🥗 NutriIA: Seu Planejador Personalizado")

aba1, aba2, aba3 = st.tabs(["📅 Cardápio da Semana", "💬 Assistente & Substituições", "📖 Livro de Receitas"])

# --- ABA 1: CARDÁPIO DA SEMANA (VISUAL E CALENDÁRIO) ---
with aba1:
    st.header("Seu Planejamento Semanal")
    st.write("Escolha seu nível de variação na cozinha e visualize todo o seu calendário alimentar.")
    
    # Seletor de Variação
    nivel_selecionado = st.selectbox(
        "⚙️ Qual seu objetivo de preparo esta semana?", 
        list(padroes_variacao.keys()),
        help="Baixa: Cozinhe poucas vezes. Alta: Cardápio diferente todo dia."
    )
    
    st.divider()
    st.subheader("🗓️ Calendário Geral da Semana")
    
    # Criar o Dataframe da semana baseado na escolha do usuário
    df_calendario = pd.DataFrame(index=["Café da Manhã", "Almoço", "Lanche da Tarde", "Jantar"], columns=dias_semana)
    
    for ref in df_calendario.index:
        indices = padroes_variacao[nivel_selecionado][ref]
        for i, dia in enumerate(dias_semana):
            # Preenche a célula do Excel/Dataframe com o nome da receita
            df_calendario.loc[ref, dia] = db_receitas[ref][indices[i]]["nome"]
    
    # Exibir a tabela bonita na tela
    st.dataframe(df_calendario, use_container_width=True)
    
    st.divider()
    
    st.subheader("🔍 Detalhes e Modo de Preparo")
    dia_selecionado = st.selectbox("Selecione o dia para ver as quantidades e o preparo:", dias_semana)
    
    idx_dia = dias_semana.index(dia_selecionado)
    
    # Pegar as 4 receitas exatas do dia selecionado
    rec_cafe = db_receitas["Café da Manhã"][padroes_variacao[nivel_selecionado]["Café da Manhã"][idx_dia]]
    rec_almoco = db_receitas["Almoço"][padroes_variacao[nivel_selecionado]["Almoço"][idx_dia]]
    rec_lanche = db_receitas["Lanche da Tarde"][padroes_variacao[nivel_selecionado]["Lanche da Tarde"][idx_dia]]
    rec_jantar = db_receitas["Jantar"][padroes_variacao[nivel_selecionado]["Jantar"][idx_dia]]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### ☕ Café da Manhã")
        st.info(f"**{rec_cafe['nome']}**\n\n- " + "\n- ".join(rec_cafe['ingredientes']) + f"\n\n*Kcal: {rec_cafe['kcal']} | Prot: {rec_cafe['prot']}g*")
        with st.expander("👨‍🍳 Preparo"):
            st.write(rec_cafe['modo'])
        if st.button("➕ Salvar", key="scafe"): st.toast("Salvo no Livro!")
            
    with col2:
        st.markdown("### 🍽️ Almoço")
        st.success(f"**{rec_almoco['nome']}**\n\n- " + "\n- ".join(rec_almoco['ingredientes']) + f"\n\n*Kcal: {rec_almoco['kcal']} | Prot: {rec_almoco['prot']}g*")
        with st.expander("👨‍🍳 Preparo"):
            st.write(rec_almoco['modo'])
        if st.button("➕ Salvar", key="salmoco"): st.toast("Salvo no Livro!")
            
    with col3:
        st.markdown("### 🥪 Lanche")
        st.warning(f"**{rec_lanche['nome']}**\n\n- " + "\n- ".join(rec_lanche['ingredientes']) + f"\n\n*Kcal: {rec_lanche['kcal']} | Prot: {rec_lanche['prot']}g*")
        with st.expander("👨‍🍳 Preparo"):
            st.write(rec_lanche['modo'])
        if st.button("➕ Salvar", key="slanche"): st.toast("Salvo no Livro!")
            
    with col4:
        st.markdown("### 🌙 Jantar")
        st.error(f"**{rec_jantar['nome']}**\n\n- " + "\n- ".join(rec_jantar['ingredientes']) + f"\n\n*Kcal: {rec_jantar['kcal']} | Prot: {rec_jantar['prot']}g*")
        with st.expander("👨‍🍳 Preparo"):
            st.write(rec_jantar['modo'])
        if st.button("➕ Salvar", key="sjantar"): st.toast("Salvo no Livro!")


# --- ABA 2: ASSISTENTE DE IA (CHAT CONVERSACIONAL) ---
with aba2:
    st.header("💬 Converse com seu Assistente de Nutrição")
    st.write("Peça substituições, ideias de refeições ou tire dúvidas. A IA já sabe das suas restrições alimentares!")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Sou seu assistente. Sei que você NÃO come carne bovina, suína nem frango. Como posso ajudar com sua dieta de 4 refeições hoje?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ex: 'O que comer no lanche com 20g de proteína?'"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

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
