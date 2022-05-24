from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import (LoginView, LogoutView,PasswordChangeView, PasswordResetDoneView)
from frontend.views import inicio
from evidencia.views import condiciones, estandares, MedioVerificacion, guardar_revision, guardar_evidencia, listar_revision, recomendaciones, requerimientos, obtener_evidencia

urlpatterns = [
    url('admin/', admin.site.urls),
    url('login/', LoginView.as_view(template_name='login/index.html'), name='login'),
    url('logout/', LogoutView.as_view(template_name='login/index.html'), name='logout'),
    path('', inicio, name='incio'),
    #Condiciones
    path('condiciones/', condiciones, name='condiciones'),
    path('requerimientos/', requerimientos, name='requerimientos'),
    path('recomendaciones/', recomendaciones, name='recomendaciones'),
    # url('estandares/(?P<oficina>[0-9]{4})/', estandares, name='estandares'),
    path('estandares/<int:oficina_id>/', estandares, name='estandares'),
    url('guardar_revision/', guardar_revision, name='guardar_revision'),
    url('guardar_evidencia/', guardar_evidencia, name='guardar_evidencia'),
    url('listar_revision/', listar_revision, name='listar_revision'),
    url('obtener_evidencia/', obtener_evidencia, name='obtener_evidencia'),
    # url('evidencia/(?P<id_medio_verificacion>[0-9]+)/', evidencia, name='evidencia'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
