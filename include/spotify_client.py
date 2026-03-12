import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import sqlite3
import os
from datetime import datetime


def get_base_path():
    """Detecta se estamos no Airflow (Docker) ou Localmente"""
    return os.getenv('AIRFLOW_HOME', os.getcwd())


def get_spotify_client():
    scope = "user-read-recently-played"
    base_path = get_base_path()
    cache_path = os.path.join(base_path, 'include', '.spotify_cache')

    # Agora buscamos do ambiente. Se não existir, retorna None.
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError(
            "ERRO: Variáveis de ambiente SPOTIFY_CLIENT_ID ou SECRET não encontradas!")

    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://127.0.0.1:8888/callback",
        scope=scope,
        cache_path=cache_path,
        open_browser=False if os.getenv('AIRFLOW_HOME') else True
    ))


def extract_and_transform():
    sp = get_spotify_client()
    try:
        results = sp.current_user_recently_played(limit=50)
    except Exception as e:
        print(f"Erro ao conectar com Spotify: {e}")
        return None

    if not results or not results['items']:
        print("Nenhuma música nova encontrada.")
        return None

    data = []
    for item in results['items']:
        data.append({
            "track_id": item['track']['id'],
            "track_name": item['track']['name'],
            "artist": item['track']['artists'][0]['name'],
            "played_at": item['played_at'],
            "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    df = pd.DataFrame(data)
    df['played_at'] = pd.to_datetime(
        df['played_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
    return df


def load_to_sqlite(df):
    if df is None or df.empty:
        return

    base_path = get_base_path()
    db_path = os.path.join(base_path, 'include', 'spotify_history.db')

    # Garante que a pasta existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)

    # Criar tabela oficial
    conn.execute("""
        CREATE TABLE IF NOT EXISTS spotify_tracks (
            track_id TEXT,
            track_name TEXT,
            artist TEXT,
            played_at TEXT,
            extracted_at TEXT,
            PRIMARY KEY (track_id, played_at)
        )
    """)

    # Salva temporário e faz o Upsert
    df.to_sql('temp_spotify', conn, if_exists='replace', index=False)
    query = """
    INSERT OR IGNORE INTO spotify_tracks (track_id, track_name, artist, played_at, extracted_at)
    SELECT track_id, track_name, artist, played_at, extracted_at FROM temp_spotify
    """
    conn.execute(query)
    conn.commit()
    conn.close()
    print(f"Dados salvos com sucesso em: {db_path}")


if __name__ == "__main__":
    print("Iniciando execução local para gerar Token...")
    dados = extract_and_transform()
    load_to_sqlite(dados)
