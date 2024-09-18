import psycopg2

class DBConnection:
    """ Superclasse para gerenciar a configuração da conexão com o banco """
    def __init__(self, host, database, user, password, port="5432"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

class Database(DBConnection):
    """ Classe para gerenciar a conexão e interação com o banco de dados """
    def __init__(self, host, database, user, password, port="5432"):
        super().__init__(host, database, user, password, port)
        self.connection = None
        self.cursor = None

    def connect(self):
        """ Método para conectar ao banco de dados """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Conexão com o banco de dados estabelecida com sucesso.")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def disconnect(self):
        """ Método para fechar a conexão com o banco de dados """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Conexão com o banco de dados encerrada.")

    def create_table(self):
        """ Método para criar a tabela de produtos no banco """
        try:
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS produtos (
                id SERIAL PRIMARY KEY,
                asin VARCHAR(255) NOT NULL,
                title VARCHAR(255) NOT NULL,
                group_name VARCHAR(255) NOT NULL,
                salesrank INT
            );
            '''
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Tabela 'produtos' criada com sucesso.")
        except Exception as e:
            print(f"Erro ao criar tabela: {e}")

    def insert_product(self, product):
        """ Método para inserir um produto no banco de dados """
        try:
            insert_query = '''
            INSERT INTO produtos (id, asin, title, group_name, salesrank)
            VALUES (%s, %s, %s, %s, %s);
            '''
            data = (product.id, product.asin, product.title, product.group, product.salesrank)
            self.cursor.execute(insert_query, data)
            self.connection.commit()
            print(f"Produto {product.title} inserido com sucesso.")
        except Exception as e:
            print(f"Erro ao inserir produto: {e}")
