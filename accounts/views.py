from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response

# Create your views here.

class RegisterUserView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    def post(self, request):

        # if email is already in use
        if UserProfile.objects.filter(phone_number=request.data['phone_number']).exists():
            return Response({'error': 'Phone Number already registered'}, status=status.HTTP_400_BAD_REQUEST)
        if UserProfile.objects.filter(email=request.data['email']).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(request.data)
            data=request.data
            data['password']= 'password'
            serializer = UserProfileSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response( {"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update user profile image
    def put(self, request):
        user = UserProfile.objects.get(email=request.user.email)
        user.avatar = request.data['avatar']
        user.save()
        return Response({'message': 'Image updated'}, status=status.HTTP_200_OK)
    
class AllUsersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # Custom logic to modify the response data
        # For example, adding custom keys or modifying existing ones
        # response.data['custom_key'] = custom_value
        
        return Response({
            'custom_response': 'Custom response data',
            'access': response.data['access'],
            'refresh': response.data['refresh']
        })

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # Custom logic to modify the response data
        # For example, adding custom keys or modifying existing ones
        # response.data['custom_key'] = custom_value
        
        return Response({
            'custom_response': 'Custom refresh response data',
            'access': response.data['access'],
            'refresh': request.data['refresh']

        })