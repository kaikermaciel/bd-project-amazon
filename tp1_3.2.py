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
        self.categories = []
        self.total_review = 0
        self.averageRating_review = 0
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

    def set_averageRating_review(self, averageRating_review):
        self.averageRating_review = averageRating_review

    # Método para imprimir o estado atual do produto
    def __str__(self):
        return (f"Produto ID: {self.id}\n"
                f"ASIN: {self.asin}\n"
                f"Title: {self.title}\n"
                f"Grupo: {self.group}\n"
                f"Salesrank: {self.salesrank}\n"
                f"Similares: {', '.join(self.similar)}\n"
                f"Categorias: {', '.join(self.categories)}\n"
                f"Total de Reviews: {self.total_review}\n"
                f"Rating Médio: {self.averageRating_review}\n"
                f"Comentários:\n" + '\n'.join([str(comment) for comment in self.comments])+'\n')

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


# Função para transcrever arquivo
def file_transcribe(input_file):
    current_section = None
    products = []
    current_product = None

    with open(input_file) as file:
        for line in file:
            stripped_line = line.strip()

            # Verifica se o produto foi descontinuado (CABOU)
            if 'discontinued product' in stripped_line:
                print(f"Produto descontinuado encontrado. Ignorando produto.")
                current_product = None  # Reseta o produto atual
                current_section = None  # Reseta a seção
                continue  # Pula para a próxima linha

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
                    elif current_section == 'TITLE':
                        current_product.set_title(stripped_line.split(':')[1].strip())
                    elif current_section == 'GROUP':
                        current_product.set_group(stripped_line.split(':')[1].strip())
                    elif current_section == 'SALESRANK':
                        current_product.set_salesrank(int(stripped_line.split(':')[1].strip()))

                    print(f"Identificador encontrado: {current_section}")
                    break

            # Processa conteúdo baseado no identificador atual
            if current_section == 'REVIEWS':
                # Exemplo: Pega total de reviews e rating médio
                parts = stripped_line.split()
                if current_product.total_review == 0:
                    current_product.set_total_review(int(parts[2]))  
                    current_product.set_averageRating_review(float(parts[7]))
                print(f"Processando REVIEW: {parts}")
            elif current_section == 'SIMILAR':
                # Adiciona similares à lista
                similar_items = stripped_line.split()[2:]  # Pega os similares a partir do índice 2
                for item in similar_items:
                    current_product.add_similar(item)
                print(f"Processando SIMILAR: {similar_items}")
            elif current_section == 'CATEGORIES':
                # Processa categorias separadas por '|'
                categories = stripped_line.split('|')[1:]
                for category in categories:
                    current_product.add_category(category)
                print(f"Processando CATEGORIES: {categories}")
            # Continua processando até encontrar uma linha em branco ou outro identificador
            if current_section and not any(k in stripped_line for k in file_identifiers):
                if current_section == 'REVIEWS':
                    # Criando e preenchendo uma instância de Comment
                    comment_parts = stripped_line.split()
                    new_comment = Comment()
                    new_comment.set_date_comment(comment_parts[0])
                    new_comment.set_customer_id(comment_parts[2])
                    new_comment.set_rating_comment(int(comment_parts[4]))
                    new_comment.set_votes_comment(int(comment_parts[6]))
                    new_comment.set_helpful_comment(int(comment_parts[8]))
                    
                    # Adiciona o comentário ao produto atual
                    current_product.add_comment(new_comment)
                    print(f"Comentário adicionado: {new_comment}")

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

