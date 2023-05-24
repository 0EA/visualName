from django import forms
from drafts.models import DraftFunc, DraftDataset
class DatasetForm(forms.ModelForm):
    graph_color = forms.CharField(label="graph color", max_length=7, widget=forms.TextInput(attrs={'type':'color'}))
    title_color = forms.CharField(label="title color", max_length=7, widget=forms.TextInput(attrs={'type':'color'}))
    class Meta:
        model = DraftDataset
        fields = ["file","file_link", "title", "title_fontsize", "title_color", "graph_color", "x_label", "y_label", "z_label"]

class FuncForm(forms.ModelForm):
    color = forms.CharField(label="graph color", max_length=7, widget=forms.TextInput(attrs={'type':'color'}))
    title_color = forms.CharField(label="title color", max_length=7, widget=forms.TextInput(attrs={'type':'color'}))
    class Meta:
        model = DraftFunc
        fields = ["title", "title_fontsize", "title_color", "equation", "range_of_func", "line_type", "color"]