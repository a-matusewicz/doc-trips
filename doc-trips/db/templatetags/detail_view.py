

from django import template
from django.shortcuts import render
from django.db import models

from db.templatetags.links import *
register = template.Library()

@register.simple_tag
def detail(db_object, fields=None):
    
    if not fields:
        fields = db_object._meta.get_all_field_names()
    
    display_fields = []
    for field_name in fields:
        
        field = db_object._meta.get_field_by_name(field_name)[0]
        value = getattr(db_object, field_name)

        if isinstance(field, models.related.RelatedObject):
            continue
            # value = value.get_queryset()
            # field.verbose_name = field.var_name
        
        if isinstance(field, models.ManyToManyField):
            t = template.Template(
                """
                {% for o in queryset %}
                {{ o }}
                {% endfor %}
                """)
            print(value.get_queryset())
            c = template.Context({'queryset': value.get_queryset()})
            value = t.render(c)
            
        display_fields.append((field.verbose_name, value))
        
    t = template.loader.get_template('db/_detail_view_tag.html')
    c = template.Context({'fields': display_fields})
    return t.render(c)
    