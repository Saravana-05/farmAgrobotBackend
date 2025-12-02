from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    user = User.objects.get(username=request.data["username"])
    if user.check_password(request.data['password']):
        token = Token.objects.create(user=user)
        return Response({"message":"Login successfull", "token":token.key},status=status.HTTP_200_OK)
    else:
        return Response({"message": "invalid data"})

@api_view(["POST"])
def logout(request):
    Token.objects.get(key=request.data['token' ]).delete()
    return Response({"message":"Logout successfull"},status=status.HTTP_200_OK)