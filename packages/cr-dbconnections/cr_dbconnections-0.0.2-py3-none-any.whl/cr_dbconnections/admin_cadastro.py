from cr_dbconnections.core_mongo import CoreMongo
from dotenv import load_dotenv
import os
import yaml

class MongoCr(CoreMongo):
    
    def __init__(self):
        load_dotenv('./Connections/.env')
        db_connections = yaml.load(os.getenv('db_connections'), Loader=yaml.Loader)
        
        self.user = db_connections['mongo_cr']['user']
        self.password = db_connections['mongo_cr']['pwd']
        self.cluster = db_connections['mongo_cr']['cluster']
        self.auth_db = db_connections['mongo_cr']['auth_db']
        self.database = db_connections['mongo_cr']['db']
        self.options = db_connections['mongo_cr']['options']
        self.cert = db_connections['mongo_cr']['cert']

        super().__init__(
            user=self.user, 
            senha=self.password, 
            cluster=self.cluster, 
            db=self.db, 
            auth_db=self.auth_db,
            options=self.options,
            cert=self.cert
        )
