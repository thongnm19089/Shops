import django_filters


class InventoryHistoryFilterSet(django_filters.FilterSet):
    is_exported = django_filters.BooleanFilter(field_name="is_exported")
    product = django_filters.UUIDFilter(field_name="product")