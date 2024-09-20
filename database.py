import psycopg2

class DBConnection:
    def __init__(self, host, database, user, password, port="5432"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

class Database(DBConnection):
    def __init__(self, host, database, user, password, port="5432"):
        super().__init__(host, database, user, password, port)
        self.connection = None
        self.cursor = None

    def connect(self):
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
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Conexão com o banco de dados encerrada.")

    def create_table(self):
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
