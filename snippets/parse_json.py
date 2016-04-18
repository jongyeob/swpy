'''
Created on 2015. 11. 25.

@author: jongyeob
'''
fw = open('json.txt','r')
text = fw.read()
fw.close()
print 'end'



import json
data = json.loads(text)

keys = ['T_REC','HARPNUM',
            'USFLUX','MEANGAM','MEANGBT','MEANGBZ','MEANGBH','MEANJZD',
            'TOTUSJZ','MEANALP','MEANJZH','TOTUSJH','ABSNJZH','SAVNCPP',
            'MEANPOT','TOTPOT','MEANSHR','SHRGT45','CRPIX1','CRPIX2',
            'CRVAL1','CRVAL2','CDELT1','CDELT2','IMCRPIX1','IMCRPIX2','CROTA2',
            'CRLN_OBS','CRLT_OBS','RSUN_OBS','SIZE_ACR','AREA_ACR']



data2 = dict([(key['name'],key['values']) for key in data['keywords']])

cols = [data2[key] for key in keys] 
rows = zip(*cols)
rows = sorted(rows)

from swpy.utils import data as da

fw = open('json_out.txt','w')
da.print_table(rows,output=fw,names=keys)






