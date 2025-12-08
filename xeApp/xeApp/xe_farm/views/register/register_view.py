from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from ...serializers import UserSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from ...models import User  # Using relative import (go up 2 levels)

permission_classes( IsAdminUser)
@api_view(["POST"])
def register(request):
    user = UserSerializer(data = request.data)
    if user.is_valid():
        user.save()        
        return Response("User Created successfully", status = status.HTTP_201_CREATED)
    else:
        return Response("invalid data")

permission_classes( IsAdminUser)
@api_view(["PUT"])
def update_user(request, user_id):
    try:
        user = User.objects.get(id = user_id)
    except User.DoesNotExist:
        return Response("user not found", status = status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user, data = request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response("User updated successfully", status = status.HTTP_200_OK)
    else:
        return Response("invalid data", status = status.HTTP_400_BAD_REQUEST)

permission_classes(IsAdminUser)
@api_view(["DELETE"])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response("user not found", status = status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response("User deleted successfully", status = status.HTTP_200_OK)