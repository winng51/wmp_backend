from django.shortcuts import render
import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

from .models import Good, Tag, ImageLabel


# Create your views here.


def get_goods(request):
    if request.method == 'GET':
        tag_list = list(Tag.objects.all().values('id', 'title'))
        for tag in tag_list:
            good_list = list(Good.objects.filter(tag__id=tag['id']).values('id', 'title', 'image', 'content',
                                                                           'price', 'seal_price', 'out_of_stock'))
            for good in good_list:
                # 添加主图
                good['image'] = 'https://wmp.winng51.cn/static/' + str(good['image'])
                # 添加商品分类
                label_dict_list = list(ImageLabel.objects.filter(good=good['id']).values('image', 'title', 'price'))
                for label_dict in label_dict_list:
                    label_dict['image'] = 'https://wmp.winng51.cn/static/' + str(label_dict['image'])
                good['labels'] = label_dict_list
            if len(good_list) == 0:
                good_list = [
                    {
                        "id": 0,
                        "title": "还没有商品，快上架呀",
                        "image": "https://wmp.winng51.cn/static/good-pictures/noitem.jpeg",
                        "content": "",
                        "out_of_stock": True,
                        "price": None,
                        "seal_price": None,
                        "labels": []
                    }
                ]
            tag['id'] = tag['id'] - 1
            tag['goods'] = good_list

        # 添加未分类标签
        new_tag = {}
        good_list = list(Good.objects.filter(tag__isnull=True).values('id', 'title', 'image', 'content',
                                                                      'price', 'seal_price', 'out_of_stock'))
        for good in good_list:
            # 添加商品分类
            label_dict_list = list(ImageLabel.objects.filter(good=good['id']).values('image', 'title', 'price'))
            for label_dict in label_dict_list:
                label_dict['image'] = 'https://wmp.winng51.cn/static/' + str(label_dict['image'])
            # 添加主图
            good['image'] = 'https://wmp.winng51.cn/static/' + str(good['image'])
            good['labels'] = label_dict_list
        # 添加一个空商品进行占位
        null_good = {
            "id": 0,
            "title": "",
            "image": "",
            "content": "",
            "out_of_stock": True,
            "price": None,
            "seal_price": None,
            "labels": []
        }
        good_list.append(null_good)
        new_tag['id'] = tag_list[-1]['id'] + 1
        new_tag['title'] = '未分类'
        new_tag['goods'] = good_list
        tag_list.append(new_tag)
        response = json.dumps(tag_list, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")
