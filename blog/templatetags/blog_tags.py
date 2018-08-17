from django import template
from ..models import Post, Category


register = template.Library()

# 这个函数的功能是获取数据库中前 num 篇文章, 这里 num 默认为5。
@register.simple_tag
def get_recent_posts(num=5):    # 最新文档标签
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():                 # 归档模板标签
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():           # 分类模板标签
    # 别忘了在顶部引入 Category 类
    return Category.objects.all()