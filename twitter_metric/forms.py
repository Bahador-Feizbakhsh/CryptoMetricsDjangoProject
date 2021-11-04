from django import forms


class TwitterHandleForm(forms.Form):
    twitter_handle = forms.CharField(label='Twitter Handle', max_length=100)
