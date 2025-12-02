from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from ...serializers import UserSerializer
from ...models import User  # Using relative import (go up 2 levels)
from rest_framework.permissions import IsAuthenticated

@api_view(["POST"])
def register(request):
    user = UserSerializer(data = request.data)
    if user.is_valid():
        user.save()        
        return Response("User Created successfully", status = status.HTTP_201_CREATED)
    else:
        return Response("invalid data")
