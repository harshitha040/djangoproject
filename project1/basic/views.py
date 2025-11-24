from django.shortcuts import render
from django.http  import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json

from django.views.decorators.csrf import csrf_exempt
from basic.models import StudentNew ,Users

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
       return JsonResponse({"status":"success"},status=200)
       user=Users.objects.create(
            username=data.get('name'),
            email=data.get("email"),
            password=data.get("password")
            )
        