from django_filters.rest_framework import FilterSet

from api.models import Computer

from django_filters import filters
class LimitFilter:

    def filter_queryset(self,request,queryset,view):
        limit=request.query_params.get("limit")
        if limit and queryset:
            limit=int(limit)
            return queryset[:limit]

        return queryset


#django_filter过滤类

class ComputerFilterSet(FilterSet):
    min_price=filters.NumberFilter(field_name="price",lookup_expr="gte")
    max_price=filters.NumberFilter(field_name="price",lookup_expr="lte")
    class Meta:
        model=Computer
        fields=("price","min_price","max_price")