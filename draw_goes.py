'''
Created on 2014. 2. 17.

@author: jongyeob
'''
import datetime
import matplotlib.pyplot as plt

def draw_goes_xray(dt, v0, v1=0, v2=0, days=3, file_path="", color=""):
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
      
    # Plot
    plt.plot(dt, v0, color=color[0])
    if (v1 != 0):
        plt.plot(dt, v1, color=color[1])

    # Title
    plt.title("GOES X-ray Flux (1 minute data)")

    # X-Axis
    plt.xlim(tick_dt[0], tick_dt[3])
    plt.xlabel("%s $\sim$ %s [UTC]"% \
               (tick_dt[0].strftime("%Y.%m.%d."),
                tick_dt[days-1].strftime("%Y.%m.%d.")),
                fontsize=14)
    
    # Y-Axis
    plt.yscale('log')
    plt.ylim([1.0e-9, 1.0e-2])
    plt.ylabel("Watts/m$^{2}$")

    # ticks
    plt.rc('xtick.major', pad=10);
    plt.rc('xtick.major', size=6);
    
    plt.rc('ytick.major', pad=12);
    plt.rc('ytick.major', size=8);
    plt.rc('ytick.minor', size=4);
    
    # X-Axis tick
    tick_str = []
    for item in tick_dt:
        tick_str.append(item.strftime("%b %d"))
    plt.xticks(tick_dt, tick_str)

    # Grid
    plt.grid(True)

    # Text
    fig.text(0.91, 0.72, 'X', fontsize=11, ha='left', va='center')
    fig.text(0.91, 0.61, 'M', fontsize=11, ha='left', va='center')
    fig.text(0.91, 0.50, 'C', fontsize=11, ha='left', va='center')
    fig.text(0.91, 0.39, 'B', fontsize=11, ha='left', va='center')
    fig.text(0.91, 0.28, 'A', fontsize=11, ha='left', va='center')

    fig.text(0.93, 0.65, "GOES-15 0.5-4.0 $\AA$", fontsize=12, ha='left', va='center', rotation='vertical', color=color[1])
    fig.text(0.93, 0.35, "GOES-15 0.5-4.0 $\AA$", fontsize=12, ha='left', va='center', rotation='vertical', color=color[0])

    # Show or Save
    if (file_path == ""):
        plt.show()
    else:
        fig.savefig(file_path)

    return

def draw_goes_mag(dt, v0, v1=0, v2=0, days=3, file_path="", color=""):
    
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
    plt.title("GOES Magnetometer (1 minute data)")
    
    # X-Axis
    plt.xlim(tick_dt[0], tick_dt[3])
    plt.xlabel("%s $\sim$ %s [UTC]"% \
               (tick_dt[0].strftime("%Y.%m.%d."),
                tick_dt[days-1].strftime("%Y.%m.%d.")),
                fontsize=14)

    # Y-Axis
    plt.ylim([0, 200])
    plt.yscale('linear')
    plt.ylabel("NanoTesla [nT]")
    
    
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
    
    # Text
    fig.text(0.92, 0.5, 'GOES 13 Hp Long. W 75', fontsize=12, ha='left', va='center', rotation='vertical', color=color[1])
    fig.text(0.95, 0.5, 'GOES 15 Hp Long. W 134', fontsize=12, ha='left', va='center', rotation='vertical', color=color[0])
    

    # Plot, and Show or Save
    plt.plot(dt, v0, color=color[0])
    
    if (file_path == ""):
        plt.show()
    else:
        fig.savefig(file_path)
    
    return

def draw_goes_proton(dt, v0, v1=0, v2=0, days=3, file_path="", color=""):
    
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
    plt.title("GOES Proton Flux (1 minute data)")
    
    # X-Axis
    plt.xlim(tick_dt[0], tick_dt[3])
    plt.xlabel("%s $\sim$ %s [UTC]"% \
               (tick_dt[0].strftime("%Y.%m.%d."),
                tick_dt[days-1].strftime("%Y.%m.%d.")),
                fontsize=14)    

    # Y-Axis
    plt.ylim([1.0e-2, 1.0e4])
    plt.yscale('log')
    plt.ylabel("Particles cm$^{-2}$s$^{-1}$sr$^{-1}$")
    
    
    # Style for Ticks
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
    
    # Text
    fig.text(0.93, 0.65, '$\ge$10 MeV', fontsize=12, ha='left', va='center', rotation='vertical', color=color[2])
    fig.text(0.93, 0.50, '$\ge$50 MeV', fontsize=12, ha='left', va='center', rotation='vertical', color=color[1])
    fig.text(0.93, 0.35, '$\ge$100 MeV', fontsize=12, ha='left', va='center', rotation='vertical', color=color[0])
    
    # Plot, and Show or Save
    plt.plot(dt, v0, color=color[0])
    
    if (file_path == ""):
        plt.show()
    else:
        fig.savefig(file_path)

    
    return


def draw_goes_electron(dt, v0, v1=0, v2=0, days=3, file_path="", color=""):
    
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
    plt.title("GOES Electron Flux (1 minute data)")
    
    # X-Axis
    plt.xlim(tick_dt[0], tick_dt[3])
    plt.xlabel("%s $\sim$ %s [UTC]"% \
               (tick_dt[0].strftime("%Y.%m.%d."),
                tick_dt[days-1].strftime("%Y.%m.%d.")),
               fontsize=14)    
    
    # Y-Axis
    plt.ylim([1.0e-1, 1.0e7])
    plt.yscale('log')
    plt.ylabel("Particles cm$^{-2}$s$^{-1}$sr$^{-1}$")
    
    
    # Style for Ticks
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
    
    # Text
    fig.text(0.93, 0.65, '$\ge$10 MeV', fontsize=12, ha='left', va='center', rotation='vertical', color=color[2])
    fig.text(0.93, 0.50, '$\ge$50 MeV', fontsize=12, ha='left', va='center', rotation='vertical', color=color[1])
    fig.text(0.93, 0.35, '$\ge$100 MeV', fontsize=12, ha='left', va='center', rotation='vertical', color=color[0])
    
    # Plot, and Show or Save
    plt.plot(dt, v0, color=color[0])
    
    if (file_path == ""):
        plt.show()
    else:
        fig.savefig(file_path)
    
    
    return