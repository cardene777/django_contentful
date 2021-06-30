from django.contrib import admin
from .models import Hospital, Data, Category, Page, Group, Tag, Element, Doctor, OutpatientDoctor, DepartmentTimeSchedule

admin.site.register(Hospital)
admin.site.register(Data)
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(Group)
admin.site.register(Tag)
admin.site.register(Element)
admin.site.register(Doctor)
admin.site.register(OutpatientDoctor)
admin.site.register(DepartmentTimeSchedule)


