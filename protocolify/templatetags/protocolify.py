import re
from urlparse import urljoin
from django import template
from django.contrib.sites.models import Site


register = template.Library()


class ProtocolifyNode(template.Node):
    # http://www.ietf.org/rfc/rfc2396.txt -- Section 3.1
    SCHEME_PATTERN = "[a-z][a-z0-9+-.]*"
    PATH_REGEX = re.compile(r""" (src|href)=("|')(?!%s:)(.*?)\2""" % SCHEME_PATTERN)

    def __init__(self, nodelist, old, new):
        self.nodelist = nodelist
        self.old = old
        self.new = new

    def render(self, context):
        old = self.old.resolve(context)
        new = self.new.resolve(context)
        # fix absolute URLs
        fixed = re.sub(r""" (src|href)=("|')%s:""" % (old or self.SCHEME_PATTERN),
                       r""" \1=\2%s:""" % new,
                       self.nodelist.render(context))
        request = context.get("request")
        # fix relative URLs (if *request* is in the context)
        if request and not old:
            # figure out what host to use:
            if request and "HTTP_HOST" in context["request"].META:
                host = request.META["HTTP_HOST"]
            else:
                host = Site.objects.get_current().domain
            # Search for all paths and manually modify them. We can't use
            # re.sub here because we actually need to use urlparse.urljoin()
            for match in self.PATH_REGEX.findall(fixed):
                template = " {0}={1}%s{1}".format(*match)  # href="%s"
                full_url = new + "://" + host + urljoin(request.path, match[2])
                fixed = fixed.replace(template % match[2], template % full_url)
        return fixed


@register.tag("protocolify")
def protocolify(parser, token):
    bits = token.split_contents()
    tag_name = bits.pop(0)
    nodelist = parser.parse(("end%s" % tag_name,))
    parser.delete_first_token()

    # e.g.: "to http"
    if len(bits) == 2:
        bits.insert(0, "")
    try:
        old, _, new = bits
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires 2 or 3 arguments" % tag_name
    return ProtocolifyNode(nodelist, parser.compile_filter(old),
                           parser.compile_filter(new))
