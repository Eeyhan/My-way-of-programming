from django.utils.deprecation import MiddlewareMixin


class MyCorsMiddelware(MiddlewareMixin):
    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "*"
        if request.method == "OPTIONS":
            response["Access-Control-Allow-Headers"] = "content-type"
            response['Access-Control-Allow-Methods'] = '*'
        return response
