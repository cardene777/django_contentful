from django.shortcuts import render
from django.views import generic
import csv
import io
from django.urls import reverse_lazy
from django.views import generic
from .forms import CSVUploadForm
from .models import Data
import sys
import random
from bs4 import BeautifulSoup as bs

csv.field_size_limit(sys.maxsize)


class Home(generic.TemplateView):
    template_name = "data/home.html"


class PostImport(generic.FormView):
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


def data_import(request):
    if request.method == "POST":
        url = request.POST["url"]
        data = Data.objects.get(url=url)

    else:
        datas = Data.objects.all()
        data = random.choice(datas)
    html = str(bs(data.html, 'html.parser'))

    params = {
        "url": data.url,
        "html": html
    }

    return render(request, 'data/data_import.html', params)


def extraction(request):
    if request.method == "POST":
        extract = "extract"
        code = request.POST["code"]
        soup = bs(request.POST["html"], 'html.parser')
        url = request.POST["url"]
        html = eval(code)
        print(type(html))
        params = {
            'html': str(html),
            'check': 'extract',
            'url': url
        }

        return render(request, 'data/data_import.html', params)

