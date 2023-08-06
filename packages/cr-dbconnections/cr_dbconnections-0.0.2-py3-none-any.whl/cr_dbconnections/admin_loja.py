from cr_dbconnections.core_relationalsql import CoreRelationalSql
from dotenv import load_dotenv
import os
import yaml

class AdminLoja(CoreRelationalSql):
    
    def __init__(self):
        
        load_dotenv('./Connections/.env')
        db_connections = yaml.load(os.getenv('db_connections'), Loader=yaml.Loader)
        
        self.user = db_connections['loja']['user']
        self.senha = db_connections['loja']['pwd']
        self.host = db_connections['loja']['host']
        self.porta = db_connections['loja']['port']
        self.database = db_connections['loja']['db']
        self.driver = 'postgresql'
                
        super().__init__(
            user=self.user, 
            senha=self.senha, 
            host=self.host, 
            porta=self.porta, 
            database=self.database,
            driver=self.driver
        )
