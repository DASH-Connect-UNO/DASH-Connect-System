from django.urls import path
from .views import (
    pillars_home, list_scholarships, add_scholarship, edit_scholarship,
    list_hardships, add_hardship, edit_hardship, list_basic_need_supports, add_basic_need_support, edit_basic_need_support,
    toggle_basic_need_support, toggle_hardship, toggle_scholarship,
)

urlpatterns = [
    path('', pillars_home, name='pillars_home'),
    path('scholarships/', list_scholarships, name='list_scholarships'),
    path('scholarships/add/', add_scholarship, name='add_scholarship'),
    path('scholarships/edit/<int:id>/', edit_scholarship, name='edit_scholarship'),
    path('hardships/', list_hardships, name='list_hardships'),
    path('hardships/add/', add_hardship, name='add_hardship'),
    path('hardships/edit/<int:id>/', edit_hardship, name='edit_hardship'),
    path('basic_need_supports/', list_basic_need_supports, name='list_basic_need_supports'),
    path('basic_need_supports/add/', add_basic_need_support, name='add_basic_need_support'),
    path('basic_need_supports/edit/<int:id>/', edit_basic_need_support, name='edit_basic_need_support'),
    path('basic_need_support/toggle/<int:id>/', toggle_basic_need_support, name='toggle_basic_need_support'),
    path('hardship/toggle/<int:id>/', toggle_hardship, name='toggle_hardship'),
    path('scholarship/toggle/<int:id>/', toggle_scholarship, name='toggle_scholarship'),
]

