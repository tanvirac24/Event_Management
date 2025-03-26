from django.db.models.signals import post_save,pre_save,m2m_changed,post_delete,pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from events.models import Event
from django.conf import settings


@receiver(post_save,sender=User)
def send_activation_email(sender,instance,created,**kwargs):
    if created:
        token=default_token_generator.make_token(instance)
        activation_url=f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"

        subject='Activate Your Account'
        message=f'Assalamu Alikum {instance.username},\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank You!!!!'
        recipient_list=[instance.email]
        try:
            send_mail(subject,message,settings.EMAIL_HOST_USER,recipient_list)
        except Exception as e:
            print(f"Failed to send email to {instance.email}:{str(e)}")

@receiver(post_save,sender=User)
def assign_role(sender,instance,created,**kwargs):
    if created:
        user_group,created=Group.objects.get_or_create(name='Participent')
        instance.groups.add(user_group)
        instance.save()

