import django_filters

from myapp.models import User


class UserFilter(django_filters.FilterSet):
    is_blocked = django_filters.BooleanFilter(name='is_blocked', help_text='1 -> all, 2 -> true, 3 -> false')
    # use date_joined range, you cant query exact date
    date_joined__gte = django_filters.DateTimeFilter(name='date_joined', lookup_expr='gte',
                                                     help_text='Date joined is greater than or equal to')
    date_joined__lte = django_filters.DateTimeFilter(name='date_joined', lookup_expr='lte',
                                                     help_text='Date joined is less than or equal to')

    class Meta:
        model = User
        fields = {
            'is_blocked', 'date_joined__gte', 'date_joined__lte'
        }
