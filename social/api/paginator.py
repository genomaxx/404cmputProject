from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class CustomPagination(PageNumberPagination):
    def get_paginated_posts(self, data, request):
        result = OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('posts', data),
            ])

        if ('size' in request.GET):
            result['size'] = request.GET['size']
            return Response(result)
        result['size'] = 20;
        return Response(result)
    
    def get_paginated_comments(self, data, request):
        result = OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('comments', data),
            ])

        if ('size' in request.GET):
            result['size'] = request.GET['size']
            return Response(result)
        result['size'] = 20;
        return Response(result)