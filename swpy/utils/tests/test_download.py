import os
import tempfile
from swpy.utils import download as swdl


def test():
    print "test()"
   
    test_url = 'https://helioviewer.org/jp2/HMI/2016/11/04/magnetogram/2016_11_04__00_00_27_405__SDO_HMI_HMI_magnetogram.jp2'
    _, test_path = tempfile.mkstemp()

    if os.path.exists(test_path):
        os.remove(test_path)
    

    swdl.download_by_wget(test_url,test_path)
    
    assert os.path.exists(test_path), "Download is not completed!"


    swdl.download_by_wget(test_url,test_path,overwrite=True)
    assert os.path.exists(test_path), "Download is not completed!"

    

    print "Passed"

        
