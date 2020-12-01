from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm


def update_comment(requset):
    # """ 提交评论 """
    referer = requset.META.get('HTTP_REFERER', reverse('home'))  # 获取跳转过来的URL  reverse解析别名为home的url。
    comment_form = CommentForm(requset.POST, user=requset.user)  # 把user 传递到forms里面进行验证
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = requset.user
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        # 判断是否是回复
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        # 发送邮件通知  使用了线程的方法进行发送邮件。  此处在model send_mail中
        comment.send_mail()

        """ Ajax 返回json数据 """
        data['status'] = 'SUCCESS',
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        # return render(requset, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]  # 返回评论内容不能为空
    return JsonResponse(data)
