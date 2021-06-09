from django import forms
from .models import Doctor, DepartmentSchedule, Page, Tag


class CSVUploadForm(forms.Form):
    file = forms.FileField(label='CSVファイル', help_text='※拡張子csvのファイルをアップロードしてください。')


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('hospital', 'title', 'name', 'profile', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hospital'].widget.attrs['class'] = 'form-control'
        self.fields['hospital'].widget.attrs['id'] = 'hospital'
        self.fields['hospital'].widget.attrs['name'] = 'hospital'
        self.fields['hospital'].widget.attrs['placeholder'] = '病院名'
        self.fields['hospital'].widget.attrs['maxlength'] = '150'

        self.fields['title'].widget.attrs['class'] = 'form-control text'
        self.fields['title'].widget.attrs['id'] = 'title'
        self.fields['title'].widget.attrs['name'] = 'title'
        self.fields['title'].widget.attrs['placeholder'] = '肩書き'

        self.fields['name'].widget.attrs['class'] = 'form-control text'
        self.fields['name'].widget.attrs['id'] = 'name'
        self.fields['name'].widget.attrs['name'] = 'name'
        self.fields['name'].widget.attrs['placeholder'] = '医師名'
        self.fields['name'].widget.attrs['maxlength'] = '100'

        self.fields['profile'].widget.attrs['class'] = 'form-control'
        self.fields['profile'].widget.attrs['id'] = 'profile'
        self.fields['profile'].widget.attrs['name'] = 'profile'
        self.fields['profile'].widget.attrs['placeholder'] = 'プロフィール'

        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['id'] = 'image'
        self.fields['image'].widget.attrs['name'] = 'image'
        self.fields['image'].widget.attrs['placeholder'] = '医師画像URL'


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = DepartmentSchedule
        fields = ('hospital', 'doctor', 'week', 'AP')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hospital'].widget.attrs['class'] = 'form-control'
        self.fields['hospital'].widget.attrs['id'] = 'hospital'
        self.fields['hospital'].widget.attrs['name'] = 'hospital'
        self.fields['hospital'].widget.attrs['placeholder'] = '病院名'

        self.fields['doctor'].widget.attrs['class'] = 'form-control'
        self.fields['doctor'].widget.attrs['id'] = 'doctor'
        self.fields['doctor'].widget.attrs['name'] = 'doctor'
        self.fields['doctor'].widget.attrs['placeholder'] = '医師名'

        self.fields['week'].widget.attrs['class'] = 'form-control'
        self.fields['week'].widget.attrs['id'] = 'week'
        self.fields['week'].widget.attrs['name'] = 'week'
        self.fields['week'].widget.attrs['placeholder'] = '曜日'

        self.fields['AP'].widget.attrs['class'] = 'form-control'
        self.fields['AP'].widget.attrs['id'] = 'AP'
        self.fields['AP'].widget.attrs['name'] = 'AP'
        self.fields['AP'].widget.attrs['placeholder'] = '午前・午後'


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('hospital', 'category', 'html', 'url', 'tag')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hospital'].widget.attrs['class'] = 'form-control'
        self.fields['hospital'].widget.attrs['id'] = 'hospital'
        self.fields['hospital'].widget.attrs['name'] = 'hospital'
        self.fields['hospital'].widget.attrs['placeholder'] = '病院名'

        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['id'] = 'category'
        self.fields['category'].widget.attrs['name'] = 'category'
        self.fields['category'].widget.attrs['placeholder'] = 'カテゴリ'

        self.fields['html'].widget.attrs['class'] = 'form-control'
        self.fields['html'].widget.attrs['id'] = 'html'
        self.fields['html'].widget.attrs['name'] = 'html'
        self.fields['html'].widget.attrs['placeholder'] = 'HTML'

        self.fields['url'].widget.attrs['class'] = 'form-control'
        self.fields['url'].widget.attrs['id'] = 'url'
        self.fields['url'].widget.attrs['name'] = 'url'
        self.fields['url'].widget.attrs['placeholder'] = 'URL'

        self.fields['tag'].widget.attrs['class'] = 'form-control'
        # self.fields['tag'].widget.attrs['id'] = 'tag'
        self.fields['tag'].widget.attrs['name'] = 'tag'
        self.fields['tag'].widget.attrs['placeholder'] = 'タグ'


class TagFrom(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['id'] = 'name'
        self.fields['name'].widget.attrs['name'] = 'name'
        self.fields['name'].widget.attrs['placeholder'] = 'タグ名'

