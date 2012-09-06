from django.shortcuts import render_to_response
from django.db import connection
from django.template import RequestContext
from django.core.urlresolvers import reverse
from chocolate.rest import TastyFactory
from django.http import HttpResponse
import json


class test_db(object):

    def __init__(self, verbosity=0):
        self.db_name = ""
        self.verbosity = verbosity

    def __enter__(self):
        connection.creation.create_test_db(self.verbosity)

    def __exit__(self, type, value, traceback):
        connection.creation.destroy_test_db(self.db_name, self.verbosity)


def doc(request, api):
    api_name = api.api_name

    view_data = {
        'api_url': reverse('api_%s_top_level' % api_name, args=[api_name]),
        'example_url': reverse(
            "tastydocs.views.example_data",
            kwargs={'resource_name': "__RESOURCE_NAME__"}
        )
    }
    return render_to_response(
        'tastydocs/doc.html', view_data,
        context_instance=RequestContext(request))


def example_data(request, resource_name, api):

    tastyfactory = TastyFactory(api)
    resource_mockup = tastyfactory[resource_name]

    with test_db(verbosity=0):
        post_data = resource_mockup.create_post_data()
        get_data = resource_mockup.create_get_data()

    json_string = json.dumps({
        'POST': post_data,
        'GET': get_data
    })

    return HttpResponse(json_string, mimetype="application/json; charset=utf-8")
