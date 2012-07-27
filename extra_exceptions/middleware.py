from django.conf import settings
from django.core.exceptions import ViewDoesNotExist
from django.http import HttpResponse
from django.template import RequestContext,Template,loader,TemplateDoesNotExist
from django.utils.importlib import import_module
from .utils import HttpException
import httplib

class HttpExceptionMiddleware(object):
    """
    Replace Status code raises for a {{status}}.html rendered template
    """
    def process_exception(self, request, exception):
        """
        Render a {{status}}.html template or default template as status page, but only if
        exception is instance of HttpException class
        """
        # we need to import to use isinstance
        if not isinstance(exception,HttpException):
            # Return None so that django will reraise the exception:
            # http://docs.djangoproject.com/en/dev/topics/http/middleware/#process_exception
            return None
        try:
            t = loader.get_template(str(exception.status) + '.html')
        except TemplateDoesNotExist:
            # doesn't exist a template in path, use default template
            t = Template("extra_exceptions/default_error_page.html")

        # now use context and render template      
        c = RequestContext(request, {
            'message': exception.message,
            'w3cname': httplib.responses.get(exception.status, str(exception.status))
        })
    
        return HttpResponse(t.render(c), status=exception.status)
