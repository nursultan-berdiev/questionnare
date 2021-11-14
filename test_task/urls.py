from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/questionnaire/', include('questionnaire.urls')),
    path('api/v1/authentication/', include('rest_framework.urls'))
]
