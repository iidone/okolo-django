from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

CATEGORY_CHOICES = [
    ('electronics', 'Электроника'),
    ('clothing', 'Одежда'),
    ('auto', 'Авто'),
    ('animals', 'Животные'),
    ('furniture', 'Мебель'),
    ('decorations', 'Украшения'),
    ('recreation_and_entertainment', 'Отдых и развлечения')
]

CONDITION_CHOICES = [
    ('null', 'Не указано'),
    ('new', 'Новый'),
    ('used', 'Б/у'),
    ('broken', 'Требует ремонта'),
]

class Ad(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='main/images/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    contact_info = models.CharField(max_length=200, verbose_name="Контакт для связи")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Объявление: {self.title}'
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class ExchangeProposal(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена')
    ]

    id = models.AutoField(primary_key=True)
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='receiver_proposals')
    comment = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Предложение #{self.id} ({self.get_status_display()})'
    
    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'

def save(self, *args, **kwargs):
    if self.ad_sender.user == self.ad_receiver.user:
        raise ValidationError("Нельзя предлагать обмен самому себе")
    super().save(*args, **kwargs)