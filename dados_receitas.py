# Este arquivo atua como nosso banco de dados temporário antes da conexão com o Google Sheets.

CATEGORIAS_COMPRAS = [
    "🥦 Hortifrúti (Horta, Pomar & Ervas)",
    "🥩 Açougue, Peixaria & Frios",
    "🥛 Laticínios & Refrigerados",
    "🌾 Mercearia Seca (Grãos, Massas & Farinhas)",
    "🫒 Condimentos, Óleos & Enlatados",
    "🌰 Castanhas, Sementes & Doces",
    "❄️ Congelados",
    "💊 Suplementos & Produtos Especiais (Opcional)"
]

RECEITAS_DB = {
    # --- CAFÉ DA MANHÃ ---
    "Panqueca de Aveia": {
        "tipo": "Café da Manhã",
        "kcal": 320,
        "proteina": 18,
        "ingredientes": [
            {"item": "Aveia em flocos", "qtd": 40, "unidade": "g", "categoria": "🌾 Mercearia Seca (Grãos, Massas & Farinhas)", "substitutos": ["Quinoa em flocos", "Farinha de amêndoas"]},
            {"item": "Ovo de galinha", "qtd": 2, "unidade": "unidades", "categoria": "🥩 Açougue, Peixaria & Frios", "substitutos": ["Ovos de codorna (8 un)", "Tofu amassado (100g)"]},
            {"item": "Banana nanica", "qtd": 1, "unidade": "unidade", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": ["Maçã ralada", "Mamão papaia"]},
            {"item": "Canela em pó", "qtd": 3, "unidade": "g", "categoria": "🫒 Condimentos, Óleos & Enlatados", "substitutos": ["Cacau em pó", "Nóz moscada"]}
        ],
        "preparo": "1. Amasse a banana com um garfo.\n2. Misture os ovos, a aveia e a canela até obter massa homogênea.\n3. Doure numa frigideira antiaderente levemente untada."
    },
    "Ovos Mexidos": {
        "tipo": "Café da Manhã",
        "kcal": 290,
        "proteina": 19,
        "ingredientes": [
            {"item": "Ovo de galinha", "qtd": 3, "unidade": "unidades", "categoria": "🥩 Açougue, Peixaria & Frios", "substitutos": ["Tofu mexido (150g)"]},
            {"item": "Azeite de oliva extra virgem", "qtd": 5, "unidade": "ml", "categoria": "🫒 Condimentos, Óleos & Enlatados", "substitutos": ["Manteiga ghee", "Óleo de abacate"]},
            {"item": "Pão integral fatiado", "qtd": 2, "unidade": "fatias", "categoria": "🌾 Mercearia Seca (Grãos, Massas & Farinhas)", "substitutos": ["Tapioca (40g)", "Pão sem glúten (2 fatias)"]},
            {"item": "Tomate cereja", "qtd": 50, "unidade": "g", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": ["Orégano seco", "Espinafre fresco"]}
        ],
        "preparo": "1. Batas os ovos levemente com sal e temperos.\n2. Aqueça o azeite na frigideira e despeje os ovos, mexendo até o ponto desejado.\n3. Sirva com as torradas de pão integral."
    },
    "Iogurte c/ Granola": {
        "tipo": "Café da Manhã",
        "kcal": 280,
        "proteina": 16,
        "ingredientes": [
            {"item": "Iogurte natural desnatado", "qtd": 170, "unidade": "g", "categoria": "🥛 Laticínios & Refrigerados", "substitutos": ["Iogurte de coco zero açucar", "Kefir de leite"]},
            {"item": "Granola sem açúcar", "qtd": 30, "unidade": "g", "categoria": "🌾 Mercearia Seca (Grãos, Massas & Farinhas)", "substitutos": ["Aveia em flocos", "Mix de castanhas"]},
            {"item": "Morango fresco", "qtd": 80, "unidade": "g", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": ["Mirtilos", "Kiwi"]},
            {"item": "Semente de chia", "qtd": 10, "unidade": "g", "categoria": "🌰 Castanhas, Sementes & Doces", "substitutos": ["Semente de linhaça", "Gergelim"]}
        ],
        "preparo": "1. Em um copo ou tigela, adicione o iogurte natural.\n2. Cubra com morangos picados, a granola e polvilhe a chia por cima."
    },
    "Vitamina de Banana": {
        "tipo": "Café da Manhã",
        "kcal": 310,
        "proteina": 22,
        "ingredientes": [
            {"item": "Leite desnatado", "qtd": 200, "unidade": "ml", "categoria": "🥛 Laticínios & Refrigerados", "substitutos": ["Leite de amêndoas", "Leite de aveia"]},
            {"item": "Banana nanica", "qtd": 1, "unidade": "unidade", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": ["Abacate (60g)", "Manga (100g)"]},
            {"item": "Whey protein ou proteína vegetal", "qtd": 20, "unidade": "g", "categoria": "💊 Suplementos & Produtos Especiais (Opcional)", "substitutos": ["Leite em pó desnatado (25g)"]},
            {"item": "Semente de linhaça", "qtd": 10, "unidade": "g", "categoria": "🌰 Castanhas, Sementes & Doces", "substitutos": ["Chia", "Semente de girassol"]}
        ],
        "preparo": "1. Adicione o leite, a banana, a proteína e a linhaça no liquidificador.\n2. Bata por 1 a 2 minutos até ficar cremoso e sirva em seguida."
    },

    # --- ALMOÇO ---
    "Tilápia Grelhada com Quinoa": {
        "tipo": "Almoço",
        "kcal": 480,
        "proteina": 38,
        "ingredientes": [
            {"item": "Filé de tilápia", "qtd": 150, "unidade": "g", "categoria": "🥩 Açougue, Peixaria & Frios", "substitutos": ["Filé de salmão", "Ovos cozidos (3 un)"]},
            {"item": "Quinoa em grãos crua", "qtd": 40, "unidade": "g", "categoria": "🌾 Mercearia Seca (Grãos, Massas & Farinhas)", "substitutos": ["Arroz integral (50g cru)", "Cuscuz marroquino (40g)"]},
            {"item": "Salada folhosa (Alface/Rúcula)", "qtd": 100, "unidade": "g", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": ["Agrião", "Espinafre"]},
            {"item": "Azeite de oliva extra virgem", "qtd": 10, "unidade": "ml", "categoria": "🫒 Condimentos, Óleos & Enlatados", "substitutos": ["Óleo de abacate", "Azeitonas verde (30g)"]}
        ],
        "preparo": "1. Lave a quinoa e cozinhe com o dobro de água por 15 min com sal.\n2. Tempere o peixe com limão e sal, grelhando em frigideira quente com azeite.\n3. Sirva o peixe acompanhado da quinoa e salada temperada."
    },
    "Bowl de Quinoa": {
        "tipo": "Almoço",
        "kcal": 450,
        "proteina": 22,
        "ingredientes": [
            {"item": "Quinoa em grãos crua", "qtd": 60, "unidade": "g", "categoria": "🌾 Mercearia Seca (Grãos, Massas & Farinhas)", "substitutos": ["Grão-de-bico cozido (150g)"]},
            {"item": "Brócolis ninja", "qtd": 100, "unidade": "g", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": ["Couve-flor", "Vagem fresca"]},
            {"item": "Cenoura", "qtd": 80, "unidade": "g", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": ["Beterraba ralada", "Abobrinha"]},
            {"item": "Azeite de oliva extra virgem", "qtd": 15, "unidade": "ml", "categoria": "🫒 Condimentos, Óleos & Enlatados", "substitutos": ["Óleo de gergelim"]}
        ],
        "preparo": "1. Cozinhe a quinoa em 120ml de água por 15 minutos.\n2. Cozinhe os legumes no vapor até ficarem 'al dente'.\n3. Monte o bowl misturando a quinoa, os vegetais e regando com azeite."
    },
    "Salada Grão de Bico": {
        "tipo": "Almoço",
        "kcal": 430,
        "proteina": 20,
        "ingredientes": [
            {"item": "Grão-de-bico seco", "qtd": 60, "unidade": "g", "categoria": "🌾 Mercearia Seca (Grãos, Massas & Farinhas)", "substitutos": ["Feijão fradinho (60g cru)", "Lentilha (60g crua)"]},
            {"item": "Tomate italiano", "qtd": 80, "unidade": "g", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": ["Pimentão amarelo", "Pepino japonês"]},
            {"item": "Cebola roxa", "qtd": 30, "unidade": "g", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": ["Cebolinha fresca", "Salsa"]},
            {"item": "Azeitona preta", "qtd": 20, "unidade": "g", "categoria": "🫒 Condimentos, Óleos & Enlatados", "substitutos": ["Azeite de oliva (10ml)"]}
        ],
        "preparo": "1. Cozinhe o grão-de-bico na pressão por 20 min (após de molho).\n2. Pique o tomate e a cebola roxa em cubos pequenos.\n3. Misture tudo com as azeitonas e tempere com sal, limão e azeite."
    },

    # --- LANCHE DA TARDE ---
    "Iogurte com Chia e Castanhas": {
        "tipo": "Lanche da Tarde",
        "kcal": 250,
        "proteina": 14,
        "ingredientes": [
            {"item": "Iogurte natural desnatado", "qtd": 170, "unidade": "g", "categoria": "🥛 Laticínios & Refrigerados", "substitutos": ["Iogurte de proteína zero lactose"]},
            {"item": "Semente de chia", "qtd": 10, "unidade": "g", "categoria": "🌰 Castanhas, Sementes & Doces", "substitutos": ["Semente de abóbora"]},
            {"item": "Castanha-de-caju sem sal", "qtd": 15, "unidade": "g", "categoria": "🌰 Castanhas, Sementes & Doces", "substitutos": ["Nozes (15g)", "Amêndoas (15g)"]}
        ],
        "preparo": "1. Adicione o iogurte em uma tigela.\n2. Misture a chia e decore com as castanhas-de-caju picadas."
    },
    "Mix de Castanhas": {
        "tipo": "Lanche da Tarde",
        "kcal": 210,
        "proteina": 8,
        "ingredientes": [
            {"item": "Castanha-do-pará", "qtd": 10, "unidade": "g", "categoria": "🌰 Castanhas, Sementes & Doces", "substitutos": ["Nozes"]},
            {"item": "Amêndoas torradas", "qtd": 15, "unidade": "g", "categoria": "🌰 Castanhas, Sementes & Doces", "substitutos": ["Avelãs"]},
            {"item": "Uva passa escura", "qtd": 15, "unidade": "g", "categoria": "🌰 Castanhas, Sementes & Doces", "substitutos": ["Cranberry desidratado"]}
        ],
        "preparo": "1. Junte todos os ingredientes em um pote e consuma diretamente."
    },

    # --- JANTAR ---
    "Sopa de Lentilha e Cogumelos": {
        "tipo": "Jantar",
        "kcal": 380,
        "proteina": 22,
        "ingredientes": [
            {"item": "Lentilha crua", "qtd": 60, "unidade": "g", "categoria": "🌾 Mercearia Seca (Grãos, Massas & Farinhas)", "substitutos": ["Ervilha seca (60g)", "Feijão azuki (60g)"]},
            {"item": "Cogumelo Paris fresco", "qtd": 100, "unidade": "g", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": ["Cogumelo Shimeji", "Shitake"]},
            {"item": "Abóbora cabotiá", "qtd": 100, "unidade": "g", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": ["Cenoura em cubos", "Chuchu"]},
            {"item": "Alho picado", "qtd": 5, "unidade": "g", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": ["Alho em pó"]}
        ],
        "preparo": "1. Deixe a lentilha de molho. Refogue o alho em azeite com os cogumelos.\n2. Adicione a lentilha, a abóbora e 400ml de água fervente.\n3. Cozinhe por 20 minutos até que a lentilha e abóbora fiquem bem macias."
    },
    "Omelete de Espinafre": {
        "tipo": "Jantar",
        "kcal": 310,
        "proteina": 21,
        "ingredientes": [
            {"item": "Ovo de galinha", "qtd": 3, "unidade": "unidades", "categoria": "🥩 Açougue, Peixaria & Frios", "substitutos": ["Claras de ovo (150ml) + 1 ovo"]},
            {"item": "Espinafre fresco", "qtd": 80, "unidade": "g", "categoria": "🥦 Hortifrúti (Horta, Pomar & Ervas)", "substitutos": ["Couve manteiga picada", "Rúcula"]},
            {"item": "Queijo cottage ou ricota", "qtd": 30, "unidade": "g", "categoria": "🥛 Laticínios & Refrigerados", "substitutos": ["Queijo minas frescal (30g)", "Tofu (30g)"]}
        ],
        "preparo": "1. Refogue o espinafre na frigideira até murchar.\n2. Batas os ovos, adicione o queijo e despeje sobre o espinafre.\n3. Vire para dourar ambos os lados."
    }
}
