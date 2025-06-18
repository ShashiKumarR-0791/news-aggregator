from server.services.external_api_service import ExternalAPIService

external_api_service = ExternalAPIService()

def fetch_news_handler(_, __):
    external_api_service.fetch_and_store_all()
    return {"message": "News fetched from all active servers"}
