from bloop import (
    BaseModel, Boolean, Column, Number, String,
    UUID, Map, List, GlobalSecondaryIndex
)

class SampleProject(BaseModel):
    class Meta:
        table_name = 'sp-{STAGE}'
        billing = {
            "mode": "on_demand"
        }

    # big 7
    entity_id = Column(UUID, hash_key=True)
    version = Column(UUID, range_key=True)

    # API attrs
    obj_type = Column(String)
    user_id = Column(UUID)
    affiliate_id = Column(String, default='')
    email = Column(String)

    # this index can be used for checking affiliate_id collision
    by_affiliate_id_and_obj_type = GlobalSecondaryIndex(
        projection='keys',
        hash_key='affiliate_id',
        range_key='obj_type'
    )

    by_user_id_and_obj_type = GlobalSecondaryIndex(
        projection='all',
        hash_key='user_id',
        range_key='obj_type'
    )

    by_email_and_obj_type = GlobalSecondaryIndex(
        projection='all',
        hash_key='email',
        range_key='obj_type'
    )