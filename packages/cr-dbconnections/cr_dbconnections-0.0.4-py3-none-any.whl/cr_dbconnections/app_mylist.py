from cr_dbconnections.core_relationalsql import CoreRelationalSql
from dotenv import load_dotenv
import os
import yaml

class App(CoreRelationalSql):
    
    def __init__(self):
        
        try:
            with open('config.yaml', 'r') as f:
                db_connections = yaml.load(f.read(), Loader=yaml.Loader)
        except:
            raise 'Arquivo config.yaml não encontrado.'
        
        self.user = db_connections.get('app_conn')['user']
        self.senha = db_connections.get('app_conn')['pwd']
        self.host = db_connections.get('app_conn')['host']
        self.porta = db_connections.get('app_conn')['port']
        self.database = db_connections.get('app_conn')['db']
        self.driver = 'postgresql'
                
        super().__init__(
            user=self.user, 
            senha=self.senha, 
            host=self.host, 
            porta=self.porta, 
            database=self.database,
            driver=self.driver
        )
