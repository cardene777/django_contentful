from django.contrib import admin
from .models import Hospital, Category, Page, Data, Doctor, DepartmentSchedule, DepartmentTime, Tag

admin.site.register(Hospital)
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(Data)
admin.site.register(Doctor)
admin.site.register(DepartmentSchedule)
admin.site.register(DepartmentTime)
admin.site.register(Tag)


