from rest_framework.pagination import PageNumberPagination


class MaterialsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class LessonPagination(MaterialsPagination):
    page_size = 5


class CoursePagination(MaterialsPagination):
    page_size = 8
