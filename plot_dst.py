'''
Created on 2013. 12. 30.

@author: jongyeob
'''
def draw_dst(dt, v0, v1=0, v2=0, days=7, file_path="", color=""):
    
    #
    global color_list
    if (color == ""):
        color = color_list
    
    # Date list for X-Axis
    tick_dt = []
    for i in range(0, days+1):
        tick_dt.append(dt[0].replace(hour=0, minute=0, second=0) + datetime.timedelta(days=i))
    
    # Figure
    fig = plt.figure(facecolor='white')
    plt.clf()
    #plt.rc('text', usetex=True)
    
    # Title
    plt.title("Dst Index")

    # X-Axis
    plt.xlim(tick_dt[0], tick_dt[days-1])
    plt.xlabel("%s $\sim$ %s [UTC]"% \
            (tick_dt[0].strftime("%Y.%m.%d."),
             tick_dt[days-1].strftime("%Y.%m.%d.")),
             fontsize=14)
    
    # Y-Axis
    plt.ylim([-120, 50])
    plt.yscale('linear')
    plt.ylabel("Dst [nT]")
    
    
    # ticks
    plt.rc('xtick.major', pad=10);
    plt.rc('xtick.major', size=6);
    
    plt.rc('ytick.major', pad=12);
    plt.rc('ytick.major', size=8);
    plt.rc('ytick.minor', size=4);
    
    # X-Axis Ticks
    tick_str = []
    for item in tick_dt:
        tick_str.append(item.strftime("%b %d"))
    plt.xticks(tick_dt, tick_str)
    
    
    
    # Grid
    plt.grid(True)

    # Plot, and Show or Save
    plt.plot(dt, v0, color=color[0])
    
    if (file_path == ""):
        plt.show()
    else:
        fig.savefig(file_path)
    
    return
