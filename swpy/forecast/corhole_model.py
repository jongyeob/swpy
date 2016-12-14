from datetime import datetime, timedelta
from math import cos,pi

v_params = [350,900]
n_params = [2,50]
t_params = [12,700]
b_params = [3,25]
vntb_legs = [4,1,3,2] #v,n,t,b
dst_params = [0,0]

def forecast_sw(time,area):
    params = [v_params,n_params,t_params,b_params]
    ret    = []
    for p,l in zip(params,vntb_legs):
        f = p[0] + p[1]*area
        t = time + timedelta(days=l)
        ret.append((t,f))

    return ret

def forecast_dst(time,area,polarity):
    
    doy  = (time - time.replace(month=1,day=1)).days
    lam  = 2 * pi * (doy-81)/365.

    t = time + timedelta(days=4)

    dst  = (-65 + 25*polarity*cos(lam))* area**0.5

    return t,dst


def convert_dst_to_kp(dst):
    return (22.2335 - 0.3467*dst)/10.



