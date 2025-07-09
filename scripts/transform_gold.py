import os
import sqlite3
import pandas as pd
from datetime import datetime

# Caminhos
SILVER_DB_PATH = os.path.join("data", "silver", "users_silver.db")
GOLD_DB_PATH = os.path.join("data", "gold", "users_gold.db")

def calculate_age(birth_date_str):
    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
    except Exception:
        # Se o formato estiver errado, retorna None
        return None
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def save_table(df, conn, table_name):
    df.to_sql(table_name, conn, if_exists="replace", index=False)

def transform_to_gold():
    # Ler da camada silver
    conn_silver = sqlite3.connect(SILVER_DB_PATH)
    df = pd.read_sql_query("SELECT * FROM users_silver", conn_silver)
    conn_silver.close()

    print(f"👤 Total usuários na silver: {len(df)}")

    # Calcular idade
    df["age"] = df["birth_date"].apply(calculate_age)

    # Criar faixa etária
    def age_group(age):
        if age is None:
            return "Desconhecido"
        if age < 30:
            return "18-29"
        elif age < 45:
            return "30-44"
        elif age < 60:
            return "45-59"
        else:
            return "60+"

    df["age_group"] = df["age"].apply(age_group)

    # Criar dimensões simplificadas com surrogate keys simuladas (incrementais)
    # Dimensão de data: pegar datas distintas de registration_timestamp_utc (converter para data)
    df['registration_date'] = pd.to_datetime(df['registration_timestamp_utc'], errors='coerce').dt.date
    dim_date = pd.DataFrame(df['registration_date'].dropna().unique(), columns=['full_date'])
    dim_date = dim_date.reset_index().rename(columns={'index':'sk_date'})  # sk_date = surrogate key incremental

    # Dimensão localização
    dim_location = pd.DataFrame(df['address'].dropna().unique(), columns=['address'])
    dim_location = dim_location.reset_index().rename(columns={'index':'sk_location'})

    # Dimensão usuário (únicos por name, email, cpf)
    dim_user = df[['name', 'email', 'cpf']].drop_duplicates().reset_index(drop=True)
    dim_user = dim_user.reset_index().rename(columns={'index':'sk_user'})

    # Criar tabela fato juntando as dimensões via merge (joins)
    fact_users = df.merge(dim_date, left_on='registration_date', right_on='full_date', how='left') \
                   .merge(dim_location, on='address', how='left') \
                   .merge(dim_user, on=['name', 'email', 'cpf'], how='left')

    fact_users = fact_users.rename(columns={'id':'user_id'})
    fact_users = fact_users[['user_id', 'sk_user', 'sk_location', 'sk_date', 'birth_date', 'phone_number']]

    # Criar pasta gold se não existir
    os.makedirs(os.path.dirname(GOLD_DB_PATH), exist_ok=True)
    conn_gold = sqlite3.connect(GOLD_DB_PATH)

    # Salvar dimensões e fato
    save_table(dim_date, conn_gold, "dim_date")
    save_table(dim_location, conn_gold, "dim_location")
    save_table(dim_user, conn_gold, "dim_user")
    save_table(fact_users, conn_gold, "fact_users")

    conn_gold.close()

    print("✅ Gold layer criado em:", GOLD_DB_PATH)
    print("Dim_date exemplo:")
    print(dim_date.head())
    print("\nDim_location exemplo:")
    print(dim_location.head())
    print("\nDim_user exemplo:")
    print(dim_user.head())
    print("\nFact_users exemplo:")
    print(fact_users.head())

if __name__ == "__main__":
    transform_to_gold()
