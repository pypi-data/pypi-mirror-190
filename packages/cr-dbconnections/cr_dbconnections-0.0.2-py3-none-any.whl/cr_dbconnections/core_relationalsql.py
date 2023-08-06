import sqlalchemy as db
from sqlalchemy.orm import sessionmaker


class CoreRelationalSql():
    """
    :Nome da classe/função: SqlAlchemy
    :descrição: Classe para realizar conexão com bancos de dados utilizando o SqlAlchemy
    :Criação: Henrique Ortiz 04/03/2022
    """

    def __init__(self, user, senha, host, porta, database, driver=['oracle', 'postgresql', 'sqlserver']):
        self.user = user
        self.senha = senha
        self.host = host
        self.porta = porta
        self.database = database
        self.drivers = {
            'oracle': 'oracle+cx_oracle',
            'postgresql': 'postgresql+psycopg2',
            'sqlserver': 'mssql+pymssql',
        }
        self.driver = self.drivers[driver]
        self.engine = None
        self.conexao = None
        self.metadata = None
        self.session = None
        self.resultset = None
 
        self.conectar()
 
    def conectar(self):
        if self.driver == 'oracle+cx_oracle':
            database_url = f'{self.driver}://{self.user}:{self.senha}@{self.host}:{self.porta}/?service_name={self.database}'
            print(database_url)
        else:
            database_url = f'{self.driver}://{self.user}:{self.senha}@{self.host}:{self.porta}/{self.database}'
        self.engine = db.create_engine(database_url)
        self.conexao = self.engine.connect().execution_options(stream_results=True)
        self.cria_sessao()
 
    def cria_sessao(self):
        self.session = sessionmaker(bind=self.engine)()
 
    def get_conexao(self):
        return self.conexao