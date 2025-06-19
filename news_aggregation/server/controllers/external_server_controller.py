from server.repositories.external_server_repository import ExternalServerRepository

class ExternalServerController:
    def __init__(self):
        self.repo = ExternalServerRepository()

    def list_servers(self):
        return self.repo.get_all_servers()

    def view_server_details(self):
        return self.repo.get_all_servers(with_api_keys=True)

    def update_api_key(self, server_id, new_key):
        return self.repo.update_api_key(server_id, new_key)
    
    def view_server_status(self):
        return self.repo.get_all_servers()
