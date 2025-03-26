# from django.db import models
from django.db.models.signals import post_save,pre_save,m2m_changed,post_delete,pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event
# Create your models here.
@receiver(m2m_changed,sender=Event.assigned_to.through)
def notify_participant_on_event_creation(sender,instance,action,**kwargs):
    if action=='post_add':
        assigned_eamils=[emp.email for emp in instance.assigned_to.all()]
        send_mail(
            "New Event Has Launched",
            f"You have been selected to the event:{instance.title} and Event Location:{instance.location}, Event Date:{instance.due_date}",
            "tanvirac024@gmail.com",
            assigned_eamils,
            fail_silently=False,
        )
