from django.shortcuts import render
from django.views import generic
import csv
import io
import re
from django.urls import reverse_lazy
from django.views import generic
from .forms import CSVUploadForm, CategoryFrom, PageForm, GroupForm, TagForm, ElementForm, DoctorForm, \
    OutpatientDoctorForm
from .models import Hospital, Data, Category, Page, Group, Tag, Element, Doctor, OutpatientDoctor, \
    DepartmentTimeSchedule
import sys
import random
from bs4 import BeautifulSoup as bs
import json
from django.utils.datastructures import MultiValueDictKeyError

from .category import get_url, get_field, get_form
from .contentful import add_hospital_name

csv.field_size_limit(sys.maxsize)


def normalization(data):
    data: str = re.sub("[\t\n\r 　]+", "", data)
    return data


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


def home(requests):
    """
    choice hospital name
    """

    # 病院名
    hospitals = Hospital.objects.all()
    hospitals_list: json = json.dumps([hospital.name for hospital in hospitals])

    # フィールド　
    fields_dict: json = json.dumps([get_field(hospital.name) for hospital in hospitals])

    params: dict = {
        "hospitals": hospitals,
        "hospitals_list": hospitals_list,
        "fields_dict": fields_dict
    }
    return render(requests, 'data/home.html', params)


def form_list():
    return ["ページ", "グループ", "要素", "医師情報", "外来担当医師", "受付・診療時間"]


def register(requests):
    if requests.method == "POST":
        hospital: str = requests.POST["hospital"]
        field: str = requests.POST["field"]
        url: str = get_url(hospital, field)

        # 表示するHTMLを調整
        if requests.POST["message"] == "button":
            html: str = Data.objects.get(url=requests.POST["href"]).html
        # セレクター
        elif requests.POST["message"] == "code":
            html: str = requests.POST["html"]
            html: str = bs(html, 'html.parser')
            html = str(str(eval(requests.POST["code"]))[1:-1])
        else:
            html: str = Data.objects.filter(url=url)[0].html

        # aタグを抜き出す
        main: str = str(bs(html, 'html.parser').find_all(id="main-content"))
        links: str = bs(main, 'html.parser').find_all("a")
        a_dict: dict = {}
        for link in links:
            a_dict[link.attrs['href']] = re.sub(r'[\n\t]', "", link.contents[0])

        # 登録フォーム群

        params: dict = {
            "hospital": hospital,
            "field": field,
            "url": url,
            "html": html,
            "a_dict": a_dict,
            "forms": form_list()
        }
        return render(requests, 'data/register.html', params)


def create_category(requests):
    if requests.method == "POST":
        # カテゴリ新規追加
        if requests.POST["message"] == "add_category":
            requests_post = requests.POST.copy()
            requests_post["url"] = normalization(requests_post["url"])
            requests_post["html"] = normalization(requests_post["html"])
            requests_post["hospital"] = Hospital.objects.get(name=requests_post["hospital"]).id
            data = CategoryFrom(requests_post)

            if data.is_valid():
                print("検証に成功。データを保存。")
                data.save()
            else:
                print("検証に失敗。検証に失敗した理由。")
                print(data.errors)
                print(requests_post["hospital"])
                print(requests_post["category"])
                print(requests_post["name"])
                print(requests_post["url"])

            params: dict = {
                "hospital": requests.POST["hospitals"],
                "field": requests.POST["field"],
                "url": requests.POST["href"],
                "html": requests.POST["html"],
                "message": "done",
                "forms": form_list()
            }

            return render(requests, 'data/register.html', params)

        forms = CategoryFrom()
        params: dict = {
            "hospital": requests.POST["hospital"],
            "field": requests.POST["field"],
            "url": requests.POST["href"],
            "html": requests.POST["html"],
            "forms": forms
        }
        return render(requests, 'data/create_category.html', params)


def create_tag(requests):
    if requests.method == "POST":
        # カテゴリ新規追加
        if requests.POST["message"] == "add_tag":
            requests_post = requests.POST.copy()
            requests_post["html"] = normalization(requests_post["html"])
            data = TagForm(requests_post)

            if data.is_valid():
                print("検証に成功。データを保存。")
                data.save()
            else:
                print("検証に失敗。検証に失敗した理由。")
                print(data.errors)

            params: dict = {
                "hospital": requests.POST["hospitals"],
                "field": requests.POST["field"],
                "url": requests.POST["href"],
                "html": requests.POST["html"],
                "message": "done",
                "forms": eval(requests.POST["forms_name"])(),
                "form": form_list(),
                "forms_name": requests.POST["forms_name"]
            }

            return render(requests, 'data/data_register.html', params)

        forms = TagForm()
        params: dict = {
            "hospital": requests.POST["hospital"],
            "field": requests.POST["field"],
            "url": requests.POST["href"],
            "html": requests.POST["html"],
            "forms_name": requests.POST["forms_name"],
            "forms": forms

        }
        return render(requests, 'data/create_tag.html', params)


def data_register(requests):
    if requests.method == "POST":
        if requests.POST["message"] == "data_register":
            # データ登録
            requests_post = requests.POST.copy()
            requests_post["url"] = normalization(requests_post["url"])
            requests_post["html"] = normalization(requests_post["html"])
            forms: str = requests.POST["forms_name"]
            model: str = eval(forms.strip("Form"))()
            data = eval(forms)(requests.POST, instance=model)

            if data.is_valid():
                print("検証に成功。データを保存。")
                data.save()
            else:
                print("検証に失敗。検証に失敗した理由。")
                print(data.errors)

            params: dict = {
                "hospital": requests.POST["hospitals"],
                "field": requests.POST["field"],
                "url": requests.POST["href"],
                "html": requests.POST["html"],
                "message": "done",
                "forms": form_list()
            }

            return render(requests, 'data/register.html', params)

        # フォーム情報取得
        forms = get_form(requests.POST["form"])
        params: dict = {
            "hospital": requests.POST["hospital"],
            "field": requests.POST["field"],
            "url": requests.POST["href"],
            "html": requests.POST["html"],
            "forms": eval(forms)(),
            "form": form_list(),
            "forms_name": forms
        }
        return render(requests, 'data/data_register.html', params)


def import_contentful(requests):
    if requests.method == "POST":
        contentful_dict: dict = {
            "病院名": [Hospital, add_hospital_name]
        }
        register_data: list = contentful_dict[requests.POST["contentful_name"]]
        datas: list = register_data[0].objects.values_list("name", flat=True)
        for data in datas:
            import pykakasi
            kks = pykakasi.kakasi()
            kks.setMode("H", "a")  # default: Hiragana -> Roman
            kks.setMode("K", "a")  # default: Katakana -> Roman
            kks.setMode("J", "a")  # default: Japanese -> Roman
            kks.setMode("r", "Hepburn")  # default: use Hepburn Roman table
            kks.setMode("s", True)  # default: Separator
            kks.setMode("C", True)  # default: Capitalize
            conv = kks.getConverter()
            data_id = conv.do(data)
            data_id = re.sub("[ 　]", "", data_id)
            register_data[1](data_id, data)

        params: dict = {
            "names": ["病院名", "医師情報"],
            "message": "done"
        }
    else:
        params: dict = {
            "names": ["病院名", "医師情報"],
        }
    return render(requests, 'data/import_contentful.html', params)