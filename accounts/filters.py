# django_filters was installed already and just needed to be imported.
# was installed with pip 
import django_filters
from django_filters import DateFilter, CharFilter

# import everything from models.py
# only works because models.py is in same directory as this file
from .models import *

# this python class will filter for us results to be used in searching for specific orders
# (this can be named whatever deemed)
class OrderFilter(django_filters.FilterSet):
    # the field_name is what we want this to be related to
    # lookup expression is saying that we want the date to be
    # the date we asked for or greater than that date (gte = Greater Than or Equal to)
    startDate =  DateFilter(field_name="date_created", lookup_expr="gte")
    # lte = Less Than or Equal to
    endDate =  DateFilter(field_name="date_created", lookup_expr="lte")
    # "icontains" just means to ignore case sensitivity
    note = CharFilter(field_name="note", lookup_expr="icontains")

    # minimum of two attributes needed
    class Meta:
        model = Order
        # which fields we want to allow
        fields = '__all__' # we said here that we want all fields
        # all the fields we want to exclude (we are excluding because we want to customise them later)
        exclude = ['customer', 'date_created']

