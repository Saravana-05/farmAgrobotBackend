from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ...serializers import UserSerializer
from django.contrib.auth.models import User

@api_view(["POST"])
def register(request):
    user = UserSerializer(data = request.data)
    
    if user.is_valid():
        user.save()
        userRestrived = User.objects.get(username=user.data["username"])
        userRestrived.set_password(user.data["password"])
        userRestrived.save()
        
        return Response(user.data, status = status.HTTP_201_CREATED)
