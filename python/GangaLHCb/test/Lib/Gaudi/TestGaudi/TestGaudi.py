import os
import shutil
import tempfile
from GangaTest.Framework.tests import GangaGPITestCase
from GangaLHCb.Lib.Gaudi.Gaudi import GaudiExtras
from GangaLHCb.Lib.Gaudi.Gaudi import Gaudi
from GangaLHCb.Lib.Gaudi.GaudiUtils import available_apps
from GangaTest.Framework.utils import read_file,failureException
import Ganga.Utility.logging

logger = Ganga.Utility.logging.getLogger()

class TestGaudi(GangaGPITestCase):

    def setUp(self):
        pass

    def test_Gaudi__auto__init__(self):
        dv = DaVinci()
        assert dv._impl.version, 'version not set automatically'
        assert dv._impl.platform, 'platform not set automatically'
        assert dv._impl.package, 'package not set automatically'
        assert dv._impl.user_release_area, 'ura not set automatically'

    def test_Gaudi_prepare(self):
        # Test standalone preparation
        d=DaVinci()
        d.prepare()
        assert d.is_prepared is not None, 'is_prepared not correctly set'
        assert d._impl.prep_inputbox, 'inputbox empty'

        # Now test as part of job
        j=Job(application=DaVinci())
        j.prepare()
        assert j.application.is_prepared is not None, 'is_prepared not correctly set'
        assert j.application._impl.prep_inputbox, 'inputbox empty'

        job = Job(application=Gauss(optsfile='./Gauss-Job.py'))
        gauss = job.application
        job.inputdata = ['pfn:dummy1.in','pfn:dummy2.in']
        job.outputdata = ['Gauss.sim']
        job.outputsandbox = ['GaussHistos.root','GaussMonitor.root']
        #inputs,extra = gauss._impl.master_configure()
        # provide basic test of where output goes - a more complete test is
        # run on the PythonOptionsParser methods.
        job.prepare()
        ok = job.application._impl.prep_outputbox.count('GaussHistos.root') > 0 and \
             job.application._impl.prep_outputbox.count('GaussMonitor.root') > 0
        assert ok, 'outputsandbox error'
        assert job.application._impl.prep_outputdata.files.count('Gauss.sim') > 0,'outputdata error'
        assert [f.name for f in job.application._impl.prep_inputbox].count('options.pkl') is not None, 'no options pickle file'
        assert [f.name for f in job.application._impl.prep_inputbox].count('gaudi-env.py.gz') is not None, 'no evn file'



    def test_Gaudi_unprepare(self):
        d=DaVinci()
        d.prepare()
        assert d.is_prepared is not None, 'is_prepared not correctly set'
        assert d._impl.prep_inputbox, 'inputbox empty'
        d.unprepare()
        assert d.is_prepared is None, 'is_prepared not correctly unset'
        assert not d._impl.prep_inputbox, 'inputbox not cleared properly'
        
    def test_Gaudi_master_configure(self):
        pass
##         job = Job(application=Gauss(optsfile='./Gauss-Job.py'))
##         gauss = job.application
##         job.inputdata = ['pfn:dummy1.in','pfn:dummy2.in']
##         job.outputdata = ['Gauss.sim']
##         job.outputsandbox = ['GaussHistos.root','GaussMonitor.root']
##         inputs,extra = gauss._impl.master_configure()
##         # provide basic test of where output goes - a more complete test is
##         # run on the PythonOptionsParser methods.
##         ok = extra.outputsandbox.count('GaussHistos.root') > 0 and \
##              extra.outputsandbox.count('GaussMonitor.root') > 0
##         assert ok, 'outputsandbox error'
##         assert extra.outputdata.files.count('Gauss.sim') > 0,'outputdata error'
##         assert extra.master_input_buffers['options.pkl'] is not None

    # this method currently does nothing
    #def test_Gaudi_configure(self):

    # not much to check here...as this method simply runs checks itself
    #def test_Gaudi__check_inputs(self):

    # Andrew's new method...hopefully he can provide a unit test for it
    #def test_Gaudi_readInputData(self):

