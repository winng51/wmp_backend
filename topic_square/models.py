from django.db import models

# Create your models here.


class Label(models.Model):
    title = models.CharField(max_length=30)
    pub_time = models.DateField(auto_now_add=True)
    pub_user = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Topic(models.Model):
    labels = models.ManyToManyField(Label, related_name='sub_topics', blank=True, verbose_name="标签")
    title = models.CharField(max_length=30, blank=True, verbose_name="标题")
    user_name = models.CharField(max_length=15, verbose_name="发布人昵称")
    user_id = models.CharField(max_length=15, verbose_name="发布人id")
    avatar = models.ImageField(default=None, upload_to='avatar', verbose_name="发布人头像")
    create_time = models.DateField(auto_now_add=True)
    edit_time = models.DateField(auto_now=True)
    content = models.TextField(blank=True, verbose_name="正文内容")
    comment_count = models.IntegerField(default=0, verbose_name="评论次数")
    star_count = models.IntegerField(default=0, verbose_name="点赞数量")
    view_count = models.IntegerField(default=0, verbose_name="浏览次数")
    comments = models.JSONField(default=dict, blank=True, verbose_name="评论列表")
    stars = models.JSONField(default=dict, blank=True, verbose_name="点赞列表")
    views = models.JSONField(default=dict, blank=True, verbose_name="查看列表")
    is_homework = models.BooleanField(default=False, verbose_name="是否为打卡")

    def __str__(self):
        return self.title


class Picture(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    pub_time = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='topic-pictures', verbose_name="图片路径")

