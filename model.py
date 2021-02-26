from pymodm import connect, fields, MongoModel
from pymongo.write_concern import WriteConcern
from pymodm.connection import connect


connect("mongodb://localhost:27017/chatbot", alias="my-app")


class User(MongoModel):
    viber_id = fields.CharField(primary_key=True)
    kindle_mail = fields.EmailField()
    search_temporary = fields.ListField()
    history = fields.ListField()
    status = fields.IntegerField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'