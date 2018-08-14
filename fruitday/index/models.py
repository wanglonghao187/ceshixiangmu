from django.db import models

# Create your models here.
class Users(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=20)
    uphone = models.CharField(max_length=11)
    uemail = models.EmailField()
    isActive = models.BooleanField(default=True)








#商品类型
class GoodsType(models.Model):
    title = models.CharField(max_length=40)
    picture = models.ImageField(upload_to="static/upload/goodstype")
    desc = models.TextField()


    def to_dict(self):
        dic = {
            "title":self.title,
            "picture":self.picture.__str__(),
            "desc":self.desc,
        }
        return dic

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '商品类型'
        verbose_name_plural = verbose_name


#商品
class Goods(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    spec = models.CharField(max_length=20)
    picture = models.ImageField(upload_to="static/upload/goods")
    isActive = models.BooleanField(default=True)
    #增加对商品类型的引用
    goodsType = models.ForeignKey(GoodsType,null=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name='商品'
        verbose_name_plural = verbose_name



class CartInfo(models.Model):
    #属性：user,外键，引用自Users实体
    user = models.ForeignKey(Users,null=True)
    #属性：good ,外键引用自Goods实体
    good = models.ForeignKey(Goods)
    #属性：ccount,整数，表示该商品的购买数量
    ccount = models.IntegerField()


    class Meta:
        verbose_name='购物车'
        verbose_name_plural = verbose_name





