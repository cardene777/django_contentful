import contentful_management
import contentful

MANAGEMENT_API_TOKEN = "CFPAT-_iiQsKzvMSbzicou9BNfhVChBEH1DMUxdohjawn9o8A"

management_client = contentful_management.Client(MANAGEMENT_API_TOKEN)

client = contentful.Client(
    # space ID
    'bknvzq2w20dx',
    # access token
    'oXLeYelyR98C2Pdm1nAJzgZHW8dJl2oR8rSrBwUGOvA'
)


def setting():
    hospital_space = management_client.spaces().find('bknvzq2w20dx')
    environment = hospital_space.environments().find('master')
    return hospital_space, environment


def register_publish(environment, entry_id, entry_attributes):
    # register
    new_entry = environment.entries().create(
        entry_id,
        entry_attributes
    )

    # Publish
    entry = environment.entries().find(entry_id)
    entry.publish()


# 病院名追加
def add_hospital(entry_id: str, hospital_name: str):
    """
    病院名を追加する関数。
    -------------------------------------------------------------
    entry_id(str): 追加するデータのID,
    hospital_name(str): 追加する病院名,
    """
    hospital_space, environment = setting()

    entry_attributes = {
        'content_type_id': 'hospital',
        'fields': {
            'name': {
                'en-US': hospital_name
            },
        }
    }

    # register
    # Publish
    register_publish(environment, entry_id, entry_attributes)


# カテゴリ追加
def add_category(entry_id: str, relation_hospital_id: str, category_name: str, relation_category_id=False):
    """
    病院名を追加する関数。
    -------------------------------------------------------------
    entry_id(str) : 追加するデータのID,
    relation_hospital_id(str): 関連病院id,
    relation_category_id(str)[任意]: 関連カテゴリ名,
    category_name(str): カテゴリ名,
    """
    hospital_space, environment = setting()

    print(entry_id, relation_hospital_id, category_name)

    if relation_category_id:
        entry_attributes = {
            'content_type_id': 'category',
            'fields': {
                "hospital": {
                    "en-US": [{
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_hospital_id
                        }
                    }]
                },
                "category": {
                    "en-US": [{
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_category_id
                        }
                    }]
                },
                'name': {
                    'en-US': category_name
                },
            }
        }
    else:
        entry_attributes = {
            'content_type_id': 'category',
            'fields': {
                "hospital": {
                    "en-US": [{
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_hospital_id
                        }
                    }]
                },
                'name': {
                    'en-US': category_name
                },
            }
        }

        # register
        # Publish
        register_publish(environment, entry_id, entry_attributes)


# タグ追加
def add_tag(entry_id: str, tag: str):
    """
    タグを追加する関数。
    -------------------------------------------------------------
    entry_id(str) : 追加するデータのID,
    tag(str) : タグ名,
    """
    hospital_space, environment = setting()

    entry_attributes = {
        'content_type_id': 'tag',
        'fields': {
            'tag': {
                'en-US': tag
            },
        }
    }

    # register
    # Publish
    register_publish(environment, entry_id, entry_attributes)


# ページ追加
def add_page(entry_id: str, relation_category_id: str, title: str, html: str, tags=False):
    """
    ページを追加する関数。
    -------------------------------------------------------------
    entry_id(str) : 追加するデータのID,
    relation_category_id(str): 関連カテゴリid,
    title(str): ページタイトル名,
    html(str): HTML　,
    tags(list)[任意]: 関連タグ,
    """
    hospital_space, environment = setting()

    if tags:
        tag_list: list = [{"sys": {"type": "Link", "linkType": "Entry", "id": tag}} for tag in tags]
        entry_attributes = {
            'content_type_id': 'page',
            'fields': {
                "category": {
                    "en-US": {
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_category_id
                        }
                    }
                },
                'title': {
                    'en-US': title
                },
                'html': {
                    'en-US': html
                },
                'tag': {
                    'en-US': tag_list
                }
            }
        }
    else:
        entry_attributes = {
            'content_type_id': 'page',
            'fields': {
                "category": {
                    "en-US": {
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_category_id
                        }
                    }
                },
                'title': {
                    'en-US': title
                },
                'html': {
                    'en-US': html
                },
            }
        }

        # register
        # Publish
        register_publish(environment, entry_id, entry_attributes)



# 要素追加
def add_element(entry_id: str, relation_group_id: str, title: str, html: str, tags=False):
    """
    要素を追加する関数。
    -------------------------------------------------------------
    entry_id(str) : 追加するデータのID,
    relation_group_id(str): 関連グループid,
    title(str): 要素タイトル,
    html(str): HTML　,
    tags(list)[任意]: 関連タグ,
    """

    hospital_space, environment = setting()

    if tags:
        tag_list: list = [{"sys": {"type": "Link", "linkType": "Entry", "id": tag}} for tag in tags]
        entry_attributes = {
            'content_type_id': 'element',
            'fields': {
                "group": {
                    "en-US": [{
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_group_id
                        }
                    }]
                },
                'title': {
                    'en-US': title
                },
                'html': {
                    'en-US': html
                },
                'tag': {
                    'en-US': tag_list
                }
            }
        }
    else:
        entry_attributes = {
            'content_type_id': 'element',
            'fields': {
                "group": {
                    "en-US": [{
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_group_id
                        }
                    }]
                },
                'title': {
                    'en-US': title
                },
                'html': {
                    'en-US': html
                },
            }
        }

        # register
        # Publish
        register_publish(environment, entry_id, entry_attributes)


# 医師情報追加
def add_doctor(entry_id: str, relation_group_id: str, name: str, title: str, profile: str, tags=False):
    """
    医師情報を追加する関数。
    -------------------------------------------------------------
    entry_id(str) : 追加するデータのID,
    relation_group_id(str): 関連グループid,
    name(str): 医師名,
    title(str): 肩書き,
    profile(str): 医師情報　,
    tags(list)[任意]: 関連タグ,
    """

    hospital_space, environment = setting()

    if tags:
        tag_list: list = [{"sys": {"type": "Link", "linkType": "Entry", "id": tag}} for tag in tags]
        entry_attributes = {
            'content_type_id': 'doctor',
            'fields': {
                "group": {
                    "en-US": [{
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_group_id
                        }
                    }]
                },
                'name': {
                    'en-US': name
                },
                'title': {
                    'en-US': title
                },
                'profile': {
                    'en-US': profile
                },
                'tag': {
                    'en-US': tag_list
                }
            }
        }
    else:
        entry_attributes = {
            'content_type_id': 'doctor',
            'fields': {
                "group": {
                    "en-US": [{
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_group_id
                        }
                    }]
                },
                'name': {
                    'en-US': name
                },
                'title': {
                    'en-US': title
                },
                'profile': {
                    'en-US': profile
                },
            }
        }

        # register
        # Publish
        register_publish(environment, entry_id, entry_attributes)


# 医師情報追加
def add_outpatient_doctor(entry_id: str, relation_group_id: str, relation_doctor_id: str,
                          dayWeek: str, amPm: str, other: str, tags=False):
    """
    医師情報を追加する関数。
    -------------------------------------------------------------
    entry_id(str) : 追加するデータのID,
    relation_group_id(str): 関連グループid,
    relation_doctor_id(str): 関連医師id,
    dayWeek(str): 曜日,
    amPm(str): 午前・午後　,
    other(str): 補足,
    tags(list)[任意]: 関連タグ,
    """

    hospital_space, environment = setting()

    if tags:
        tag_list: list = [{"sys": {"type": "Link", "linkType": "Entry", "id": tag}} for tag in tags]
        entry_attributes = {
            'content_type_id': 'outpatientDoctor',
            'fields': {
                "group": {
                    "en-US": [{
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_group_id
                        }
                    }]
                },
                "doctor": {
                    "en-US": [{
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_doctor_id
                        }
                    }]
                },
                'dayWeek': {
                    'en-US': dayWeek
                },
                'amPm': {
                    'en-US': amPm
                },
                'other': {
                    'en-US': other
                },
                'tag': {
                    'en-US': tag_list
                }
            }
        }
    else:
        entry_attributes = {
            'content_type_id': 'outpatientDoctor',
            'fields': {
                "group": {
                    "en-US": [{
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_group_id
                        }
                    }]
                },
                "doctor": {
                    "en-US": [{
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_doctor_id
                        }
                    }]
                },
                'dayWeek': {
                    'en-US': dayWeek
                },
                'amPm': {
                    'en-US': amPm
                },
                'other': {
                    'en-US': other
                },
            }
        }

        # register
        # Publish
        register_publish(environment, entry_id, entry_attributes)


# 医師情報追加
def add_time_department_schedule(entry_id: str, relation_group_id: str, check: str,
                                 startTime: str, endTime: str, types: str, tags=False):
    """
    医師情報を追加する関数。
    -------------------------------------------------------------
    entry_id(str) : 追加するデータのID,
    relation_group_id(str): 関連グループid,
    check(str): 受付時間・診療時間選択,
    startTime(str): 開始時間　,
    endTime(str): 終了時間,
    types(str): 初診・再診選択,
    tags(list)[任意]: 関連タグ,
    """

    hospital_space, environment = setting()

    if tags:
        tag_list: list = [{"sys": {"type": "Link", "linkType": "Entry", "id": tag}} for tag in tags]
        entry_attributes = {
            'content_type_id': 'timeDepartmentSchedule',
            'fields': {
                "group": {
                    "en-US": [{
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_group_id
                        }
                    }]
                },
                'check': {
                    'en-US': check
                },
                'startTime': {
                    'en-US': startTime
                },
                'endTime': {
                    'en-US': endTime
                },
                'type': {
                    'en-US': types
                },
                'tag': {
                    'en-US': tag_list
                }
            }
        }
    else:
        entry_attributes = {
            'content_type_id': 'timeDepartmentSchedule',
            'fields': {
                "group": {
                    "en-US": [{
                        "sys": {
                            "type": "Link",
                            "linkType": "Entry",
                            "id": relation_group_id
                        }
                    }]
                },
                'check': {
                    'en-US': check
                },
                'startTime': {
                    'en-US': startTime
                },
                'endTime': {
                    'en-US': endTime
                },
                'type': {
                    'en-US': types
                },
            }
        }

        # register
        # Publish
        register_publish(environment, entry_id, entry_attributes)