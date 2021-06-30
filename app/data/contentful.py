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

hospital_space = management_client.spaces().find('bknvzq2w20dx')
environment = hospital_space.environments().find('master')


# 病院名追加
def add_hospital_name(entry_id: str, hospital_name: str, space_id="bknvzq2w20dx", environment_id='master'):
    """
    病院名を追加する関数。
    -------------------------------------------------------------
    entry_id(str) : 追加するデータのID(任意),
    hospital_name(str) : 追加する病院名,
    """
    hospital_space = management_client.spaces().find('bknvzq2w20dx')
    environment = hospital_space.environments().find('master')

    entry_attributes = {
        'content_type_id': 'hospital',
        'fields': {
            'name': {
                'en-US': hospital_name
            },
        }
    }

    # register
    new_entry = environment.entries().create(
        entry_id,
        entry_attributes
    )

    # Publish
    entry = environment.entries().find(entry_id)
    entry.publish()


