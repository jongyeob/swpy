'''
    @author: Seonghwan Choi (shchoi@kasi.re.kr)
             Jongyeob Park (pjystar@gmail.com)
'''
from __future__ import absolute_import


binary_score_keywords= ['yy','yn','ny','nn','acc', 'pody', 'podn', 'far', 'bias', 'csi', 'tss', 'hss', 'gss']

def f_score(c,beta=1):
    '''
    return f-score
    '''
    b2 = beta*beta
    f  = (1+b2)*c['yy']
    f_ = f + b2*c['ny'] + c['yn'] 
    
    return f/f_
def relative_value(c,alpha=1):
    '''
    return relative_value, alpha is cost/loss ratio
    '''
    freq = (c['yy']+c['ny']) / (c['yy']+c['ny']+c['yn']+c['nn']) # Event frequency
    
    me_cli  = min(alpha,freq) # Mean expected expense for climate forecast
    me_perf = freq*alpha      # Mean expected expense for Perfect forecast
    me_fore = c['pofd']*alpha*(1-freq) \
              - c['pody']*(1-alpha)*freq \
              + freq          # Mean expected expense for forecast
    
    return (me_fore - me_cli)/(me_perf - me_cli)
     
def binary_scores(data):
    '''
    calculates all scores from 2-dim contingency table
             
    :param data: (tuple) yy, yn, ny, nn 
        yy : the number of 'Yes' forecasts and 'Yes' observations
        yn: the number of 'Yes' forecasts and 'No' observations
        ny: the number of 'No' forecasts and 'Yes' observations
        nn: the number of 'No' forecasts and 'No' observations

    :return: (dict) list of all scores
    
        pody : yy/(yy+ny), probability of detection of 'yes' observations
        podn : nn/(yn+nn), probability of detection of 'no' observations
        pofd : yn/(yn+nn), probability of false detection, so called false alarm rate
        far  : yn/(yy+yn), false alarm ratio
        csi  : yy/(yy+ny+yn), critical success index
        bias : (yy+yn)/(yy+ny), forecast bias
        tss  : pody + podn - 1, true skill statistic
        hss  : Heidke skill score, [(yy+nn) - c1] / (total - c1) when .....
        gss  : Gilbert skill score, (yy-c2) / [ (yy-c2) + yn + ny ] when ....
        
    
    '''
    
    scores = {}
    yy,yn,ny,nn  = [float(i) for i in data]
    scores['yy'],scores['yn'],scores['ny'],scores['nn'] = yy,yn,ny,nn
    
    total = float(yy+yn+ny+nn)
    if (total == 0):
        print("yy, yn, nn, ny are 0.")
        return False
    
    scores['acc']	= (yy+nn) / total
    c1	= ( (yy+yn) * (yy+ny) + (ny+nn) * (yn+nn) ) / total
    c2	= (yy+yn) * (yy + ny) / total
    
    #print ("yy=%(yy)d, yn=%(yn)d, ny=%(ny)d, nn=%(nn)d, yy+nn=%(yynn)d, all=%(all).4f"%{"yy":yy, "yn":yn, "ny":ny, "nn":nn, "yynn":yy+nn,"all":all})

    try :    scores['pody'] = yy/(yy+ny)                       # probabilty of detection of 'yes' observations
    except : scores['pody'] = float('nan')
    try :    scores['podn'] = nn/(yn+nn)                       # probability of detection of 'no' observations
    except : scores['podn'] = float('nan')
    try :    scores['pofd'] = yn/(yn+nn)                       # probability of false detection
    except : scores['pofd'] = float('nan')
    try :    scores['far']  = yn/(yy+yn)                       # false alarm ratio
    except : scores['far']  = float('nan')
    try :    scores['csi']  = yy/(yy+ny+yn)                     # critical success index
    except : scores['csi']  = float('nan')
    try :    scores['bias'] = (yy+yn)/(yy+ny)                  # forecast bias
    except : scores['bias'] = float('nan')
    
    scores['tss']	 = scores['pody'] + scores['podn'] - 1                                           # true skill statistic
    try:     scores['hss']  = ( (yy+nn) - c1 ) / (total - c1)  # Heidke skill score;
    except : scores['hss']  = float('nan')
    try:     scores['gss']  = (yy - c2) / ( ( yy-c2) + yn + ny) # Gilbert skill score
    except : scores['gss']  = float('nan')
    
     

    return scores

def binary_scores_text(scores):
    
    yy = scores['yy']
    yn = scores['yn']
    ny = scores['ny']
    nn = scores['nn']
    total = yy+yn+ny+nn
    
    text = ''    
    text.append("           Observation\n")
    text.append("               Y     N\n")
    text.append("----------------------------\n");
    text.append("Forecast Y %5d %5d %5d\n"% yy, yn, yy+yn)
    text.append("         N %5d %5d %5d\n"% ny, nn, ny+nn)
    text.append("           %5d %5d %5d\n"% yy+ny, yn+nn, total)
    text.append("\n")
    text.append("pody = %.4f"% scores['pody'])
    text.append("podn = %.4f"% scores['podn'])
    text.append("far  = %.4f"% scores['far'])
    text.append("csi  = %.4f"% scores['csi'])
    text.append("bias = %.4f"% scores['bias'])
    text.append("tss  = %.4f"% scores['tss'])
    text.append("hss  = %.4f"% scores['hss'])
    text.append("gss  = %.4f"% scores['gss'])
    text.append("")
    return text
