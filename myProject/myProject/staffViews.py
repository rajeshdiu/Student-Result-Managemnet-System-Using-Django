from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from myApp.models import *
from django.contrib import messages
from myApp import EmailBackEnd
from django.contrib.auth import login as auth_login


def myNotification(request):
    
    teacher=teacherModel.objects.filter(admin=request.user.id)
    
    for i in teacher:
        
        teacher_id= i.id
        
        notification=staffNotificationModel.objects.filter(staff_id=teacher_id)
        
        context={
            "notification":notification,
        }
    
    
    return render(request,"Staff/notification.html",context)


def markasDone(request,status):
    
    notification = staffNotificationModel.objects.get(id= status)
    notification.status=1
    notification.save()
    
    return redirect("myNotification")

def StudentLeaveList(request):
    
    student_leave= studetnLeaveModel.objects.all()
    
    context={
        "student_leave":student_leave,
    }
    
    
    return render(request,"Staff/studentLeaveList.html",context)




def studentLeaveApprove(request,id):
    
    leave= studetnLeaveModel.objects.get(id=id)
    leave.status=1
    leave.save()
    
    return redirect("StudentLeaveList")

def studentLeaveDisApprove(request,id):
    
    leave= studetnLeaveModel.objects.get(id=id)
    leave.status=2
    leave.save()
    
    return redirect("StudentLeaveList")

def teacherSendFeedback(request):
    
    staff_id=teacherModel.objects.get(admin=request.user.id)
    
    feeback_history=teacherFeebackModel.objects.filter(staff_id=staff_id)
    
    context={
        "feeback_history":feeback_history
    }
    
    
    
    return render(request,"Staff/teacherSendFeedbackPage.html",context)

def teacherFeedbackSave(request):
    
    error_messages = {
        'success': 'Feedback Sent Successfully',
        'error': 'Feedback Sent Failed',
    }
     
    
    if request.method == "POST":
        feed_back = request.POST.get("FeedbackMessage")
        
        staff_id=teacherModel.objects.get(admin= request.user.id)
        
        feed_back=teacherFeebackModel(
            
            staff_id=staff_id,
            feedback=feed_back,
            feedback_reply="",
        )
        feed_back.save()
        
        messages.success(request, error_messages['success'])
        
        return redirect("teacherSendFeedback")
    else:
        messages.success(request, error_messages['error'])
    
    

    
    
    

