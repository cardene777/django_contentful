def get_url(hospital_name, field_name):
    url_dict: dict = {
        "藤元メディカルシステム": {"TOP": "http://www.fujimoto.com/"},
        "藤元総合病院": {
            "診療科・部門": "http://fgh.fujimoto.com/services/",
            "医療関係者の皆さまへ": "http://fgh.fujimoto.com/relation/",
            "藤元総合病院について": "http://fgh.fujimoto.com/about/",
            "外来受診について": "http://fgh.fujimoto.com/outpatients/",
            "入院のご案内について": "http://fgh.fujimoto.com/admitted/",
            "はじめてご来院の方へ": "http://fgh.fujimoto.com/first/",
            "お知らせ": "http://fgh.fujimoto.com/information/"
        },
        "藤元病院": {"TOP": "http://www.fujimoto.or.jp/fujimoto/"},
        "大吾病院": {"TOP": "http://www.fujimoto.or.jp/daigo/"},
        "星井眼科": {"TOP": "http://hoshii.fujimoto.com/"},
        "グリーンホーム": {"TOP": "http://www.fujimoto.or.jp/green/"},
        "藤元メディカルシステム付属医療専門学校": {"TOP": "http://fujimoto.ac.jp/"},
        "社会福祉法人常緑会": {"TOP": "http://joryokukai.com"},
        "社会福祉法人星空の都": {"TOP": "http://ichijukai.com"},
        "採用情報": {"TOP": "htt,p://recruit.fujimoto.com"},
        "星空の都なかごう": {"TOP": "http://www.joryokukai.com/nakagoen/"},
        "星空の都みまた": {"TOP": "http://www.joryokukai.com/sankoen/"},
        "星空の都さどわら": {"TOP": "http://www.ichijukai.com/syokoen/"},
        "星空の都かみながえ": {"TOP": "http://www.joryokukai.com/sazankaen/"},
        "星空の都ポピー保育園": {"TOP": "http://www.joryokukai.com/poppy/"},
        "星空の都みやざき": {"TOP": "http://www.ichijukai.com/hyugaen/"},
    }
    return url_dict[hospital_name][field_name]


def get_field(hospital_name):
    field_dict: dict = {
        "藤元メディカルシステム": ["TOP"],
        "藤元総合病院": ["診療科・部門", "医療関係者の皆さまへ", "藤元総合病院について", "外来受診について", "入院のご案内について",
                   "はじめてご来院の方へ", "お知らせ"],
        "藤元病院": ["TOP"],
        "大吾病院": ["TOP"],
        "星井眼科": ["TOP"],
        "グリーンホーム": ["TOP"],
        "藤元メディカルシステム付属医療専門学校": ["TOP"],
        "社会福祉法人常緑会": ["TOP"],
        "社会福祉法人星空の都": ["TOP"],
        "採用情報": ["TOP"],
        "星空の都なかごう": ["TOP"],
        "星空の都みまた": ["TOP"],
        "星空の都さどわら": ["TOP"],
        "星空の都かみながえ": ["TOP"],
        "星空の都ポピー保育園": ["TOP"],
        "星空の都みやざき": ["TOP"]
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
