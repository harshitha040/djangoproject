from django.shortcuts import render
from django.http  import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import StudentNew

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
        data = json.loads(request.body)
        student=StudentNew.objects.create(
        name=data.get("name"), 
            age=data.get("age"),
            email=data.get("email")
        )
        return JsonResponse({"status":"success","id":student.id}, status=200)
    return JsonResponse({"error": "use post method"}, status=400)