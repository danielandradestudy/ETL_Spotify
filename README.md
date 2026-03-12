# 🎧 Spotify Airflow ETL Pipeline

Este projeto realiza o processo de **ETL (Extract, Transform, Load)** de dados da API do Spotify, utilizando **Apache Airflow** para orquestração e **SQLite** como Data Warehouse local.

O objetivo é capturar o histórico de músicas ouvidas recentemente e armazená-las de forma persistente e sem duplicatas, permitindo análises futuras de hábitos musicais.

## 🛠️ Tecnologias e Ferramentas
* **Linux**: Onde foi executado o projeto.
* **Python**: Lógica principal de extração e transformação.
* **Apache Airflow (Astro CLI)**: Orquestração e agendamento das tarefas.
* **Docker**: Conteinerização do ambiente de dados.
* **Pandas**: Manipulação e limpeza dos dados.
* **SQLite**: Armazenamento dos dados processados.
* **Spotipy**: Biblioteca para integração com a API Web do Spotify.

## 📈 Arquitetura do Projeto
O pipeline segue o fluxo:
1. **Extração**: Consumo da API do Spotify (Endpoint `recently-played`).
2. **Transformação**: Limpeza dos dados, seleção de campos relevantes e criação de metadados de auditoria (`extracted_at`).
3. **Carga**: Inserção no SQLite utilizando lógica de **Upsert** (Idempotência) baseada em uma Primary Key composta (`track_id` + `played_at`).

## 📈 Monitoramento no Airflow

Dashboard da DAG no Airflow
<img width="1375" height="814" alt="image" src="https://github.com/user-attachments/assets/ad550041-3fda-4c08-87de-0393c61a388b" />
<img width="1615" height="1144" alt="image" src="https://github.com/user-attachments/assets/7bbde1e5-0a1a-46bf-b31b-c2475fe0097a" />




## 🚀 Como Executar

### Pré-requisitos
* Docker instalado.
* Astro CLI instalado.
* Conta no [Spotify Developer Console](https://developer.spotify.com/dashboard/) para obter as credenciais.

### Instalação
 Clone o repositório:
   ```bash
   git clone [https://github.com/danielandradestudy/projeto-spotify-airflow.git]
   Configure as Variáveis de Ambiente:
Crie um arquivo .env na raiz do projeto e adicione suas credenciais do Spotify:

SPOTIFY_CLIENT_ID='seu_id_aqui'
SPOTIFY_CLIENT_SECRET='seu_secret_aqui'
Inicie o ambiente Airflow:
Certifique-se de que o Docker está rodando e execute:

Bash
astro dev start

