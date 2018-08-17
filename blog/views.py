# blog/views.py
# Create your views here.

# from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import Post,Category
import markdown

# Form 表单评论框
from comments.forms import CommentForm


"""
这个两行的函数体现了这个过程。
它首先接受了一个名为 request 的参数，这个 request 就是 Django 为我们封装好的 HTTP 请求，
它是类 HttpRequest 的一个实例。然后我们便直接返回了一个 HTTP 响应给用户，这个 HTTP 响应也是 Django 帮我们封装好的，
它是类 HttpResponse 的一个实例，只是我们给它传了一个自定义的字符串参数。
"""
# 首页视图函数
def index(request):
    # return HttpResponse("Hello my django_blog !!!")
    # return render(request, 'blog/index.html', context={
    #     'title': '我的博客首页',
    #     'welcome': '欢迎访问我的博客首页！'
    # })
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 博客文章详细视图函数 detail 
'''
根据从 URL 捕获的文章 id（也就是 pk，这里 pk 和 id 是等价的）获取数据库中文章 id 为该值的记录，
然后传递给模板。注意这里我们用到了从 django.shortcuts 模块导入的 get_object_or_404 方法，
其作用就是当传入的 pk 对应的 Post 在数据库存在时，就返回对应的 post，如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在。
'''
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)   # get_object_or_404 别忘记在顶上 import

    # 对 post 的 body 的值做一下渲染, 把 markdown 文本转为 HTML 文本再传递给模板. (记得在顶部引入 markdown )
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',      # extra 本身包含很多拓展
                                      'markdown.extensions.codehilite', # 语法高亮
                                      'markdown.extensions.toc',        # 允许自动生成目录
                                  ])                       

    # 加入表单评论部分(记得在顶部导入 CommentForm)
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传递给 detail.html 模板, 以便渲染相应数据
    context = {
        'post':post,
        'form':form,
        'comment_list': comment_list
    }

    # return render(request, 'blog/detail.html', context={'post':post})     # 这样写, 进入文章后,评论区不显示表格, 只能在文章评论发表后看到,进入文章却没有
    return render(request, 'blog/detail.html', context=context) # 需要把 form 传递给模板,将上面改成这样就可以了。


# 归档视图
'''
使用模型管理器 (objects) 的 filter 函数来过滤文章。由于是按照日期归档, 因此这里根据文章发表的年和月来过滤。 
具体来说,就是根据 `created_time` 的 `year` 和 `month` 属性过滤, 筛选处问斩发表在对应的 year 年和 month 月的文章。
Python 中类实例调用属性的方法通常是 created_time.year，但是由于这里作为函数的参数列表，所以 Django 要求我们把点替换成了两个下划线，
即 created_time__year。

同时和 index 视图中一样，我们对返回的文章列表进行了排序。此外由于归档的下的文章列表的显示和首页是一样的，因此我们直接渲染了 index.html 模板。
'''
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

# 分类视图函数
'''
首先根据传入的 pk 值,(也就是被访问的分类的 id 值) 从数据中获取到这个分类。`get_object_or_404` 函数和 detail 视图中一样, 
其作用是如果用户访问的分类不存在, 则返回一个 404 错误页面以提示用户访问的资源不存在。
然后通过 filter 函数过滤处了该分类下的全部文章, 同样也和首页视图中一样对返回的文章列表进行了排序。
'''
def category(request, pk):
    # 记得导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})