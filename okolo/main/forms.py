from django import forms
from .models import Ad, CATEGORY_CHOICES, CONDITION_CHOICES, ExchangeProposal

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = [
                'title', 
                'description', 
                'image', 'category', 
                'condition', 
                'contact_info'
            ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Например: iPhone 13 Pro Max 256GB'
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea',
                'placeholder': 'Укажите город, район, или адрес, а также подробно опишите товар...',
                'rows': 5
            }),
            'contact_info': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Телефон, email или ссылка на соцсеть'
            }),
            'category': forms.Select(attrs={
                'class': 'select'
            }),
            'condition': forms.Select(attrs={
                'class': 'select'
            }),
        }

class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'textarea',
                'placeholder': 'Опишите ваше предложение обмена...',
                'rows': 3
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.receiver_ad = kwargs.pop('receiver_ad', None)
        super(ExchangeProposalForm, self).__init__(*args, **kwargs)