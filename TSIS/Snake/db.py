import psycopg2
from config import DB_DSN


def _conn():
    return psycopg2.connect(DB_DSN)


def init_db():
    with _conn() as c:
        with c.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id       SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id            SERIAL PRIMARY KEY,
                    player_id     INTEGER REFERENCES players(id),
                    score         INTEGER   NOT NULL,
                    level_reached INTEGER   NOT NULL,
                    played_at     TIMESTAMP DEFAULT NOW()
                )
            """)


def get_or_create_player(username):
    with _conn() as c:
        with c.cursor() as cur:
            cur.execute("SELECT id FROM players WHERE username = %s", (username,))
            r = cur.fetchone()
            if r:
                return r[0]
            cur.execute(
                "INSERT INTO players(username) VALUES(%s) RETURNING id",
                (username,)
            )
            return cur.fetchone()[0]


def save_session(player_id, score, level):
    with _conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "INSERT INTO game_sessions(player_id, score, level_reached) VALUES(%s,%s,%s)",
                (player_id, score, level)
            )


def get_leaderboard():
    with _conn() as c:
        with c.cursor() as cur:
            cur.execute("""
                SELECT p.username, gs.score, gs.level_reached,
                       TO_CHAR(gs.played_at, 'YYYY-MM-DD')
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC
                LIMIT 10
            """)
            return cur.fetchall()


def get_personal_best(player_id):
    with _conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "SELECT MAX(score) FROM game_sessions WHERE player_id = %s",
                (player_id,)
            )
            r = cur.fetchone()
            return r[0] if r and r[0] is not None else 0