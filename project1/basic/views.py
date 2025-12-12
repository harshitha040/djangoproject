from django.shortcuts import render
from django.http  import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import StudentNew ,Users
from django.contrib.auth.hashers import make_password, check_password
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Create your views here.
def sample(request):
    return HttpResponse('harshitha')

def sampleInfo(request):
    # data={"name":"harshitha","age":21,"city":"bangalore"}
    data=[1,2,3,4]
    return JsonResponse(data,safe=False)


def dynamicResponse(request):
    name=request.GET.get('name',"")
    age=request.GET.get('age',"")
    response=f"Hello, my name is {name} and I am {age} years old."
    return HttpResponse(response)

def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return JsonResponse({"status": "ok","db": "connected"})
    except Exception as e:
        return JsonResponse({"status": "error","db": str(e)})
 
@csrf_exempt
def addStudent(request):
    print(request.method)
    if request.method == "POST":
        data=json.loads(request.body)
        student=StudentNew.objects.create(
            name=data.get('name'),
            age=data.get("age"),
            email=data.get("email")
            )
        return JsonResponse({"status":"success", "id":student.id },status=200)

    elif request.method=="GET":
        print(request.method,"hello")
        result=list(StudentNew.objects.values())
        print(result)
        return JsonResponse({"status":"ok","data":result},status=200)


    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id") #getting id
        new_email=data.get("email") #getting email
        existing_student=StudentNew.objects.get(id=ref_id) #fetched the object as per the id
        existing_student.email=new_email #updating with new email
        existing_student.save()
        updated_data=StudentNew.objects.filter(id=ref_id).values().first()        
        return JsonResponse({"status":"data updated successfully","updated_data":updated_data},status=200)


    elif request.method=="DELETE":
        data=json.loads(request.body)
        ref_id=data.get("id") #getting id
        get_delting_data=StudentNew.objects.filter(id=ref_id).values().first()
        to_be_delete=StudentNew.objects.get(id=ref_id)
        to_be_delete.delete()
        return JsonResponse({"status":"success","message":"student record deleted successfully","deleted data":get_delting_data},status=200)
    return JsonResponse({"error":"use post method"},status=400)


@csrf_exempt
def signup(request):
    return JsonResponse({
        "status": "success",
        "message": "User signup valid and processed"
    })
    
    
def job1(request):
    return JsonResponse({"status": "success","message": "u have successfully applied to job1"},status=200)
def job2(request):
    return JsonResponse({"status": "success","message": "u have successfully applied to job2"},status=200)

@csrf_exempt
def signUp(request):
    if request.method == "POST":
       data=json.loads(request.body)
       print(data)   
       user=Users.objects.create(
            username=data.get("username"),
            email=data.get("email"),
            password=make_password(data.get("password"))
)
    return JsonResponse({"status":"success"},status=200)


@csrf_exempt
def login(request):
    if request.method=="POST":
        data=request.POST
        username=data.get("username")
        password=data.get("password")
        print(username,password)
        try:
            user=Users.objects.get(username=username) #checking user is available or not
            print(user)
            issued_time=datetime.now(ZoneInfo("Asia/Kolkata"))
            expired_time=issued_time + timedelta(minutes=1)
            if check_password(password,user.password):
                # token="a json web token"
                payload={"username":username,"email":user.email,"id":user.id,"exp":expired_time}
                token=jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256",)
                return JsonResponse({"status":"success","message":"login successful","token":token,"issued_at":issued_time,"expired_at":expired_time,"expires_in":int((expired_time-issued_time).total_seconds()/60)},status=200)
            else:
                return JsonResponse({"status":"error","message":"invalid credentials"},status=400)
        except Users.DoesNotExist: 
            return JsonResponse({"status":"error","message":"user not found"},status=404)
    

@csrf_exempt
def check(request):
    hashed="pbkdf2_sha256$870000$WKR4oxyQYSz5XohCwunMYu$SbRuOYvYdtRzg2OF54Xl9sWKGhBJzOHStZVhFfpBDjY="
    inputdata=request.POST # data is given in form data
    print(inputdata)
    # hashed=make_password(inputdata.get("ip"))
    x=check_password(inputdata.get("ip"),hashed)
    print(x)
    return JsonResponse({"status":"success","data":x},status=200)


@csrf_exempt
def getAllusers(request):
    if request.method=="GET":
        users=list(Users.objects.values())
        print(request.token_data,"token in views") #accessing payload data in views using request()
        print(request.token_data.get("username"),"username") #accessing username from payload data
        print(users,"all users")
        for user in users:
            print(user['username'],"username from users list")
            if user['username'] == request.token_data.get("username"):
                return JsonResponse({"status":"success","login_user":request.token_data,"data":users},status=200)
        else:
            return JsonResponse({"error":"unauthorized access"},status=401)
        



