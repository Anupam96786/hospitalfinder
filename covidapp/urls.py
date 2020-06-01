from django.urls import path
from . import views
urlpatterns =[
    path('',views.home,name='home'),
    path('survey',views.takesurvey,name='survey'),
    path('tracker',views.trackerna,name='tracker'),
    path('finder',views.finder,name='finder'),
    path('signup', views.signup,name="signup"),
    path('fallback',views.fallback,name='fallback')
]