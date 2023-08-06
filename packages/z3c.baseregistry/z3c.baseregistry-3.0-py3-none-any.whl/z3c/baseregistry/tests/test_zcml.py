##############################################################################
#
# Copyright (c) 2017 Zope Foundation and Contributors.
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

import unittest

from z3c.baseregistry import zcml


class TestActionsProxy(unittest.TestCase):

    def _makeOne(self, list_=None):
        list_ = list_ or []
        return list_, zcml.ActionsProxy(list_, self)

    def test_set_decorates(self):
        list_, proxy = self._makeOne(['abc'])
        proxy[0] = {'discriminator': 'foo'}
        self.assertEqual([{'discriminator': (self, 'foo')}], list_)

    def test_slice_decorates(self):
        list_, proxy = self._makeOne(['abc'])
        proxy[:] = [{'discriminator': 'foo'}]
        self.assertEqual([{'discriminator': (self, 'foo')}], list_)

    def test_iadd_decorates(self):
        list_, proxy = self._makeOne()
        proxy += [{'discriminator': 'foo'}]
        self.assertEqual([{'discriminator': (self, 'foo')}], list_)

    def test_insert_decorates(self):
        list_, proxy = self._makeOne(['abc'])
        proxy.insert(0, {'discriminator': 'foo'})
        self.assertEqual([{'discriminator': (self, 'foo')}, 'abc'], list_)

    def test_extend_decotares(self):
        list_, proxy = self._makeOne(['abc'])
        proxy.extend(({'discriminator': 'foo'},))
        self.assertEqual(['abc', {'discriminator': (self, 'foo')}], list_)

    def test_proxy(self):
        list_, proxy = self._makeOne()
        self.assertEqual(list_.index, proxy.index)

    def test_len(self):
        list_, proxy = self._makeOne(['abc'])
        self.assertEqual(len(list_), len(proxy))
        self.assertEqual(1, len(proxy))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
