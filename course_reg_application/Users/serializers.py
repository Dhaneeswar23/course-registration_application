from rest_framework import serializers

from .models import User,Course,CourseRegistration

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password','name','role']
        
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields  =  "__all__"
        
class CoureRegSeralizer(serializers.ModelSerializer):
    class Meta:
        model = CourseRegistration
        fields = "__all__"
        
        
