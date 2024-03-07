 
from sqlalchemy import create_engine
import config

 
engine = create_engine(f'postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOSTNAME}/{config.DB_NAME}')