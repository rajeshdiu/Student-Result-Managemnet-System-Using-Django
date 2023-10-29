from django.contrib import admin

from .models import *
from django.contrib.auth.admin import UserAdmin


class userModel(UserAdmin):
    list_display=["username","user_type"]

admin.site.register(customUser,userModel)

admin.site.register(courseModel)
admin.site.register(sessionYearModel)
admin.site.register(studentModel)
admin.site.register(teacherModel)
admin.site.register(subjectModel)
admin.site.register(staffNotificationModel)
admin.site.register(studentNotificationModel)
admin.site.register(teacherLeaveModel)
admin.site.register(studetnLeaveModel)
admin.site.register(teacherFeebackModel)