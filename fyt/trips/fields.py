
from django import forms
from django.utils.safestring import mark_safe


class LeaderSectionChoiceField(forms.ModelMultipleChoiceField):
    """
    Section choice field with TRIPPEE dates.
    """
    def label_from_instance(self, obj):
        return mark_safe(obj.name + ' &mdash; '  + obj.leader_date_str())


class TrippeeSectionChoiceField(forms.ModelMultipleChoiceField):
    """ 
    Section choice field with TRIPPEE dates.
    """
    def label_from_instance(self, obj):
        label = '%s &mdash; %s' % (obj.name, obj.trippee_date_str())
        return mark_safe(label)


class TripChoiceField(forms.ModelChoiceField):
    """ 
    Field with verbose Trip labels .
    """
    def label_from_instance(self, obj):
        return "{}{}: {}: {}".format(
            obj.section.name, obj.template.name,
            obj.template.triptype.name,
            obj.template.description_summary
        )

