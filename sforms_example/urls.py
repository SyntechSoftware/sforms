from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from django.contrib import admin
from .views import SampleFormView, SampleTagView
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('template/', SampleTagView.as_view()),
    path('<slug:sform_id>/', SampleFormView.as_view(), name="form_example"),
]

urlpatterns += static(settings.STATIC_URL)

