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
        self._max_depth = 0
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
            
            # update maximum depth of keywords
            ks  = k.split(':')
            ksn = len(ks)
            
            if ksn > self._max_depth:
                self._max_depth = ksn 
            
            # when key is already been. add number after key name.
            i = 2
            new_k = k
            while (self._data.has_key(new_k) == True):
                new_k = '%s%d'%(ks[0],i)
                for i in range(1,ksn):
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
            
            # comparison key length and data length                                           
            ns = key.split(':') # namespace
            knl = len(ns[-1])   # last name length   
           
            if knl > l : l = knl
            
            
            if self._parsed == True:
                f += fmt[:di][:n]
            
            f += str(l)
            
            if self._parsed == True:
                f += fmt[di:-1]
            
            f += fmt[-1]
            
            
            new.append(f)
            
                            
        return new   
    
    def print_text(self,summary=0,f=sys.stdout):
        
        keys = self.get_keywords()
        data = self.get_data(keywords=keys)
        
        fmts = self.get_formats()
        
        if summary > 0:
            f.write('**** Print table summary\n')       
            f.write('total : %d\n'%(self.length()))
        
        
        # Creating titles
        max_depth = self._max_depth
        num_keys  = len(keys)
        
        key_map = [['' for _ in range(max_depth)] for _ in range(num_keys)]
        key_lens = [0 for _ in range(num_keys)]
        
        
        for i in range(num_keys):
            ns = keys[i].split(':')
            
            l = len(ns)            
            key_map[i][max_depth-l:] = ns
            key_lens[i] = int(float(fmts[i][1:-1]))
        
        
        
        for j in range(max_depth):
            
            
            last_key = key_map[0]
            last_len = 0
            offset   = 0
            
            for i in range(num_keys):
            
                if key_map[i][:j+1] == last_key[:j+1]: # when key name is same
                    last_len   += key_lens[i]   # add spaces
                    continue

                offset = last_len  - len(last_key[j])
                if offset < 0:    key_lens[i] -= offset
                    
                last_key = key_map[i]
                last_len = key_lens[i]
                
                
        
            offset = last_len - len(last_key[j])
            if offset < 0:    key_lens[i] -= offset
        
        

        for j in range(max_depth):
            line = ''
            last_key  = key_map[0]
            last_len  = 0
            count     = -1
            for i in range(num_keys):
                
                if key_map[i][:j+1] == last_key[:j+1]: # when key name is same
                    last_len += key_lens[i]
                    count    += 1 
                    continue
                
                fk  = '|%%-%ds'%(last_len+count) 
                key = last_key[j]     
                line += fk%(key)
                
                last_key = key_map[i]
                last_len = key_lens[i]
                count    = 0
                    
    
            fk = '|%%-%ds'%(last_len+count)
            key = last_key[j]
            line += fk%(key)
            
            print line+'|'
            
        
        num_line  = self.length()
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
    t1.print_text()
    
    data = {'a:a:a':['1','2','3'],'b:a:b':['a','b','c'],'b:b:c':['1.1','2.2','3.3'],'b:d':['20100101_120000','2011-11-22 22:00:00','2013/03/02T11:00:01.333'],'e':[[1,2],[2,3],[3,4]]}
    keys = ['a:a:a','b:a:b','b:b:c','b:d','e']
    fmts = ['02d','4s','5.3f','t','']
    
    t2 = Table(data=data)
    t2.print_text()
    
     
    t3 = Table(keys=keys, data=data)
    t3.print_text()
    
     
    t4 = Table(keys=keys, data=data, fmts=fmts,primekeys='b:d')
    t4.print_text()
    
    
    t4.set_data(keys=keys, data=data, fmts=fmts)
    t4.print_text()
    t4.print_text(summary=2)
    
    
    t5 = Table(keys=keys, data=data, fmts=fmts,primekeys='b:d',parse=True)
    t5.print_text()
    
    t5_keys = t5.get_keywords('b')
    print t5_keys
    data = t5.get_data(keywords=t5_keys)
    print data
    
    data = {'1234567890:1:1':[1,2,3],'1234567890:1:2':[1,2,3]}
    keys = ['1234567890:1:1','1234567890:1:2']
    
    t6 = Table(data=data,keys=keys)
    t6.print_text()
    
    

if __name__ =='__main__':
    test()
