from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views

urlpatterns = [
    # djoser
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    # django rest framework social auth 2
    path('auth/', include('rest_framework_social_oauth2.urls')),
    # "Users endpoints
    path('users', views.user_list),
    path('users/email/<str:email>', views.user_detail_email),
    path('users/<int:id>', views.user_detail_id),
    # activation and password reset urls
    path('users/activate/<str:uid>/<str:token>', views.activation),
    path('users/password-reset/<str:uid>/<str:token>', views.reset),
    # houses endpoints APIs
    path('all_houses', views.get_houses),
    path('all_houses/random', views.get_houses_random),
    path('houses/<int:owner_id>', views.get_houses_owner_id),
    path('shuffled_houses', views.get_shuffled_houses),
    path('all_houses/point', views.get_houses_around_specific_point),
    path('all_houses/categories/<int:category_id>', views.get_houses_category_id),
    path('create_house', views.create_house),
    path('house_images', views.house_image),
    # categories
    path('categories', views.get_categories)
]
