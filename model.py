from pymodm import connect, fields, MongoModel
from pymongo.write_concern import WriteConcern
from pymodm.connection import connect
import config
from pymodm.connection import connect


connect(config.MONGO_URL, alias="user")


class User(MongoModel):
    viber_id = fields.CharField(primary_key=True)
    kindle_mail = fields.EmailField()
    search_temporary = fields.ListField()
    time = fields.FloatField()
    status = fields.IntegerField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'user'