from django.urls import path

from . import views

urlpatterns = [
      path("create/", views.create_presentation, name="create_presentation"),
      path("<uuid:presentation_id>/", views.get_presentation, name="get_presentation"),
      path("<uuid:presentation_id>/reactions/", views.add_reaction, name="add_reaction"),
  ]