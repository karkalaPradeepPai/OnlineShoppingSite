from django import forms
from myapp.models import Order

#Created a class OrderForm with necessary widgets and labels
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product','num_units']
        widgets = {'client': forms.RadioSelect(),}
        labels = {'num_units': u'Quantity', 'client': u'ClientName' }

#Created a class InterestForm with required fields and radioselect Button
class InterestForm(forms.Form):
    interested = forms.TypedChoiceField(widget=forms.RadioSelect, coerce=int, choices =((1, "Yes"), (0, "No")))
    quantity = forms.IntegerField(initial=1, min_value=1)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments', required=False)