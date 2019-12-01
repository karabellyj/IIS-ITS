# -*- coding: utf-8 -*-
from django.conf.urls import include
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
from django.urls import path
import users.views as user_views
from core.views import HomeView

urlpatterns = [
    # add your own patterns here
    path('', HomeView.as_view(), name='home'),
    path('', include('core.urls', namespace='core')),
    path('', include('users.urls', namespace='users')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', user_views.SignUpView.as_view(), name='signup'),
] + aldryn_addons.urls.patterns() + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
