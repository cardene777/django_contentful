def get_url(hospital_name, field_name):
    url_dict: dict = {
        "藤元メディカルシステム": {"お知らせ": "url"},
        "藤元総合病院": {
            "診療科・部門": "http://fgh.fujimoto.com/services/",
            "医療関係者の皆さまへ": "http://fgh.fujimoto.com/relation/",
            "藤元総合病院について": "http://fgh.fujimoto.com/about/",
            "外来受診について": "http://fgh.fujimoto.com/outpatients/",
            "入院のご案内について": "http://fgh.fujimoto.com/admitted/",
            "はじめてご来院の方へ": "http://fgh.fujimoto.com/first/",
            "お知らせ": "http://fgh.fujimoto.com/information/"
        },
        "藤元病院": {"お知らせ": "url"},
        "大吾病院": {"お知らせ": "url"},
        "星井眼科": {"お知らせ": "url"},
        "グリーンホーム": {"お知らせ": "url"},
        "藤元メディカルシステム付属医療専門学校": {"お知らせ": "url"},
        "社会福祉法人常緑会": {"お知らせ": "url"},
        "社会福祉法人星空の都": {"お知らせ": "url"},
        "採用情報": {"お知らせ": "url"},

    }
    return url_dict[hospital_name][field_name]


def get_field(hospital_name):
    field_dict: dict = {
        "藤元メディカルシステム": ["お知らせ"],
        "藤元総合病院": ["診療科・部門", "医療関係者の皆さまへ", "藤元総合病院について", "外来受診について", "入院のご案内について",
                   "はじめてご来院の方へ", "お知らせ"],
        "藤元病院": ["お知らせ"],
        "大吾病院": ["お知らせ"],
        "星井眼科": ["お知らせ"],
        "グリーンホーム": ["お知らせ"],
        "藤元メディカルシステム付属医療専門学校": ["お知らせ"],
        "社会福祉法人常緑会": ["お知らせ"],
        "社会福祉法人星空の都": ["お知らせ"],
        "採用情報": ["お知らせ"]
    }
    fields: list = field_dict[hospital_name]
    return fields


def get_form(form_name):
    forms: dict = {
        "ページ": "PageForm",
        "グループ": "GroupForm",
        "要素": "ElementForm",
        "医師情報": "DoctorForm",
        "外来担当医師": "OutpatientDoctorForm",
        "受付・診療時間": "DepartmentTimeScheduleForm"

    }
    form = forms[form_name]
    return form
