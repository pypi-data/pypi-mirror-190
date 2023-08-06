from cr_dbconnections.core_relationalsql import CoreRelationalSql
from dotenv import load_dotenv
import os
import yaml

class AdminLoja(CoreRelationalSql):
    
    def __init__(self):
        
        try:
            with open('config.yaml', 'r') as f:
                db_connections = yaml.load(f.read(), Loader=yaml.Loader)
        except:
            raise 'Arquivo config.yaml não encontrado.'
        
        self.user = db_connections.get('loja')['user']
        self.senha = db_connections.get('loja')['pwd']
        self.host = db_connections.get('loja')['host']
        self.porta = db_connections.get('loja')['port']
        self.database = db_connections.get('loja')['db']
        self.driver = 'postgresql'
                
        super().__init__(
            user=self.user, 
            senha=self.senha, 
            host=self.host, 
            porta=self.porta, 
            database=self.database,
            driver=self.driver
        )
