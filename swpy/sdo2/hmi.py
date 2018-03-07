import logging

from swpy.base import FilePathRequest,TimeFormattedPath

LOG    = logging.getLogger(__name__)


CFG = {
    'path-pattern':'data/NASA/SDO/HMI/{format}/{type}/%Y/%Y%m%d/%Y%m%d_%H%M%S_SDO_HMI_{type}.{ext}'
    }

class SdoHmiFilePath(FilePathRequest): pass

class SdoHmiPathFactory():
    '''
    TYPES =   ['Ic','Ld','Lw','M','V','S',
               'Ic_45s','Ld_45s','Lw_45s','M_45s','V_45s',
               'Ic_720s','Ld_720s','Lw_720s','M_720s','S_720s',
               'continuum','magnetogram']
    FORMATS = ['jp2','jpg_512','jpg_1024','jpg_4096','fits','fits_synoptic']

    '''
    @staticmethod
    def create(type,format):
        ext        = format.split('_')[0]
        pattern = CFG['path-pattern'].format(type=type,format=format,ext=ext)
        
        return SdoHmiFilePath(TimeFormattedPath(pattern))