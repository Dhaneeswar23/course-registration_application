from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, role="admin", **extra_fields)
    
    
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    name = models.CharField(max_length=100)
  

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'name',]

    def __str__(self):
        return f"{self.email} ({self.role})"
    
    class Meta:
        db_table = 'users_table'
        managed = True
        verbose_name = 'ModelName'
        verbose_name_plural = 'ModelNames'
    
   
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    offered_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'faculty'})

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        db_table = 'course_table'
        managed = True
        verbose_name = 'ModelName'
        verbose_name_plural = 'ModelNames'
    

class CourseRegistration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    registered_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.email} - {self.course.code}"
    
    class Meta:
        db_table = 'course_registraion'
        managed = True
        verbose_name = 'ModelName'
        verbose_name_plural = 'ModelNames'
    
    


