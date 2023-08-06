from cr_dbconnections.core_mongo import CoreMongo
from dotenv import load_dotenv
import os
import yaml

class MongoCr(CoreMongo):
    
    def __init__(self):
        
        try:
            with open('config.yaml', 'r') as f:
                db_connections = yaml.load(f.read(), Loader=yaml.Loader)
        except:
            raise 'Arquivo config.yaml não encontrado.'
        
        self.user = db_connections.get('receita_digital')['user']
        self.password = db_connections.get('receita_digital')['pwd']
        self.cluster = db_connections.get('receita_digital')['cluster']
        self.auth_db = db_connections.get('receita_digital')['auth_db']
        self.database = db_connections.get('receita_digital')['db']
        self.options = db_connections.get('receita_digital')['options']
        self.cert = db_connections.get('receita_digital')['cert']

        super().__init__(
            user=self.user, 
            senha=self.password, 
            cluster=self.cluster, 
            db=self.db, 
            auth_db=self.auth_db,
            options=self.options,
            cert=self.cert,
            ssl=False
        )
