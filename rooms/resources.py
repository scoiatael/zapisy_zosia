from import_export import resources
from .models import *

class RoomResource(resources.ModelResource):

    class Meta:
        model = Room
        fields = ('id', 'number', 'capacity', 'description',)
