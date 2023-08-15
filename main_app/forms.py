from django.forms import ModelForm
from .models import Feeding

class FeedingForm(ModelForm):
    # 'Meta' refers to the details/config options for the class
    class Meta:
        model = Feeding
        fields = ['date','meal']
        