from bloop import (
    BaseModel, Boolean, Column, Number, String,
    UUID, Map, List, GlobalSecondaryIndex
)


class Deployment(BaseModel):
    class Meta:
        table_name = 'sp-deployment'
        billing = {
            "mode": "on_demand"
        }

    script_number = Column(Number, range_key=True)
    stage = Column(String, hash_key=True)