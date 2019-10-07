# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    # add your own patterns here
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', include('core.urls', namespace='core')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
] + aldryn_addons.urls.patterns() + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
