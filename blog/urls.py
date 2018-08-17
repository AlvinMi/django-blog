# blog/urls.py 
# 在项目根目录的 blogproject\ 目录下（即 settings.py 所在的目录），
# 原本就有一个 urls.py 文件，这是整个工程项目的 URL 配置文件。而我们这里新建了一个 urls.py 文件，
# 且位于 blog 应用下。这个文件将用于 blog 应用相关的 URL 配置。不要把两个文件搞混了。
from django.conf.urls import url
from . import views

# new 
"""
注意这里我们的网址是用正则表达式写的，Django 会用这个正则表达式去匹配用户实际输入的网址，
如果匹配成功，就会调用其后面的视图函数做相应的处理。

比如说我们本地开发服务器的域名是 http://127.0.0.1:8000，那么当用户输入网址 http://127.0.0.1:8000 后，
Django 首先会把协议 http、域名 127.0.0.1 和端口号 8000 去掉，此时只剩下一个空字符串，
而 r'^$' 的模式正是匹配一个空字符串（这个正则表达式的意思是以空字符串开头且以空字符串结尾），
于是二者匹配，Django 便会调用其对应的 views.index 函数。
"""
app_name = 'blog'
urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='index'),
    # 第一个参数是网址, 第二个参数是处理函数, 另外一个参数是 name
    url(r'^$', views.index, name='index'),      # 首页视图匹配的 URL 去掉域名之后其实就是个空字符串
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),    # 文章详情视图 URL
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),  # new 归档视图 url 
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
]