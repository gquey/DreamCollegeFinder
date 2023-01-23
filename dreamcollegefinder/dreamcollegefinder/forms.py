# import the standard Django Forms
# from built-in library
from django import forms
from dreamcollegefinder.models import Quiz

class InputForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = "__all__"