from urllib import urlencode
try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

from django import template
from django.template.defaultfilters import stringfilter

from django.contrib.auth.models import User

import re

register = template.Library()

class BuildQueryStringNode(template.Node):
    def __init__(self, sortfield):
        self.sortfield = sortfield

    def render(self, context):
        qs = parse_qs(context['current_query'])
        if qs.has_key('sort') and self.sortfield in qs['sort']:
            if self.sortfield.startswith('-'):
                qs['sort'] = [self.sortfield[1:]]
            else:
                qs['sort'] = ['-' + self.sortfield]
        else:
            qs['sort'] = [self.sortfield]
        return urlencode(qs, True)

@register.tag(name='buildsortqs')
def do_buildsortqs(parser, token):
    try:
        tagname, sortfield = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
                "%r tag requires a single argument" % tagname)
    if not (sortfield[0] == sortfield[-1] and sortfield[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
                "%r tag's argument should be in quotes" % tagname)
    return BuildQueryStringNode(sortfield[1:-1])


@stringfilter
def replace(name, char):
    #print  "replace: ", name, char
    return name.replace(char, '/')

@stringfilter
def split(name, delimiter):
    #print  "split:", name, delimiter
    return name.split(delimiter)

def getVersion(value, lang='en'):
    if value[0].startswith('2'):
        return value[0] 
    else:
        value = value[0]
        if lang == 'tr':
            return "Kurumsal" + value[-1]
        else:
            return "Corporate" + value[-1]

@stringfilter
def dist_replace(value):
    parts = value.split('-')
    if parts[1] == 'stable':
        parts[1] = 'testing'
    return '/'.join(parts)

@stringfilter
def packager_username(packager):
    """Return search page link with packages filtered by packager."""
    try:
        packager = User.objects.get(username=packager)
        return packager.username
    except User.DoesNotExist:
        return None

@stringfilter
def find_files(file_list, file_name):
    pattern = re.compile(file_name, re.IGNORECASE)
    return [pattern.sub(lambda match: '<span class="highlight">' + match.group(0) + '</span>', f) \
            for f in file_list.split('\n') if file_name in f.lower()]



register.filter('getVersion', getVersion)
#register.filter('indexAt', indexAt)
register.filter('replace', replace)
register.filter('split', split)
register.filter('dist_replace', dist_replace)
register.filter('packager_username', packager_username)
register.filter('find_files', find_files)
