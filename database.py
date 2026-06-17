import psycopg2
import psycopg2.extras
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:BCoZxyTplmCsRmCEgmNynTDVojgUXKGR@thomas.proxy.rlwy.net:59210/railway')

def conectar():
    conn = psycopg2.connect(DATABASE_URL)
    return conn