from django.shortcuts import render
from django.views import generic
import csv
import io
import re
from django.urls import reverse_lazy
from django.views import generic
from .forms import CSVUploadForm, CategoryFrom, PageForm, TagForm, ElementForm, DoctorForm, \
    OutpatientDoctorForm, DepartmentTimeScheduleForm
from .models import Hospital, Data, Category, Page, Tag, Element, Doctor, OutpatientDoctor, \
    DepartmentTimeSchedule
import sys
import random
from bs4 import BeautifulSoup as bs
import json
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q


from .category import get_url, get_field, get_form
from .contentful import add_hospital, add_category, add_tag, add_page, add_element, \
    add_doctor, add_outpatient_doctor, add_time_department_schedule

csv.field_size_limit(sys.maxsize)


def normalization(data):
    data: str = re.sub("[\t\n\r 　]+", "", data)
    return data


def scraping_href(html):
    main: str = str(bs(html, 'html.parser').find_all())
    links: str = bs(main, 'html.parser').find_all("a")
    a_dict: dict = {}
    for link in links:
        if ".jpg" in str(link) or "<img" in str(link):
            continue
        print(link)
        a_dict[link.attrs['href']] = re.sub(r'[\n\t<span>/]', "", str(link.contents[0]))
    return a_dict


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CheckData, self).get_context_data()
        context["data_all"] = Data.objects.all().count()
        context["data_no"] = Data.objects.filter(check="no").count()
        return context


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
    return ["ページ", "要素", "医師情報", "外来担当医師", "受付・診療時間"]


def register(requests):
    if requests.method == "POST":
        hospital: str = requests.POST["hospital"]
        field: str = requests.POST["field"]
        url: str = get_url(hospital, field)

        top_url: str = url

        # 表示するHTMLを調整
        if requests.POST["message"] == "button":
            href: str = normalization(requests.POST["href"])
            html: str = Data.objects.get(url=href).html
        # セレクター
        elif requests.POST["message"] == "code":
            html: str = requests.POST["html"]
            html: str = bs(html, 'html.parser')
            html = str(str(eval(requests.POST["code"]))[1:-1])
        else:
            html: str = Data.objects.filter(url=url)[0].html

        # aタグを抜き出す
        a_dict: dict = scraping_href(html)

        # 登録フォーム群
        try:
            url = requests.POST["href"]
        except:
            pass

        params: dict = {
            "hospital": hospital,
            "field": field,
            "url": url,
            "html": html,
            "a_dict": a_dict,
            "forms": form_list(),
            "top_url": top_url
        }
        return render(requests, 'data/register.html', params)


def create_category(requests):
    if requests.method == "POST":
        # カテゴリ新規追加
        if requests.POST["message"] == "add_category":
            requests_post = requests.POST.copy()
            html: str = normalization(requests_post["html"])
            requests_post["url"] = normalization(requests_post["url"])
            requests_post["html"] = html
            requests_post["hospital"] = Hospital.objects.get(name=requests_post["hospital"]).id
            data = CategoryFrom(requests_post)

            if data.is_valid():
                print("検証に成功。データを保存。")
                data.save()
            else:
                print("検証に失敗。検証に失敗した理由。")
                print(data.errors)

            # aタグを抜き出す
            a_dict: dict = scraping_href(html)

            params: dict = {
                "hospital": requests.POST["hospitals"],
                "field": requests.POST["field"],
                "url": requests.POST["href"],
                "html": requests.POST["html"],
                "message": "done",
                "forms": form_list(),
                "a_dict": a_dict,
                "top_url": requests.POST["top_url"]
            }

            return render(requests, 'data/register.html', params)

        forms = CategoryFrom()
        params: dict = {
            "hospital": requests.POST["hospital"],
            "field": requests.POST["field"],
            "url": requests.POST["href"],
            "html": requests.POST["html"],
            "forms": forms,
            "top_url": requests.POST["top_url"]
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
                "forms_name": requests.POST["forms_name"],
                "top_url": requests.POST["top_url"]
            }

            return render(requests, 'data/data_register.html', params)

        forms = TagForm()
        params: dict = {
            "hospital": requests.POST["hospital"],
            "field": requests.POST["field"],
            "url": requests.POST["href"],
            "html": requests.POST["html"],
            "forms_name": requests.POST["forms_name"],
            "forms": forms,
            "top_url": requests.POST["top_url"]
        }
        return render(requests, 'data/create_tag.html', params)


def data_register(requests):
    if requests.method == "POST":
        if requests.POST["message"] == "data_register":
            # データ登録
            requests_post = requests.POST.copy()
            urls: str = normalization(requests_post["url"])
            html: str = normalization(requests_post["html"])
            requests_post["url"] = urls
            requests_post["html"] = html
            forms: str = requests.POST["forms_name"]
            model: str = eval(forms.strip("Form"))()
            data = eval(forms)(requests.POST, instance=model)

            if data.is_valid():
                print("検証に成功。データを保存。")
                data.save()
                data_check: set = Data.objects.get(url=urls)
                if data_check.check == "no":
                    data_check.check = "ok"
                    if data.is_valid():
                        data_check.save()
                    else:
                        print(urls)
                        print(data_check.errors)
            else:
                print("検証に失敗。検証に失敗した理由。")
                print(data.errors)

            # aタグを抜き出す
            a_dict: dict = scraping_href(html)

            params: dict = {
                "hospital": requests.POST["hospitals"],
                "field": requests.POST["field"],
                "url": requests.POST["href"],
                "html": requests.POST["html"],
                "message": "done",
                "forms": form_list(),
                "a_dict": a_dict,
                "top_url": requests.POST["top_url"]
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
            "forms_name": forms,
            "top_url": requests.POST["top_url"]
        }
        return render(requests, 'data/data_register.html', params)


def import_contentful(requests):
    names: list = ["病院名", "カテゴリ名", "ページ", "グループ名", "タグ名", "要素名", "医師情報", "外来担当医師", "診療時間"]
    if requests.method == "POST":
        def change_pykakasi(data):
            import pykakasi
            kks = pykakasi.kakasi()
            kks.setMode("H", "a")  # default: Hiragana -> Roman
            kks.setMode("K", "a")  # default: Katakana -> Roman
            kks.setMode("J", "a")  # default: Japanese -> Roman
            kks.setMode("r", "Hepburn")  # default: use Hepburn Roman table
            kks.setMode("s", True)  # default: Separator
            kks.setMode("C", True)  # default: Capitalize
            conv = kks.getConverter()
            # lowercase
            data_id: str = conv.do(data).lower()
            # remove space
            data_id = re.sub("[ 　]", "", data_id)
            return data_id

        contentful_dict: dict = {
            "病院名": [Hospital, add_hospital, "pattern1"],
            "カテゴリ名": [Category, add_category, "pattern1"],
            "ページ": [Page, add_page],
            "タグ名": [Tag, add_tag],
            "要素名": [Element, add_element],
            "医師情報": [Doctor, add_doctor],
            "外来担当医師": [OutpatientDoctor, add_outpatient_doctor],
            "診療時間": [DepartmentTimeSchedule, add_time_department_schedule],
        }
        contentful_name: str = requests.POST["contentful_name"]
        register_data: list = contentful_dict[contentful_name]

        model_all: set = register_data[0].objects.all()
        data_count: str = str(Hospital.objects.all().count() + Category.objects.all().count() + \
                              Page.objects.all().count() + Tag.objects.all().count() + \
                              Element.objects.all().count() + Doctor.objects.all().count() + OutpatientDoctor.objects.all().count() + \
                              DepartmentTimeSchedule.objects.all().count())
        print(data_count)
        try:
            datas: list = register_data[0].objects.values_list("name", flat=True)
        except:
            try:
                datas: list = register_data[0].objects.values_list("title", flat=True)
            except:
                try:
                    datas: list = register_data[0].objects.values_list("day_week", flat=True)
                except:
                    datas: list = register_data[0].objects.values_list("check", flat=True)
                finally:
                    datas: list = list(map(lambda one_data: one_data+data_count, datas))

            # setting id
        count: int = 0
        for index, data in enumerate(datas):
            data_id: str = change_pykakasi(data)
            try:
                if contentful_name == "病院名":
                    register_data[1](data_id, data)

                elif contentful_name == "カテゴリ名":
                    try:
                        relation_category: str = change_pykakasi(model_all[index].category.name)
                    except:
                        relation_category: bool = False
                    register_data[1](data_id, change_pykakasi(model_all[index].hospital.name),
                                     model_all[index].name, relation_category)

                elif contentful_name == "ページ":
                    try:
                        tags: list = [tag.name for tag in model_all[index].tag]
                    except:
                        tags: bool = False
                    register_data[1](data_id, change_pykakasi(model_all[index].category.name),
                                     model_all[index].title, model_all[index].html, tags)

                elif contentful_name == "グループ名":
                    try:
                        print("True")
                        print(model_all[index].tag_set.all())
                        tags: list = [tag.name for tag in model_all[index].tag]
                        print(tags)
                    except:
                        print("False")
                        tags: bool = False
                    register_data[1](data_id, change_pykakasi(model_all[index].category.name),
                                     model_all[index].name, tags)

                elif contentful_name == "タグ名":
                    register_data[1](data_id, model_all[index].name)
                elif contentful_name == "要素名":
                    register_data[1](data_id, model_all[index].category.name, model_all[index].title, model_all[index].html,
                                     model_all[index].tag.name)
                elif contentful_name == "医師情報":
                    register_data[1](data_id, model_all[index].category.name, model_all[index].name, model_all[index].title,
                                     model_all[index].profile, model_all[index].image, model_all[index].tag.name)
                elif contentful_name == "外来担当医師":
                    register_data[1](data_id, model_all[index].category.name, model_all[index].doctor.name,
                                     model_all[index].day_week, model_all[index].am_pm, model_all[index].other,
                                     model_all[index].tag.name)
                elif contentful_name == "診療時間":
                    register_data[1](data_id, model_all[index].category.name, model_all[index].check,
                                     model_all[index].start_time, model_all[index].end_time, model_all[index].type,
                                     model_all[index].tag.name)

                count += 1
            except Exception as e:
                print(e)
                continue

        params: dict = {
            "names": names,
            "message": "done",
            "count": count,
        }
    else:
        params: dict = {
            "names": names,
        }
    return render(requests, 'data/import_contentful.html', params)