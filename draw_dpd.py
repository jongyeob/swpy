'''
Created on 2014. 1. 10.

:author: jongyeob
'''


def draw_dpd(data, days=0, file_path="", color=""):
    import matplotlib.pyplot as plt
    #
    if (color == ""):
        color = COLOR_LIST
    
    #
    dt = data["t0"]
    
    
    # Date list for X-Axis
    tick_dt = []
    if (days == 0):
        days = (max(dt) - min(dt)).days + 1

    #if (days > 7):
    #       days = 7
    
    for i in range(0, days+1):
        tick_dt.append(dt[0].replace(hour=0, minute=0, second=0) + dt.timedelta(days=i))
    
    # Figure
    fig = plt.figure(facecolor='white')

    plt.clf()
    
    # ticks
    plt.rc('xtick.major', pad=12);
    plt.rc('xtick.major', size=6);
    
    plt.rc('ytick.major', pad=12);
    plt.rc('ytick.major', size=8);
    plt.rc('ytick.minor', size=4);

    # Plot
    plt.plot(dt, data['mev1'], color=color[0], marker="o", label="Proton (> 1 MeV)")
    plt.plot(dt, data['mev10'], color=color[1], marker="*", label="Proton (> 10 MeV)")
    plt.plot(dt, data['mev100'], color=color[2], marker="^", label="Proton (>100 MeV)")

#plt.plot(dt, data['mev06'], color=color[3], marker="^", label="Electron (> .6 MeV)")
    plt.plot(dt, data['mev20'], color=color[4], marker="^", label="Electron (> 2 MeV)")

    plt.legend(loc='upper right')

    
    # Title
    plt.title("NOAA Daily Proton Data")
    
    # Scale
    plt.yscale('log')

    # Limitation
    plt.xlim(tick_dt[0], tick_dt[days-1])
    plt.ylim([1.0e2, 1.0e10])

    # Labels for X and Y axis 
    plt.xlabel("%s $\sim$ %s [UTC]"% \
               (tick_dt[0].strftime("%Y.%m.%d."),
                tick_dt[days-1].strftime("%Y.%m.%d.")),
               fontsize=14)
    
    plt.ylabel("Particles/cm$^{2}$ cm sr")

    
    # X-Axis tick
    tick_dt = []
    tick_str = []

    for i in range(0, days+1, 5):
        tick_dt.append(dt[0].replace(hour=0, minute=0, second=0) + dt.timedelta(days=i))

    for item in tick_dt:
        tick_str.append(item.strftime("%b %d"))

    plt.xticks(tick_dt, tick_str)
    
    # Grid
    plt.grid(True)

    # Show or Save
    if (file_path == ""):
        plt.show()
    else:
        fig.savefig(file_path)
    
    return
