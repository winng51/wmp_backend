from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from rest_framework_jwt.utils import jwt_decode_handler

import json
from .models import Label, Topic, Picture, Comment, SubComment, User


def pub_topic(request):
    if request.method == 'POST':
        token = request.POST['token']
        labels_id = request.POST['labels']
        user_info = jwt_decode_handler(token)

        user = User.objects.get(id=user_info['user_id'])
        labels = Label.objects.get(id in labels_id)
        new_topic = Topic(labels=labels, title=request.POST['title'], content=request.POST['content'],
                          user=user, is_homework=request.POST['homework'])
        new_topic.save()

        response_data = {
            "topicId": new_topic.id,
        }

        response = json.dumps(response_data, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")


def pub_comment(request):
    if request.method == 'POST':
        token = request.POST['token']
        user_info = jwt_decode_handler(token)

        topic_id = request.POST['topic']
        topic = Topic.objects.get(id=topic_id)
        user = User.objects.get(id=user_info['user_id'])

        # 已认证的同学可以点赞评论
        if user.authority > 0:
            mode = request.POST['mode']

            if mode == 'comment':
                new_comment = Comment(topic=topic, content=request.POST['content'], user=user)
                new_comment.save()
                status = 200

            elif mode == 'like':
                # 点过赞了取消
                if user.id in topic.likes:
                    topic.like_count -= 1
                    topic.view_count -= 2
                    topic.likes.remove(user.id)
                # 没点过赞点赞
                else:
                    topic.like_count += 1
                    topic.likes.append(user.id)

                topic.save()
                status = 200

            elif mode == 'star':
                # 已收藏的取消
                if topic_id in user.stars:
                    topic.star_count -= 1
                    topic.view_count -= 5
                    topic.stars.pop(str(user.id))
                    user.stars.remove(topic_id)
                # 没收藏过收藏
                else:
                    topic.star_count += 1
                    topic.view_count += 3
                    topic.stars.update({user.id: 'https://wmp.winng51.cn/static/' + str(user.avatar)})
                    user.stars.append(topic_id)

                topic.save()
                user.save()
                status = 200

            # 返回403
            else:
                status = 403

        # 返回未认证
        else:
            status = 401

        response_data = {
            "status": status,
        }

        response = json.dumps(response_data, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")


def delete(request):
    if request.method == 'POST':
        token = request.POST['token']
        user_info = jwt_decode_handler(token)
        mode = request.POST['mode']

        if mode == 'topic':
            try:
                topic_id = request.POST['topic']
                topic = Topic.objects.get(id=topic_id, user_id=user_info['user_id'])
                print(topic.delete())

                status = 200

            except Topic.DoesNotExist:
                print('orz')

                status = 403

        else:

            status = 403

        response_data = {
            "status": status,
        }

        response = json.dumps(response_data, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")


def report(request):
    if request.method == 'POST':
        token = request.POST['token']
        user_info = jwt_decode_handler(token)

        mode = request.POST['mode']
        topic_id = request.POST['topic']
        topic = Topic.objects.get(id=topic_id, user_id=user_info['user_id'])

        response_data = {
            "topicId": topic.id,
        }

        response = json.dumps(response_data, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")
