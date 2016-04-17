
import jsoc_aia_fits
import jsoc_hmi_fits
import aia
import hv_hmi_jp2
import hmi
import jsoc
import kasi

from swpy.utils import config

def initialize(**kwargs):
    jsoc_aia_fits.initialize(**kwargs.pop(jsoc_aia_fits.__name__,{}))
    jsoc_hmi_fits.initialize(**kwargs.pop(jsoc_hmi_fits.__name__,{}))
    
    aia.initialize(**kwargs.pop(aia.__name__,{}))
    hv_hmi_jp2.initialize(**kwargs.pop(hv_hmi_jp2.__name__,{}))
    hmi.initialize(**kwargs.pop(hmi.__name__,{}))
    jsoc.initialize(**kwargs.pop(jsoc.__name__,{}))
    kasi.initialize(**kwargs.pop(kasi.__name__,{}))
    