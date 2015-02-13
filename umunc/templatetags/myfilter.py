#coding=utf8
from django.template import Library 
from django.template.defaultfilters import stringfilter 

register = Library() 

@stringfilter 
def truncatehanzi(value, arg):     
    """     
    Truncates a string after a certain number of words including     
    alphanumeric and CJK characters.      
    Argument: Number of words to truncate after.     
    """     
    try:
        bits = []
        for x in arg.split(u':'):
            if len(x) == 0:
                bits.append(None)
            else:
                bits.append(int(x))
        if int(x) < len(value):
            return value[slice(*bits)] + '...'
        return value[slice(*bits)]

    except (ValueError, TypeError):
        return value # Fail silently.
 
@stringfilter 
def transconference(value):
	if value in [1,2,3,4,5,6,7,8,9]:return 1
	if value in [10,11,12,13,14,15,16]:return 2
	if value in [17,18,19,20,21,22,23]:return 3

register.filter('truncatehanzi', truncatehanzi)
register.filter('transconference', transconference)