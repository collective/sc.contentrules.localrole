# -*- coding: utf-8 -*-
from sc.contentrules.localrole.testing import INTEGRATION_TESTING
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class VocabulariesTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_allfields_vocabulary(self):
        name = 'sc.contentrules.localrole.allfields'
        util = queryUtility(IVocabularyFactory, name)
        self.assertIsNotNone(util, None)
        all_fields = util(self.portal)
        self.assertGreater(len(all_fields), 40)
