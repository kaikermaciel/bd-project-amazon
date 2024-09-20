
import time
import psycopg2
import re


# Dicionário com identificadores
file_identifiers = {
    'Id:' : 'ID',
    'ASIN:' : 'ASIN',
    'title' : 'TITLE',
    'group:' : 'GROUP',
    'salesrank:' : 'SALESRANK',
    'similar' : 'SIMILAR',
    'categories' : 'CATEGORIES',
    'reviews' : 'REVIEWS',
    'discontinued product' : 'CABOU'
}

class Produto:
    def __init__(self):
        self.id = 0
        self.asin = ''
        self.title = ''
        self.group = ''
        self.salesrank = ''
        self.similar = []
        self.categories = []  # Agora armazena instâncias de Category
        self.total_review = 0
        self.average_rating = 0
        self.comments = []  # Armazena instâncias da classe Comment

    # Setters
    def set_id(self, id):
        self.id = id

    def set_asin(self, asin):
        self.asin = asin

    def set_title(self, title):
        self.title = title

    def set_group(self, group):
        self.group = group

    def set_salesrank(self, salesrank):
        self.salesrank = salesrank

    def add_similar(self, item):
        self.similar.append(item)

    def add_category(self, category):
        self.categories.append(category)

    def add_comment(self, comment):
        self.comments.append(comment)

    def set_total_review(self, total_review):
        self.total_review = total_review

    def set_average_rating(self, average_rating):
        self.average_rating = average_rating

    # Método para imprimir o estado atual do produto
    def __str__(self):
        return (f"Produto ID: {self.id}\n"
                f"ASIN: {self.asin}\n"
                f"Title: {self.title}\n"
                f"Grupo: {self.group}\n"
                f"Salesrank: {self.salesrank}\n"
                f"Similares: {', '.join(self.similar)}\n"
                f"Categorias:\n" + '\n'.join([str(category) for category in self.categories]) + '\n'
                f"Total de Reviews: {self.total_review}\n"
                f"Rating Médio: {self.average_rating}\n"
                f"Comentários:\n" + '\n'.join([str(comment) for comment in self.comments]) + '\n')


class Category:
    def __init__(self):
        self.category_name = ''
        self.category_id = 0
        self.subcategories = []  # Armazena instâncias de Subcategory

    def set_category_name(self, category_name):
        self.category_name = category_name

    def set_category_id(self, category_id):
        self.category_id = category_id

    def add_subcategory(self, subcategory):
        self.subcategories.append(subcategory)

    def __str__(self):
        return (f"Categoria: {self.category_name} (ID: {self.category_id})\n"
                f"Subcategorias:\n" + '\n'.join([str(subcategory) for subcategory in self.subcategories]) + '\n')


class Subcategory:
    def __init__(self):
        self.subcategory_name = ''
        self.subcategory_id = 0
        self.category_id_associated = 0

    def set_subcategory_name(self, subcategory_name):
        self.subcategory_name = subcategory_name

    def set_subcategory_id(self, subcategory_id):
        self.subcategory_id = subcategory_id

    def set_category_id_associated(self, category_id_associated):
        self.category_id_associated = category_id_associated

    def __str__(self):
        return f"Subcategoria: {self.subcategory_name} (ID: {self.subcategory_id}) Category Associated: {self.category_id_associated}"


class Comment:
    def __init__(self):
        self.date_comment = ''
        self.customer_id = ''
        self.rating_comment = 0
        self.votes_comment = 0
        self.helpful_comment = 0

    def set_date_comment(self, date_comment):
        self.date_comment = date_comment

    def set_customer_id(self, customer_id):
        self.customer_id = customer_id

    def set_rating_comment(self, rating_comment):
        self.rating_comment = rating_comment

    def set_votes_comment(self, votes_comment):
        self.votes_comment = votes_comment

    def set_helpful_comment(self, helpful_comment):
        self.helpful_comment = helpful_comment

    def __str__(self) -> str:
        return (f'Data: {self.date_comment}, '
                f'Cliente: {self.customer_id}, '
                f'Rating: {self.rating_comment}, '
                f'Votos: {self.votes_comment}, '
                f'Ajudas: {self.helpful_comment}')



# Função atualizada para transcrição do arquivo e verificação de subcategorias
def file_transcribe_with_regex(input_file):
    # Regex patterns
    patterns = {
        'ID': re.compile(r'Id:\s*(\d+)'),
        'ASIN': re.compile(r'ASIN:\s*(\w+)'),
        'TITLE': re.compile(r'title:\s*(.+)'),
        'GROUP': re.compile(r'group:\s*(\w+)'),
        'SALESRANK': re.compile(r'salesrank:\s*(\d+)'),
        'SIMILAR': re.compile(r'similar:\s*(\d+)\s*(.+)'),
        'CATEGORY': re.compile(r'(.+)\[(\d+)\]'),  # Categoria[ID]
        'REVIEWS': re.compile(r'reviews:\s*total:\s*(\d+)\s*downloaded:\s*(\d+)\s*avg rating:\s*(\d+\.\d+)'),
        'COMMENT': re.compile(r'(\d{4}-\d{1,2}-\d{1,2})\s+cutomer:\s+(\w+)\s+rating:\s+(\d+)\s+votes:\s+(\d+)\s+helpful:\s+(\d+)')
    }

    current_product = None
    products = []
    current_category = None  # Para armazenar a categoria principal temporariamente

    with open(input_file, 'r') as file:
        for line in file:
            stripped_line = line.strip()

            # Ignora produto descontinuado
            if 'discontinued product' in stripped_line:
                # print("Produto descontinuado encontrado. Ignorando produto.")
                current_product = None
                current_category = None
                continue

            # Verifica por ID
            match_id = patterns['ID'].search(stripped_line)
            if match_id:
                if current_product:
                    products.append(current_product)
                current_product = Produto()
                current_category = None  # Reseta a categoria atual ao encontrar um novo produto
                current_product.set_id(int(match_id.group(1)))
                # print(f"ID encontrado: {match_id.group(1)}")
                continue

            # Verifica por ASIN
            match_asin = patterns['ASIN'].search(stripped_line)
            if match_asin:
                current_product.set_asin(match_asin.group(1))
                # print(f"ASIN encontrado: {match_asin.group(1)}")
                continue

            # Verifica por TITLE
            match_title = patterns['TITLE'].search(stripped_line)
            if match_title:
                current_product.set_title(match_title.group(1))
                # print(f"Title encontrado: {match_title.group(1)}")
                continue

            # Verifica por GROUP
            match_group = patterns['GROUP'].search(stripped_line)
            if match_group:
                current_product.set_group(match_group.group(1))
                # print(f"Group encontrado: {match_group.group(1)}")
                continue

            # Verifica por SALESRANK
            match_salesrank = patterns['SALESRANK'].search(stripped_line)
            if match_salesrank:
                current_product.set_salesrank(int(match_salesrank.group(1)))
                # print(f"Salesrank encontrado: {match_salesrank.group(1)}")
                continue

            # Verifica por SIMILAR
            match_similar = patterns['SIMILAR'].search(stripped_line)
            if match_similar:
                similar_items = match_similar.group(2).split()
                for item in similar_items:
                    current_product.add_similar(item)
                # print(f"Similar encontrado: {similar_items}")
                continue

            # Verifica por CATEGORIES e SUBCATEGORIES
            if '|' in stripped_line:
                categories = stripped_line.split('|')[1:]  # Remove o primeiro elemento
                for index, category_str in enumerate(categories):
                    match_category = patterns['CATEGORY'].search(category_str)
                    if match_category:
                        category_name = match_category.group(1).strip()
                        category_id = int(match_category.group(2))

                        if index == 0:  # Primeiro item é a categoria principal
                            new_category = Category()
                            new_category.set_category_name(category_name)
                            new_category.set_category_id(category_id)
                            current_product.add_category(new_category)
                            current_category = new_category  # Define como a categoria atual
                            # print(f"Categoria adicionada: {category_name}")
                        else:  # Os itens subsequentes são subcategorias
                            if current_category is not None:  # Verifica se existe uma categoria principal
                                new_subcategory = Subcategory()
                                new_subcategory.set_subcategory_name(category_name)
                                new_subcategory.set_subcategory_id(category_id)
                                new_subcategory.set_category_id_associated(current_category.category_id)
                                current_category.add_subcategory(new_subcategory)
                                # print(f"Subcategoria adicionada: {category_name} à categoria {current_category.category_name}")
                            # else:
                            #     print(f"Erro: Tentando adicionar subcategoria '{category_name}', mas não há categoria principal.")
                        continue

            # Verifica por REVIEWS
            match_reviews = patterns['REVIEWS'].search(stripped_line)
            if match_reviews:
                total_reviews = int(match_reviews.group(1))
                downloaded_reviews = int(match_reviews.group(2))
                average_rating = float(match_reviews.group(3))
                current_product.set_total_review(total_reviews)
                current_product.set_average_rating(average_rating)
                # print(f"Reviews: Total - {total_reviews}, Média - {average_rating}")
                continue
            
            # Verifica por Comentários dentro das Reviews
            match_comment = patterns['COMMENT'].search(stripped_line)
            if match_comment:
                date_comment = match_comment.group(1)
                customer_id = match_comment.group(2)
                rating_comment = int(match_comment.group(3))
                votes_comment = int(match_comment.group(4))
                helpful_comment = int(match_comment.group(5))

                # Cria uma nova instância de Comment
                new_comment = Comment()
                new_comment.set_date_comment(date_comment)
                new_comment.set_customer_id(customer_id)
                new_comment.set_rating_comment(rating_comment)
                new_comment.set_votes_comment(votes_comment)
                new_comment.set_helpful_comment(helpful_comment)

                # Adiciona o comentário ao produto atual
                current_product.add_comment(new_comment)
                # print(f"Comentário adicionado: {new_comment}")
                continue

        # Adiciona o último produto ao array
        if current_product:
            products.append(current_product)

    return products



# Função para criar as tabelas no banco de dados
def create_tables(conn):
    with conn.cursor() as cur:
        # Criação da tabela Produto
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Produto (
            asin VARCHAR(120) PRIMARY KEY,
            title TEXT,
            "group" TEXT,
            salesrank INTEGER,
            review INTEGER,
            media_avaliacao FLOAT
        );
        ''')

        # Criação da tabela Categoria
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Categoria (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT UNIQUE
        );
        ''')

        # Criação da tabela Subcategoria
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Subcategoria (
            subcategory_id INTEGER PRIMARY KEY,
            subcategory_name TEXT,
            category_associated_id INTEGER REFERENCES Categoria(category_id),
            UNIQUE(subcategory_name, category_associated_id)
        );
        ''')

        # Criação da tabela Comentario
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Comentario (
            id SERIAL PRIMARY KEY,
            date_comment DATE,
            customer_id VARCHAR(120),
            rating_comment INTEGER,
            votes_comment INTEGER,
            helpful_comment INTEGER,
            id_asin VARCHAR(120) REFERENCES Produto(asin)
        );
        ''')

        # Criação da tabela Similar_book_by_origin (Produtos Similares)
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Similar_book_by_origin (
            origin_asin VARCHAR(120) REFERENCES Produto(asin),
            asin_similar_book VARCHAR(120) NOT NULL,
            PRIMARY KEY (origin_asin, asin_similar_book)
        );
        ''')

        # Criação da tabela categories_book_by_origin (Associação de Categorias com Produtos)
        cur.execute('''
        CREATE TABLE IF NOT EXISTS categories_book_by_origin (
            origin_asin VARCHAR(120) REFERENCES Produto(asin),
            category_associated INTEGER REFERENCES Categoria(category_id),
            PRIMARY KEY (origin_asin, category_associated)
        );
        ''')

        # Comitando as alterações
        conn.commit()

# Função para inserir os produtos e categorias no banco de dados
def insert_data(conn, products):
    with conn.cursor() as cur:
        for product in products:
            # Verifica se o salesrank é válido (inteiro), caso contrário insere NULL
            salesrank = product.salesrank if isinstance(product.salesrank, int) else None
            
            # Insere o produto
            cur.execute('''
            INSERT INTO Produto (asin, title, "group", salesrank, review, media_avaliacao)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING asin;
            ''', (product.asin, product.title, product.group, salesrank, product.total_review, product.average_rating))

            produto_asin = cur.fetchone()[0]
            
            # Insere categorias e subcategorias e associa com o produto
            for category in product.categories:
                # Insere a categoria, garantindo que não haja duplicatas
                cur.execute('''
                INSERT INTO Categoria (category_id, category_name)
                VALUES (%s, %s) ON CONFLICT (category_name) DO NOTHING RETURNING category_id;
                ''', (category.category_id, category.category_name))
                category_id = cur.fetchone()
                
                if category_id is None:
                    cur.execute('SELECT category_id FROM Categoria WHERE category_name = %s;', (category.category_name,))
                    category_id = cur.fetchone()[0]
                else:
                    category_id = category_id[0]

                # Insere na tabela categories_book_by_origin
                cur.execute('''
                INSERT INTO categories_book_by_origin (origin_asin, category_associated)
                VALUES (%s, %s) ON CONFLICT DO NOTHING;
                ''', (produto_asin, category_id))

                # Insere subcategorias e associa com a categoria
                for subcategory in category.subcategories:
                    # Verifica se a subcategoria já existe para essa categoria associada
                    cur.execute('''
                    SELECT subcategory_id FROM Subcategoria
                    WHERE subcategory_name = %s AND category_associated_id = %s;
                    ''', (subcategory.subcategory_name, category_id))
                    existing_subcategory = cur.fetchone()

                    if not existing_subcategory:
                        # Insere a subcategoria se ela não existir
                        cur.execute('''
                        INSERT INTO Subcategoria (subcategory_id, subcategory_name, category_associated_id)
                        VALUES (%s, %s, %s) ON CONFLICT (subcategory_id) DO NOTHING RETURNING subcategory_id;
                        ''', (subcategory.subcategory_id, subcategory.subcategory_name, category_id))

                    subcategory_id = subcategory.subcategory_id  # Se ela já existir, usa o ID existente
                            
            # Insere produtos similares e associa com o produto
            for similar_asin in product.similar:
                # Insere na tabela Similar_book_by_origin
                cur.execute('''
                INSERT INTO Similar_book_by_origin (origin_asin, asin_similar_book)
                VALUES (%s, %s) ON CONFLICT DO NOTHING;
                ''', (produto_asin, similar_asin))
            
            # Insere comentários
            for comment in product.comments:
                cur.execute('''
                INSERT INTO Comentario (date_comment, customer_id, rating_comment, votes_comment, helpful_comment, id_asin)
                VALUES (%s, %s, %s, %s, %s, %s);
                ''', (comment.date_comment, comment.customer_id, comment.rating_comment, comment.votes_comment, comment.helpful_comment, produto_asin))

        conn.commit()

# Função para excluir todas as tabelas
def drop_tables(conn):
    with conn.cursor() as cur:
        cur.execute('''
        DROP TABLE IF EXISTS Comentario, Subcategoria, Categoria, 
                            Similar_book_by_origin, categories_book_by_origin, Produto CASCADE;
        ''')
        conn.commit()

# Função principal para executar o código
def main():
    # Conectando ao banco de dados e executando as operações
    try:
        # Conexão com o banco de dados
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="1234",
            host="localhost",  # ou o host do banco de dados
            port="5432"
        )

        # Excluir as tabelas
        drop_tables(conn)

        # Cria as tabelas (caso ainda não existam)
        create_tables(conn)

        # Insere os dados dos produtos processados
        start_time = time.time()
        
        produtos = file_transcribe_with_regex("teste.txt")
        print("\n================== Inserindo Dados, Aguarde! ==================\n")
        insert_data(conn, produtos)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print("\n\n================== Dados Inseridos com Sucesso! ==================\n\n")
        print(f"Tempo total para inserção de dados: {elapsed_time:.2f} segundos.")

        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
