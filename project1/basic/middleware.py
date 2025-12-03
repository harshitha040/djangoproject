from django.http import JsonResponse
import re , json
from basic.models import Users

class basicMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self,request):
        # print(request,"hello")
        if(request.path=="/student/"):
            print(request.method,"method")
            print(request.path,"path")
        response=self.get_response(request)
        return response
    
 
import json
import re
from django.http import JsonResponse
class SignupMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
# Only validate for Signup API
        if request.path.startswith("/signup") and request.method == "POST":
            try:
                body_unicode = request.body.decode('utf-8')
                if not body_unicode:
                    return JsonResponse({"error": "Empty request body"}, status=400)
                data = json.loads(body_unicode)
            except Exception:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
            username = data.get("username")
            email = data.get("email")
            dob = data.get("dob")
            password = data.get("password")

            # -----------------------------
            # REGEX VALIDATIONS
            # -----------------------------

            # Username: only letters & numbers, 4-15 chars
            if not re.match(r"^[A-Za-z0-9]{4,15}$", username or ""):
                return JsonResponse({"error": "Invalid username"}, status=400)
            
            # Email validation
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email or ""):
                return JsonResponse({"error": "Invalid email"}, status=400)

            # DOB: YYYY-MM-DD format
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', dob or ""):
                return JsonResponse({"error": "Invalid DOB format"}, status=400)

            # Password: at least 8 chars, one uppercase, one number, one special char
            if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password or ""):
                return JsonResponse({"error": "Weak password"}, status=400)

        # Continue request
        response = self.get_response(request)
        return response
    
    
# for independent classes ( ) are no need 
class SscMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if(request.path in ["/job1/","/job2/"]):
            ssc_result=(request.GET.get("ssc"))
            print(ssc_result,'hello')
            if(ssc_result !='True'):
                return  JsonResponse({"error":"u should qualify atleast ssc for applying this job"},status=400)
        return self.get_response(request)
    
class MedicalFitMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if(request.path == "/job1/"):
            medical_fit_result=(request.GET.get("medically_fit"))
            if(medical_fit_result !='True'):
                return JsonResponse({"error":"u not medically fit to apply for this job role"},status=400)
        return self.get_response(request)
 
class AgeMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if (request.path in ["/job1/","/job2/"]):
            Age_checker=int(request.GET.get("age",17))
            if(Age_checker >25 and Age_checker<18):
                return JsonResponse({"error":"age must be in b/w 18 and 25"},status=400)
        return self.get_response(request)

        
        
        
        
class UsernameMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if(request.path=="/signUp/"):
            data=json.loads(request.body)
            username=data.get("username"," ")
            # checks username is empty or not
            if not username:
                return JsonResponse({"error":"username is required"},status=400)
            # checks length
            if len(username)<3 or len(username)>20:
                return JsonResponse({"error":"username should contain 3 to 20 chars"},status=400)
            # checks starting and ending
            if username[0] in '._' or username[-1] in '._':
                return JsonResponse({"error":"username should not start or end with . or _"},status=400)
            # checks allowed characters
            if not re.match(r'^[A-Za-z0-9._]+$', username):
                return JsonResponse({"error":"username should contain only  letters, numbers, dot  and underscore"},status=400)
            # checks .. and __
            if '__' in username or '..' in username:
                return JsonResponse({"error":"username should not contain .. or __"},status=400)
        return self.get_response(request)
    
    
    
    
class EmailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if(request.path == "/signUp/"):
            data = json.loads(request.body)
            email = data.get("email", " ")
            if email == " ":
                return JsonResponse({"error": "email should not be empty"}, status=400)
       # 2. Basic email pattern
            pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
            if not re.match(pattern, email):
                return JsonResponse({"error": " must have basic email pattern "}, status=400)
            # 3. Duplicate email check
            if Users.objects.filter(email=email).exists():
                return JsonResponse({"error": "email already exists"}, status=400)
        return self.get_response(request)
