import django_filters

from myapp.models import User


class UserFilter(django_filters.FilterSet):
    is_blocked = django_filters.BooleanFilter(name='is_blocked')
    date_joined = django_filters.DateTimeFilter(name='date_joined', lookup_expr='exact')
    date_joined__gte = django_filters.DateTimeFilter(name='date_joined', lookup_expr='gte')
    date_joined__lte = django_filters.DateTimeFilter(name='date_joined', lookup_expr='lte')

    class Meta:
        model = User
        fields = {
            'is_blocked', 'date_joined', 'date_joined__gte', 'date_joined__lte'
        }
