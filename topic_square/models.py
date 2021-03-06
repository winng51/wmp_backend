from django.db import models

# Create your models here.


class User(models.Model):
    COLLEGE_CHOICES = [
        (0, '软件'),
        (1, '软国'),
        (2, '微电'),
        (3, '其它'),
    ]
    USER_GENDER_CHOICES = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )
    USER_AUTHORITY = (
        (0, '路人'),
        (1, '组员'),
        (2, '管理员'),
    )
    username = models.CharField(max_length=15, verbose_name="用户昵称")
    openid = models.CharField(max_length=30, verbose_name="微信openid")
    avatar = models.ImageField(default=None, upload_to='avatar', verbose_name="头像文件")
    identity = models.BooleanField(default=False, verbose_name="是否申请身份认证")
    authority = models.SmallIntegerField(choices=USER_AUTHORITY, default=0, verbose_name="身份")
    gender = models.SmallIntegerField(choices=USER_GENDER_CHOICES, default=0, verbose_name="性别")
    college = models.SmallIntegerField(null=True, default=0, choices=COLLEGE_CHOICES, verbose_name="学院")
    grade = models.CharField(max_length=10, null=True, default=None, blank=True, verbose_name="年级")
    classes = models.CharField(max_length=10, null=True, default=None, blank=True, verbose_name="班级")
    name = models.CharField(default=None, null=True, max_length=15, blank=True, verbose_name="姓名")
    phone = models.CharField(max_length=15, null=True, default=None, blank=True, verbose_name="手机号")
    signature = models.CharField(max_length=50, null=True, default='还没有签名呢(￣▽￣")', blank=True, verbose_name="个性签名")
    stars = models.JSONField(default=list, blank=True, verbose_name="收藏列表")

    def __str__(self):
        return self.username

    def student_info(self):
        if self.grade is None and self.college is None and self.classes is None:
            return None
        college = '??' if self.college is None else self.get_college_display()
        grade = '??' if self.grade is None else self.grade[-2:]
        if self.classes is None:
            classes = '??'
        elif len(self.classes) < 2:
            classes = '0' + str(self.classes)
        else:
            classes = str(self.classes)
        return college + grade + classes

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "论坛用户"


class Label(models.Model):
    title = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    selectable = models.BooleanField(default=False, verbose_name="是否可被组员选择")
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=True, db_index=False)
    visible = models.BooleanField(default=True, verbose_name="是否可见")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "话题标签"


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
    likes = models.JSONField(default=list, blank=True, verbose_name="点赞列表")
    views = models.JSONField(default=list, blank=True, verbose_name="浏览列表")
    is_homework = models.BooleanField(default=False, verbose_name="是否为打卡")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "话题"
        verbose_name_plural = "话题"


class Picture(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    pub_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='topic-pictures', verbose_name="图片路径")


class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.TextField(blank=True, verbose_name="正文内容")
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, db_index=False)
    like_count = models.IntegerField(default=0, verbose_name="点赞次数")
    likes = models.JSONField(default=dict, blank=True, verbose_name="点赞列表")

    def __str__(self):
        return self.topic.title

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "话题评论"


class SubComment(models.Model):
    topic = models.ForeignKey(Comment, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, verbose_name="正文内容")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, db_index=False)
    like_count = models.IntegerField(default=0, verbose_name="点赞次数")
    likes = models.JSONField(default=dict, blank=True, verbose_name="点赞列表")

    def __str__(self):
        return self.topic.topic.title


class Report(models.Model):
    title = models.CharField(max_length=30, blank=True, verbose_name="举报说明")
    report_user = models.ForeignKey(User, on_delete=models.PROTECT, db_index=False, verbose_name="举报人")
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, verbose_name="内容")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="原话题")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name="原评论")
    sub_comment = models.ForeignKey(SubComment, on_delete=models.CASCADE, verbose_name="原评论")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "举报"
        verbose_name_plural = "举报"
