from django.urls import path

from rest_framework.routers import SimpleRouter
from .views import AuthorViewSet, CategoryViewSet, BookViewSet

router = SimpleRouter()
router.register('authors', AuthorViewSet, basename="authors")
router.register('categories', CategoryViewSet, basename="categories")
router.register('', BookViewSet, basename="books")

urlpatterns = router.urls
