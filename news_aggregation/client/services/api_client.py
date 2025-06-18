import json
import urllib.request

BASE_URL = "http://localhost:8000"

class APIClient:
    def request(self, method, path, data=None):
        url = f"{BASE_URL}{path}"
        data_bytes = json.dumps(data).encode('utf-8') if data else None
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method.upper())

        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as e:
            error_msg = e.read().decode()
            return {"error": f"{e.code} - {error_msg}"}
        except Exception as e:
            return {"error": str(e)}
