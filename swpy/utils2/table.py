'''
Created on 2016. 10. 15.

@author: jongyeob
'''

class TableHeaderIO():
    def __init__(self,key_width=10,prefix=':',sep='='):
        self.prefix = prefix
        self.key_width = key_width
        self.sep = sep
        
            
    def read(self,file,dtype={}):
        data = {}
        
        for line in file:    
            
            if not line.startswith(self.prefix): # pass for comment flag
                continue
            
            p = line.find(self.sep)
            key = line[1:p].strip()
            
            if self.key_width < len(key):
                self.key_width = len(key)
            
            convert = lambda x:x
            if dtype.has_key(key):
                convert = dtype[key]
            
            val = line[p+2:].strip('\r\n#')
         
            
            data[key] = convert(val)
            
            
        return data
    
    def write(self,file,data,keys=[]):
                
        input_keys = keys
        if not keys:
            input_keys = data.keys()
            input_keys.sort()
        
        self.key_width = max([len(k) for k in input_keys])
        style = self.prefix + "{:"+"{}".format(self.key_width)+"s} = {}\n"

        
        for key in input_keys:
            text = style.format(key,data[key])
            file.write(text)        
    
            
class TableIO():
    
    def __init__(self,tab=' '):
        self.tab = tab
        
    def read(self,file,widths,keys=[],dtype={}):
        data = {}
        
        input_widths = widths
        if isinstance(widths,str):
            input_widths = [int(w) for w in widths.split()]
             
        input_keys = ['field{}'.format(i+1) for i in range(len(input_widths))]
         
        if keys:
            input_keys = keys
            
        for k in input_keys:
            data[k] = []
        
        line = ''
        position_list = [1]*len(input_widths)
        for i in range(1,len(input_widths)):
            position_list[i] += sum(input_widths[:i]) + i*len(self.tab)
        
        for line in file:    
            
            if line[0] in ['#',':']: # pass for flags #,:
                continue
         
            eval_row = [ line[p:p+w].strip() for p,w in zip(position_list,input_widths)]
            
            for k,r in zip(input_keys,eval_row):
                convert = dtype.pop(k,lambda x:x)        
                data[k].append(convert(r))
        
        
        return data
        
        
    def write(self,file,data,keys=[],style={},format={}):
        
        input_keys = keys
        
        if not keys:
            input_keys = data.keys()
            input_keys.sort()
        

        style_string = ''
            
        for i,k in enumerate(input_keys):
            
            key_width = len(k)
            if data[k] and not style.has_key(k):
                record_width = max(map(lambda x:len(str(x)), data[k]))
            
            width = [key_width,record_width][key_width<record_width]
            style_format = style.pop(k,width)
            style_unit  = '{:'+ '{}'.format(style_format) +'}'
                
            if i < len(input_keys)-1:
                style_unit += self.tab
                
            style_string += style_unit
        
        
        line = '#'
        line += style_string.format(*input_keys)
        line += '\n'
        file.write(line)
            
        for row_list in zip(*(data[sk] for sk in input_keys) ):
            
             
            row_string = [ ("{:"+format.pop(k,'')+"}").format(r) for k,r in zip(input_keys,row_list) ]
            
            line = ' '
            line += style_string.format(*row_string)
            line += '\n'
            file.write(line)
            
            