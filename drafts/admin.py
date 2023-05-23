from django.contrib import admin


from .models import DraftDataset, DraftFunc
# Register your models here.
admin.site.register(DraftDataset)
admin.site.register(DraftFunc)

