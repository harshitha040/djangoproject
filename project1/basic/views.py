from django.shortcuts import render
from django.http  import HttpResponse
from django.http import JsonResponse
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