from django.urls import path
from . import views


app_name = "cards"
urlpatterns = [
    path("view/<str:setcode>/<str:collectornum>/", views.card_detail, name="card_detail"),
]
