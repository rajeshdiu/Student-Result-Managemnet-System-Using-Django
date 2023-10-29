from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from myApp.models import *
from django.contrib import messages
from myApp import EmailBackEnd
from django.contrib.auth import login as auth_login


def signupPage(request):
    error_messages = {
        'password_error': 'Password and Confirm Password not match',
    }
    if request.method == "POST":
        uname = request.POST.get("name")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("confirmpassword")

        if pass1!= pass2:
             messages.error(request, error_messages['password_error'])
        else:
            # Use your customUser model to create a user
            myuser = customUser.objects.create_user(username=uname, email=email, password=pass1)
            myuser.save()
            return redirect("loginPage")

    # messages.success(request, 'Signup successful.')
    return render(request, "signup.html")

def logoutPage(request):
    logout(request)
    return redirect("loginPage")

def loginPage(request):
    error_messages = {
        'username_error': 'Username is required.',
        'password_error': 'Password is required.',
        'login_error': 'Invalid username or password. Please try again.',
    }

    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("password")
        
        if not username:
            messages.error(request, error_messages['username_error'])
        elif not pass1:
            messages.error(request, error_messages['password_error'])
        else:
            user = EmailBackEnd.authenticate(request, username=username, password=pass1,)

            if user is not None:
                login(request,user)
                user_type = user.user_type
                if user_type == '1':
                    return redirect("adminPage")
                elif user_type == '2':
                    return redirect("staffPage")
                elif user_type == '3':
                    return redirect("studentPage")
                else:
                    return redirect("signupPage")
            else:
                messages.error(request, error_messages['login_error'])

    return render(request, "login.html")


def staffPage(request):
    

    return render(request,"Staff/teacherHome.html")



def adminPage(request):
    
    studentCount= studentModel.objects.all().count()
    teacherCount= teacherModel.objects.all().count()
    departmentCount= courseModel.objects.all().count()
    subjectCount= subjectModel.objects.all().count()
    
    student_male_count=studentModel.objects.filter(gender="Male").count()
    student_female_count=studentModel.objects.filter(gender="Female").count()
    
    context={
        "studentCount":studentCount,
        "teacherCount":teacherCount,
        "departmentCount":departmentCount,
        "subjectCount":subjectCount,
        "student_male_count":student_male_count,
        "student_female_count":student_female_count,
        }
    
    return render(request,"myAdmin/adminhome.html",context)


def myProfile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)

from django.contrib.auth.hashers import check_password

def profileUpdate(request):
    error_messages = {
        'success': 'Profile Update Successfully',
        'error': 'Profile Not Updated',
        'password_error': 'Current password is incorrect',
    }
    
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        password = request.POST.get("password")
        username = request.POST.get("username")
        email = request.POST.get("email")
        
        try:
            cuser = customUser.objects.get(id=request.user.id)
            
            cuser.first_name = firstname
            cuser.last_name = lastname
            cuser.profile_pic = profile_pic
            
            # Verify the current password provided matches the user's current password
            if not cuser.check_password(password):
                messages.error(request, error_messages['password_error'])
            else:
                # If the current password is correct, proceed to update other fields
                if profile_pic is not None:
                    cuser.profile_pic = profile_pic
                
                # You can add additional fields to update here as needed

                cuser.save()
                auth_login(request, cuser)
                messages.success(request, error_messages['success'])
                return redirect("profileUpdate")
        except:
            messages.error(request, error_messages['error'])
    
    return render(request, 'profile.html')


# views.py

def changePassword(request):
    error_messages = {
        'success': 'Changed Successfully',
        'mismatch': 'New password and confirm password not matched',
        'old_password': 'Old password not match',
    }
    
    if request.method == "POST":
        old_password = request.POST.get("oldPassword")
        new_password = request.POST.get("newpassword")
        confirm_password = request.POST.get("confirmPassword")
        user = request.user
        
        if user.check_password(old_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, error_messages['success'])
                return redirect("loginPage")
            else:
                messages.error(request, error_messages['mismatch'])
        else:
            messages.error(request, error_messages['old_password'])

    return render(request, "changepassword.html")



def addStudent(request):
    error_messages = {
        'success': 'Student Add Successfully',
        'error': 'Student Add Failed',
    }
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")  # Changed from 'user_name' to 'username'
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("courseid")
        session_year_id = request.POST.get("sessionyearid")

        # Check if email or username already exists
        if customUser.objects.filter(email=email).exists() or customUser.objects.filter(username=username).exists():
            messages.error(request, error_messages['error'])
        else:
            # Create the customUser instance
            user = customUser.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.profile_pic = profile_pic
            user.user_type = 3  # Assuming '3' represents students

            # Save the user instance
            user.save()

            # Retrieve the selected course and session year
            myCourse = courseModel.objects.get(id=course_id)
            mySessionYear = sessionYearModel.objects.get(id=session_year_id)

            # Create the student instance
            student = studentModel(
                admin=user,
                address=address,
                sessionyearid=mySessionYear,
                courseid=myCourse,
                gender=gender,
            )

            # Save the student instance
            student.save()

            messages.success(request, error_messages['success'])
            return redirect("addStudent")

    # Fetch the course and session year data to display in the form
    course = courseModel.objects.all()
    session_year = sessionYearModel.objects.all()
    st=studentModel.objects.all()
    context = {
        "course": course,
        "session": session_year,
        "st":st,   
    }

    return render(request, "myAdmin/addStudent.html", context)

def studentList(request):
    
    allStudent=studentModel.objects.all()
    print(allStudent)
    
    return render(request,"myAdmin/studentlist.html",{"student":allStudent})

def editStudent(request,id):
    student=studentModel.objects.filter(id=id)
    course = courseModel.objects.all()
    session_year = sessionYearModel.objects.all()
    st=studentModel.objects.all()
    context = {
        "course": course,
        "session": session_year,
        "student":student,
        
    }
    
    return render(request,"myAdmin/editStudent.html",context)

def updateStudent(request):
    error_messages = {
        'success': 'Student Updated Successfully',
        'error': 'Student Updated Failed',
    }
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")  # Changed from 'user_name' to 'username'
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("courseid")
        session_year_id = request.POST.get("sessionyearid")
        
        user=customUser.objects.get(id=student_id)
        
        user.first_name = first_name
        user.last_name = last_name
        user.email=email
        user.username=username
        
        if password is not None and password!="":
            user.set_password(password)
        if password is not None and profile_pic!="":
            user.profile_pic=profile_pic
        user.save()
        
        student=studentModel.objects.get(admin=student_id)
        student.address=address
        student.gender=gender
        
        course=courseModel.objects.get(id=course_id)
        student.course_id=course
        
        session=sessionYearModel.objects.get(id=session_year_id)
        student.session_year_id=session
        
        student.save()
        
        
        messages.success(request, error_messages['success'])
        return redirect("studentList")
    
    return render(request,"myAdmin/editStudent.html")

def addTeacher(request):
    error_messages = {
        'success': 'Teacher Add Successfully',
        'erroremail': 'email already exist',
        'errorusername': 'username already exist',
    }
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")  # Changed from 'user_name' to 'username'
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("courseid")
        mobile = request.POST.get("mobile")
        experience = request.POST.get("experience")

        # Check if email or username already exists
        if customUser.objects.filter(email=email).exists():
            messages.error(request, error_messages['erroremail'])
        if customUser.objects.filter(username=username).exists():
            messages.error(request, error_messages['errorusername'])
        else:
            # Create the customUser instance
            user = customUser.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.profile_pic = profile_pic
            user.user_type = 2  # Assuming '2' represents students

            # Save the user instance
            user.save()

            # Retrieve the selected course and session year
            myCourse = courseModel.objects.get(id=course_id)

            # Create the student instance
            teacher = teacherModel(
                admin=user,
                address=address,
                courseid=myCourse,
                gender=gender,
                mobile=mobile,
                experience=experience,
            )

            # Save the student instance
            teacher.save()

            messages.success(request, error_messages['success'])
            return redirect("teacherList")

    # Fetch the course and session year data to display in the form
    course = courseModel.objects.all()
    st=teacherModel.objects.all()
    context = {
        "course": course,
    }

    return render(request, "myAdmin/addTeacher.html", context)


def teacherList(request):
    
    allTeacher=teacherModel.objects.all()
    print(allTeacher)
    
    return render(request,"myAdmin/teacherList.html",{"teacher":allTeacher})


def editTeacher(request,id):
    teacher=teacherModel.objects.filter(id=id)
    course = courseModel.objects.all()
    context = {
        "course": course,
        "teacher":teacher,
    }
    
    return render(request,"myAdmin/editTeacher.html",context)


def updateTeacher(request):
    
    error_messages = {
        'success': 'Teacher Updated Successfully',
        'error': 'Teacher update Failed',
    }
    if request.method == "POST":
        teacher_id = request.POST.get("teacher_id")
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username") 
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("courseid")
        mobile = request.POST.get("mobile")
        experience = request.POST.get("experience")
        
        user=customUser.objects.get(id=teacher_id)
        
        user.first_name = first_name
        user.last_name = last_name
        user.email=email
        user.username=username
        
        
        if password is not None and password!="":
            user.set_password(password)
        if password is not None and profile_pic!="":
            user.profile_pic=profile_pic
        user.save()
        
        teacher=teacherModel.objects.get(admin=teacher_id)
        
        teacher.address=address
        teacher.gender=gender
        teacher.mobile=mobile
        teacher.experience=experience
        
        course=courseModel.objects.get(id=course_id)
        teacher.course_id=course
        
        teacher.save()
        
        
        messages.success(request, error_messages['success'])
        return redirect("teacherList")
    return render(request,"myAdmin/editTeacher.html")
    
    
def addDepartment(request):
    
    error_messages = {
        'success': 'Department Add Successfully',
        'department_exist_error': 'Department already exist',
    }
    if request.method == "POST":
        department_name = request.POST.get("department_name")
        
        print(department_name)
        
        if courseModel.objects.filter(name=department_name):
            messages.error(request, error_messages['department_exist_error'])
        else:
            
            course=courseModel(
                
                name=department_name,
                
            )
            
            course.save()
            messages.success(request, error_messages['success'])
            
            return redirect("departmentList")
       
    
    
    return render(request,"myAdmin/addDepartment.html")

def departmentList(request):
    
    department = courseModel.objects.all()
    context = {
        "department": department,
    }
    
    return render(request,"myAdmin/departmentList.html",context)


def editDepartment(request,id):
    
    course = courseModel.objects.get(id=id)
    context = {
        "course": course,
    }
    
    return render(request,"myAdmin/editDepartment.html",context)


def updateDepartment(request):

    error_messages = {
        'success': 'Department Updated Successfully',
        'error': 'Department Update Failed',
    }
    if request.method == "POST":
        department_id = request.POST.get("department_id")
        department_name = request.POST.get("department_name")
        
        print(department_id,department_name)
        
        course=courseModel.objects.get(id=department_id)
        
        course.name= department_name
        
        course.save()
        
        
        messages.success(request, error_messages['success'])
        return redirect("departmentList")
    else:
        messages.error(request, error_messages['error'])
        
        return redirect("editDepartment")
    
    return render(request,"myAdmin/editDepartment.html")
   


def addSubject(request):
    
    course=courseModel.objects.all()
    teacher=teacherModel.objects.all()
    
    
    error_messages = {
        'success': 'Subject Add Successfully',
        'subjecterror': 'Subject already exist',
    }
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        teacher_id = request.POST.get("teacher_id")
        subject_name = request.POST.get("subject_name")
       
        courseid=courseModel.objects.get(id=course_id)
        teacherid=teacherModel.objects.get(id=teacher_id)
    
        subject=subjectModel(
        
        name=subject_name,
        course=courseid,
        teacher=teacherid,
        )
        
        
    
        subject.save()
 
        messages.success(request, error_messages['success'])

        return redirect("subjectList")
    
    context={
        "course":course,
        "teacher":teacher,
        }    
    

    return render(request,"myAdmin/addSubject.html",context)



def subjectList(request):
    
    subject = subjectModel.objects.all()
    context = {
        "subject": subject,
    }
    
   
    return render(request,"myAdmin/subjectList.html",context)



def editSubject(request,id):
    
    subject=subjectModel.objects.filter(id=id)
    course=courseModel.objects.all()
    teacher=teacherModel.objects.all()
    
    
    context={
        
        "subject":subject,
        "course":course,
        "teacher":teacher,
    }
    
    
    return render(request,"myAdmin/editSubject.html",context)



def updateSubject(request):
    
    error_messages = {
        'success': 'Subject Update Successfully',
        'subjecterror': 'Subject Update Failed',
    }
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        course_id = request.POST.get("course_id")
        teacher_id = request.POST.get("teacher_id")
        subject_name = request.POST.get("subject_name")
       
        courseid=courseModel.objects.get(id=course_id)
        teacherid=teacherModel.objects.get(id=teacher_id)
    
        subject=subjectModel(
        id=subject_id,
        name=subject_name,
        course=courseid,
        teacher=teacherid,
        )
        
        subject.save()
 
        messages.success(request, error_messages['success'])

        return redirect("subjectList")
    
    return render(request,"myAdmin/editSubject.html")


def addSession(request):
    error_messages = {
        'success': 'Session Add Successfully',
        'sessionError': 'Session Add Failed',
    }
    if request.method == "POST":
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        
        session=sessionYearModel(
            sessionStart=session_start,
            sessionEnd=session_end,
        )
        
        session.save()
        messages.success(request, error_messages['success'])
        return redirect("sessionList")
    
    return render(request,"myAdmin/addSession.html")


def sessionList(request):
    session=sessionYearModel.objects.all()
    context={
        
        "session":session,
    }
    return render(request,"myAdmin/sessionList.html",context)



def editSession(request,id):
    session=sessionYearModel.objects.filter(id=id)
    
    context={
        
        "session":session,
    }
    
    return render(request,"myAdmin/editSession.html",context)


def updateSession(request):
    error_messages = {
        'success': 'Session Updated Successfully',
        'error': 'Session Update Failed',
    }
    if request.method == "POST":
        session_id = request.POST.get("session_id")
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        session=sessionYearModel.objects.get(id=session_id)
        session.sessionStart= session_start
        session.sessionEnd=session_end
        session.save()
        messages.success(request, error_messages['success'])
        return redirect("sessionList")
    else:
        messages.error(request, error_messages['error'])
        
        return redirect("editSession")


def SentTeacherNotification(request):
    
    teacher=teacherModel.objects.all()
    see_notification=staffNotificationModel.objects.all().order_by("-id")[0:5]
    
    context={
        "teacher":teacher,
        "see_notification":see_notification,
    }
    
    return render(request,"myAdmin/SentTeacherNotification.html",context)

    

def saveTeacherNotification(request):
    error_messages = {
        'success': 'Notification Sent Successfully',
        'error': 'Notification Sent Failed',
    }
    if request.method == "POST":
        message = request.POST.get("message")
        teacher_id = request.POST.get("teacher_id")
        
        teacher=teacherModel.objects.get(admin=teacher_id)
        
        notification=staffNotificationModel(
            
            staff_id=teacher,
            message=message,
        )
        notification.save()
        
        messages.success(request, error_messages['success'])
        
        return redirect("SentTeacherNotification")
    else:
        messages.success(request, error_messages['error'])
  
 
 #Teacher Or Staff Leave
 


def applyLeaveSave(request):
    
    error_messages = {
        'success': 'Message Sent Successfully',
        'error': 'Message Sent Failed',
    }
    if request.method == "POST":
        leave_Date = request.POST.get("leaveDate")
        leave_Message = request.POST.get("leaveMessage")
        staff_id = teacherModel.objects.get(admin = request.user.id)
        
        leave=teacherLeaveModel(
            staff_id = staff_id,
            data = leave_Date,
            message = leave_Message,
        )
        
        leave.save()
        messages.success(request, error_messages['success'])
    
    return redirect("teacherleavePage")



def teacherLeavelist(request):
    
    staff_leave= teacherLeaveModel.objects.all()
    
    context={
        "staff_leave":staff_leave,
    }
      
    return render(request,"myAdmin/teacherLeavelist.html",context)

def teacherLeaveApprove(request,id):
    
    leave= teacherLeaveModel.objects.get(id=id)
    leave.status=1
    leave.save()
    
    return redirect("teacherLeavelist")


def teacherLeaveDisApprove(request,id):
    
    leave= teacherLeaveModel.objects.get(id=id)
    leave.status=2
    leave.save()
    
    return redirect("teacherLeavelist")
 
 
def teacherleavePage(request):
     
    teacher = teacherModel.objects.filter(admin = request.user.id)
     
    for i in teacher:
        
        teacher_id = i.id
        print(i.id)
        
        staff_leave_history = teacherLeaveModel.objects.filter(staff_id=teacher_id)    
 
    
        context={
        "staff_leave_history": staff_leave_history,
        }
 
        return render(request,"myAdmin/teacherleave.html",context)
    
    
def teacherFeedbackPageList(request):
    
    feedback= teacherFeebackModel.objects.all()
    
    context={
        "feedback":feedback,
    }
    
    
    return render(request,"myAdmin/teacherFeedbackPage.html",context)

def teacherFeedbackReplySave(request):
    
    error_messages = {
        'success': 'Message Sent Successfully',
        'error': 'Message Sent Failed',
    }
    if request.method == "POST":
        feedback_reply = request.POST.get("feedback_reply")
        feedback_id = request.POST.get("feedback_id")
        feedback = teacherFeebackModel.objects.get(id = feedback_id)
        
        feedback.feedback_reply=feedback_reply
        
        feedback.save()
        messages.success(request, error_messages['success'])
    
    return redirect("teacherFeedbackPageList")
    
    


#Teacher or Staff Panel




