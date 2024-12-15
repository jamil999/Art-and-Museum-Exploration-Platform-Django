# custom_tags.py

from django import template

register = template.Library()

def zip_lists(obj, my_list):
    return zip(obj, my_list)

register.filter('zip_lists', zip_lists)