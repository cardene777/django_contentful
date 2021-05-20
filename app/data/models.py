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
        return f"{self.name} {self.url}"


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
        return f"{self.hospital} {self.name}"


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
        return f"{self.hospital} {self.category} {self.name} {self.href} {self.url}"


class LinkList(models.Model):
    class Meta:
        verbose_name = "リンクリスト"
        verbose_name_plural = "リンクリスト"

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
        return f"{self.hospital} {self.menu} {self.html} {self.url}"


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
        return f"{self.hospital} {self.menu} {self.html} {self.url}"


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
