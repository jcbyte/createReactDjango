from django.urls import path

from .views import Foo

urlpatterns = [
    path("Foo", Foo.as_view()),
]
