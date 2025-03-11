from django import forms

class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "bg-[#042820] border border-[#0a4d3f] text-gray-100 text-sm rounded-lg focus:ring-[#0a4d3f] focus:border-[#0a4d3f] block w-full p-2.5 placeholder-gray-400",
            "placeholder": "Your name"
        })
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "bg-[#042820] border border-[#0a4d3f] text-gray-100 text-sm rounded-lg focus:ring-[#0a4d3f] focus:border-[#0a4d3f] block w-full p-2.5 placeholder-gray-400",
            "placeholder": "Write your comment here...",
            "rows": 4
        })
    )