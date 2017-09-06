import pytest
import datetime
from swpy import goes


dt = [datetime.datetime(2012, 01, 01, 0, 0, 0),
      datetime.datetime(2012, 01, 02, 0, 0, 0),
      datetime.datetime(2012, 01, 03, 0, 0, 0)]


@pytest.mark.webtest
def test_download():
    goes.download_mag_csv(dt[0], dt[1])

    goes.download_xray_csv(dt[0], dt[1])
 
    goes.download_xray(dt[0], dt[1])
 
def test_draw():
    y = [2.0e-5, 2.0e-5, 2.0e-5]
    goes.draw_goes_xray(dt, y, days=3)
    #draw_goes_xray(dt, y, file_path='xray.png')
    
    y = [10, 20, 30]
    goes.draw_goes_mag(dt, y, days=3)
    #draw_goes_mag(dt, y, file_path='mag.png')
    
    y = [2.0e2, 2.0e1, 2.0e3]
    goes.draw_goes_proton(dt, y, days=3)
    #draw_goes_proton(dt, y, file_path='proton.png')
    
    y = [2.0e2, 2.0e1, 2.0e3]
    goes.draw_goes_electron(dt, y, days=3)
    #draw_goes_proton(dt, y, file_path='proton.png')
