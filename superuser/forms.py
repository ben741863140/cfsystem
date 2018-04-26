from django import forms
from django.forms import DateTimeInput
import datetime


class StaticBoardForm(forms.Form):
    # class Meta:
    #     model = RatingChangeStaticBoard
    #     fields = ['name', 'start_time', 'end_time']
    #     labels = {
    #         'name': '名称',
    #         'start_time': '开始时间',
    #     }
    #     widgets = {
    #         'name': forms.TextInput(attrs={'class': 'form-control'}),
    #         'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format=['%Y-%m-%dT%H:%M']),
    #     }

    name = forms.CharField(label='名称', min_length=2, max_length=20,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    effective_time = forms.DateTimeField(label='有效起始时间', widget=DateTimeInput(attrs={'type': 'datetime-local'}),
                                         input_formats=['%Y-%m-%dT%H:%M'], required=False)
    start_time = forms.DateTimeField(label='开始时间', widget=DateTimeInput(attrs={'type': 'datetime-local'}),
                                     input_formats=['%Y-%m-%dT%H:%M'])
    end_time = forms.DateTimeField(label='结束时间', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                                   input_formats=['%Y-%m-%dT%H:%M'])

    # type = forms.ChoiceField(label='类型',
    #                          widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
    #                          choices=(('static', '静态榜'), ('dynamic', '动态榜')), required=False)
    type = forms.ChoiceField(label='类型',
                             widget=forms.Select(attrs={'class': 'form-control'}),
                             choices=(('rating', '分数榜'), ('rating_change', '升级榜')), required=False)

    list_text = forms.CharField(label='名单导入', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '15'}))

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data.get('end_time')
        start_time = self.cleaned_data.get('start_time')
        print(start_time, end_time)
        if start_time >= end_time:
            raise forms.ValidationError('结束时间不能在开始时间之前')
        return end_time
