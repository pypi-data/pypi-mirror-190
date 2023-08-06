from cr_dbconnections.core_relationalsql import CoreRelationalSql
from dotenv import load_dotenv
import os
import yaml

class Datawarehouse(CoreRelationalSql):
    
    def __init__(self):
        
        load_dotenv('./Connections/.env')
        db_connections = yaml.load(os.getenv('db_connections'), Loader=yaml.Loader)
        
        self.user = db_connections['dw_conn']['user']
        self.senha = db_connections['dw_conn']['pwd']
        self.host = db_connections['dw_conn']['host']
        self.porta = db_connections['dw_conn']['port']
        self.database = db_connections['dw_conn']['db']
        self.driver = 'postgresql'
                
        super().__init__(
            user=self.user, 
            senha=self.senha, 
            host=self.host, 
            porta=self.porta, 
            database=self.database,
            driver=self.driver
        )
