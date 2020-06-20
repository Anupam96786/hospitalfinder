from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf.urls import url

urlpatterns =[
    path('',views.home,name='home'),
    path('survey',views.takesurvey,name='survey'),
    path('tracker',views.trackerna,name='tracker'),
    path('finder',views.finder,name='finder'),
    path('signup', views.signup,name="signup"),
    path('fallback',views.fallback,name='fallback'),
    path('awareness',views.awareness,name='awareness'),
    path('diet',views.diet,name='diet'),
    path('chatindex', views.chatindex, name='chatindex'),
    path('chat', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
    path('api/users/<int:pk>', views.user_list, name='user-detail'),
    path('api/users', views.user_list, name='user-list'),
    path('logout', LogoutView.as_view(next_page='home'), name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]