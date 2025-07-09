# Big Data Pipeline com Apache Airflow

Este projeto cria um pipeline de dados fake e simula as camadas Raw, Bronze, Silver e Gold utilizando Apache Airflow para orquestração.

---

## Estrutura do Projeto

big_data_airflow_project/  
├── dags/                    # DAGs do Airflow  
│   ├── big_data_pipeline_dag.py  
│   ├── generate_raw_data_dag.py  
│   ├── transform_bronze_dag.py  
│   ├── transform_silver_dag.py  
│   └── transform_gold_dag.py  
├── scripts/                 # Scripts Python para geração e transformação dos dados  
│   ├── generate_data.py  
│   ├── transform_bronze.py  
│   ├── transform_silver.py  
│   └── transform_gold.py  
├── data/                    # Dados em diferentes camadas (raw, bronze, silver, gold)  
├── docker-compose.yaml      # Configuração Docker para Airflow e Postgres  
└── README.md                # Este arquivo  

---

## 🛠️ Pré-requisitos

Certifique-se de ter o seguinte instalado em sua máquina:

* **Docker** e **Docker Compose**
* **Python 3.13** (opcional, para rodar scripts localmente)
* Sistema Operacional: **Windows**, **Linux** ou **macOS**

---

## 🚀 Como Rodar

Siga os passos abaixo para configurar e executar o projeto:

1.  **Clone o projeto:**
    ```bash
    git clone <seu-repositorio.git>
    cd big_data_airflow_project
    ```

2.  **Suba os containers do Airflow com Docker Compose:**
    ```bash
    docker compose up -d
    ```

3.  **Inicialize o banco de dados do Airflow** (se for a primeira vez):
    ```bash
    docker compose run airflow-webserver airflow db init
    ```

4.  **Crie o usuário administrador** para login na interface do Airflow:
    ```bash
    docker compose run airflow-webserver airflow users create \
      --username airflow \
      --firstname Admin \
      --lastname User \
      --role Admin \
      --email airflow@example.com \
      --password airflow
    ```

5.  **Acesse a interface do Airflow** no navegador:
    [http://localhost:8080](http://localhost:8080)

    **Credenciais padrão:**
    * **Usuário:** `airflow`
    * **Senha:** `airflow`

6.  **Ative e execute a DAG `big_data_pipeline`** na interface do Airflow para rodar o pipeline completo.

---

## ➡️ DAGs Disponíveis

Este projeto inclui as seguintes DAGs:

* `generate_raw_data` — Gera dados fake em formato JSON (camada **Raw**)
* `transform_bronze` — Converte JSON para banco SQLite (camada **Bronze**)
* `transform_silver` — Realiza limpeza e validação dos dados (camada **Silver**)
* `transform_gold` — Agregação e preparação da camada final de dados (camada **Gold**)
* `big_data_pipeline` — DAG orquestradora que executa todas as 4 etapas em sequência.

---

## 💡 Estrutura do Pipeline

O fluxo do pipeline é o seguinte:

generate_raw_data -> transform_bronze -> transform_silver -> transform_gold

---

## ✉️ Contatos e Suporte

Para dúvidas ou sugestões, sinta-se à vontade para entrar em contato:

**Sérgio Medeiros Fonte**
Email: s.fonte@yahoo.com