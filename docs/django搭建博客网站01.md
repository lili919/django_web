**django搭建博客网站01**

# 创建项目和应用

- 创建项目，声明项目名称为lilisblog：Django-admin startproject lilisblog

- 创建应用（blog），声明应用名称为blog
cd lilisblog #先进入项目目录
python manage.py startapp blog

- 网站配置
修改文件./lilisblog/settings.py的两处代码：
 INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # 新增
]
TIME_ZONE = 'Asia/Shanghai'  # 设置时区为东八区

# 编写博客的数据模型类

- 编辑文件./blog/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class BlogArticles(models.Model):
    title = models.CharField(max_length=300)
    # ForeignKey(外键)对应多对一，外键要定义在“多”的一方
    # 本例通过author字段规定了文章与用户的关系，多篇文章可以对应一个用户，即文章对用户是"多对一"
    # related_name="blog_posts"的作用是，允许通过类User反向查询到BlogArticles，这个参数我们可以不设置，Django会默认以模型的小写作为反向关联名 
    # 以后从User对象反向关联到他所写的BlogArticles，就可以使用user.blog_posts了
    author = models.ForeignKey(User, related_name="blog_posts", on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-publish",)  # publish的倒序排序。此处是元祖，不要忘写后面的逗号

    def __str__(self):
        return self.title  # 对应后台文章列表中的默认显式字段

ForeignKey(外键)对应多对一，外键要定义在“多”的一方。本例通过author字段规定了文章与用户的关系，多篇文章可以对应一个用户，即文章对用户是"多对一"
related_name="blog_posts"的作用是允许通过类User反向查询到BlogArticles，这个参数我们可以不设置，Django会默认以模型的小写作为反向关联名 。以后从User对象反向关联到他所写的BlogArticles，就可以使用user.blog_posts了

- 根据数据模型类创建数据表
依次执行以下两条命令：
python manage.py makemigrations blog
python manage.py migrate

# 以超级用户身份进入博客后台
- 创建超级用户（用户名：admin 密码：helloworld）
python manage.py createsuperuser
根据提示输入，例如：用户名admin 邮箱：lili919@yeah.net 密码：helloworld

- 运行Django服务器，并登录admin
python manage.py runserver

执行完上一行命令之后，在浏览器输入 http://127.0.0.1:8000，运行Django服务器
在浏览器中输入 http://127.0.0.1:8000/admin 进入Django默认的后台,输入用户名（admin）和密码(helloworld)后登陆后台

- 在后台中显示BlogArticle栏目
编辑文件./blog/admin.py
from django.contrib import admin
from .models import BlogArticles

admin.site.register(BlogArticles)

# 发布博客
- 点击上图中的“add”进入博客发布页面

- 优化博客列表的显示
修改./blog/admin.py优化博客列表的显示
from django.contrib import admin
from .models import BlogArticles

class BlogArticleAdmin (admin.ModelAdmin):
    list_display = ("title", "author", "publish")
    list_filter = ("publish", "author")
    search_fields = ("title", "body")
    raw_id_fields = ("author", )
    date_hierarchy = "publish"
    ordering = ["publish", "author"]

admin.site.register(BlogArticles, BlogArticleAdmin)

# 展示博客
- 在前端展示博客列表
编辑./blog/views.py
from django.shortcuts import render
from .models import BlogArticles

def blog_list(request):
    blogs = BlogArticles.objects.all()
    return render(request, "blog/blog_list.html", {"blogs": blogs})

render()的作用是将数据渲染到指定的模板，第一个参数必须是request，第二个参数是模板的位置，第三个参数是要传递到模板的数据，这些数据是字典形式的。

编辑./lilisblog/urls.py
from django.conf.urls import url
from django.contrib import admin
from django.urls import include

urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^', include('blog.urls')), #新增
]

新建 ./blog/urls.py 并编辑
from django.shortcuts import render
from .models import BlogArticles

def blog_list(request):
    blogs = BlogArticles.objects.all()
    return render(request, "blog/blog_list.html", {"blogs":blogs})

新建 ./blog/templates/base.html 并编辑
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="http://necolas.github.io/normalize.css/">
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>
<body>
<div class="container">
    {% block content %}
    {% endblock %}
</div>
<script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.js"></script>
<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

</body>
</html>

本例的 templates 目录是Django默认的存放本应用所需模板的目录，如果不用自定义的方式指定模板位置，Django会在运行时自动来这里查找render()函数中所指定的模板文件。

新建 ./blog/templates/blog/blog_list.html 并编辑
{% extends 'base.html" %}

{% block title %} blog titles {% endlock %}

{% block content %}

<div class="row text-center vertical-middlw-sm">
    <h1>我的博客</h1>
</div>
<div class="row">
    <div class="col-xs-12 col-md-8">
        <ul>
            {% for blog in blogs %}
            <li><a href="{{blog.id}}">{{blog.title}}</a></li>
            {% endfor %}
        </ul>
    </div>
    <div class="col-xs-6 col-md-4">
        <img width="200px" src="https://mmbiz.qpic.cn/mmbiz_jpg/50ZAC2pjue1m3aXiccoFZRU1icIUCROtkRn5X9mpJRZicZr71gEuSdfrKCtlziawJ0icyWNM2YN49QYpJXuEC3ibVNZA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1">
    </div>
</div>

重新运行Django（执行python manage.py runserver），浏览器输入http://127.0.0.1:8000/blog/



