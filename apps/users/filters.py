import django_filters

from django.db.models import Q


class BusinessUserFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', field_name='fullname')
    phone = django_filters.CharFilter(lookup_expr='icontains', field_name='phone')
    role = django_filters.UUIDFilter(field_name='role_id')
    shift = django_filters.UUIDFilter(field_name='shift_id')
    ordering = django_filters.OrderingFilter(
        fields=("created_at", "fullname", "phone", "username")
    )

    search = django_filters.CharFilter(method="search_filter")

    def search_filter(self, queryset, name, value):
        if value:
            return queryset.filter(Q(fullname__icontains=value) |
                                   Q(phone__icontains=value))
        return queryset
