from website.models import User

class KeyLogin:
    def __init__(self, get_response):
        self.get_response = get_response
       

    def __call__(self, req):
        req.res = {
            "status": 403,
            "message": "not_authorized"
        }
        
        queries = req.GET
        
        if queries.get("key") and not req.user.is_authenticated:
            user = User.objects.filter(api_key=queries.get("key"))
            if user:
                req.user = user[0]
        
        if req.user.is_authenticated:
            req.res = {
                "status": 500,
                "message": "internal server error"
            }
            
        response = self.get_response(req)
        
        # Code to be executed for each request/response after
        # the view is called.

        return response