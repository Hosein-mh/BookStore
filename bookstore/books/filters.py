import django_filters
from books.models import Book, Tag

class BookFilter(django_filters.FilterSet):
  title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
  category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
  merchant = django_filters.CharFilter(field_name='merchant__username', lookup_expr='icontains')
  # tags = django_filters.ModelMultipleChoiceFilter(
  #   queryset=Tag.objects.all(),
  #   to_field_name='name',
  #   conjoined=True
  # )

  class Meta:
    model = Book
    fields = ['title', 'category']#, 'tags']