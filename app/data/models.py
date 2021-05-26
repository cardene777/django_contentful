from django.db import models
import sys
import csv

csv.field_size_limit(sys.maxsize)


class Hospital(models.Model):
    class Meta:
        verbose_name = "病院名"
        verbose_name_plural = "病院名"

    name = models.CharField(
        verbose_name="病院名",
        max_length=100,
    )

    url = models.TextField(
        verbose_name="URL"
    )

    def __str__(self):
        return self.name


class Category(models.Model):
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

    def __str__(self):
        return self.name


class Menu(models.Model):
    class Meta:
        verbose_name = "メニュー"
        verbose_name_plural = "メニュー"

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

    CHOICES_MENU = (
        ("ナビゲーションメニュー", "navigation_menu"),
        ("サイドメニュー", "side_menu"),
    )
    name = models.CharField(
        verbose_name="メニュー名",
        max_length=100,
        choices=CHOICES_MENU
    )

    href = models.TextField(
        verbose_name="リンク名",
    )

    url = models.TextField(
        verbose_name="URL"
    )

    def __str__(self):
        return self.name


class Page(models.Model):
    class Meta:
        verbose_name = "ページ"
        verbose_name_plural = "ページ"

    hospital = models.ForeignKey(
        Hospital,
        verbose_name="関連病院名",
        on_delete=models.CASCADE
    )

    menu = models.ForeignKey(
        Menu,
        verbose_name="関連メニュー",
        on_delete=models.CASCADE
    )

    html = models.TextField(
        verbose_name="HTML",
    )

    url = models.TextField(
        verbose_name="URL"
    )

    def __str__(self):
        return self.html


class Data(models.Model):
    class Meta:
        verbose_name = "データ"
        verbose_name_plural = "データ"

    url = models.CharField(
        verbose_name="URL",
        max_length=250
    )

    html = models.TextField(
        verbose_name="HTML"
    )

    def __str__(self):
        return f"{self.url} {self.html}"


class Doctor(models.Model):
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

    image = models.TextField(
        verbose_name="医師画像",
    )

    def __str__(self):
        return self.name


class Schedule(models.Model):
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
