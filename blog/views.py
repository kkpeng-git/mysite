from django.shortcuts import render, get_object_or_404, render
from read_statistics.utils import read_statistics_once_read
from django.core.paginator import Paginator
from django.db.models import Count

from mysite.settings import EACH_PAGE_BLOGS
from .models import Blog, BlogType


def get_blog_list_common_data(blogs_all_list, requset):
    paginator = Paginator(blogs_all_list, EACH_PAGE_BLOGS)  # 每10篇进行分页
    page_num = requset.GET.get("page", 1)  # 获取页码参数(get请求)
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number  # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    # 获取博客分类的对应博客数量
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))  # 关联模型的小写 Blog == blog
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(requset):
    """ 博客列表 """
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(blogs_all_list, requset)
    return render(requset, "blog/blog_list.html", context)


def blog_with_type(requset, blog_type_pk):
    """ 博客列表 - 根据类型 """
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(blogs_all_list, requset)
    context['blog_type'] = blog_type

    return render(requset, "blog/blog_with_type.html", context)


def blog_with_date(requset, year, month):
    """ 博客列表 - 根据时间 """
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(blogs_all_list, requset)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(requset, "blog/blog_with_date.html", context)


def blog_detail(requset, blog_pk):
    """ 博客内容 """
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(requset, blog)  # 增加博客阅读数

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()  # 上一篇  根据创建时间
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 下一篇  根据创建时间
    context['blog'] = blog
    response = render(requset, "blog/blog_detail.html", context)  # 响应
    # response.set_cookie(read_cookie_key, 'true', max_age=60)
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
    return response
