# comment 应用写 URL 模式

# comments/urls.py

from django.conf.urls import url
from . import views

app_name = 'comments'   # 这里是 comments

urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment')  # 还需要在 blogproject 里包含 `comment/urls.py`
]