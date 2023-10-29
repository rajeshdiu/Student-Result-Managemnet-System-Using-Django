from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from myApp.models import *
from django.contrib import messages
from myApp import EmailBackEnd
from django.contrib.auth import login as auth_login


def studentPage(request):
    
    
    return render(request,"Students/studentPage.html",)



def sentStudentNotification(request):
    
    
    teacher=studentModel.objects.all()
    see_notification=studentNotificationModel.objects.all().order_by("-id")[0:5]
    
    context={
        "teacher":teacher,
        "see_notification":see_notification,
    }
    
    
    return render(request,"myAdmin/sentStudentNotificationPage.html",context)



def saveStudentNotification(request):
    error_messages = {
        'success': 'Notification Sent Successfully',
        'error': 'Notification Sent Failed',
    }
     
    if request.method == "POST":
        message = request.POST.get("message")
        student_id = request.POST.get("studentid")
        
        student=studentModel.objects.get(admin=student_id)
        
        student_notification=studentNotificationModel(
            
            student_id=student,
            message=message,
        )
        student_notification.save()
        
        messages.success(request, error_messages['success'])
        
        return redirect("sentStudentNotification")
    else:
        messages.success(request, error_messages['error'])
        



def studentNotificationPage(request):
    
    student=studentModel.objects.filter(admin=request.user.id)
    
    for i in student:
        
        student_id= i.id
        
        notification=studentNotificationModel.objects.filter(student_id=student_id)
        
        context={
            "notification":notification,
        }
    
    
    return render(request,"Staff/notification.html",context)

def markasDone(request,status):
    
    notification = studentNotificationModel.objects.get(id= status)
    notification.status=1
    notification.save()
    
    return redirect("studentNotificationPage")


def studentApplyLeave(request,status):
    
    error_messages = {
        'success': 'Applied Successfully',
        'error': 'Apply Failed',
    }
    
def studentApplyForLeavePage(request):
    
    
    return render(request,"Students/studentApplyForLeave.html")

def studentapplyLeaveSave(request):
    
    error_messages = {
        'success': 'Message Sent Successfully',
        'error': 'Message Sent Failed',
    }
    
    if request.method == "POST":
        leave_Date = request.POST.get("leaveDate")
        leave_Message = request.POST.get("leaveMessage")
        student_id = studentModel.objects.get(admin = request.user.id)
        
        leave=studetnLeaveModel(
            studentid = student_id,
            data = leave_Date,
            message = leave_Message,
        )
        
        leave.save()
        messages.success(request, error_messages['success'])
    
    return redirect("studentApplyForLeavePage")

    
    
