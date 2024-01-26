from django.db import models
from accounts.models import Profile
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Pay(models.Model):
    STATUS=(
        ('PAY','PAY'),
        ('RECEIV','RECEIV'),
        ('TRANSFORM','TRANSFORM'),
    )
    amount_paid=models.IntegerField()
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_payments')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_payments')
    status=models.CharField(max_length=12,choices=STATUS)
    time = models.TimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.sender} {self.status} {self.amount_paid} to {self.receiver}"


    # this to funcation def save and def update_wallets make the same work ? you can chose what u want to chose 
    # def save(self, *args, **kwargs):
    #     # Update sender and receiver wallets
    #     self.sender.wallet.wallet -= self.amount_paid
    #     self.receiver.wallet.wallet += self.amount_paid
    #     self.sender.wallet.save()
    #     self.receiver.wallet.save()
    #     super(Pay, self).save(*args, **kwargs)

@receiver(post_save, sender=Pay)
def update_wallets(sender, instance, **kwargs):
    # Update sender and receiver wallets after Pay instance is saved
    instance.sender.wallet.wallet -= instance.amount_paid
    instance.receiver.wallet.wallet += instance.amount_paid
    instance.sender.wallet.save()
    instance.receiver.wallet.save()
    
class Wallet(models.Model):
    owner=models.OneToOneField(Profile,on_delete=models.CASCADE)
    wallet=models.IntegerField(default=0)
    password=models.CharField(default='',max_length=1000)
    

    def __str__(self):
        return f"{self.owner} wallet is  {self.wallet} "

    def create_wallet(sender ,*args, **kwargs):
        if kwargs['created']:
            user_wallet=Wallet.objects.create(owner=kwargs['instance'])    
    post_save.connect(create_wallet , sender=Profile)
    

class Order(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    total=models.IntegerField(default=0,verbose_name=_("Total"))
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return ' Order id: ' + str(self.id)

    # def __unicode__(self):
    #     return 
