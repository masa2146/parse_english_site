from flask import Response, request
from database.models import NewsLevels, Contact
from flask_restful import Resource
import logging

logger = logging.getLogger('root')


class NewsLevelsApi(Resource):
    def get(self):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        offset = (page - 1) * per_page
        print("Offset: " , offset , " per_page: " , per_page , " page: " , page)
        data = NewsLevels.objects.skip(offset).limit(per_page).to_json()
        # data = Contact.objects().to_json()
        return Response(data, mimetype="application/json", status=200)
    
    # def post(self):
    #     body = request.get_json()
    #     data = Contact(**body).save()
    #     id = data.id
    #     return {'id': str(id)}, 200
