from django.urls import path 

from . import views 

"""
    Для модульности у каждого приложения должен быть свой urls.py 
    - где задается соответствие между веб-адресом и представлением 
"""

# Пространство имен приложения, 
# но необходимо оставлять префикс в urls.py проекта, нужно, чтобы задать url в шаблонах 

# Нужно немного приучиться к отладке
app_name = "django_tutorial"

urlpatterns = [
    path("", views.index, name='index'),

    path("last_5/", views.index_last_5, name="last_5"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    
    path("<int:question_id>/detail_template/", views.detail_templated, name="detail_templated"),

    path("last_5_templated/", views.index_last_5_templated, name="last_5_templated"),
    path("<int:question_id>/detail_form/", views.detail_form, name="detail_form"),
    path("<int:question_id>/vote_form/", views.vote_form, name="vote_form"),
    path("<int:question_id>/results_templated/", views.results_templated, name="results_templated"),

    path("gv/", views.IndexView.as_view(), name="gv_index"),
    path("gv/<int:pk>/", views.DetailView.as_view(), name="gv_detail"),
    path("gv/<int:pk>/results/", views.ResultsView.as_view(), name="gv_results"),
    path("gv/<int:question_id>/vote/", views.vote_form_2, name="vote_form_2"),
]
