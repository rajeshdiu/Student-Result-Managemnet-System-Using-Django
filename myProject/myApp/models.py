from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class customUser(AbstractUser):
    
    USER=(
        (1,"admin"),
        (2,"Teacher"),
        (3,"students"),
    )

    user_type=models.CharField(choices=USER,max_length=50,default=1)
    profile_pic=models.ImageField(upload_to="media/profile_pic")
    


class courseModel(models.Model):
    name=models.CharField(max_length=100)
    createat=models.DateTimeField(auto_now_add=True)
    updateat=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
class sessionYearModel(models.Model):
    sessionStart=models.CharField(max_length=100)
    sessionEnd=models.CharField(max_length=100)
    def __str__(self):
        return self.sessionStart + "/" + self.sessionEnd
  
class studentModel(models.Model):
    admin = models.OneToOneField(customUser, on_delete=models.CASCADE)
    address=models.TextField()
    gender = models.CharField(max_length=100)
    courseid = models.ForeignKey(courseModel, on_delete=models.DO_NOTHING,default=1)  # Set the default course
    sessionyearid = models.ForeignKey(sessionYearModel, on_delete=models.DO_NOTHING,default=1)
    cratedat = models.DateTimeField(auto_now_add=True)  # Set the default value using timezone.now
    updateat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
   
   
class teacherModel(models.Model):
    admin = models.OneToOneField(customUser, on_delete=models.CASCADE)
    address=models.TextField()
    gender = models.CharField(max_length=100)
    mobile=models.CharField(max_length=100)
    courseid = models.ForeignKey(courseModel, on_delete=models.DO_NOTHING,default=2)
    experience=models.CharField(max_length=100)
    cratedat = models.DateTimeField(auto_now_add=True)  # Set the default value using timezone.now
    updateat = models.DateTimeField(auto_now=True)
       
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    
    
    
# class teacherModel(models.Model):
#     admin = models.OneToOneField(customUser, on_delete=models.CASCADE)
#     address=models.TextField()
#     gender = models.CharField(max_length=100)
#     mobile=models.CharField(max_length=100)
#     courseid = models.ForeignKey(courseModel, on_delete=models.DO_NOTHING,default=2)
#     experience=models.CharField(max_length=100)
#     cratedat = models.DateTimeField(auto_now_add=True)  # Set the default value using timezone.now
#     updateat = models.DateTimeField(auto_now=True)
       
#     def __str__(self):
#         return self.admin.first_name + " " + self.admin.last_name
   
# # class createSection(models.Model):
    


class subjectModel(models.Model):
    name=models.CharField(max_length=100)
    course=models.ForeignKey(courseModel,on_delete=models.CASCADE)
    teacher=models.ForeignKey(teacherModel,on_delete=models.CASCADE)
    cratedat = models.DateTimeField(auto_now_add=True, null=True)  # Set the default value using timezone.now
    updateat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class studentNotificationModel(models.Model):
    student_id=models.ForeignKey(studentModel,on_delete=models.CASCADE)
    message= models.TextField()
    createAt= models.DateTimeField(auto_now_add=True)
    status=models.IntegerField(null=True,default=0)
    
    def __str__(self):
        return self.student_id.admin.first_name

    
class staffNotificationModel(models.Model):
    staff_id=models.ForeignKey(teacherModel,on_delete=models.CASCADE)
    message= models.TextField()
    createAt= models.DateTimeField(auto_now_add=True)
    status=models.IntegerField(null=True,default=0)
    
    
    def __str__(self):
        return self.staff_id.admin.first_name
    
    
class teacherLeaveModel(models.Model):
    
    staff_id=models.ForeignKey(teacherModel,on_delete=models.CASCADE)
    data= models.CharField(max_length=100)
    message= models.TextField()
    status=models.IntegerField(default=0)
    createAt= models.DateTimeField(auto_now_add=True)
    updateat = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.staff_id.admin.first_name + self.staff_id.admin.last_name
    
    
class studetnLeaveModel(models.Model):
    
    studentid=models.ForeignKey(studentModel,on_delete=models.CASCADE)
    data= models.CharField(max_length=100)
    message= models.TextField()
    status=models.IntegerField(default=0)
    createAt= models.DateTimeField(auto_now_add=True)
    updateat = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.studentid.admin.first_name + self.studentid.admin.last_name
    
class teacherFeebackModel(models.Model):
    
    staff_id=models.ForeignKey(teacherModel,on_delete=models.CASCADE)
    feedback= models.TextField()
    feedback_reply=models.TextField()
    createAt= models.DateTimeField(auto_now_add=True)
    updateat = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.staff_id.admin.first_name + self.staff_id.admin.last_name
    
    
    
 