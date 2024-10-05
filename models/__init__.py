from tools.database import Base, engine

print('Log: Creating tables by Models')
Base.metadata.create_all(bind=engine)