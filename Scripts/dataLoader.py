import pandas as pd
import psycopg2 as pg


def load_from_db():
    # connection to postgres database 
    try: 
        engine = pg.connect("dbname='telecomdb' user='postgres' host='127.0.0.1' port='5432' password='postgresP@ss'")
        df = pd.read_sql('select * from xdr_data', con=engine)
        return df
    except:
        return "Database connection couldn't made"



def clean_data_loader(path='C:/Users/Diriba/Desktop/10AC/Week1/Project/TenAcademyWeek1/data/clean_data.csv'):
    # Read your data into a pandas DataFrame
    try:
        df = pd.read_csv(path)
        return df
    except BaseException:
        return "file does not exist or path is not correct"  