from django.contrib import admin
from django.utils import timezone

from api.models import Occurence, OccurenceState


class OccurenceAdmin(admin.ModelAdmin):
    exclude = ('creation_date','modified_date',)
    readonly_fields = []

    def get_form(self, request, obj=None, **kwargs):
        """Override the get_form and extend the 'exclude' keyword arg"""
        if obj is None:
            kwargs.update({
                'exclude': getattr(kwargs, 
                                   'exclude', 
                                   self.exclude) \
                            + ('occurence_state',),
            })
        else:
            self.readonly_fields = ['creation_date',
                                    'modified_date']
        return super(OccurenceAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creation_date = timezone.now()
            obj.occurence_state_id = OccurenceState.objects.get(
                                        description='por validar').id
        else:
            obj.occurence_state = form.cleaned_data['occurence_state']
        
        obj.modified_date = timezone.now()
        
        super(OccurenceAdmin, self).save_model(request, obj, form, change)

admin.site.register(Occurence, OccurenceAdmin)