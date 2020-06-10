from django.db import models

# Create your models here.

class Business(models.Model):
    # id
    caption = models.CharField(max_length=32)
    code = models.CharField(max_length=32, default="sa") # null=True

class Host(models.Model):
    nid = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=32, db_index=True) # db_index: 索引
    ip = models.GenericIPAddressField(protocol="both", db_index=True) # protocol: 支持ipv4还是ipv6
    port = models.IntegerField()
    b = models.ForeignKey("Business", to_field="id", on_delete=models.CASCADE)

class Application(models.Model):
    name = models.CharField(max_length=32)
    r = models.ManyToManyField("Host") # django将自动帮助创建下面这张表HostToApp

# class HostToApp(models.Model):
#     hobj = models.ForeignKey(to="Host", to_field="nid", on_delete=models.CASCADE)
#     aobj = models.ForeignKey(to='Application', to_field='id', on_delete=models.CASCADE)