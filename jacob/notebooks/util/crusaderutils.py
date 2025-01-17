import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex, Normalize
from matplotlib.patches import Polygon
from matplotlib.colorbar import ColorbarBase
from mpl_toolkits.basemap import Basemap as Basemap
#supress deprecated warnings for now
import warnings
warnings.filterwarnings("ignore")

### state lists, by abbreviation and by state name
statelist_abbrs = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL",
"GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI",
"MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
"OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
"WI", "WY"]

statelist_names = ["Alaska", "Alabama", "Arizona", "Arkansas", "California",
"Colorado", "Connecticut", "Delaware", "Florida", "Georgia","Hawaii", "Idaho",
"Illinois", "Indiana", "Iowa", "Kansas", "Kentucky","Louisiana", "Maine",
"Maryland","Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
"Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey","New Mexico",
"New York", "North Carolina", "North Dakota","Ohio", "Oklahoma", "Oregon",
"Pennsylvania", "Rhode Island", "South Carolina","South Dakota", "Tennessee",
"Texas", "Utah", "Vermont", "Virginia", "Washington","West Virginia",
"Wisconsin", "Wyoming"]

### feed list of values to pair with states by name or abbr
### returns dict with state name/abbr as key, list values as vals
make_state_obj_abbrs = lambda vals: {x:y for x,y in zip(statelist_abbrs,vals)}
make_state_obj_names = lambda vals: {x:y for x,y in zip(statelist_names,vals)}

### stateobj_names --> dict {'statename0':val,'statename1':val,...}
### min --> smallest val value
### max ---> larget val value
### map_title --> 'some cool name for this map' or default
def map_compare_states(stateobj_names, min, max, map_title='TRI Visualization',c='viridis'):
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
                projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    shp_info = m.readshapefile('./state_shapes/cb_2016_us_state_500k','states',drawbounds=True)

    colors={}
    statenames=[]
    #set colors here -- plt.cm.<color set type>
    # other color types than viridis are plasma, inferno, magma, more at https://matplotlib.org/users/colormaps.html
    #TODO: add arg to select color map -- maybe several preset options
    if c == 'viridis':
        cmap = plt.cm.viridis
    elif c == 'autumn':
        cmap = plt.cm.autumn
    elif c == 'plasma':
        cmap = plt.cm.plasma
    elif c == 'inferno':
        cmap = plt.cm.inferno
    elif c == 'magma':
        cmap = plt.cm.magma
    elif c == 'Greys':
        cmap = plt.cm.Greys

    #set value ranges
    vmin = min; vmax = (max + (max*0.15))
    ignore = ['District of Columbia','United States Virgin Islands','Puerto Rico','American Samoa','Guam','Commonwealth of the Northern Mariana Islands']
    for shapedict in m.states_info:
        statename = shapedict['NAME']
        # ignore shapes in shapefile that we don't want -- ie: non-states
        if statename not in ignore:
            # takes array of state names with values {'Alabama':<value>,'Alaska':<value>,...}
            val = stateobj_names[statename]
            # calling colormap with value between 0 and 1 returns
            # rgba value.
            colors[statename] = cmap(1.-np.sqrt((val-vmin)/(vmax-vmin)))[:3]
        statenames.append(statename)

    # cycle through state names, color each one.
    for nshape,seg in enumerate(m.states):
        if statenames[nshape] not in ignore:
            # translate alaska and hawaii to be on our US map
            if statenames[nshape] == 'Alaska':
                # alaska needs to be scaled down to fit
                seg = list(map(lambda (x,y): (0.25*x + 750000, 0.25*y-800000), seg))
            if statenames[nshape] == 'Hawaii':
                seg = list(map(lambda (x,y): (x + 5100000, y-1300000), seg))

            color = rgb2hex(colors[statenames[nshape]])
            poly = Polygon(seg,facecolor=color,edgecolor=color)
            ax = plt.gca()
            ax.add_patch(poly)
    #so we can see alaska and Hawaii
    #TODO: figure out how to draw alaska and hawaii boundaries and translate
    m.drawmapboundary(fill_color='#99eeff')
    plt.title(map_title)
    cax = plt.gcf().add_axes([0.33, 0.72, 0.4, 0.015]) # posititon
    cb = ColorbarBase(cax,cmap=cmap.reversed(),norm=Normalize(vmin=vmin, vmax=vmax),orientation='horizontal',label='Emission in Pounds -- Darker == Higher Value')
    cb.ax.set_xticklabels([])
    cb.ax.set_xticks([])
    cb.ax.xaxis.set_label_position('top')
    plt.show()
