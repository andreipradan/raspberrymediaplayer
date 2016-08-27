from django import forms


class YoutubeForm(forms.Form):
    youtube_url = forms.CharField(
        widget=forms.TextInput(attrs={'size': 100, 'class': 'col-xs-12'}),
        max_length=512,
    )
