import json

def json_response(data, status=200):
    return {
        "status": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(data)
    }

def error_response(message="Something went wrong", status=500):
    return {
        "status": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": message})
    }
