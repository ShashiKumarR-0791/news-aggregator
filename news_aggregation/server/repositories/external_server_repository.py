import sqlite3
from server.database.connection import get_connection
from server.repositories.base_repository import BaseRepository
from server.models.external_server import ExternalServer

class ExternalServerRepository(BaseRepository):
    def add_server(self, server: ExternalServer):
        query = '''
            INSERT INTO external_servers (name, api_url, api_key, is_active, last_accessed, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.execute(query, (
            server.name,
            server.api_url,
            server.api_key,
            int(server.is_active),
            server.last_accessed,
            server.created_at
        ))

    def get_all_servers(self, with_api_keys=False):
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = "SELECT server_id, name, is_active, last_accessed FROM external_servers"
        if with_api_keys:
            query = "SELECT * FROM external_servers"

        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def update_api_key(self, server_id, new_key):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE external_servers SET api_key = ? WHERE server_id = ?", (new_key, server_id))
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated

        
