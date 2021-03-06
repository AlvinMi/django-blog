# blog/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse    # new 
# Create your models here.
# 创建数据模型
# Category 就是一个标准的 Python 类，
# 它继承了 models.Model 类，类名为 Category 。Category 类有一个属性 name，它是 models.CharField 的一个实例
class Category(models.Model):
    name = models.CharField(max_length=100)

    # 解决了文章分类是汉字, 后台保存后还是显示 category
    def __str__(self):
        return self.name



class Tag(models.Model):
    """
    标签 Tag 也比较简单,和 Category 一样。
    再次强调一定要集成 models.Model 类！
    """
    name = models.CharField(max_length=100)

    # 解决了文章标签是汉字, 后台保存后还是显示 tag
    def __str__(self):
        return self.name

class Post(models.Model):
    """
    文章的数据库表稍微复杂一点，主要是涉及的字段更多。
    """

    # 文章标题
    title = models.CharField(max_length=70)

    # 文章正文, 使用了 TextField
    # 储存比较短的字符串可以使用 CharField, 但是对于文章的正文来说可能会是一大段文本, 因此使用 TextField 来储存大段文本。
    body = models.TextField()

    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    """
    我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    """
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    '''
    django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    这里我们通过 ForeignKey 把文章和 User 关联了起来。
    因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    '''
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    # 自己定义 get_absolute_url 方法 | 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):     # 返回的是 post 对应的 URL, 因此在 detail.html 中 {{post.get_absolute_url}} 最终会被替换成该 post 自身的 URL。
        return reverse('blog:detail', kwargs={'pk': self.pk})       # blog 应用下的 name=detail 函数
