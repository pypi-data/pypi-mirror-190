# -*- coding: utf-8 -*-

from django_file_download import views as file_download_views
from django_file_upload import views as file_upload_views
from django_six import re_path


app_name = 'django_file'


urlpatterns = [
    re_path(r'^upload$', file_upload_views.file_upload, name='file_upload'),
    re_path(r'^download$', file_download_views.file_download, name='file_download'),
]
