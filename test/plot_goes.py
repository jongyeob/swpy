'''
Created on 2013. 12. 30.

@author: jongyeob
'''
dt = [datetime.datetime(2012, 01, 01, 0, 0, 0),
      datetime.datetime(2012, 01, 02, 0, 0, 0),
      datetime.datetime(2012, 01, 03, 0, 0, 0)]


y = [2.0e-5, 2.0e-5, 2.0e-5]
draw_goes_xray(dt, y, days=3)
#draw_goes_xray(dt, y, file_path='xray.png')

y = [10, 20, 30]
draw_goes_mag(dt, y, days=3)
#draw_goes_mag(dt, y, file_path='mag.png')

y = [2.0e2, 2.0e1, 2.0e3]
draw_goes_proton(dt, y, days=3)
#draw_goes_proton(dt, y, file_path='proton.png')

y = [2.0e2, 2.0e1, 2.0e3]
draw_goes_electron(dt, y, days=3)
#draw_goes_proton(dt, y, file_path='proton.png')
    '''
