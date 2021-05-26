from django.shortcuts import render
from django.views import generic
import csv
import io
from django.urls import reverse_lazy
from django.views import generic
from .forms import CSVUploadForm, DoctorForm, ScheduleForm
from .models import Data, Category, Menu, Hospital, Page, Doctor, Schedule
import sys
import random
from bs4 import BeautifulSoup as bs
from django.views.decorators.clickjacking import xframe_options_exempt
import json

csv.field_size_limit(sys.maxsize)


class Home(generic.TemplateView):
    """
    home page
    """
    template_name = "data/home.html"


class PostImport(generic.FormView):
    """
    csv file import
    """
    template_name = 'data/import.html'
    success_url = reverse_lazy('data:home')
    form_class = CSVUploadForm

    def form_valid(self, form):
        # csv.readerに渡すため、TextIOWrapperでテキストモードなファイルに変換
        csvfile = io.TextIOWrapper(form.cleaned_data['file'], encoding='utf-8')
        reader = csv.reader(csvfile)
        # 1行ずつ取り出し、作成していく
        for index, row in enumerate(reader):
            data, created = Data.objects.get_or_create(pk=index)
            data.url = row[0]
            data.html = row[1]
            data.save()
        return super().form_valid(form)


class CheckData(generic.ListView):
    """
    data list & search data
    """
    template_name = 'data/check.html'
    model = Data
    context_object_name = 'datas'
    paginate_by = 10

    # 検索機能
    def get_queryset(self):
        datas = Data.objects.all()
        length = datas.count()
        if 'q' in self.request.GET and self.request.GET['q'] is not None:
            q = self.request.GET['q']
            datas = datas.filter(url__icontains=q)
        return datas


def data_choice(request):
    """
    data category choice
    :param request:
    :return:
    """
    if request.method == "POST":
        category = request.POST["category"]
        if category == "医師情報":
            check = "choice"
            form = DoctorForm()
            params = {
                "check": check,
                "forms": form,
                "model": "Doctor",
                "form": "DoctorForm"
            }
        elif category == "診療時間と担当医師":
            check = "choice"
            form = ScheduleForm()
            params = {
                "check": check,
                "forms": form,
                "model": "Schedule",
                "form": "ScheduleForm"
            }
    else:
        check = "data_import"
        categories = ["医師情報", "診療時間と担当医師"]

        params = {
            "check": "category",
            "categories": categories
        }

    return render(request, 'data/data_choice.html', params)


def extraction(request):
    if request.method == "POST":
        code = request.POST["code"]
        soup = bs(request.POST["html"], 'html.parser')
        url = request.POST["url"]
        html = eval(code)
        print("#################################################################")
        print(type(html))
        print("#################################################################")
        htmls = bs(str(html), 'html.parser')

        category = list(Category.objects.values_list('name', flat=True))
        print(category)
        menu = list(Menu.objects.values_list('name', flat=True))
        hospital = list(Hospital.objects.values_list('name', flat=True))
        params = {
            'html': str(html),
            'check': "extract",
            'url': url,
            'category': category,
            'menu': menu,
            'hospital': hospital,
        }

        return render(request, 'data/data_imports.html', params)


def register(request):
    if request.method == "POST":
        # obj = eval(request.POST["model"])
        # friend = eval(request.POST, instance=obj)
        model = eval(request.POST["model"])()
        data = eval(request.POST["form"])(request.POST, instance=model)
        data.save()

        return render(request, 'data/data_choice.html')
