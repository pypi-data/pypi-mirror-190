from pymongo import MongoClient

class CoreMongo():
    """
    :Nome da classe/função: SqlAlchemy
    :descrição: Classe para realizar conexão com bancos de dados utilizando o SqlAlchemy
    :Criação: Henrique Ortiz 04/03/2022
    """

    def __init__(self, user, password, cluster, db, auth_db=None, options=None, ssl=True, cert=None, secondary=True):
        self.user = user
        self.password = password
        self.cluster = cluster
        self.auth_db = auth_db
        self.db = db
        self.resultset = None
        self.options = options
        self.ssl = ssl
        self.cert = cert
        self.secondary = secondary
        self.client = None
 
        self.conectar()
 
    def conectar(self):
        """
        Conexão a um banco MongoDB usando pymongo
        """
        if auth_db is None:
            auth_db = self.db
        CONNECTION_STRING = f"mongodb://{self.user}:{self.pwd}@{self.cluster}/{auth_db}?{self.options}"
        if self.ssl:
            if self.secondary:
                self.client = MongoClient(CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True,
                                    tlsCAFile=self.cert, readPreference='secondaryPreferred')
            else:
                self.client = MongoClient(CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True,
                                    tlsCAFile=self.cert)
        else:
            if self.secondary:
                self.client = MongoClient(CONNECTION_STRING, readPreference='secondaryPreferred')
            else:
                self.client = MongoClient(CONNECTION_STRING)