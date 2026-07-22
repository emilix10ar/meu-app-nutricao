import streamlit as st

st.set_page_config(
    page_title="NutriIA - Sua Dieta Inteligente",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 NutriIA: Seu Planejador Personalizado")

# Menu de navegação por Abas
aba1, aba2, aba3 = st.tabs(["📅 Cardápio da Semana", "💬 Assistente & Substituições", "📖 Livro de Receitas"])

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
        st.info("**Omelete com Aveia e Frutas**\n\n- 2 Ovos inteiros\n- 30g de Aveia em flocos\n- 50g de Morangos picados\n- 1 colher (chá) de manteiga ou azeite\n- Sal, pimenta e canela a gosto\n\n*Kcal: 350 | Prot: 20g*")
        
        with st.expander("👨‍🍳 Modo de Preparo"):
            st.write("""
1. Lave bem os morangos, pique-os e reserve (adicione uma pitada de canela, se gostar).
2. Em uma tigela, bata bem os ovos com um garfo.
3. Misture a aveia, uma pitada de sal e de pimenta-do-reino aos ovos.
4. Aqueça uma frigideira antiaderente em fogo baixo e unte com a manteiga ou azeite.
5. Despeje a mistura e deixe cozinhar até firmar de um lado, depois vire para dourar o outro.
6. Sirva o omelete em um prato acompanhado dos morangos picados.
            """)
        if st.button("➕ Salvar no Livro", key="salvar_cafe"):
            st.toast("Receita salva no seu Livro!")
            
    with col2:
        st.markdown("### 🍽️ Almoço")
        st.success("**Tilápia Grelhada com Quinoa**\n\n- 150g de Filé de Tilápia\n- 40g de Quinoa crua\n- 1 xícara de folhas verdes\n- 1 colher (sopa) de Azeite\n- Limão, alho, páprica, sal e pimenta\n\n*Kcal: 480 | Prot: 38g*")
        
        with st.expander("👨‍🍳 Modo de Preparo"):
            st.write("""
1. Tempere a tilápia com suco de meio limão, 1 dente de alho amassado, páprica, sal e pimenta. Deixe marinar por 10 minutos.
2. Lave a quinoa em água corrente usando uma peneira fina. 
3. Cozinhe a quinoa em uma panela com 1 xícara de água e uma pitada de sal. Deixe ferver, baixe o fogo, tampe e cozinhe por cerca de 15 minutos até a água secar e os grãos ficarem macios.
4. Aqueça uma frigideira com um fiozinho do azeite (separe o resto para a salada) e grelhe a tilápia por 3 a 4 minutos de cada lado até dourar.
5. Lave as folhas verdes e monte no prato.
6. Sirva o peixe ao lado da quinoa e regue a salada com o restante do azeite.
            """)
        if st.button("➕ Salvar no Livro", key="salvar_almoco"):
            st.toast("Receita salva no seu Livro!")
            
    with col3:
        st.markdown("### 🥪 Lanche da Tarde")
        st.warning("**Iogurte com Chia e Castanhas**\n\n- 170g Iogurte Natural (1 potinho)\n- 10g (1 colher de sopa) de Semente de Chia\n- 15g de Mix de Castanhas\n- 1 colher (chá) de mel (opcional)\n\n*Kcal: 250 | Prot: 14g*")
        
        with st.expander("👨‍🍳 Modo de Preparo"):
            st.write("""
1. Em uma taça ou copo, despeje o iogurte natural.
2. Adicione a semente de chia (e o mel, se desejar) e misture muito bem.
3. Deixe descansar na geladeira por 10 a 15 minutos. Isso fará a chia hidratar e o iogurte ficar muito mais cremoso (tipo um pudim).
4. Pique grosseiramente as castanhas com uma faca.
5. Retire o iogurte da geladeira, salpique as castanhas por cima e sirva imediatamente.
            """)
        if st.button("➕ Salvar no Livro", key="salvar_lanche"):
            st.toast("Receita salva no seu Livro!")
            
    with col4:
        st.markdown("### 🌙 Jantar")
        st.error("**Sopa de Lentilha e Cogumelos**\n\n- 50g de Lentilha crua\n- 100g de Cogumelos Paris frescos\n- 1/2 Cenoura e 1/2 Cebola picadas\n- 1 colher (chá) de Azeite, Alho, Louro\n- 300ml de Água quente\n- Sal e pimenta a gosto\n\n*Kcal: 380 | Prot: 22g*")
        
        with st.expander("👨‍🍳 Modo de Preparo"):
            st.write("""
1. Lave bem a lentilha crua em água corrente.
2. Em uma panela, aqueça o azeite e refogue a cebola picada, o alho e a cenoura até a cebola ficar translúcida.
3. Adicione a lentilha, 1 folha de louro, uma pitada de sal e pimenta-do-reino. 
4. Despeje a água quente, misture, tampe parcialmente a panela e cozinhe em fogo médio/baixo por 20 a 25 minutos, até a lentilha ficar macia. Se precisar, pingue mais água.
5. Enquanto isso, em uma frigideira separada sem óleo, salteie os cogumelos fatiados rapidamente até dourarem (eles soltam a própria água).
6. Adicione os cogumelos dourados à sopa de lentilha pronta, deixe ferver por mais 2 minutos para incorporar o sabor. Finalize com cheiro-verde e sirva quente.
            """)
        if st.button("➕ Salvar no Livro", key="salvar_jantar"):
            st.toast("Receita salva no seu Livro!")

    st.divider()
    st.subheader("🔄 Troca Rápida de Refeição")
    col_a, col_b = st.columns(2)
    with col_a:
        st.selectbox("Trocar a refeição:", ["Almoço de Terça", "Jantar de Quinta", "Lanche de Sexta"])
    with col_b:
        st.selectbox("Pela refeição de:", ["Jantar de Sexta", "Almoço de Sábado", "Lanche de Domingo"])
    st.button("Confirmar Troca no Cardápio")

with aba2:
    st.info("O Chat de IA será construído aqui na Fase 2!")

with aba3:
    st.info("Seu banco de receitas será organizado aqui na Fase 3!")
