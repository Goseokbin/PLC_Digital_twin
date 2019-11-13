from django import forms
from datetimepicker.widgets import DateTimePicker


class SampleForm(forms.Form):

    datetime = forms.DateTimeField(
        widget=DateTimePicker(),
    )