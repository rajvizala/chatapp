from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'mychat/lobby.html')

def room(request,room_name):
    return render(request,'mychat/chat_room.html',{"room_name":room_name})