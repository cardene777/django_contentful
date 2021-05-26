from django import forms
from .models import Doctor, Schedule


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
        model = Schedule
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
