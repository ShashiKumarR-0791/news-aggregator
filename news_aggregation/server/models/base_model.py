from datetime import datetime

class BaseModel:
    def __init__(self):
        self.created_at = datetime.utcnow().isoformat()
