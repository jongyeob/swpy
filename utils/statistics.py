'''
    @author: Seonghwan Choi (shchoi@kasi.re.kr)
             Jongyeob Park (pjystar@gmail.com)
'''

binary_score_keywords= ['yy','yn','ny','nn','acc', 'pody', 'podn', 'far', 'bias', 'csi', 'tss', 'hss', 'gss']

def binary_scores(data):
    '''
    @summary: calculates all scores from 2-dim contingency table
             
    @param data: (tuple) yy, yn, ny, nn 
        yy : the number of 'Yes' forecasts and 'Yes' observations
        yn: the number of 'Yes' forecasts and 'No' observations
        ny: the number of 'No' forecasts and 'Yes' observations
        nn: the number of 'No' forecasts and 'No' observations

    @return: (dict) list of all scores
    
        pody : yy/(yy+ny), probability of detection of 'yes' observations
        podn : nn/(yn+nn), probability of detection of 'no' observations
        far  : yn/(yy+yn), false alarm ratio
        csi  : yy/(yy+ny+yn), critical success index
        bias : (yy+yn)/(yy+ny), forecast bias
        tss  : pody + podn - 1, true skill statistic
        hss  : Heidke skill score, [(yy+nn) - c1] / (total - c1) when .....
        gss  : Gilbert skill score, (yy-c2) / [ (yy-c2) + yn + ny ] when ....
    
    @version: 2013-12-10
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

    if (yy+ny != 0.0):       scores['pody'] = yy/(yy+ny)                       # probabilty of detection of 'yes' observations
    if (yn+nn != 0.0):       scores['podn'] = nn/(yn+nn)                       # probability of detection of 'no' observations
    if (yy+yn != 0.0):       scores['far']  = yn/(yy+yn)                       # false alarm ratio
    if (yy+ny+yn != 0.0):    scores['csi'] = yy/(yy+ny+yn)                     # critical success index
    if (yy+ny != 0.0):       scores['bias'] = (yy+yn)/(yy+ny)                  # forecast bias
    
    scores['tss']	 = scores['pody'] + scores['podn'] - 1                                           # true skill statistic
    if (total-c1 != 0.0):    scores['hss']  = ( (yy+nn) - c1 ) / (total - c1)  # Heidke skill score;
    if (yy-c2+yn+ny != 0.0): scores['gss']  = (yy - c2) / ( ( yy-c2) + yn + ny) # Gilbert skill score

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