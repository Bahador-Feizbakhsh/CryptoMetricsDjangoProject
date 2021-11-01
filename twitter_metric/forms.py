from django import forms

import scrape_twitter_metrics_bearer


class TwitterHandleForm(forms.Form):
    twitter_handle = forms.CharField(label='Twitter Handle', max_length=100)

    # def clean(self):
    #     twitter_handle = self.cleaned_data.get('twitter_handle')
    #     user_id = scrape_twitter_metrics_bearer.get_user_id(twitter_handle)
    #     if user_id == 0:
    #         raise forms.ValidationError("Invalid Twitter Handle!")
    #     return twitter_handle, user_id
