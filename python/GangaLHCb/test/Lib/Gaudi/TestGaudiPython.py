import os
from GangaTest.Framework.tests import GangaGPITestCase
from GangaLHCb.Lib.Gaudi.Gaudi import GaudiExtras
from GangaLHCb.Lib.Gaudi.GaudiPython import GaudiPython

class TestGaudiPython(GangaGPITestCase):

    def setUp(self):
        self.job = Job(application=GaudiPython())
        gp = self.job.application
        gp._impl._auto__init__()
        gp.script = [File('dummy.script')]
        self.job.inputdata = ['pfn:dummy1.in','pfn:dummy2.in']               
        self.gp = gp._impl
        self.master_config = self.gp.master_configure()[1]
        #self.job = job

    def test_GaudiPython__auto__init__(self):
        assert self.gp.project, 'project not set automatically'
        assert self.gp.version, 'version not set automatically'
        assert self.gp.platform, 'platform not set automatically'
        assert not self.gp.user_release_area

    def test_GaudiPython_master_configure(self):
        gp = self.gp
        #gp.master_configure() # must call this in set up for configure to work
        #assert gp.extra.inputdata == self.job.inputdata._impl, 'inputdata err'
        found_script = False
        for f in self.master_config.inputbox:
            print 'f.name =', f.name
            if f.name.rfind('dummy.script') >= 0:
                found_script = True
                break
        assert found_script, 'script not in sandbox'
        

    def test_GaudiPtython_configure(self):
        gp = self.gp
        subconfig = gp.configure(None)[1]
        assert 'gaudipython-wrapper.py' in [f.name for f in subconfig.inputbox] , 'didnt find gaudipython wrapper'
        f=file([file.name for file in subconfig.inputbox if file.name is 'gaudipython-wrapper.py'][0],'r')
        buffer = f.read()
        f.close()
        assert buffer is not ''

    # not much to check here...as this method simply runs checks itself
    #def test_GaudiPython__check_inputs(self):

