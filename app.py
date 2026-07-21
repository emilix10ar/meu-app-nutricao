# ... existing code ...
    # Dividindo a tela em 4 colunas para as 4 refeições
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### ☕ Café da Manhã")
        st.info("**Omelete com Aveia e Frutas**\n\n- 2 Ovos inteiros\n- 30g de Aveia em flocos\n- 50g de Morangos picados\n- 1 colher (chá) de manteiga/azeite\n- Sal, pimenta e canela a gosto\n\n*Kcal: 350 | Prot: 20g*")
        
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
        st.success("**Tilápia Grelhada com Quinoa**\n\n- 150g de Filé de Tilápia\n- 40g de Quinoa crua\n- 1 xícara de folhas verdes\n- 1 col. (sopa) de Azeite\n- Limão, alho, páprica, sal e pimenta\n\n*Kcal: 480 | Prot: 38g*")
        
        with st.expander("👨‍🍳 Modo de Preparo"):
            st.write("""
1. Tempere a tilápia com limão, 1 dente de alho amassado, páprica, sal e pimenta. Deixe marinar por 10 min.
2. Lave a quinoa. Cozinhe em panela com 1 xícara de água e uma pitada de sal por ~15 min (fogo baixo), até secar e amaciar.
3. Aqueça uma frigideira com um fiozinho de azeite e grelhe a tilápia por 3 a 4 minutos de cada lado.
4. Lave as folhas verdes e monte a salada no prato.
5. Sirva o peixe, a quinoa e regue a salada com o restante do azeite.
            """)
        if st.button("➕ Salvar no Livro", key="salvar_almoco"):
            st.toast("Receita salva no seu Livro!")
            
    with col3:
        st.markdown("### 🥪 Lanche da Tarde")
        st.warning("**Iogurte com Chia e Castanhas**\n\n- 170g Iogurte Natural\n- 10g (1 col. sopa) de Chia\n- 15g de Mix de Castanhas\n- 1 col. (chá) de mel (opcional)\n\n*Kcal: 250 | Prot: 14g*")
        
        with st.expander("👨‍🍳 Modo de Preparo"):
            st.write("""
1. Em uma taça, despeje o iogurte natural.
2. Adicione a semente de chia (e o mel, se desejar) e misture muito bem.
3. Deixe descansar na geladeira por 10 a 15 minutos para a chia hidratar e o iogurte ficar mais cremoso.
4. Pique grosseiramente as castanhas com uma faca.
5. Retire o iogurte da geladeira, salpique as castanhas por cima e sirva.
            """)
        if st.button("➕ Salvar no Livro", key="salvar_lanche"):
            st.toast("Receita salva no seu Livro!")
            
    with col4:
        st.markdown("### 🌙 Jantar")
        st.error("**Sopa de Lentilha e Cogumelos**\n\n- 50g de Lentilha crua\n- 100g de Cogumelos Paris frescos\n- 1/2 Cenoura e 1/2 Cebola picadas\n- 1 col. (chá) Azeite, Alho, Louro\n- 300ml de Água quente\n- Sal e pimenta a gosto\n\n*Kcal: 380 | Prot: 22g*")
        
        with st.expander("👨‍🍳 Modo de Preparo"):
            st.write("""
1. Lave a lentilha crua.
2. Em uma panela, aqueça o azeite e refogue a cebola, o alho e a cenoura picada.
3. Adicione a lentilha, 1 folha de louro, sal e pimenta. Despeje a água quente.
4. Cozinhe com panela semitampada por 20 a 25 min, até a lentilha ficar macia.
5. Em frigideira separada, salteie os cogumelos fatiados rapidamente até dourarem.
6. Adicione os cogumelos à sopa, ferva por mais 2 minutos, finalize com cheiro-verde e sirva.
            """)
        if st.button("➕ Salvar no Livro", key="salvar_jantar"):
            st.toast("Receita salva no seu Livro!")

with aba2:
# ... existing code ...
```

Ficou muito mais claro agora! Verifique na pré-visualização como ficou e me diga se deseja fazer mais algum ajuste no layout da nossa Fase 1 antes de partirmos para o chat inteligente da Fase 2!
