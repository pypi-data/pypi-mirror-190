from __future__ import absolute_import

from coderadar.pytest import CoverageReport


def test_CoverageReport():
    my_report = CoverageReport()
    assert isinstance(my_report, CoverageReport)