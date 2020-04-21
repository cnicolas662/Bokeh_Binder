from os.path import join, dirname
import datetime
import pandas as pd
from bokeh.models import RadioButtonGroup, TextInput, Div, Paragraph
from bokeh.io import output_file, show
from bokeh.plotting import figure
import bokeh.io
from bokeh.layouts import column, widgetbox, row, layout
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, CustomJS, Slider, TapTool, TextInput
import numpy as np
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import Legend
from bokeh.io import curdoc
import os

#### IMPORT FILES ######

folder = "data" 



### M25 ###
March_M25 = pd.read_csv(join(dirname(__file__), 'data/Github_March_M25.csv'))
  
April_M25 = pd.read_csv(os.path.join(folder, 'Github_April_M25.csv'))
May_M25 = pd.read_csv(os.path.join(folder, 'Github_May_M25.csv'))
June_M25 = pd.read_csv(os.path.join(folder, 'Github_June_M25.csv'))
September_M25 = pd.read_csv(os.path.join(folder, 'Github_September_M25.csv'))
October_M25 = pd.read_csv(os.path.join(folder, 'Github_October_M25.csv'))

### Link Roads ###

March_LR = pd.read_csv(os.path.join(folder, 'Github_March_LinkRoads.csv'))
April_LR = pd.read_csv(os.path.join(folder, 'Github_April_LinkRoads.csv'))
May_LR = pd.read_csv(os.path.join(folder, 'Github_May_LinkRoads.csv'))
June_LR = pd.read_csv(os.path.join(folder, 'Github_June_LinkRoads.csv'))
September_LR = pd.read_csv(os.path.join(folder, 'Github_September_LinkRoads.csv'))
October_LR = pd.read_csv(os.path.join(folder, 'Github_October_LinkRoads.csv'))

              
sites = pd.read_excel(os.path.join(folder, 'Junction_to_Junction.xlsx'))
sites_LR = pd.read_csv(os.path.join(folder, 'Detectors_with_infos.csv'))

#########################

def data_visualization(direction):

    Junctions = sites[sites["Direction"] ==direction]["Jct_to_Jct"].unique().tolist()

    TOOLTIPS = [("Hour", "$x{0.0}"),
                    ("Volume", "@y{0,0}"),]
    List1 = []

    March_= March_M25[March_M25["Direction"] ==direction]
    April_= April_M25[April_M25["Direction"]==direction]
    May_= May_M25[May_M25["Direction"]==direction]
    June_= June_M25[June_M25["Direction"]==direction]
    September_= September_M25[September_M25["Direction"]==direction]
    October_= October_M25[October_M25["Direction"]==direction]

    for i in Junctions:
        March1 = March_[March_["Jct_to_Jct"]==i]
        April1 = April_[April_["Jct_to_Jct"]==i]
        May1 = May_[May_["Jct_to_Jct"]==i]
        June1 = June_[June_["Jct_to_Jct"]==i]
        September1 = September_[September_["Jct_to_Jct"]==i]
        October1 = October_[October_["Jct_to_Jct"]==i]

        Ratio = 0
        AADT_List = [March1["Total Volume"].sum(), April1["Total Volume"].sum(), \
                     May1["Total Volume"].sum(), June1["Total Volume"].sum(), \
                September1["Total Volume"].sum(), October1["Total Volume"].sum()]
        AADT_List = [x for x in AADT_List if x!=0]
        AADT = int(np.mean(AADT_List))
        
        HGV_AADT_List = [March1["HGV Volume"].sum(), April1["HGV Volume"].sum(), \
                     May1["HGV Volume"].sum(), June1["HGV Volume"].sum(), \
                September1["HGV Volume"].sum(), October1["HGV Volume"].sum()]
        HGV_AADT_List = [x for x in HGV_AADT_List if x!=0]
        HGV_AADT = int(np.mean(HGV_AADT_List))
       
        try:
            Ratio = round(HGV_AADT/AADT *100, 1)
        except:
            pass

        if "Dartford" in i:
            name = " - " + str(i)
        else:
            name = " - Junction " + str(i[1:])
        
        p = figure(plot_width=950, plot_height=500, \
                 tools=['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save'], \
                   title = str("M25 ") + str(direction) + name + " : " + "AADT = " + "{:,}".format(AADT)  + \
                   " vehicles/day including " + "{:,}".format(HGV_AADT) + " HGV/day (i.e., " + str(Ratio) + "% HGV)." )

        z = p.line(March1["Hour"], March1["Total Volume"], line_width=3, color="purple", alpha=0.5)
        z1 = p.line(March1["Hour"], March1["HGV Volume"], line_width=3, line_dash = 'dashed', color="purple", alpha=0.5)
        
        a = p.line(April1["Hour"], April1["Total Volume"], line_width=3, color="blue", alpha=0.5)
        a1 = p.line(April1["Hour"], April1["HGV Volume"], line_width=3, line_dash = 'dashed', color="blue", alpha=0.5)

        b = p.line(May1["Hour"], May1["Total Volume"], line_width=3, color="green", alpha=0.5)
        b1 = p.line(May1["Hour"], May1["HGV Volume"], line_width=3, line_dash = 'dashed', color="green", alpha=0.5)

        c = p.line(June1["Hour"], June1["Total Volume"], line_width=3, color="red", alpha=0.5)
        c1 = p.line(June1["Hour"], June1["HGV Volume"], line_width=3, line_dash = 'dashed', color="red", alpha=0.5)

        d = p.line(September1["Hour"], September1["Total Volume"], line_width=3, color="orange", alpha=0.5)
        d1 = p.line(September1["Hour"], September1["HGV Volume"], line_width=3, line_dash = 'dashed', color="orange", alpha=0.5)

        e = p.line(October1["Hour"], October1["Total Volume"], line_width=3, color="pink", alpha=0.5)
        e1 = p.line(October1["Hour"], October1["HGV Volume"], line_width=3, line_dash = 'dashed', color="pink", alpha=0.5)

        f = p.line([0,24], [3600,3600], color='brown', line_dash = 'dashed', line_width=1.5)
        g = p.line([0,24], [2400,2400], color='grey', line_dash = 'dashed', line_width=1.5)
        h = p.line([0,24], [1200,1200], color='black', line_dash = 'dashed', line_width=1.5)

        L = [z, z1, a, a1, b, b1, c,c1, d,d1, e,e1, f, g, h]
        L1 = ["March 2019", "HGV March 2019", "April 2019","HGV April 2019", "May 2019", "HGV May 2019","June 2019", "HGV June 2019",\
              "September 2019", "HGV September 2019", "October 2019","HGV October 2019", \
                 "1 Lane Closure Capacity", "2 Lane Closure Capacity",  "3 Lane Closure Capacity"]

        legend_it = []
        for j in range(len(L)):
            legend_it.append((L1[j], [L[j]]))

        p.xaxis.axis_label = 'Hour'
        p.yaxis.axis_label = 'Average of Hourly Flow'
        legend = Legend(items=legend_it, location=(0, 1))
        legend.click_policy="hide"
        legend.title = 'Legend:'
        legend.border_line_color = "black"
        legend.background_fill_color = "white"
        legend.border_line_width = 2
        legend.background_fill_alpha = 1
        legend.title_text_font_style = "bold"
        p.add_layout(legend, 'right')
        p.add_tools(HoverTool(tooltips=TOOLTIPS, line_policy="interp"))
        tab = Panel(child=p, title=i)
        List1.append(tab)

    return List1
    


def data_visualization_Link_Roads(direction):

    Junctions = sites_LR[sites_LR["Direction"].isin(direction)]["Link Road"].unique().tolist()

    TOOLTIPS = [("Hour", "$x{0.0}"),
                    ("Volume", "@y{0,0}"), 
               ]

    List1 = []

    March_= March_LR[March_LR["Direction"].isin(direction)]
    April_= April_LR[April_LR["Direction"].isin(direction)]
    May_= May_LR[May_LR["Direction"].isin(direction)]
    June_= June_LR[June_LR["Direction"].isin(direction)]
    September_= September_LR[September_LR["Direction"].isin(direction)]
    October_= October_LR[October_LR["Direction"].isin(direction)]
    
    
    
    for i in Junctions:
        sites1 = sites_LR[sites_LR["Direction"].isin([direction[0], direction[1]])]
        direct = sites1[sites1["Link Road"] ==i].iloc[0,8]
        
        March1 = March_[March_["Link Road"]==i]
        April1 = April_[April_["Link Road"]==i]
        May1 = May_[May_["Link Road"]==i]
        June1 = June_[June_["Link Road"]==i]
        September1 = September_[September_["Link Road"]==i]
        October1 = October_[October_["Link Road"]==i]
        
        Ratio = 0
        AADT_List = [March1["Total Volume"].sum(), April1["Total Volume"].sum(), \
                     May1["Total Volume"].sum(), June1["Total Volume"].sum(), \
                September1["Total Volume"].sum(), October1["Total Volume"].sum()]
        AADT_List = [x for x in AADT_List if x!=0]
        AADT = int(np.mean(AADT_List))
        
        HGV_AADT_List = [March1["HGV Volume"].sum(), April1["HGV Volume"].sum(), \
                     May1["HGV Volume"].sum(), June1["HGV Volume"].sum(), \
                September1["HGV Volume"].sum(), October1["HGV Volume"].sum()]
        HGV_AADT_List = [x for x in HGV_AADT_List if x!=0]
        HGV_AADT = int(np.mean(HGV_AADT_List))
        
        try:
            Ratio = round(HGV_AADT/AADT *100, 1)
        except:
            pass

        p = figure(plot_width=950,plot_height=500, \
                   tools=['pan', 'wheel_zoom', 'box_zoom', 'reset', 'save'], \
                   title = str("DBFO Link Road ") + str(i) + " " + str(direct) + " : " + "AADT = " + "{:,}".format(AADT)  + \
                   " vehicles/day including " + "{:,}".format(HGV_AADT) + " HGV/day (i.e., " + str(Ratio) + "% HGV)." )

        z = p.line(March1["Hour"], March1["Total Volume"], line_width=3, color="purple", alpha=0.5)
        z1 = p.line(March1["Hour"], March1["HGV Volume"], line_width=3, line_dash = 'dashed', color="purple", alpha=0.5)
        
        
        a = p.line(April1["Hour"], April1["Total Volume"], line_width=3, color="blue", alpha=0.5)
        a1 = p.line(April1["Hour"], April1["HGV Volume"], line_width=3, line_dash = 'dashed', color="blue", alpha=0.5)

        b = p.line(May1["Hour"], May1["Total Volume"], line_width=3, color="green", alpha=0.5)
        b1 = p.line(May1["Hour"], May1["HGV Volume"], line_width=3, line_dash = 'dashed', color="green", alpha=0.5)


        c = p.line(June1["Hour"], June1["Total Volume"], line_width=3, color="red", alpha=0.5)
        c1 = p.line(June1["Hour"], June1["HGV Volume"], line_width=3, line_dash = 'dashed', color="red", alpha=0.5)


        d = p.line(September1["Hour"], September1["Total Volume"], line_width=3, color="orange", alpha=0.5)
        d1 = p.line(September1["Hour"], September1["HGV Volume"], line_width=3, line_dash = 'dashed', color="orange", alpha=0.5)

        e = p.line(October1["Hour"], October1["Total Volume"], line_width=3, color="pink", alpha=0.5)
        e1 = p.line(October1["Hour"], October1["HGV Volume"], line_width=3, line_dash = 'dashed', color="pink", alpha=0.5)


        f = p.line([0,24], [3600,3600], color='brown', line_dash = 'dashed', line_width=1.5)
        g = p.line([0,24], [2400,2400], color='grey', line_dash = 'dashed', line_width=1.5)
        h = p.line([0,24], [1200,1200], color='black', line_dash = 'dashed', line_width=1.5)

        L = [z, z1, a, a1, b, b1, c,c1, d,d1, e,e1, f, g, h]
        L1 = ["March 2019","HGV March 2019","April 2019","HGV April 2019", "May 2019", "HGV May 2019","June 2019", "HGV June 2019",\
              "September 2019", "HGV September 2019", "October 2019","HGV October 2019", \
                 "1 Lane Closure Capacity", "2 Lane Closure Capacity",  "3 Lane Closure Capacity"]

        legend_it = []
        for j in range(len(L)):
            legend_it.append((L1[j], [L[j]]))

        p.xaxis.axis_label = 'Hour'
        p.yaxis.axis_label = 'Average of Hourly Flow'
        legend = Legend(items=legend_it, location=(0, 1))
        legend.click_policy="hide"
        legend.title = 'Legend:'
        legend.border_line_color = "black"
        legend.background_fill_color = "white"
        legend.border_line_width = 2
        legend.background_fill_alpha = 1
        legend.title_text_font_style = "bold"

        p.add_layout(legend, 'right')
        p.add_tools(HoverTool(tooltips=TOOLTIPS, line_policy="interp"))
        tab = Panel(child=p, title=i)
        List1.append(tab)

    return List1


List1 = data_visualization("Clockwise")
List2 = data_visualization("Anti-clockwise")

List3 = data_visualization_Link_Roads(["Northbound", "Westbound"])
List4 = data_visualization_Link_Roads(["Southbound", "Eastbound"])

tabs_M25CL = Tabs(tabs=List1)
tabs_MACL = Tabs(tabs=List2)
tabs_LR_NW = Tabs(tabs=List3)
tabs_LR_SE = Tabs(tabs=List4)

title = Paragraph(text= 'M25 DBFO: Average Hourly Traffic Profiles', height=30)
title.style={'color': 'black', 'font-weight': 'bold', 'font-family': \
                   'Helvetica Neue, Helvetica, Arial, sans-serif;', 'font-size': '2em'}
title.sizing_mode = "scale_width"
title.margin = 20

presentation = Div(text="""If you require any further information, please contact
        <a href="mailto:clement.nicolas@connectplusm25.co.uk">clement.nicolas@connectplusm25.co.uk</a>.<br>
        <br>
        Click on legend entries to hide the corresponding lines.<br>
        <b>*AADT :</b> Annual Average Daily Traffic
        """)

presentation.style={'color': 'black',  'font-family': \
                   'Helvetica Neue, Helvetica, Arial, sans-serif;', 'font-size': '1.1em'}
presentation.sizing_mode = "scale_width"
presentation.margin = 20

text_banner2 = Paragraph(text= 'M25 : Clockwise (LEFT) versus Anti-Clockwise (RIGHT)', height=30)
text_banner2.style={'color': '#0269A4', 'font-family': \
                   'Helvetica Neue, Helvetica, Arial, sans-serif;', 'font-size': '2em'}
text_banner2.sizing_mode = "scale_width"
text_banner2.margin = 20

text_banner3 = Paragraph(text= 'Link Roads : Northbound/Westbound (LEFT) versus Southbound/Eastbound (RIGHT)', height=30)
text_banner3.style={'color': '#0269A4', 'font-family': \
                   'Helvetica Neue, Helvetica, Arial, sans-serif;', 'font-size': '2em'}
text_banner3.sizing_mode = "scale_width"
text_banner3.margin = 20

bokeh.io.output_notebook()

l = layout([[title], [presentation],
    [text_banner2],
    [tabs_M25CL, tabs_MACL], 
    [text_banner3],
    [tabs_LR_NW,tabs_LR_SE],
])

l.sizing_mode = "scale_width"

curdoc().add_root(l)

