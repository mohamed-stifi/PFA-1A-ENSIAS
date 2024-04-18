from django import forms

class RecommendrdForm(forms.Form):
    search_term = forms.CharField(max_length=200)
