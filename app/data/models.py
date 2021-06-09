from django.db import models
import sys
import csv
from django.utils import timezone

csv.field_size_limit(sys.maxsize)


class Hospital(models.Model):
    """
    hospital name
    """

    class Meta:
        verbose_name = "病院名"
        verbose_name_plural = "病院名"

    name = models.CharField(
        verbose_name="病院名",
        max_length=100,
        unique=False
    )

    url = models.TextField(
        verbose_name="URL",
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    category name
    """

    class Meta:
        verbose_name = "カテゴリ"
        verbose_name_plural = "カテゴリ"

    hospital = models.ForeignKey(
        Hospital,
        verbose_name="関連病院名",
        on_delete=models.CASCADE
    )

    name = models.CharField(
        verbose_name="カテゴリ名",
        max_length=100
    )

    url = models.TextField(
        verbose_name="URL",
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    class Meta:
        verbose_name = "タグ"
        verbose_name_plural = "タグ"

    name = models.CharField(
        verbose_name="タグ",
        max_length=50
    )

    def __str__(self):
        return self.name


class Page(models.Model):
    """
    page data
    """

    class Meta:
        verbose_name = "ページ"
        verbose_name_plural = "ページ"

    hospital = models.ForeignKey(
        Hospital,
        verbose_name="関連病院名",
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        verbose_name="関連カテゴリ",
        on_delete=models.CASCADE
    )

    html = models.TextField(
        verbose_name="HTML",
    )

    url = models.TextField(
        verbose_name="URL",
    )

    tag = models.ManyToManyField(
        Tag,
        verbose_name="タグ",
        blank=True
    )

    def __str__(self):
        return self.html


class Data(models.Model):
    """
    hospital page data list
    """

    class Meta:
        verbose_name = "データ"
        verbose_name_plural = "データ"

    url = models.TextField(
        verbose_name="URL",
    )

    html = models.TextField(
        verbose_name="HTML"
    )

    CHECK_CHOICE = (
        ("ok", "ok"),
        ("no", "no")
    )

    check = models.CharField(
        verbose_name="振り分け判定",
        max_length=10,
        choices=CHECK_CHOICE
    )

    def __str__(self):
        return f"{self.url} {self.html}"


class Doctor(models.Model):
    """
    doctor information
    """

    class Meta:
        verbose_name = "医師情報"
        verbose_name_plural = "医師情報"

    hospital = models.ForeignKey(
        Hospital,
        verbose_name="関連病院名",
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        verbose_name="肩書き",
        max_length=200,
    )

    name = models.CharField(
        verbose_name="医師名",
        max_length=50,
    )

    profile = models.TextField(
        verbose_name="プロフィール",
    )

    image = models.URLField(
        verbose_name="医師画像",
        max_length=250
    )

    def __str__(self):
        return self.name


class DepartmentSchedule(models.Model):
    """
    Consultation Time
    """

    class Meta:
        verbose_name = "診療時間と担当医師"
        verbose_name_plural = "診療時間と担当医師"

    hospital = models.ForeignKey(
        Hospital,
        verbose_name="関連病院名",
        on_delete=models.CASCADE,
    )

    doctor = models.ForeignKey(
        Doctor,
        verbose_name="医師",
        on_delete=models.CASCADE,
    )

    CHOICES_WEEK = (
        ("月曜日", "Monday"),
        ("火曜日", "Tuesday"),
        ("水曜日", "Wednesday"),
        ("木曜日", "Thursday"),
        ("金曜日", "Friday"),
    )

    week = models.CharField(
        verbose_name="曜日",
        max_length=50,
        choices=CHOICES_WEEK
    )

    CHOICES_AM_PM = (
        ("午前", "午前"),
        ("午後", "午後"),
    )

    AP = models.CharField(
        verbose_name="午前・午後",
        max_length=50,
        choices=CHOICES_AM_PM
    )

    def __str__(self):
        return str(self.doctor)


class News(models.Model):
    class Meta:
        verbose_name = "ニュース"
        verbose_name_plural = "ニュース"

    hospital = models.ForeignKey(
        Hospital,
        verbose_name="関連病院名",
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        verbose_name="関連カテゴリ",
        on_delete=models.CASCADE
    )

    INFORMATION_TYPE = (
        ("information", "お知らせ"),
        ("media", "メディア"),
        ("close_substitute", "休診・代診"),
        ("free", "無料講座")
    )

    type = models.CharField(
        verbose_name="お知らせ種類",
        max_length=100,
        choices=INFORMATION_TYPE
    )

    html = models.TextField(
        verbose_name="HTML",
    )

    url = models.TextField(
        verbose_name="URL",
    )

    def __str__(self):
        return self.html


class DepartmentTime(models.Model):
    class Meta:
        verbose_name = "時間"
        verbose_name_plural = "時間"

    hospital = models.ForeignKey(
        Hospital,
        verbose_name="関連病院名",
        on_delete=models.CASCADE
    )

    KIND_CHOICES = (
        ("reception", "受付時間"),
        ("diagnosis", "診療時間")
    )

    kind = models.CharField(
        verbose_name="種類",
        choices=KIND_CHOICES,
        max_length=10
    )

    am_start = models.TimeField(
        verbose_name="午前開始時間",
        default=timezone.datetime.now()
    )

    am_end = models.TimeField(
        verbose_name="午前終了時間",
        default=timezone.datetime.now()
    )

    pm_start = models.TimeField(
        verbose_name="午後開始時間",
        default=timezone.datetime.now()
    )

    pm_end = models.TimeField(
        verbose_name="午後終了時間",
        default=timezone.datetime.now()
    )

    def __str__(self):
        return self.name