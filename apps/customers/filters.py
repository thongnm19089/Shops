import django_filters

from django.db.models import Q


class CustomerFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', field_name='name')
    phone = django_filters.CharFilter(lookup_expr='icontains', field_name='phone')
    email = django_filters.CharFilter(lookup_expr='icontains', field_name='email')
    code = django_filters.CharFilter(lookup_expr='icontains', field_name='code')
    role = django_filters.UUIDFilter(field_name='role_id')
    shift = django_filters.UUIDFilter(field_name='shift_id')
    ordering = django_filters.OrderingFilter(
        fields=("created_at", "name", "phone", "username")
    )

    search = django_filters.CharFilter(method="search_filter")

    def search_filter(self, queryset, name, value):
        if value:
            return queryset.filter(Q(name__icontains=value) |
                                   Q(ascii_name__icontains=value)|
                                   Q(phone__icontains=value))
        return queryset
