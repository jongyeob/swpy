'''
Created on 2013. 12. 15.

@author: Jongyeob
'''


import sys
import date_time as dt


table_keys = ['keywords','data']


class Table():
    
    def __init__(self,primekeys=[],keys=[],data={},fmts=[],parse=False):             
        ''' 
        :param list primekey: prime keys
        :param list keywords: keywords
        :param dict data: data
        :param list fmts: formats 
        '''
        self._data = {}
        self._keys = []
        self._primes = []
        self._fmts = []
        self._max_len = []
        self._num_data = 0
        
        self._changed = False
        self._parsed = False
             
        
        if len(keys) == 0:
            keys = data.keys()
                
        self.set_data(keys,data,fmts,parse=parse)
            
        if len(primekeys) > 0:
            self.set_primes(primekeys)          
    
    def length(self):
        if self._changed == True:
            pkey = self.get_primes()
            p = self._keys[0]
            if len(pkey) > 0:
                p = self._primes[0]
            self._num_data = len(self._data[p])
            self._changed = False
    
    
        return self._num_data
                 
    def set_data(self,keys,data,fmts=[],parse=False):
        
        if len(fmts) == 0:
            fmts = ['']*len(keys)
            
        if len(keys) != len(fmts):
            return False
                             
        for k,fmt in zip(keys,fmts):
    
            if self.length() > 0 and self.length() != len(data[k]):
                return False
            
            i = 2
            new_k = k
            while (self._data.has_key(new_k) == True):
                ks = k.split(':')
                new_k = '%s%d'%(ks[0],i)
                for i in range(1,len(ks)):
                    new_k += ':%s'%ks[i]
                i += 1
            
            ki = -1
            try: ki = self._keys.index(new_k)
            except: self._keys.append(new_k)
            
                   
            max_len = 0
            f = 's'
            if fmt != '': f = fmt
            parsed_data = []
            for d in data[k]:
                    
                
                if parse == True:
                    if   f[-1] == 'd': d = int(d)
                    elif f[-1] == 'f': d = float(d)
                    elif f[-1] == 's': d = str(d)
                    elif f[-1] == 't': d = dt.parse(d) 
                    
                    
                    parsed_data.append(d)
                    
                    
                l = len(str(d))
                if max_len < l: max_len = l
                    
            
            if fmt == '' : f = '%ds'%(max_len)
            if ki == -1:
                self._fmts.append(f)
                self._max_len.append(max_len)
            else:
                self._fmts[ki] = f
                self._max_len[ki] = max_len
                
            if parse == True:
                self._data[new_k] = parsed_data
            else:
                self._data[new_k] = data[k]
                
            self._changed = True
            self._parsed = parse
            
        return True
        
        
    def set_primes(self,primes):
        '''Set prime key'''
    
        if isinstance(primes,str) == True:
            self._primes = [primes]
            return True
        
        if isinstance(primes,list) == True:
            self._primes = primes
            
        return True
         
    def get_data(self,keywords=['*']):
        l = []
        keys = []
        for k in keywords:
            if k == '*':
                keys = self._keys
                continue
            elif self._data.has_key(k) == False:
                keys.extend(self.get_keywords(k))
                continue
            
            keys.append(k)
                
        for k in keys:
            l.append(self._data[k])
                
        return l
    
    def get_keywords(self,keyword='*'):
        ret = []
        if keyword == '*':
            ret.extend(self._keys)
            return ret

        for ns in self._keys: # ns: namespace            
            key = ''          
            for k in ns.split(':'):
                key += k
                if keyword == key:
                    ret.append(ns)
                    break
                key += ':' 
                
        return ret
    def get_primes(self):       return self._primes
    def get_formats(self):
        new = []

        for maxl,key,fmt in zip(self._max_len,self._keys,self._fmts):
            
            f = '%'
                       
            if fmt[-1] == 't':
                fmt = fmt[:-1]+'s'
                
            if self._parsed == False:
                fmt = fmt[:-1]+'s'
            
            
            di = fmt.find('.')
                
            n = len(fmt[:di])
            l,kl = 0,0
            
            try:    
                l  = abs(int(fmt[:di]))
                n -= len(str(l))
            except: l = maxl
            
                                                       
            kl = 0
            for kn in key.split(':'): #key name
                knl = len(kn)
                if kl < knl:
                    kl = knl
                    
            if kl > l : l = kl
            
            
            if self._parsed == True:
                f += fmt[:di][:n]
            
            f += str(l)
            
            if self._parsed == True:
                f += fmt[di:-1]
            
            f += fmt[-1]
            
            
            new.append(f)
            
                            
        return new   
    
def print_text(table,summary=0,f=sys.stdout):
    
    keys = table.get_keywords()
    data = table.get_data(keywords=keys)
    
    fmts = table.get_formats()
    
    if summary > 0:
        f.write('**** Print table summary\n')       
        f.write('total : %d\n'%(table.length()))
        
    
    lines  = ['']
    last_key  = {0:''} 
    max_depth = 0
    
    
    for key,fmt in zip(keys,fmts):
        num = int(float(fmt[1:-1]))       
        fk = '|%%%ds'%(num)
        ns = key.split(':') # namespaces
        ns.reverse()
        l = len(ns)
        if l > max_depth:
            for i in range(max_depth,l):
                last_key[i] = ''
                lines.append(lines[-1])
            
            max_depth = l
            
            
        key_changed = False
        for i in range(max_depth):
            i = max_depth-1 -i 
            
            #print "i:", i, "lines : ", lines[i]
            if i > l -1:
                last_key[i] = ''
                lines[i]   += fk%('*')
                key_changed = True
                continue
            
            if last_key[i] != ns[i] :
                key_changed = True
            
            if key_changed == True:
                last_key[i] = ns[i]
                lines[i]   += fk%(ns[i])
                continue

            lines[i]   += ' '+fk[1:]%('')
            
                 
    
    for i in range(max_depth):
        f.write(lines[max_depth-1 -i]+'\n')
    
    
    num_line  = table.length()
    ll = num_line
    if summary > 0 and summary < num_line :
        ll = summary
        
    ll2 = ll/2 
    
    linefmts = {}
    for key,fmt in zip(keys,fmts):
        linefmts[key] =' %s'%(fmt), abs(int(float(fmt[1:-1]))) # format, max_len    
    
    for i in range(ll2):
        line = ''
        for key,d in zip(keys,data):
            fk,max_len = linefmts[key]
            t = fk%(d[i])
            if  max_len < len(t) - 1:
                t = t[:max_len-1] +'~ '
            line += t
            
        f.write(line+'\n')
    
    if summary > 0:   
        f.write(' '*(ll2-1) + '...'+'\n')
    
    
    for i in range(ll2,ll):
        line = ''
        for key,d in zip(keys,data):
            fk,max_len = linefmts[key]
            
            t = fk%(d[i])
            if  max_len < len(t) - 1:
                t = t[:max_len-1] +'~ '
            line += t
        
        f.write(line+'\n')
            
                
    line = ''
    if summary > 0:
        f.write('****'+'\n')
    


def combine(*data_args,**kargs):
    '''
    Data have same number of list, ans same period
    
    ex1) combine_data(data1,data2)
    ex2) combine_data(data1,data2,prime_key=['prefix','prefix2'])
    ex2) combine_data(data1,data2,prefix=['prefix','prefix2'])
    ex3) combine)data(data1,data2,operation=['overlap','sort'])
    
    @return: None, if error
    '''
        
    combined_data = {}
    if kargs.has_key('datetime') == True:
        combined_data['datetime'] = []
        combined_data['datetime'].extend(kargs['datetime'])
             
    for data in data_args:
        prefix = ''
        if isinstance(data,tuple):
            data,prefix = data
        
        for key in data.iterkeys():
            new_key = prefix + ':' + key
            if len(prefix) == 0:
                new_key = key
                
            if combined_data.has_key(new_key) == True:
                print ("Same Keynames !")
                return None
            
            combined_data[new_key] = []
            combined_data[new_key].extend(data[key])
            
    
    return combined_data      


combine_data = combine
    
def test():
    
    t1 = Table()
    print t1
    print_text(t1)
    
    data = {'a:a:a':['1','2','3'],'b:a:b':['a','b','c'],'b:b:c':['1.1','2.2','3.3'],'b:d':['20100101_120000','2011-11-22 22:00:00','2013/03/02T11:00:01.333'],'e':[[1,2],[2,3],[3,4]]}
    keys = ['a:a:a','b:a:b','b:b:c','b:d','e']
    fmts = ['02d','4s','5.3f','t','']
    
    t2 = Table(data=data)
    print_text(t2)
    
     
    t3 = Table(keys=keys, data=data)
    print_text(t3)
    
     
    t4 = Table(keys=keys, data=data, fmts=fmts,primekeys='b:d')
    print_text(t4)
    
    
    t4.set_data(keys=keys, data=data, fmts=fmts)
    print_text(t4)
    print_text(t4,summary=2)
    
    
    t5 = Table(keys=keys, data=data, fmts=fmts,primekeys='b:d',parse=True)
    print_text(t5)
    
    t5_keys = t5.get_keywords('b')
    print t5_keys
    data = t5.get_data(keywords=t5_keys)
    print data
    
    

if __name__ =='__main__':
    test()