from tools.database import Base, engine
from decouple import config


RECREATE_DATABASE =  config('RECREATE_DATABASE')

if RECREATE_DATABASE != 'False':
    print('Log: Droping and Creating tables based in Models')
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine) 