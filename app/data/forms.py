from django import forms
from .models import Category, Page, Tag, Element, Doctor, OutpatientDoctor, DepartmentTimeSchedule


class CSVUploadForm(forms.Form):
    file = forms.FileField(label='CSVファイル', help_text='※拡張子csvのファイルをアップロードしてください。')


class CategoryFrom(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("hospital", "category", "name", "url")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hospital'].widget.attrs['class'] = 'form-control'
        self.fields['hospital'].widget.attrs['id'] = 'hospital'
        self.fields['hospital'].widget.attrs['name'] = 'hospital'

        self.fields['category'].widget.attrs['class'] = 'form-control text'
        self.fields['category'].widget.attrs['id'] = 'category'
        self.fields['category'].widget.attrs['name'] = 'category'

        self.fields['name'].widget.attrs['class'] = 'form-control text'
        self.fields['name'].widget.attrs['id'] = 'name'
        self.fields['name'].widget.attrs['name'] = 'name'
        self.fields['name'].widget.attrs['placeholder'] = 'カテゴリ名'

        self.fields['url'].widget.attrs['class'] = 'form-control'
        self.fields['url'].widget.attrs['id'] = 'url'
        self.fields['url'].widget.attrs['name'] = 'url'
        self.fields['url'].widget.attrs['placeholder'] = 'URL'


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('category', 'title', 'html', 'tag', 'url')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['id'] = 'category'
        self.fields['category'].widget.attrs['name'] = 'category'

        self.fields['title'].widget.attrs['class'] = 'form-control text'
        self.fields['title'].widget.attrs['id'] = 'title'
        self.fields['title'].widget.attrs['name'] = 'title'
        self.fields['title'].widget.attrs['placeholder'] = 'ページタイトル'

        self.fields['html'].widget.attrs['class'] = 'form-control text'
        self.fields['html'].widget.attrs['id'] = 'html'
        self.fields['html'].widget.attrs['name'] = 'html'
        self.fields['html'].widget.attrs['placeholder'] = 'HTML'

        self.fields['tag'].widget.attrs['class'] = 'form-control'
        self.fields['tag'].widget.attrs['id'] = 'tag'
        self.fields['tag'].widget.attrs['name'] = 'tag'

        self.fields['url'].widget.attrs['class'] = 'form-control'
        self.fields['url'].widget.attrs['id'] = 'url'
        self.fields['url'].widget.attrs['name'] = 'url'
        self.fields['url'].widget.attrs['placeholder'] = 'URL'



class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control text'
        self.fields['name'].widget.attrs['id'] = 'name'
        self.fields['name'].widget.attrs['name'] = 'name'
        self.fields['name'].widget.attrs['placeholder'] = 'タグ名'


class ElementForm(forms.ModelForm):
    class Meta:
        model = Element
        fields = ('category', 'title', 'html', 'url', 'tag')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['class'] = 'form-control text'
        self.fields['category'].widget.attrs['id'] = 'category'
        self.fields['category'].widget.attrs['name'] = 'category'

        self.fields['title'].widget.attrs['class'] = 'form-control text'
        self.fields['title'].widget.attrs['id'] = 'title'
        self.fields['title'].widget.attrs['name'] = 'title'
        self.fields['title'].widget.attrs['placeholder'] = '要素タイトル'

        self.fields['html'].widget.attrs['class'] = 'form-control text'
        self.fields['html'].widget.attrs['id'] = 'html'
        self.fields['html'].widget.attrs['name'] = 'html'
        self.fields['html'].widget.attrs['placeholder'] = 'HTML'

        self.fields['url'].widget.attrs['class'] = 'form-control text'
        self.fields['url'].widget.attrs['id'] = 'url'
        self.fields['url'].widget.attrs['name'] = 'url'
        self.fields['url'].widget.attrs['placeholder'] = 'URL'

        self.fields['tag'].widget.attrs['class'] = 'form-control text'
        self.fields['tag'].widget.attrs['id'] = 'tag'
        self.fields['tag'].widget.attrs['name'] = 'tag'


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('category', 'name', 'title', 'profile', 'url', 'tag')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['id'] = 'category'
        self.fields['category'].widget.attrs['name'] = 'category'

        self.fields['name'].widget.attrs['class'] = 'form-control text'
        self.fields['name'].widget.attrs['id'] = 'name'
        self.fields['name'].widget.attrs['name'] = 'name'
        self.fields['name'].widget.attrs['placeholder'] = '医師名'

        self.fields['title'].widget.attrs['class'] = 'form-control text'
        self.fields['title'].widget.attrs['id'] = 'title'
        self.fields['title'].widget.attrs['name'] = 'title'
        self.fields['title'].widget.attrs['placeholder'] = '肩書き'

        self.fields['profile'].widget.attrs['class'] = 'form-control'
        self.fields['profile'].widget.attrs['id'] = 'profile'
        self.fields['profile'].widget.attrs['name'] = 'profile'
        self.fields['profile'].widget.attrs['placeholder'] = 'プロフィール'

        self.fields['url'].widget.attrs['class'] = 'form-control text'
        self.fields['url'].widget.attrs['id'] = 'url'
        self.fields['url'].widget.attrs['name'] = 'url'
        self.fields['url'].widget.attrs['placeholder'] = 'URL'

        self.fields['tag'].widget.attrs['class'] = 'form-control text'
        self.fields['tag'].widget.attrs['id'] = 'tag'
        self.fields['tag'].widget.attrs['name'] = 'tag'


class OutpatientDoctorForm(forms.ModelForm):
    class Meta:
        model = OutpatientDoctor
        fields = ('category', 'doctor', 'day_week', 'am_pm', 'other', 'url', 'tag')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['id'] = 'category'
        self.fields['category'].widget.attrs['name'] = 'category'

        self.fields['doctor'].widget.attrs['class'] = 'form-control text'
        self.fields['doctor'].widget.attrs['id'] = 'doctor'
        self.fields['doctor'].widget.attrs['name'] = 'doctor'

        self.fields['day_week'].widget.attrs['class'] = 'form-control text'
        self.fields['day_week'].widget.attrs['id'] = 'day_week'
        self.fields['day_week'].widget.attrs['name'] = 'day_week'
        self.fields['day_week'].widget.attrs['placeholder'] = '曜日'

        self.fields['am_pm'].widget.attrs['class'] = 'form-control'
        self.fields['am_pm'].widget.attrs['id'] = 'am_pm'
        self.fields['am_pm'].widget.attrs['name'] = 'am_pm'
        self.fields['am_pm'].widget.attrs['placeholder'] = '午前・午後'

        self.fields['other'].widget.attrs['class'] = 'form-control'
        self.fields['other'].widget.attrs['id'] = 'other'
        self.fields['other'].widget.attrs['name'] = 'other'
        self.fields['other'].widget.attrs['placeholder'] = '補足'

        self.fields['url'].widget.attrs['class'] = 'form-control text'
        self.fields['url'].widget.attrs['id'] = 'url'
        self.fields['url'].widget.attrs['name'] = 'url'
        self.fields['url'].widget.attrs['placeholder'] = 'URL'

        self.fields['tag'].widget.attrs['class'] = 'form-control text'
        self.fields['tag'].widget.attrs['id'] = 'tag'
        self.fields['tag'].widget.attrs['name'] = 'tag'


class DepartmentTimeScheduleForm(forms.ModelForm):
    class Meta:
        model = DepartmentTimeSchedule
        fields = ('category', 'check', 'start_time', 'end_time', 'type', 'url', 'tag')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['id'] = 'category'
        self.fields['category'].widget.attrs['name'] = 'category'
        self.fields['category'].widget.attrs['placeholder'] = 'グループ名'

        self.fields['check'].widget.attrs['class'] = 'form-control'
        self.fields['check'].widget.attrs['id'] = 'check'
        self.fields['check'].widget.attrs['name'] = 'check'

        self.fields['start_time'].widget.attrs['class'] = 'form-control text'
        self.fields['start_time'].widget.attrs['id'] = 'start_time'
        self.fields['start_time'].widget.attrs['name'] = 'start_time'
        self.fields['start_time'].widget.attrs['placeholder'] = '開始時刻'

        self.fields['end_time'].widget.attrs['class'] = 'form-control'
        self.fields['end_time'].widget.attrs['id'] = 'end_time'
        self.fields['end_time'].widget.attrs['name'] = 'end_time'
        self.fields['end_time'].widget.attrs['placeholder'] = '終了時刻'

        self.fields['type'].widget.attrs['class'] = 'form-control'
        self.fields['type'].widget.attrs['id'] = 'type'
        self.fields['type'].widget.attrs['name'] = 'type'

        self.fields['url'].widget.attrs['class'] = 'form-control text'
        self.fields['url'].widget.attrs['id'] = 'url'
        self.fields['url'].widget.attrs['name'] = 'url'
        self.fields['url'].widget.attrs['placeholder'] = 'URL'

        self.fields['tag'].widget.attrs['class'] = 'form-control text'
        self.fields['tag'].widget.attrs['id'] = 'tag'
        self.fields['tag'].widget.attrs['name'] = 'tag'




