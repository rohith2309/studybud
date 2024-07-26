from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from.serialization import RoomSerilizer
from base.models import project

routes=['GET routes/','GET api/rooms','GET api/room/<pk:id>']
rot='hello'

@api_view(['GET'])
def getRoutes(request):
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    room=project.objects.all()
    Roomserial=RoomSerilizer(room,many=True)
    print(Roomserial)
    return Response(Roomserial.data)
    
@api_view(['GET'])
def getRoom(request,pk):
    room=project.objects.get(id=pk)
    Roomserial=RoomSerilizer(room,many=False)
    return Response(Roomserial.data)
    
    
       


