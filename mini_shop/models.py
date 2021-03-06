from django.db import models

# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=30)
    create_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"


class Good(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, default=None, null=True, blank=True, db_index=False,
                            verbose_name="商品类别")
    create_time = models.DateField(auto_now_add=True)
    edit_time = models.DateField(auto_now=True)
    title = models.CharField(max_length=30, verbose_name="商品名称")
    image = models.ImageField(upload_to='good-pictures', verbose_name="商品主图")
    content = models.TextField(blank=True, verbose_name="商品描述")
    price = models.IntegerField(default=0, verbose_name="商品价格")
    seal_price = models.IntegerField(default=None, null=True, blank=True, verbose_name="促销价格")
    out_of_stock = models.BooleanField(default=False, verbose_name="是否缺货")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "产品"
        verbose_name_plural = "文创产品"


class ImageLabel(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    pub_time = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=0, verbose_name="单价")
    title = models.CharField(max_length=30, verbose_name="图片描述")
    image = models.ImageField(upload_to='good-pictures', verbose_name="图片路径")

    def __str__(self):
        return self.title
