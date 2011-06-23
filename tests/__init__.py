from attest import Assert, AssertImportHook, Tests
# In Django <= 1.3 django.utils.module_loading.module_has_submodule is busted
AssertImportHook.disable()
from django.conf import settings

settings.configure(
    INSTALLED_APPS = [
        'protocolify',
    ],
)


from django.template import Template, Context
from django.test.client import RequestFactory


everything = Tests()


@everything.test
def templatetag():
    factory = RequestFactory(HTTP_HOST="example.com")
    context = Context({"request": factory.get("/blah/")})

    # {% protocolify to FOO %}
    template = (
        '{% load protocolify %}'
        '{% protocolify to "https" %}'
        '<a href="/abcd/"></a>'  # path (absolute)
        '<a href="abcd/"></a>'  # path (relative)
        '<a href="./abcd/"></a>'  # path (relative)
        '<a href="../abcd/"></a>'  # path (relative)
        '<a href="http://example.com/abcd/"></a>'  # scheme + domain + path
        '<a href="http://example.com"></a>'  # scheme + domain
        '<a href="ftp://example.com/abcd/"></a>'  # scheme + domain + path
        '<a href="ftp://example.com"></a>'  # scheme + domain
        '<a href="ftp://example.com/"></a>'  # scheme + domain + path
        '<a href=""></a>'  # scheme + domain + path
        '{% endprotocolify %}'
    )
    expected = (
        '<a href="https://example.com/abcd/"></a>'
        '<a href="https://example.com/blah/abcd/"></a>'
        '<a href="https://example.com/blah/abcd/"></a>'
        '<a href="https://example.com/abcd/"></a>'
        '<a href="https://example.com/abcd/"></a>'
        '<a href="https://example.com"></a>'
        '<a href="https://example.com/abcd/"></a>'
        '<a href="https://example.com"></a>'
        '<a href="https://example.com/"></a>'
        '<a href="https://example.com/blah/"></a>'
    )
    Assert(expected) == Template(template).render(context)

    # {% protocolify FOO to BAR %}
    template = (
        '{% load protocolify %}'
        '{% protocolify "http" to "https" %}'
        '<a href="/abcd/"></a>'  # path (absolute)
        '<a href="http://example.com/abcd/"></a>'  # scheme + domain + path
        '<a href="http://example.com"></a>'  # scheme + domain
        '<a href="ftp://example.com/abcd/"></a>'  # scheme + domain + path
        '<a href="ftp://example.com"></a>'  # scheme + domain
        '{% endprotocolify %}'
    )
    expected = (
        '<a href="/abcd/"></a>'
        '<a href="https://example.com/abcd/"></a>'
        '<a href="https://example.com"></a>'
        '<a href="ftp://example.com/abcd/"></a>'
        '<a href="ftp://example.com"></a>'
    )
    Assert(expected) == Template(template).render(context)
