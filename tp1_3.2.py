class Produto:
    def __init__(self):
        self.id = 0
        self.asin = ''
        self.group = ''
        self.salesrank = ''
        self.similar = []
        self.categories = []
        self.total_review = 0
        self.dowloaded_review = 0
        self.averageRating_review = 0
        self.date_comment = ''
        self.customer_id = ''
        self.rating_comment = 0
        self.votes_comment = 0
        self.helpful_comment = 0

    # Setters
    def set_id(self, id):
        self.id = id

    def set_asin(self, asin):
        self.asin = asin

    def set_group(self, group):
        self.group = group

    def set_salesrank(self, salesrank):
        self.salesrank = salesrank

    def add_similar(self, item):
        self.similar.append(item)

    def add_category(self, category):
        self.categories.append(category)

    def set_total_review(self, total_review):
        self.total_review = total_review

    def set_averageRating_review(self, averageRating_review):
        self.averageRating_review = averageRating_review

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

    # Método para imprimir o estado atual do produto
    def __str__(self):
        return (f"Produto ID: {self.id}\n"
                f"ASIN: {self.asin}\n"
                f"Grupo: {self.group}\n"
                f"Salesrank: {self.salesrank}\n"
                f"Similares: {', '.join(self.similar)}\n"
                f"Categorias: {', '.join(self.categories)}\n"
                f"Total de Reviews: {self.total_review}\n"
                f"Rating Médio: {self.averageRating_review}\n"
                f"Comentário - Data: {self.date_comment}, Cliente: {self.customer_id}, "
                f"Rating: {self.rating_comment}, Votos: {self.votes_comment}, "
                f"Ajudas: {self.helpful_comment}\n")

# Dicionário com identificadores
file_identifiers = {
    'Id:' : 'ID',
    'ASIN:' : 'ASIN',
    'group:' : 'GROUP',
    'salesrank:' : 'SALESRANK',
    'similar' : 'SIMILAR',
    'categories' : 'CATEGORIES',
    'reviews' : 'REVIEWS',
    'discontinued product' : 'CABOU'
}

# Função para transcrever arquivo
def file_transcribe(input_file):
    current_section = None  # Variável para armazenar o identificador atual
    products = []  # Lista para armazenar produtos
    current_product = None  # Armazena o produto atual

    with open(input_file) as file:
        for line in file:
            stripped_line = line.strip()

            if len(stripped_line) == 0:  # Se for uma linha em branco
                current_section = None
                continue

            for key in file_identifiers:
                if key in stripped_line:
                    current_section = file_identifiers[key]

                    # Quando encontrar um novo ID, cria um novo produto
                    if current_section == 'ID':
                        if current_product:
                            products.append(current_product)  # Armazena o produto anterior
                        current_product = Produto()  # Cria um novo produto
                        current_product.set_id(int(stripped_line.split(':')[1].strip()))

                    # Atribui os outros identificadores
                    elif current_section == 'ASIN':
                        current_product.set_asin(stripped_line.split(':')[1].strip())
                    elif current_section == 'GROUP':
                        current_product.set_group(stripped_line.split(':')[1].strip())
                    elif current_section == 'SALESRANK':
                        current_product.set_salesrank(int(stripped_line.split(':')[1].strip()))

                    # print(f"Identificador encontrado: {current_section}")
                    break

            # Processa conteúdo baseado no identificador atual
            if current_section == 'REVIEWS':
                # Exemplo: Pega total de reviews e rating médio
                parts = stripped_line.split()
                current_product.set_total_review(parts[2])
                current_product.set_averageRating_review(parts[4])
                print(f"Processando REVIEW: {stripped_line}")
            elif current_section == 'SIMILAR':
                # Adiciona similares à lista
                similar_items = stripped_line.split()[2:]  # Pega os similares a partir do índice 2
                for item in similar_items:
                    current_product.add_similar(item)
                # print(f"Processando SIMILAR: {similar_items}")
            elif current_section == 'CATEGORIES':
                # Processa categorias separadas por '|'
                categories = stripped_line.split('|')
                for category in categories:
                    current_product.add_category(category)
                # print(f"Processando CATEGORIES: {categories}")

            # Continua processando até encontrar uma linha em branco ou outro identificador
            if current_section and not any(k in stripped_line for k in file_identifiers):
                print(f"Conteúdo da seção {current_section}: {stripped_line}")

    # Certifique-se de adicionar o último produto processado
    if current_product:
        products.append(current_product)

    return products

# Teste da função
produtos = file_transcribe("teste.txt")

# Imprime o estado de cada produto após processamento
for produto in produtos:
    print(produto)
