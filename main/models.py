from django.db import models

# Create your models here.
class user(models.Model):
	UserId = models.PositiveIntegerField(PrimaryKey = True, null = False, default = None)
	UserName = models.CharField(default='NAME', length = 30)
	EmailId = models.CharField(default=None, length = 50)
	AddressRoomNo = models.CharField(default = None, length = 10, unique=True)
	
