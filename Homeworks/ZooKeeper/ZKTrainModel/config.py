import os

os.environ['USER'] = 'root'
os.environ['PASSWORD'] = 'fika'
os.environ['DB_NAME'] = 'ml'
os.environ['PORT'] = '10000'
os.environ['HOST'] = 'localhost'

user = os.environ['USER']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']
host = os.environ['HOST']
port = os.environ['PORT']

storage_path = "storage"
datasets_path = "datasets"