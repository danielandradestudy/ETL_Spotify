# 🎧 Spotify Airflow ETL Pipeline

Este projeto realiza o processo de **ETL (Extract, Transform, Load)** de dados da API do Spotify, utilizando **Apache Airflow** para orquestração e **SQLite** como Data Warehouse local.

O objetivo é capturar o histórico de músicas ouvidas recentemente e armazená-las de forma persistente e sem duplicatas, permitindo análises futuras de hábitos musicais.

## 🛠️ Tecnologias e Ferramentas
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



## 🚀 Como Executar

### Pré-requisitos
* Docker instalado.
* Astro CLI instalado.
* Conta no [Spotify Developer Console](https://developer.spotify.com/dashboard/) para obter as credenciais.

### Instalação
1. Clone o repositório:
   ```bash
   git clone [https://github.com/danielandradestudy/projeto-spotify-airflow.git]
