from django.db import models
from colorfield.fields import ColorField
from django.core.validators import FileExtensionValidator


# Create your models here.
class DraftDataset(models.Model):
    creator = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['csv', 'xslsx'])], upload_to="datasets/")
    file_link = models.CharField(max_length=300, verbose_name='File link(if the file is not uploaded)', blank=True, null=True)

    title = models.CharField(max_length=50)
    title_fontsize = models.IntegerField(default=13)
    title_color = ColorField(default='#000000')

    graph_color = ColorField(default='#000000')

    x_label = models.CharField(max_length=50, default='x')
    y_label = models.CharField(max_length=50, default='y')
    z_label = models.CharField(max_length=50, default='z', blank=True, null=True)

    def __str__(self):
        return self.title
    

class DraftFunc(models.Model):
    creator = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50, default="title")
    title_fontsize = models.IntegerField(default=13)
    title_color = ColorField(default='#000000')

    equation = models.CharField(max_length=50, verbose_name='Equation in terms of x,y and z (function should be given in python math syntax, ex: x**2+y**2)')
    range_of_func = models.CharField(default="[(-10, 10), (-10, 10), (-10, 10)]",max_length=50, verbose_name="supply in the format of 3 tuples inside one list: [(x_min,x_max), (y_min,y_max), (z_min,z_max)]")
    color = ColorField(default='#000000')
    line_type_choices = [
        ('dashed','DASHED'),
        ('dotted', 'DOTTED'),
    ]
    line_type = models.CharField(choices=line_type_choices, max_length=50)
    def __str__(self):
        return self.equation
    






