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
from django.utils.datastructures import MultiValueDictKeyError

csv.field_size_limit(sys.maxsize)
CATEGORIES = Category.objects.values_list("name", flat=True)


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
        # 検索
        try:
            search = request.POST["search"]
            url = request.POST["url"]
            urls = Data.objects.get(url=url)
            params = {
                "check": "category",
                "categories": CATEGORIES,
                "url": urls.url,
                "html": urls.html
            }
            return render(request, 'data/data_choice.html', params)
        except MultiValueDictKeyError:
            pass
        # カテゴリごとに渡すデータを変更。
        category = request.POST["category"]
        url = request.POST["url"]
        html = request.POST["html"]
        if category == "医師情報":
            forms = DoctorForm()
            model = "Doctor"
            form = "DoctorForm"
        elif category == "診療時間と担当医師":
            forms = ScheduleForm()
            model = "Schedule"
            form = "ScheduleForm"
        params = {
            "check": "choice",
            "forms": forms,
            "model": model,
            "form": form,
            "url": url,
            "html": html
        }
    else:
        check = "data_import"
        datas = Data.objects.all()
        data = random.choice(datas)
        params = {
            "check": "category",
            "categories": CATEGORIES,
            "url":data.url,
            "html": data.html
        }

    return render(request, 'data/data_choice.html', params)


def register(request):
    def set_hospital_name(url):
        urls = {
            "http://fujimoto.com": "藤元メディカルシステム",
            "http://fujimoto.or.jp": "藤元メディカルシステム",
            "http://fgh.fujimoto.com": "藤元総合病院",
            "http://fujimoto.or.jp/fujimoto": "藤元病院",
            "http://fujimoto.or.jp/green": "グリーンホーム",
            "http://fujimoto.ac.jp": "藤元メディカルシステム付属医療専門学校",
            "http://fujimoto.or.jp/kensin/hayasuzu": "藤元総合病院",
            "http://fujimoto.or.jp/kensin/central": "藤元総合病院",
            "http://fujimoto.or.jp/daigo": "大吾病院",
            "http://hoshii.fujimoto.com": "星井眼科",
            "http://joryokukai.com": "社会福祉法人常緑会",
            "http://ichijukai.com": "社会福祉法人星空の都",
            "http://recruit.fujimoto.com": "採用情報"
        }
        split_url = url.split("/")
        split_url[2] = split_url[2].replace("www.", "")
        for index in range(len(split_url)):
            new_url = "/".join(split_url[: len(split_url) - index])
            try:
                hospital_name = urls[new_url]
                break
            except:
                continue
        else:
            hospital_name = None
        return hospital_name
    if request.method == "POST":
        model = eval(request.POST["model"])()
        url = set_hospital_name(request.POST["url"])
        request_post = request.POST.copy()
        request_post["hospital"] = Hospital.objects.filter(name=url).values_list('name', flat=True)[0]
        data = eval(request_post["form"])(request.POST, instance=model)
        print(request_post)
        data.save()

        params = {
            "check": "category",
            "categories": CATEGORIES,
            "url": request.POST["url"],
            "html": request.POST["html"]
        }
        return render(request, 'data/data_choice.html', params)
    else:
        return render(request, 'data/data_register.html')


def extraction(request):
    if request.method == "POST":
        check = request.POST['check']
        forms = request.POST['forms']
        model = request.POST['model']
        form = request.POST['form']
        url = request.POST['url']
        html = request.POST['html']
        print("check", check)

        params = {
            "check": check,
            "forms": forms,
            "model": model,
            "form": form,
            "url": url,
            "html": html
        }

        return render(request, 'data/data_choice.html', params)