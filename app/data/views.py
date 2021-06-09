from django.shortcuts import render
from django.views import generic
import csv
import io
from django.urls import reverse_lazy
from django.views import generic
from .forms import CSVUploadForm, DoctorForm, ScheduleForm, PageForm
from .models import Data, Category, Hospital, Page, Doctor, DepartmentSchedule
import sys
import random
from bs4 import BeautifulSoup as bs
import json
from django.utils.datastructures import MultiValueDictKeyError

csv.field_size_limit(sys.maxsize)

FORMS: dict = {
            "診療科・部門": ["ページ", "医師情報", "診療時間"]
        }


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
            data.check = "no"
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
            datas = datas.filter(check="no").filter(url__icontains=q)
        return datas


def data_choice(request):
    """
    data category choice
    :param request:
    :return:
    """
    if request.method == "POST":
        if request.POST["message"] == "choice_category":
            url: str = request.POST["category"]
            datas = Data.objects.filter(url__contains=url)
            params: dict = {
                "message": "choice_data",
                "datas": datas
            }
        elif request.POST["message"] == "choice_data":
            url: str = request.POST["data"]
            data = Data.objects.get(url=url)
            params: dict = {
                "message": "get_data",
                "data": data
            }
        elif request.POST["message"] == "choice_form":
            url: str = request.POST["url"]
            html: str = request.POST["html"]
            html: str = str(bs(html, 'html.parser'))
            form: str = request.POST["register_form"]
            forms = eval(form)()
            params: dict = {
                "message": "select_form",
                "url": url,
                "html": html,
                "forms": forms,
                "register_form": form,
            }

    return render(request, 'data/data_choice.html', params)


def extract(request):
    if request.method == "POST":
        code: str = request.POST["code"]
        url: str = request.POST["url"]
        html: str = request.POST["html"]
        html = bs(html, 'html.parser')
        new_html = eval(code)
        register_form = request.POST["register_form"]
        forms = eval(register_form)()
        params: dict = {
            "message": "extract_html",
            "url": url,
            "html": str(html),
            "new_html": new_html,
            "register_form": register_form,
            "forms": forms
        }

    return render(request, 'data/data_choice.html', params)


def register(request):
    def set_hospital_name(url):
        """
        病院名とURLの変換
        :param url:
        :return:
        """
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
        model: dict = {
            "DoctorForm": Doctor,
            "ScheduleForm": DepartmentSchedule,
            "PageForm": Page
        }
        request_post = request.POST.copy()
        request_post["hospital"] = set_hospital_name(request_post["url"])
        select_model = model[request.POST["register_form"]]
        data = eval(request.POST["register_form"])(request.POST, instance=select_model())
        # data = select_model(request.POST)
        data.save()

        url: str = request.POST["url"].replace("\r", "").replace("\n", "")
        data = Data.objects.get(url=url)
        params: dict = {
            "message": "get_data",
            "data_check": "on",
            "data": data
        }


        # model = eval(request.POST["model"])()
        # url = set_hospital_name(request.POST["url"])
        # request_post = request.POST.copy()
        # request_post["hospital"] = Hospital.objects.filter(name=url).values_list('name', flat=True)[0]
        # data = eval(request_post["form"])(request.POST, instance=model)
        # print(request_post)
        # data.save()

        return render(request, 'data/data_choice.html', params)
    else:
        categories: list = Category.objects.all()
        params: dict = {
            "categories": categories,
        }
        return render(request, 'data/data_register.html', params)


def choice_hospital(request):
    """
    choice hospital name
    """
    hospitals = Hospital.objects.all()
    params: dict = {
        "hospitals": hospitals
    }
    return render(request, 'data/choice_hospital.html', params)


def choice_category(request):
    """
    choice hospital category
    """
    hospital_id: int = Hospital.objects.filter(name=request.POST["hospital"])[0].id
    categories: list = Category.objects.filter(hospital=hospital_id)
    params: dict = {
        "categories": categories,
    }
    return render(request, 'data/choice_category.html', params)


def choice_url(request):
    category: str = request.POST["category"]
    url: str = Category.objects.filter(name=category)[0].url
    urls: list = list(Data.objects.filter(url__contains=url).values_list("url", flat=True))
    params: dict = {
        "urls": urls,
        "category": category
    }
    return render(request, 'data/choice_url.html', params)


def choice_form(request):
    if request.method == "POST":
        category: str = request.POST["category"]
        select_forms: list = FORMS[category]
        url: str = request.POST["url"]
        if request.POST["message"] == "extract":
            html: str = request.POST["html"]
            html: str = bs(html, 'html.parser')
            extract_html = str(str(eval(request.POST["code"]))[1:-1])
        else:
            html: str = Data.objects.filter(url=url)[0].html
            extract_html: str = "none"
        params: dict = {
            "select_forms": select_forms,
            "url": url,
            "html": html,
            "category": category,
            "extract_html": extract_html
        }
        return render(request, 'data/choice_form.html', params)


def data_register(request):
    if request.method == "POST":
        if request.POST["message"] == "register":
            model: dict = {
                "DoctorForm": Doctor(),
                "ScheduleForm": DepartmentSchedule(),
                "PageForm": Page()
            }
            one_form: str = request.POST["one_form"]
            select_model: str = model[one_form]
            data = eval(one_form)(request.POST, instance=select_model)
            data.save()

            category: str = Category.objects.filter(id=request.POST["category"])[0].name
            select_forms: list = FORMS[category]
            url: str = request.POST["url"].replace("\r", "").replace("\n", "")
            html: str = Data.objects.filter(url=url)[0].html
            extract_html: str = "none"
            params: dict = {
                "select_forms": select_forms,
                "url": url,
                "html": html,
                "category": category,
                "extract_html": extract_html
            }
            return render(request, 'data/choice_form.html', params)

        select_form: dict = {
            "ページ": "PageForm",
            "医師情報": "DoctorForm",
            "診療時間": "ScheduleForm"
        }
        category: str = request.POST["category"]
        url: str = request.POST["url"]
        html: str = request.POST["html"]
        form: str = request.POST["select_form"]
        forms: str = eval(select_form[form])()
        one_form: str = select_form[form]
        params: dict = {
            "url": url,
            "html": html,
            "category": category,
            "forms": forms,
            "one_form": one_form
        }
    return render(request, 'data/data_register.html', params)

