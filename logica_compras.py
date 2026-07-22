from dados_receitas import RECEITAS_DB, CATEGORIAS_COMPRAS

def consolidar_lista_compras(refeicoes_aprovadas):
    """
    Soma as quantidades dos ingredientes de todas as refeições aprovadas no check-in.
    Retorna um dicionário organizado pelas 8 categorias de compras.
    """
    lista_consolidada = {cat: {} for cat in CATEGORIAS_COMPRAS}
    
    for refeicao_nome in refeicoes_aprovadas:
        # Busca a receita no nosso banco
        receita = RECEITAS_DB.get(refeicao_nome)
        if not receita:
            continue
            
        for ing in receita["ingredientes"]:
            nome = ing["item"]
            qtd = ing["qtd"]
            unidade = ing["unidade"]
            categoria = ing["categoria"]
            substitutos = ing.get("substitutos", [])
            
            # Garante que a categoria existe no dicionário
            if categoria not in lista_consolidada:
                lista_consolidada[categoria] = {}
                
            chave_ingrediente = (nome, unidade)
            
            if chave_ingrediente in lista_consolidada[categoria]:
                lista_consolidada[categoria][chave_ingrediente]["qtd"] += qtd
            else:
                lista_consolidada[categoria][chave_ingrediente] = {
                    "qtd": qtd,
                    "substitutos": substitutos
                }
                
    return lista_consolidada

def buscar_opcoes_troca(refeicao_atual_nome):
    """
    Procura no banco de dados 2 opções de receitas do mesmo tipo com macros parecidos.
    """
    receita_atual = RECEITAS_DB.get(refeicao_atual_nome)
    if not receita_atual:
        return []
        
    tipo = receita_atual["tipo"]
    opcoes = []
    
    for nome, dados in RECEITAS_DB.items():
        if nome != refeicao_atual_nome and dados["tipo"] == tipo:
            opcoes.append({
                "nome": nome,
                "kcal": dados["kcal"],
                "proteina": dados["proteina"]
            })
            if len(opcoes) == 2:
                break
                
    return opcoes

def gerar_texto_google_keep(lista_consolidada):
    """
    Gera o texto formatado com marcadores [ ] prontos para colar no Google Keep.
    """
    texto = "🛒 MINHA LISTA DE COMPRAS - NUTRIIA\n\n"
    
    for categoria, itens in lista_consolidada.items():
        if itens:
            texto += f"--- {categoria} ---\n"
            for (nome, unidade), dados in itens.items():
                qtd = dados["qtd"]
                texto += f"[ ] {nome} - {qtd}{unidade}\n"
            texto += "\n"
            
    return texto
