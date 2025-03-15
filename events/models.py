from django.db import models

from datetime import date

# Create your models here.
class persons(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    

#after 6.4
    def __str__(self):
        return self.name

class Event(models.Model):
    STATUS_CHOICES=[
        ('ENDED','Ended'),
        ('UPCOMING','Upcoming'),
        ('RUNNING','Running')
    ]
    catagory=models.ForeignKey(
        "Catagory",
        on_delete=models.CASCADE,
        default=1
    )
    
    assigned_to=models.ManyToManyField(persons,related_name='events')
    title=models.CharField(max_length=250)
    description= models.TextField()
    location=models.CharField(max_length=350)
    due_date=models.DateField()
    status= models.CharField(max_length=15,choices=STATUS_CHOICES,default="UPCOMING")
    # is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class EventDetail(models.Model):
    # HIGH= 'H'
    # MEDIUM='M'
    # LOW='L'
    # PRIORITY_OPTIONS= (
    #     (HIGH,'HIGH'),
    #     (MEDIUM,'MEDIUM'),
    #     (LOW,'LOW')
    # )
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name='details',
    )

    # assigned_to=models.CharField(max_length=100)
   
    event_details=models.TextField(blank=True,null=True)

    # def __str__(self):
    #     return f"Details from Task {self.event.title}"

    
     

class Catagory(models.Model):
    name=models.CharField(max_length=200)
    description= models.TextField(blank=True,null=True)
    

    def __str__(self):
        return self.name
    




