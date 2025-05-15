from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Course, CourseRegistration
from .serializers import UsersSerializer, CourseSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view

# Create your views here.

class RegisterStudent(APIView):
    def post(self, request):
        #here using cipy beacause of we need to modify the incoming data to make it hased pwd beacuse of that 
        data = request.data.copy()
        data['password'] = make_password(data['password'])
        
        #here we checking role can be present in table and roel not equal to student then raise an error this view only for students
        if 'role' in data and data['role']!='student':
            return Response({"msg":"Only students can register this api"})
        
        #after valdiations we set data in serializer if its valid it saved on db
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
# Register Faculty
class RegisterFaculty(APIView):
    def post(self, request):
        data = request.data.copy()
        
        data['password'] = make_password(data['password'])
        if 'role' in data and data['role']!='faculty':
            return Response({"msg":"Only faculty can register this view"})
        
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Faculty registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View for both students and faculty same view using jwt auth
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#this view is only faculty can add courses 
class AddCourse(APIView):
    def post(self, request):
        
        #request.user means currently authenticated user we get the details
        user = request.user
        print("The user is ",user)
        
        #faculty is not accessing the view we raise an error
        if user.role != 'faculty':
            return Response({'error': 'Only faculty can offer courses'}, status=status.HTTP_403_FORBIDDEN)

        course_name = request.data.get('name')
        course_code = request.data.get('code')
        
        #if course code is already exist we raise error
        if Course.objects.filter(code=course_code).exists():
            return Response({'error': 'Course code already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        Course.objects.create(name=course_name, code=course_code, offered_by=user)
        return Response({'msg': 'Course added successfully'}, status=status.HTTP_201_CREATED)
    
    
class RegisterCourse(APIView):
    def post(self, request):
        user = request.user
        
        if user.role != 'student':
            return Response({'error': 'Only students can register for courses'}, status=status.HTTP_403_FORBIDDEN)

        course_id = request.data.get('course_id')
        
        try:
            course = Course.objects.get(id=course_id)
            
        except Course.DoesNotExist:
            return Response({'error': 'Invalid course ID'}, status=status.HTTP_404_NOT_FOUND)

        if CourseRegistration.objects.filter(student=user).count() >= 2:
            return Response({'error': 'You can register for a maximum of 2 courses'}, status=status.HTTP_400_BAD_REQUEST)

        CourseRegistration.objects.create(student=user, course=course)
        return Response({'msg': 'Course registered successfully'}, status=status.HTTP_201_CREATED)
    
    
@api_view(['GET'])
def get_data(request):
    users = User.objects.all()
    serializer = UsersSerializer(users,many=True)
    return Response(serializer.data)

    