from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import AllowAny

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password =  request.data.get("password")

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=400)
    
    user = User.objects.create_user(username=username, email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid Credentials'}, status=400)

@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({'message': "Logged Out"})
