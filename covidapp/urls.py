from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns =[
    path('',views.home,name='home'),
    path('survey',views.takesurvey,name='survey'),
    path('tracker',views.trackerna,name='tracker'),
    path('finder',views.finder,name='finder'),
    path('signup', views.signup,name="signup"),
    path('fallback',views.fallback,name='fallback'),
    path('chatindex', views.chatindex, name='chatindex'),
    path('chat', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
    path('api/users/<int:pk>', views.user_list, name='user-detail'),
    path('api/users', views.user_list, name='user-list'),
    path('logout', LogoutView.as_view(next_page='home'), name='logout'),
]