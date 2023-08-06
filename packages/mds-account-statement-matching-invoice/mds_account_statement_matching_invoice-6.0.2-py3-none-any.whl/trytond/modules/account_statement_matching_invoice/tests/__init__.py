# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.account_statement_matching_invoice.tests.test_statement import StatementTestCase

__all__ = ['suite']


class MatchingModuleTestCase(\
            StatementTestCase):
    'Test statement module'
    module = 'account_statement_matching_invoice'

# end MatchingModuleTestCase


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(MatchingModuleTestCase))
    return suite
