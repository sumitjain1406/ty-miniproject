from django.urls import path
from . import views

urlpatterns = [
    path('',views.calculate),
    path('plan/',views.plan)
]
