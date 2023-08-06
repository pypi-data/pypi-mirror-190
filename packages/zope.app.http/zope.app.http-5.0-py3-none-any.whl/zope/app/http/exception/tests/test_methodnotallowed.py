##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Tests for HTTP error views
"""
from io import BytesIO
from unittest import TestCase
from unittest import TestSuite
from unittest import makeSuite

from zope.component import provideAdapter
from zope.interface import Interface
from zope.interface import implementer
from zope.publisher.http import HTTPRequest
from zope.publisher.interfaces.http import IHTTPRequest


class Iface(Interface):
    pass


@implementer(Iface)
class C:
    pass


class GetView:
    def __init__(self, context, request):
        pass

    def GET(self):
        pass


class DeleteView:
    def __init__(self, context, request):
        pass

    def DELETE(self):
        pass


class TestMethodNotAllowedView(TestCase):

    def setUp(self):
        provideAdapter(GetView, (Iface, IHTTPRequest), Interface, 'GET')
        provideAdapter(DeleteView, (Iface, IHTTPRequest), Interface, 'DELETE')
        provideAdapter(GetView, (Iface, IHTTPRequest), Interface, 'irrelevant')
        provideAdapter(
            DeleteView, (Iface, IHTTPRequest), Interface, 'also_irrelevant')

        from zope.publisher.interfaces import IDefaultViewName
        from zope.publisher.interfaces.browser import IBrowserRequest

        # do the same as defaultView would for something like:
        # <defaultView
        #    for=".test_methodnotallowed.I"
        #    name="index.html"
        #    />

        provideAdapter(
            'index.html', (Iface, IBrowserRequest), IDefaultViewName)

    def test(self):
        from zope.publisher.interfaces.http import MethodNotAllowed

        from zope.app.http.exception.methodnotallowed import \
            MethodNotAllowedView

        context = C()
        request = HTTPRequest(BytesIO(b'PUT /bla/bla HTTP/1.1\n\n'), {})
        error = MethodNotAllowed(context, request)
        view = MethodNotAllowedView(error, request)

        result = view()

        self.assertEqual(request.response.getStatus(), 405)
        self.assertEqual(request.response.getHeader('Allow'), 'DELETE, GET')
        self.assertEqual(result, b'Method Not Allowed')

    def test_defaultView(self):
        # do the same with a BrowserRequest
        # edge case is that if someone does a defaultView for the context
        # object but the app is not prepared for webdav or whatever
        # and someone comes with a not allowed method, the exception
        # view fails on getAdapters
        # this might be an issue with zope.publisher, as it provides
        # a unicode object with provideAdapter, but I don't think I can
        # change zope.publisher
        from zope.publisher.browser import BrowserRequest
        from zope.publisher.interfaces.http import MethodNotAllowed

        from zope.app.http.exception.methodnotallowed import \
            MethodNotAllowedView

        context = C()
        request = BrowserRequest(BytesIO(b'PUT /bla/bla HTTP/1.1\n\n'), {})

        error = MethodNotAllowed(context, request)
        view = MethodNotAllowedView(error, request)

        result = view()

        self.assertEqual(request.response.getStatus(), 405)
        # well this is empty, but we're grateful that it does not break
        self.assertEqual(request.response.getHeader('Allow'), '')
        self.assertEqual(result, b'Method Not Allowed')


def test_suite():
    return TestSuite((
        makeSuite(TestMethodNotAllowedView),
    ))
