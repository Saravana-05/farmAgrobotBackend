from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from ...serializers import UserSerializer, AssignPageSerializer 
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from ...models import User, Role, Page, AssignPage, UserProfile # Using relative import (go up 2 levels)

# permission_classes( IsAdminUser)
@api_view(["POST"])
def register(request):
    user = UserSerializer(data = request.data)
    if user.is_valid():
        user.save()        
        return Response({"message":"User Created successfully"}, status = status.HTTP_201_CREATED)
    else:
        return Response({"message":"invalid data"})

# permission_classes(IsAdminUser)
@api_view(["PUT"])
def update_user(request, user_id):
    try:
        user = User.objects.get(id = user_id)
    except User.DoesNotExist:
        return Response({"message":"user not found"}, status = status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user, data = request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"User updated successfully"}, status = status.HTTP_200_OK)
    else:
        return Response({"message":"invalid data"}, status = status.HTTP_400_BAD_REQUEST)

# permission_classes(IsAdminUser)
@api_view(["DELETE"])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message":"user not found"}, status = status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response({"message":"User deleted successfully"}, status = status.HTTP_200_OK)

@api_view(["POST"])
def assign_pages_to_role(request, role_id):
    page_list = request.data.get('page',[])
    try:
        role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        return Response({"message":"Role is required"}, status=status.HTTP_400_BAD_REQUEST)
    AssignPage.objects.filter(role = role).delete()
    
    for p in page_list:
        page_obj, created = Page.objects.get_or_create(name = p.strip().capitalize())
        AssignPage.objects.create(role = role,page=page_obj)
    return Response({"message":"pages were added"}, status=status.HTTP_200_OK)
 
@api_view(["GET"])
def get_assigned_page(request, user_id):
    try:
        profile = UserProfile.objects.get(user_id = user_id)
    except UserProfile.DoesNotExist:
        return Response({"message":"user not found"}, status = status.HTTP_404_NOT_FOUND)
    role = profile.role
    assign_page = AssignPage.objects.filter(role = role).select_related("page")
    
    return Response({
        "username": profile.user.username,
        "role": role.name,
        "pages": [{'id':p.page.id,'page':p.page.name} for p in assign_page]
    })