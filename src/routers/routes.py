from .news_levels import NewsLevelsApi

def initialize_routes(api):
    api.add_resource(NewsLevelsApi, '/api/news')