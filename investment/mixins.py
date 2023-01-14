import json

from rest_framework.viewsets import GenericViewSet


class FilterCustomAttrsMixin(GenericViewSet):
    """ Миксин, который применяется для viewsets и позволяет делать гибкие и сложные фильтрации по JSONFIELD с именем
    custom_attrs"""

    def get_queryset(self):
        queryset = self.queryset
        filter_string = self.request.query_params.get('custom_attrs')

        if filter_string:
            filter_dictionary = json.loads(filter_string)
            queryset = queryset.filter(**filter_dictionary)

        return queryset