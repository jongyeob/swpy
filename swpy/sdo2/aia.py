'''
Created on 2017. 4. 4.

@author: jongyeob
'''
import logging

from swpy.base import FilePathRequest,TimeFormattedPath

LOG= logging.getLogger(__name__)

CFG = {
    'path-pattern':'data/NASA/SDO/AIA/{wavelength}/{format}/%Y/%Y%m%d/%Y%m%d_%H%M%S_SDO_AIA_{wavelength}.{ext}'
    }

LOG    = logging.getLogger(__name__)


class SdoAiaFilePath(FilePathRequest): pass

class SdoAiaPathFactory():
    '''
    WAVELENGTHS   = ['131','1600','1700','171','193','211','304','335','4500','94']
    FORMATS       = ['jp2',
                     'jpg_512','jpg_1024','jpg_2048','jpg_4096',
                     'fits','fits_synoptic']
    '''
    @staticmethod
    def create(wavelength,format):
        ext        = format.split('_')[0]
        pattern = CFG['path-pattern'].format(wavelength=wavelength,format=format,ext=ext)
        
        return SdoAiaFilePath(TimeFormattedPath(pattern))
