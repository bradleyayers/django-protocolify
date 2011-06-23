django-protocolify
==================

A template tag for Django that allows the protocol/scheme used in links within
a block of template code to be changed.

A use-case for this is when a section of your Web site uses HTTPS (e.g. a
payment page) and you want the user to return to using HTTP if they leave the
page. Typically you'll be using the ``{% url <name> %}`` template tag to generate
URLs, however this will result in URLs like::

    /products/

rather than::

    http://example.com/products/

This means that once a user enters a HTTPS page, they will be *stuck* using
HTTPS unless they manually modify the URL in their browser's address bar.

This is where django-protocolify shines.


Usage
-----

::

    {% protocolify [old] to <new> %}

Example (assuming request was to ``http://example.com/blah/``)::

    {% load protocolify %}
    {% protocolify to "https" %}
    <a href="/abcd/"></a>
    <a href="abcd/"></a>
    <a href="./abcd/"></a>
    <a href="../abcd/"></a>
    <a href="http://example.com/abcd/"></a>
    <a href="http://example.com"></a>
    <a href="ftp://example.com/abcd/"></a>
    <a href="ftp://example.com"></a>
    <a href="ftp://example.com/"></a>
    <a href=""></a>
    {% endprotocolify %}

renders to::

    <a href="https://example.com/abcd/"></a>
    <a href="https://example.com/blah/abcd/"></a>
    <a href="https://example.com/blah/abcd/"></a>
    <a href="https://example.com/abcd/"></a>
    <a href="https://example.com/abcd/"></a>
    <a href="https://example.com"></a>
    <a href="https://example.com/abcd/"></a>
    <a href="https://example.com"></a>
    <a href="https://example.com/"></a>
    <a href="https://example.com/blah/"></a>

This is currently implemented using a couple of simplistic regular expressions
and ``urlparse.urljoin()`` (Note: *old* defaults to ``[a-zA-Z]+``)::

    # e.g. href="http://google.com"
    re.sub(r' (src|href)="%s://' % old, r' \1="%s://' % new, ...)
    # e.g. href="../products"
    re.findall(r""" (src|href)=("|')(?![a-z][a-z0-9+-.]*:)(.*?)\2""")

When a relative path is replaced (e.g. ``../products``) it's joined to the
``request.path``. For this to work, the template context must contain the
``HttpRequest`` in a ``request`` variable. This can be achieved by using a
``RequestContext`` and adding ``"django.core.context_processors.request"`` to
the ``TEMPLATE_CONTEXT_PROCESSORS`` setting.

Domain ambiguitity is introduced when a relative path (e.g. ``/products/``) is
protocolified (because the domain must be specified). Domain guesses are
performed in the following order:

1. ``request.META["HTTP_HOST"]`` -- when the context contains ``request``
2. ``Site.objects.get_current().domain``


Installation
------------

1. Download and install: ``pip install django-protocolify``
2. Add ``"protocolify"`` to the ``INSTALLED_APPS`` setting in your project.
