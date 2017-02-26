'''
Created on 2016. 10. 15.

@author: jongyeob
'''

class TableIO():
    def __init__(self,style,tab=' '):
        '''
            style: list of column format specified by python
        '''
        self.tab = tab 
        self.style  = ''
        for i,s in enumerate(style):
            style_unit  = '{:'+ '{}'.format(style[i]) +'}'
            
            if i < len(style)-1:
                style_unit += tab
                
            self.style += style_unit
        
        
    def read(self,file,key,type=[]):
        data = {}
        for k in key:
            data[k] = []
        
        line = ''
        style_list = self.style.split(self.tab)
        length_list = [len(s.format('')) for s in style_list]
        position_list = [1]*len(style_list)
        
        
        for i in range(1,len(style_list)):
            position_list[i] += sum(length_list[:i]) + i*len(self.tab)
        
        idx = 0
        for line in file:
            
            
            if line[0] in ['#']: # pass for comment flag
                continue
         
            eval_row = [ line[p:p+l].strip() for p,l in zip(position_list,length_list)]
         
            for k,r in zip(key,eval_row):
                data[k].append(r)
        
        return data
        
        
    def write(self,file,data,key=[],format=[]):
        
        selected_key = data.keys()
        if key:
            selected_key = key
            
        line = '#'
        line += self.style.format(*selected_key)
        line += '\n'
        file.write(line)



        format_list = []

        for f in format:
            format_string = '{:'+ '{}'.format(f) +'}'
            format_list.append(format_string)
            
        if not format_list:
            format_list = self.style.split(self.tab)
        
        
        for row_list in zip(*(data[sk] for sk in selected_key) ):
            
            row_string = [ f.format(r) for f,r in zip(format_list,row_list) ]
            
            line = ' '
            line += self.style.format(*row_string)
            line += '\n'
            file.write(line)