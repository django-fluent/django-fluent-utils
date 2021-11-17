"""
Generic Ajax functionality
"""
import json

from django.http import HttpResponse


class JsonResponse(HttpResponse):
    """
    A convenient HttpResponse class, which encodes the response in JSON format.
    """

    def __init__(self, jsondata, status=200):
        self.jsondata = jsondata
        super().__init__(
            json.dumps(jsondata), content_type="application/json; charset=utf-8", status=status
        )
