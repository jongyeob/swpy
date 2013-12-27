'''
Created on 2013. 12. 15.

@author: Jongyeob
'''
def empty_data(keys):
    pass

def convert_text(data,keys=None):
    '''
    @summary:           Convert data to text format
    '''
    text = ''
    
    input_data = data
    input_keys = data.keys()
    input_keys.sort()
    if keys != None:
        input_data = select_keys(data,keys)
        input_keys = keys
        
                 
    for i in range(len(data.values()[0])):
        for key in input_keys:
            if i == 0:
                text += key + ' '
            else:
            
                text += str(input_data[key][i-1])
                text += ' '
        text += '\n'
                    
        
    return text
def select_keys(data,keys):
    '''
    @summary: select data and making new data
    '''
    
    selected_data = {}
    for key in data.iterkeys():
        try:
            keys.index(key)
            selected_data[key] = data[key]
        except:
            continue
    
    return selected_data
    

def combine_data(*data_args,**kargs):
    '''
    @precondition: data have same number of list, ans same period
    
    ex1) combine_data(data1,data2)
    ex2) combine_data(data1,(data2,'prefix2'))
    ex3) combine)data((data1,'prefix'),(data2,'prefix2'),operation=['overlap','sort'])
    
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
        
        
    
def key_namespaces(keyname_string):
    '''
    Resolve keynames from seperation (:)
    @return: (list)
    '''
    ret = keyname_string.split(':')
    ret.sort(reverse=True)
    return ret
    
def test():
    
    ret = key_namespaces('')
    print ('\'\' : '+ str(ret))
    ret = key_namespaces('a')
    print ('a : '+ str(ret))
    ret = key_namespaces('a:b:c')
    print ('a:b:c'+str(ret))

if __name__ =='__main__':
    test()