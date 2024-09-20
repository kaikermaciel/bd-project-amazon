import psycopg2

# Função para conectar ao banco de dados
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="1234",
            host="localhost",  # ou o host do banco de dados
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# (a) Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 com menor avaliação
def list_most_useful_comments(cur, asin_produto):
    query = '''
        SELECT id, date_comment, customer_id, rating_comment, votes_comment, helpful_comment, id_asin
        FROM Comentario
        WHERE id_asin = %s
        ORDER BY helpful_comment DESC, rating_comment DESC
        LIMIT 5;
    '''
    cur.execute(query, (asin_produto,))
    resultados = cur.fetchall()

    for resultado in resultados:
        id_comentario = resultado[0]
        data_comentario = resultado[1]
        usuario = resultado[2]
        nota = resultado[3]
        votos = resultado[4]
        uteis = resultado[5]
        asin_produto = resultado[6]

        mensagem = f"Comentário {id_comentario} feito por {usuario} em {data_comentario}: Nota {nota}, {votos} votos, {uteis} votos úteis no produto {asin_produto}."
        print(mensagem)

def list_similar_product_with_more_sales(cur, asin):
    query = '''
        SELECT p_sim.asin_similar_book, p.title, p.salesrank
        FROM Similar_book_by_origin p_sim
        JOIN Produto p ON p_sim.asin_similar_book = p.asin
        WHERE p_sim.origin_asin = %s AND p.salesrank < (
            SELECT salesrank FROM Produto WHERE asin = %s
        )
        ORDER BY p.salesrank ASC;
    '''
    cur.execute(query, (asin, asin))
    resultados = cur.fetchall()

    for resultado in resultados:
        asin_similar = resultado[0]
        titulo_produto = resultado[1]
        ranking_vendas = resultado[2]

        mensagem = f"O produto similar {titulo_produto} (ASIN: {asin_similar}) tem um ranking de vendas de {ranking_vendas}."
        print(mensagem)

# (c) Dado um produto, mostrar a evolução diária das médias de avaliação
def daily_review_average(cur, asin_produto):
    query = '''
        SELECT date_comment, AVG(rating_comment) AS media_avaliacao
        FROM Comentario
        WHERE id_asin = %s
        GROUP BY date_comment
        ORDER BY date_comment ASC;
    '''
    cur.execute(query, (asin_produto))
    resultados = cur.fetchall()

    for resultado in resultados:
        data_comentario = resultado[0]
        media_avaliacao = round(resultado[1], 2)

        mensagem = f"Em {data_comentario}, a média de avaliações foi {media_avaliacao:.2f}."
        print(mensagem)


# (d) Listar os 10 produtos líderes de venda em cada grupo de produtos
def leader_by_group(cur):
    query = '''
        SELECT p.asin, p.title, p."group", p.salesrank
        FROM Produto p
        WHERE p.salesrank IS NOT NULL
        ORDER BY p."group", p.salesrank ASC
        LIMIT 10;
    '''
    cur.execute(query)
    resultados = cur.fetchall()

    for resultado in resultados:
        asin_produto = resultado[0]
        titulo_produto = resultado[1]
        grupo_produto = resultado[2]
        ranking_vendas = resultado[3]

        mensagem = f"O produto {titulo_produto} (ASIN: {asin_produto}) lidera vendas no grupo {grupo_produto} com ranking {ranking_vendas}."
        print(mensagem)

# (e) Listar os 10 produtos com a maior média de avaliações úteis positivas
def higher_helpful_review_average(cur):
    query = '''
        SELECT p.asin, p.title, AVG(c.helpful_comment) AS media_uteis
        FROM Produto p
        JOIN Comentario c ON p.asin = c.id_asin
        GROUP BY p.asin, p.title
        ORDER BY media_uteis DESC
        LIMIT 10;
    '''
    cur.execute(query)
    resultados = cur.fetchall()

    for resultado in resultados:
        asin_produto = resultado[0]
        titulo_produto = resultado[1]
        media_uteis = round(resultado[2], 2)

        mensagem = f"O produto {titulo_produto} (ASIN: {asin_produto}) tem uma média de {media_uteis:.2f} avaliações úteis."
        print(mensagem)

# (f) Listar as 5 categorias de produto com a maior média de avaliações úteis
def category_highest_helpful_review_average(cur):
    query = '''
        SELECT c.category_name, AVG(co.helpful_comment) AS media_uteis
        FROM Categoria c
        JOIN Subcategoria sc ON c.category_id = sc.category_associated_id
        JOIN categories_book_by_origin cbo ON sc.category_associated_id = cbo.category_associated
        JOIN Comentario co ON cbo.origin_asin = co.id_asin
        GROUP BY c.category_name
        ORDER BY media_uteis DESC
        LIMIT 5;
    '''
    cur.execute(query)
    resultados = cur.fetchall()

    for resultado in resultados:
        nome_categoria = resultado[0]
        media_uteis = round(resultado[1], 2)

        mensagem = f"A categoria {nome_categoria} tem uma média de {media_uteis:.2f} avaliações úteis por produto."
        print(mensagem)

# (g) Listar os 10 clientes que mais comentaram por grupo de produto
def client_with_most_comments_byGroup(cur):
    query = '''
        SELECT c.customer_id, COUNT(c.id) as num_comentarios, p."group"
        FROM Comentario c
        JOIN Produto p ON c.id_asin = p.asin
        GROUP BY c.customer_id, p."group"
        ORDER BY num_comentarios DESC
        LIMIT 10;
    '''
    cur.execute(query)
    resultados = cur.fetchall()

    for resultado in resultados:
        usuario = resultado[0]
        num_comentarios = resultado[1]
        grupo_produto = resultado[2]

        mensagem = f"Esse usuário {usuario} comentou {num_comentarios} vezes no grupo {grupo_produto}."
        print(mensagem)


def main():
    
    while True:
        print("\nSelecione uma opção para realizar uma consulta no dashboard:")
        print("[A] Listar os 5 comentários mais úteis e com maior/minor avaliação")
        print("[B] Listar produtos similares com maiores vendas")
        print("[C] Mostrar a evolução diária das médias de avaliação")
        print("[D] Listar os 10 produtos líderes de venda em cada grupo de produtos")
        print("[E] Listar os 10 produtos com a maior média de avaliações úteis positivas")
        print("[F] Listar as 5 categorias com a maior média de avaliações úteis por produto")
        print("[G] Listar os 10 clientes que mais fizeram comentários por grupo de produto")
        print("[S] Sair")

        # Recebe a escolha do usuário
        opcao = input("\nDigite a letra correspondente à consulta que deseja realizar: ").lower()
        conn = connect_to_db()
        cur = conn.cursor()
            
        if opcao == 'a':
            id_produto = input("Digite o ASIN do produto: ")
            list_most_useful_comments(cur, id_produto)
        
        elif opcao == 'b':
            id_produto = input("Digite o ASIN do produto: ")
            list_similar_product_with_more_sales(cur,id_produto)
        
        elif opcao == 'c':
            id_produto = input("Digite o ASIN do produto: ")
            daily_review_average(cur,id_produto)
        
        elif opcao == 'd':
            leader_by_group(cur)
        
        elif opcao == 'e':
            higher_helpful_review_average(cur)
        
        elif opcao == 'f':
            category_highest_helpful_review_average(cur)
        
        elif opcao == 'g':
            client_with_most_comments_byGroup(cur)
        
        elif opcao == 's':
            print("Saindo do dashboard.")
            break
        
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
