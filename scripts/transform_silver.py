import os
import sqlite3
import pandas as pd
import re

# Caminhos
BRONZE_DB_PATH = os.path.join("data", "bronze", "users_bronze.db")
SILVER_DB_PATH = os.path.join("data", "silver", "users_silver.db")

# Validador de email simples
def is_valid_email(email):
    if email is None:
        return False
    regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(regex, email)

def transform_to_silver():
    # Ler dados da camada bronze
    conn_bronze = sqlite3.connect(BRONZE_DB_PATH)
    df = pd.read_sql_query("SELECT * FROM users_bronze", conn_bronze)
    conn_bronze.close()

    print(f"🔍 Registros na bronze: {len(df)}")

    # Remover registros sem ID
    df = df[df['id'].notnull()]

    # Remover duplicatas por ID (mantém o primeiro)
    df = df.drop_duplicates(subset='id')

    # Validar emails (ajuste para garantir bool)
    df = df[df['email'].apply(lambda x: bool(is_valid_email(x)))]

    # Preencher valores nulos com placeholders (opcional)
    df = df.fillna({
        "name": "Nome Desconhecido",
        "email": "sem_email@dominio.com",
        "address": "Endereço não informado",
        "phone_number": "000000000",
        "birth_date": "1900-01-01",
        "cpf": "000.000.000-00"
    })

    # Criar banco silver
    os.makedirs(os.path.dirname(SILVER_DB_PATH), exist_ok=True)
    conn_silver = sqlite3.connect(SILVER_DB_PATH)

    # Salvar
    df.to_sql("users_silver", conn_silver, if_exists="replace", index=False)
    conn_silver.close()

    print(f"✅ Dados tratados salvos na camada Silver: {SILVER_DB_PATH}")
    print(f"✅ Registros válidos: {len(df)}")

if __name__ == "__main__":
    transform_to_silver()
