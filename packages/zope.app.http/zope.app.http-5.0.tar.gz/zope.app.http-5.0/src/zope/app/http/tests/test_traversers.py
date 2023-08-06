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
"""Test HTTP-specific object traversers
"""
from unittest import TestCase
from unittest import TestSuite
from unittest import makeSuite

from zope.publisher.browser import TestRequest
from zope.publisher.interfaces import NotFound

from zope.app.http.put import NullResource
from zope.app.http.traversal import ContainerTraverser
from zope.app.http.traversal import ItemTraverser


class Items:

    def __init__(self, data):
        self.data = data

    def __getitem__(self, name):
        return self.data[name]


class Container(Items):

    def get(self, name, default=None):
        return self.data.get(name, default)


class TestContainer(TestCase):

    Container = Container
    Traverser = ContainerTraverser

    def testSubobject(self):
        container = self.Container({'foo': 42})
        request = TestRequest()
        traverser = self.Traverser(container, request)
        self.assertEqual(traverser.publishTraverse(request, 'foo'), 42)

    def testNotFound(self):
        container = self.Container({'foo': 42})
        request = TestRequest()
        traverser = self.Traverser(container, request)
        self.assertRaises(NotFound,
                          traverser.publishTraverse, request, 'bar')

    def testNull(self):
        container = self.Container({'foo': 42})
        request = TestRequest()
        request.method = 'PUT'
        traverser = self.Traverser(container, request)
        null = traverser.publishTraverse(request, 'bar')
        self.assertEqual(null.__class__, NullResource)
        self.assertEqual(null.container, container)
        self.assertEqual(null.name, 'bar')


class TestItem(TestContainer):

    Container = Items
    Traverser = ItemTraverser


def test_suite():
    return TestSuite((
        makeSuite(TestContainer),
        makeSuite(TestItem),
    ))
