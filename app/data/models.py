from django.db import models
import sys
import csv
from django.utils import timezone

csv.field_size_limit(sys.maxsize)


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
        return str(self.url)


class Tag(models.Model):
    """
    tag data
    """

    class Meta:
        verbose_name = "タグ"
        verbose_name_plural = "タグ"

    name = models.CharField(
        verbose_name="タグ",
        max_length=50
    )

    def __str__(self):
        return self.name


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

    category = models.ForeignKey(
        "self",
        verbose_name="関連カテゴリ",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="sub_category"
    )

    name = models.CharField(
        verbose_name="カテゴリ名",
        max_length=100,
        unique=True
    )

    url = models.TextField(
        verbose_name="URL",
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

    category = models.OneToOneField(
        Category,
        verbose_name="関連カテゴリ",
        on_delete=models.CASCADE
    )

    title = models.CharField(
        verbose_name="ページタイトル",
        max_length=200,
        blank=True,
        null=True,
    )

    html = models.TextField(
        verbose_name="HTML",
    )

    tag = models.ManyToManyField(
        Tag,
        verbose_name="タグ",
        blank=True,
        null=True,
    )

    url = models.TextField(
        verbose_name="URL",
    )

    def __str__(self):
        return self.html


# class Group(models.Model):
#     """
#     group data
#     """
#     class Meta:
#         verbose_name = "グループ"
#         verbose_name_plural = "グループ"
#
#     category = models.ForeignKey(
#         Category,
#         verbose_name="関連カテゴリ",
#         on_delete=models.CASCADE
#     )
#
#     name = models.CharField(
#         verbose_name="グループ名",
#         max_length=200
#     )
#
#     url = models.TextField(
#         verbose_name="URL",
#     )
#
#     tag = models.ManyToManyField(
#         Tag,
#         verbose_name="タグ",
#         blank=True
#     )
#
#     def __str__(self):
#         return self.name


class Element(models.Model):
    """
    element data
    """
    class Meta:
        verbose_name = "要素"
        verbose_name_plural = "要素"

    category = models.ForeignKey(
        Category,
        verbose_name="関連カテゴリ名",
        on_delete=models.CASCADE
    )

    title = models.CharField(
        verbose_name="タイトル",
        max_length=200,
        blank=True,
        null=True,
    )

    html = models.TextField(
        verbose_name="内容"
    )

    url = models.TextField(
        verbose_name="URL",
    )

    tag = models.ManyToManyField(
        Tag,
        verbose_name="タグ",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.html


class Doctor(models.Model):
    """
    doctor information
    """

    class Meta:
        verbose_name = "医師情報"
        verbose_name_plural = "医師情報"

    category = models.ForeignKey(
        Category,
        verbose_name="関連カテゴリ名",
        on_delete=models.CASCADE
    )

    name = models.CharField(
        verbose_name="医師名",
        max_length=50,
    )

    title = models.CharField(
        verbose_name="肩書き",
        max_length=250,
    )

    profile = models.TextField(
        verbose_name="プロフィール",
    )

    url = models.TextField(
        verbose_name="URL",
    )

    tag = models.ManyToManyField(
        Tag,
        verbose_name="タグ",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class OutpatientDoctor(models.Model):
    """
    outpatient data
    """
    class Meta:
        verbose_name = "外来担当医師"
        verbose_name_plural = "外来担当医師"

    category = models.ForeignKey(
        Category,
        verbose_name="関連カテゴリ名",
        on_delete=models.CASCADE
    )

    doctor = models.ManyToManyField(
        Doctor,
        verbose_name="医師名",
    )

    DAY_WEEK_CHOICE = (
        (1, "月曜日"),
        (2, "火曜日"),
        (3, "水曜日"),
        (4, "木曜日"),
        (5, "金曜日"),
    )

    day_week = models.CharField(
        verbose_name="曜日",
        max_length=10,
        choices=DAY_WEEK_CHOICE
    )

    AM_PM_CHOICE = (
        (1, "午前"),
        (2, "午後")
    )

    am_pm = models.CharField(
        verbose_name="午前・午後",
        max_length=10,
        choices=AM_PM_CHOICE
    )

    other = models.TextField(
        verbose_name="補足"
    )

    url = models.TextField(
        verbose_name="URL",
    )

    tag = models.ManyToManyField(
        Tag,
        verbose_name="タグ",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.doctor


class DepartmentTimeSchedule(models.Model):
    """
    Department Time Schedule
    """

    class Meta:
        verbose_name = "受付・診療時間"
        verbose_name_plural = "受付・診療時間"

    category = models.ForeignKey(
        Category,
        verbose_name="関連カテゴリ名",
        on_delete=models.CASCADE
    )

    CHECK_CHOICES = (
        ("受付", 1),
        ("診療", 2),
    )

    check = models.CharField(
        verbose_name="受付・診療選択",
        max_length=10,
        choices=CHECK_CHOICES
    )

    start_time = models.TimeField(
        verbose_name="開始時間",
        default=0
    )

    end_time = models.TimeField(
        verbose_name="終了時間",
        default=0
    )

    TYPE_CHOICES = (
        ("初診", 1),
        ("再診", 2),
    )

    type = models.CharField(
        verbose_name="初診・再診",
        max_length=10,
        choices=TYPE_CHOICES
    )

    url = models.TextField(
        verbose_name="URL",
    )

    tag = models.ManyToManyField(
        Tag,
        verbose_name="タグ",
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.check)
