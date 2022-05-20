import os

os.environ['USER'] = 'root'
os.environ['PASSWORD'] = 'fika'
os.environ['DB_NAME'] = 'ml'
os.environ['PORT'] = '30008'
os.environ['HOST'] = 'k8s-master.unic.kg.ac.rs'

user = os.environ['USER']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']
host = os.environ['HOST']
port = os.environ['PORT']

storage_path = "storage"