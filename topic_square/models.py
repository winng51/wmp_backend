from django.db import models

# Create your models here.


class User(models.Model):
    COLLEGE_CHOICES = [
        ('SW', '软件'),
        ('IS', '软国'),
        ('ME', '微电'),
        ('OT', '其它'),
    ]
    USER_GENDER_CHOICES = (
        (0, '未知'),
        (1, '男'),
        (0, '女'),
    )
    username = models.CharField(max_length=15, verbose_name="用户昵称")
    openid = models.CharField(max_length=30, verbose_name="微信openid")
    gender = models.SmallIntegerField(choices=USER_GENDER_CHOICES, default=0, verbose_name="性别")
    name = models.CharField(default="无", null=True, max_length=15, verbose_name="姓名")
    avatar = models.ImageField(default=None, upload_to='avatar', verbose_name="用户头像")
    college = models.CharField(max_length=10, null=True, default=None, choices=COLLEGE_CHOICES, verbose_name="学院")
    grade = models.CharField(max_length=10, null=True, default=None, verbose_name="年级")
    classes = models.CharField(max_length=10, null=True, default=None, verbose_name="班级")
    is_member = models.BooleanField(default=False, verbose_name="是否为组员")
    is_manager = models.BooleanField(default=False, verbose_name="是否为管理员")

    def __str__(self):
        return self.username


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


class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.TextField(blank=True, verbose_name="正文内容")
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, db_index=False)
    like_count = models.IntegerField(default=0, verbose_name="点赞次数")
    likes = models.JSONField(default=dict, blank=True, verbose_name="点赞列表")

    def __str__(self):
        return self.topic.title


class SubComment(models.Model):
    topic = models.ForeignKey(Comment, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, verbose_name="正文内容")
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, db_index=False)
    like_count = models.IntegerField(default=0, verbose_name="点赞次数")
    likes = models.JSONField(default=dict, blank=True, verbose_name="点赞列表")

    def __str__(self):
        return self.topic.topic.title
