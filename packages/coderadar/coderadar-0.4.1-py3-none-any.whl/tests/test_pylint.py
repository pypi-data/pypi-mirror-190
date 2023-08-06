from __future__ import absolute_import

from coderadar.pylint import PylintReport


class TestPylintReport():
    

    def setup_class(self):
        pass

    def teardown_class(self):
        pass
        
    def setup_method(self, test_method):
        pass
    
    def teardown_method(self, test_method):
        pass


    def test_init(self, mocker):
        mock_load_report = mocker.patch('coderadar.pylint.PylintReport._loadJsonReport')
        my_report = PylintReport()
        assert isinstance(my_report, PylintReport)