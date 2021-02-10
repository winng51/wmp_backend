from django.db import models

# Create your models here.


class User(models.Model):
    COLLEGE_CHOICES = [
        ('SW', '软件'),
        ('IS', '软国'),
        ('ME', '微电'),
        ('OT', '其它'),
    ]
    nickname = models.CharField(max_length=15, verbose_name="用户昵称")
    wechat_id = models.CharField(max_length=30, verbose_name="微信id")
    avatar = models.ImageField(default=None, upload_to='avatar', verbose_name="用户头像")
    grade = models.CharField(max_length=10, default=2019, verbose_name="年级")
    college = models.CharField(max_length=10, default='SW', choices=COLLEGE_CHOICES, verbose_name="学院")
    classes = models.CharField(max_length=10, default='01', verbose_name="班级")

    def __str__(self):
        return self.nickname


class Label(models.Model):
    title = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, db_index=False)

    def __str__(self):
        return self.title


class Topic(models.Model):
    labels = models.ManyToManyField(Label, related_name='sub_topics', blank=True, verbose_name="标签")
    title = models.CharField(max_length=30, blank=True, verbose_name="标题")
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, db_index=False)
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True, verbose_name="正文内容")
    like_count = models.IntegerField(default=0, verbose_name="点赞次数")
    view_count = models.IntegerField(default=0, verbose_name="浏览次数")
    star_count = models.IntegerField(default=0, verbose_name="收藏次数")
    stars = models.JSONField(default=dict, blank=True, verbose_name="收藏列表")
    likes = models.JSONField(default=dict, blank=True, verbose_name="点赞列表")
    views = models.JSONField(default=dict, blank=True, verbose_name="浏览列表")
    is_homework = models.BooleanField(default=False, verbose_name="是否为打卡")

    def __str__(self):
        return self.title


class Picture(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    pub_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='topic-pictures', verbose_name="图片路径")


class Comments(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.TextField(blank=True, verbose_name="正文内容")
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, db_index=False)
    like_count = models.IntegerField(default=0, verbose_name="点赞次数")
    likes = models.JSONField(default=dict, blank=True, verbose_name="点赞列表")

    def __str__(self):
        return self.topic.title


class SubComments(models.Model):
    topic = models.ForeignKey(Comments, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, verbose_name="正文内容")
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, db_index=False)
    like_count = models.IntegerField(default=0, verbose_name="点赞次数")
    likes = models.JSONField(default=dict, blank=True, verbose_name="点赞列表")

    def __str__(self):
        return self.topic.topic.title
