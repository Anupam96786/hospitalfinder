from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('covidapp.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^serviceworker.js', (TemplateView.as_view(template_name="serviceworker.js", content_type='application/javascript', )), name='serviceworker.js'),
]
