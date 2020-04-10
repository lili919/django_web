**搭建简单的博客网站扩展——自定义模块和静态文件位置**

# 自定义模板和静态文件位置
当项目比较大的时候，往往会创建多个应用，这种情况下，模板、静态文件都要指定放在某个位置，比如把所有应用的模板都放在 ./templates中，把所有应用的静态文件都放在 ./static中。

- 自定义模板位置
修改./lilisblog/setting.py中的TEMPLATES
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ], #自定义模板位置
        'APP_DIRS': False, #自定义模板位置，不再允许按照默认方式寻找模板文件
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
把 ./blog中的 templates 文件夹移动到最外层，即 ./blog/templates 变成了 ./templates

- 自定义静态文件位置
修改./lilisblog/setting.py在STATIC_URL = ‘/static/’下面加上三行代码
```python
STATICFILES_DIRS = (  # 自定义静态文件位置
    os.path.join(BASE_DIR, "static"),  # 注意不要丢掉这个逗号，因为这是个元祖
)
```

新建./static文件夹，并添加子文件夹CSS/fonts/images/js和文件

# 使用通用静态文件和基础模板

- 通用header.html
创建./templates/header.html
```html
{% load staticfiles %}
<div class="container">
    <nav class="navbar navbar-default" role="navigation">
        <div class="navbar-header">
            <a class="navbar-brand"><img src="{% static '/images.logo.png' %}" width="100px"></a>
        </div>
        <div>
            <ul class="nav navbar-nav" role="navigation">
                <li><a href="{% url 'blog:blog_list' %}BLOG"></a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right" style="margin-right:20px">
                <li><a href="#">LOGIN</a></li>
            </ul>
        </div>
    </nav>
</div>
```

- 通用footer.html
创建,.templates/footer.html
```html
<div class="container">
    <hr>
    <p class="text-center">copy right</p>
</div>
```

- 完善base.html
修改./templates/base.html
```html
{% load staticfiles %}
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/bootstrap.css' %}">
</head>
<body>
{% include "header.html" %}
<div class="container">
    {% block content %} {% endblock %}
</div>
{% include "footer.html" %}
{% block javascript %} {% endblock %}
</body>
</html>
```

# 效果展现
运行Django后，浏览器中输入 http://127.0.0.1:8000/blog/

# 重置后台管理模块
运行Django后，浏览器中输入 http://127.0.0.1:8000/admin/ 会报错

因为我们已经将默认的文件模板位置都指向了自定义模板的位置，所以需要把后台相关模板文件复制到自定义模板位置。
把 django/contrib/admin/templates 目录下的 admin 和 registration 两个文件夹复制到 ./templates 里面

此时，重新运行Django，再次打开 http://127.0.0.1:8000/admin/ 又一切正常了





