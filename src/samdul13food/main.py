import os
from typing import Union
from fastapi import FastAPI
import time
from fastapi.middleware.cors import CORSMiddleware
#import pandas as pd
import pymysql
import csv

app = FastAPI()

origins = [
    "https://samdul13food.web.app",
    "http://localhost:8899",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_path():
    file_path = __file__
    dirpath = os.path.dirname(file_path)
    print(dirpath)
    return dirpath

@app.get("/")
def read_root():
    return {"Hello": "n13"}

@app.get("/food")
def food(name: str):

    # 시간을 구함
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # df = pd.DataFrame([[t, name]], columns=['time', 'name'])
    
    path = get_path()
    
    dir_path = os.path.join(path, 'data')
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, 'food13.csv')
    
    data = {"food":name, "time":t}

    with open(file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['food', 'time'])
        writer.writerow(data)
    
    import pymysql.cursors
    db = pymysql.connect(
            host = os.getenv("DB_IP", "localhost"),
            user = 'food',
            passwd = '1234',
            db = 'fooddb',
            charset = 'utf8',
            port = int(os.getenv("MY_PORT", "33306"))
    )
    
    cursor = db.cursor(pymysql.cursors.DictCursor)

    sql = "INSERT INTO foodhistory(username, foodname, dt) VALUES(%s, %s, %s)"
    
    with db:
        with db.cursor() as cursor:
            cursor.execute(sql, ('n13', name, t))
        db.commit()
    # df.to_csv(file_path, mode='a', header=False, index=False)
    
    return data
