#***************************************************************************
#* LIBRARIES
#***************************************************************************
import numpy as np

get_ipython().run_line_magic('matplotlib', 'widget')
import matplotlib.gridspec as gridspec
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Button, TextBox
import matplotlib.pyplot as plt
import seaborn as sns

from dataclasses import dataclass

#***************************************************************************
#* Classes
#***************************************************************************
@dataclass
class UserInputs():
    ref_lat : float 
    ref_long : float

    bld_length : float 

    hub_cp_height : float 
    hub_cp_radius : float 
    hub_cp_offset_dist : float 
    hub_cp_offset_degr : float 

    fwp_radius : float 
    fwp_num_per_level : float 
    fwp_delta_dist_vert : float 
    fwp_delta_dist_horz : float 
    fwp_dist_hub_radius : float 


class ButtonEvent:
    indx = 0
    def view_Top(self,event):
        indx += 1
        print("AAA")
        ax_3D.view_init(elev=90, azim=-90)
        plt.draw()

    def view_Side(self,event):
        indx += 2
        print("BBB")
        ax_3D.view_init(elev=0, azim=90)
        plt.draw()

    def view_Front(self,event):
        indx += 3
        print("CCC")
        ax_3D.view_init(elev=0, azim=0)
        plt.draw()

    def view_3D(self,event):
        indx += 4
        print("DDD")
        ax_3D.view_init(elev=90, azim=90)
        plt.draw()


#***************************************************************************
#* FUNCTION - gen_textboxes
#***************************************************************************
def format_UI():

    # Close all open figures
    for i in plt.get_fignums():
        plt.figure(i)
        plt.close()

    # Creating the figure with a constrained layout to avoid axes overlapping
    fig = plt.figure(figsize=(9, 10), dpi=100, constrained_layout = True)
    fig.suptitle('\nWind Turbine Mission Planning\n', fontstyle='oblique', fontsize='x-large', color="maroon")

    # Creating a gridspec to display 2 distinct Boxes - 3D Graph + User Input
    GridSpec = gridspec.GridSpec(ncols=3, nrows=5, figure= fig, wspace = 0.05, hspace=0.05,height_ratios=(0.05,5,0.05,3,0.05),width_ratios=(0.05,1,0.05))

    # Subfigure which displays 3D Graph
    subfigure_3D = fig.add_subfigure(GridSpec[1,1],facecolor='lightgrey',edgecolor="maroon",linewidth=1)
    ax_3D = subfigure_3D.add_subplot(projection='3d',facecolor='lightgrey')
    ax_3D.set_xlim(-100, 100)
    ax_3D.set_ylim(-100, 100)
    ax_3D.set_zlim(0, 200)
    ax_3D.set_xlabel('X AXIS',color="#800022", fontsize='small')
    ax_3D.set_ylabel('Y AXIS',color="#800022", fontsize='small')
    ax_3D.set_zlabel('Z AXIS',color="#800022", fontsize='small')
    ax_3D.tick_params(labelsize=8)
    ax_3D.xaxis.pane.set_color('lightyellow')
    ax_3D.yaxis.pane.set_color('mintcream')
    ax_3D.zaxis.pane.set_color('lavender')
    
    # Subfigure which displays User Input via Text boxes and buttons
    subfigure_Inp = fig.add_subfigure(GridSpec[3,1],facecolor='lightgrey',edgecolor="maroon",linewidth=1)
    
    # Create sub GridSpec to contain text boxes and buttons
    gs_txt = gridspec.GridSpec(ncols=7, nrows=6, height_ratios=(1,1,1,1,1,1),width_ratios=(0.5,2,2,2,1.5,3,0.25))
    gs_txt.update(left=0.2,   hspace=0.75, wspace=0.75)
    ax_txtbox = [subfigure_Inp.add_subplot(gs_txt[i,j]) for i,j in [[0,1],[0,3],[0,5],[1,1],[1,3],[1,5],[2,1],[2,3],[2,5],[3,1],[3,3],[3,5],[4,1],[4,3],[5,1],[5,3],[5,5],[4,5]]]
    
    return ax_3D, ax_txtbox
    
#***************************************************************************
#* FUNCTION - gen_textboxes
#***************************************************************************
def gen_textboxes(ax_txtbox,ds_user_inputs):    
    # create the textboxes
    tb_ref_lat = TextBox(ax_txtbox[0],'Ref Latitude',  initial = str(ds_user_inputs.ref_lat), label_pad=0.05)
    tb_ref_long = TextBox(ax_txtbox[1],'Ref Longitude', initial = str(ds_user_inputs.ref_long), label_pad=0.05)

    # create TextBox objects with initial values - Hub
    tb_bld_length = TextBox(ax_txtbox[3], 'Blade Length', initial=str(ds_user_inputs.bld_length), label_pad=0.05)
    tb_hub_cp_height = TextBox(ax_txtbox[6], 'Hub CP - Height', initial=str(ds_user_inputs.hub_cp_height), label_pad=0.05)
    tb_hub_cp_radius = TextBox(ax_txtbox[9], 'Hub CP - Radius', initial=str(ds_user_inputs.hub_cp_radius), label_pad=0.05)
    tb_hub_cp_offset = TextBox(ax_txtbox[12], 'Offset from (0,0)', initial=str(ds_user_inputs.hub_cp_offset_dist), label_pad=0.05)
    tb_hub_cp_offset_degr = TextBox(ax_txtbox[14], 'Degrees from MN', initial=str(ds_user_inputs.hub_cp_offset_degr), label_pad=0.05)


    # create TextBox objects with initial values - Waypoints
    tb_fwp_radius = TextBox(ax_txtbox[4], 'WP Radius', initial=str(ds_user_inputs.fwp_radius), label_pad=0.05)
    tb_fwp_num_per_level = TextBox(ax_txtbox[7], 'WPs per level', initial=str(ds_user_inputs.fwp_num_per_level), label_pad=0.05)
    tb_fwp_delta_dist_vert = TextBox(ax_txtbox[10], 'Delta Vert Dist', initial=str(ds_user_inputs.fwp_delta_dist_vert), label_pad=0.05)
    tb_fwp_delta_dist_horz = TextBox(ax_txtbox[13], 'Delta Horiz Dist', initial=str(ds_user_inputs.fwp_delta_dist_horz), label_pad=0.05)
    tb_fwp_dist_hub_radius = TextBox(ax_txtbox[15], 'Min Dist from Hub', initial=str(ds_user_inputs.fwp_dist_hub_radius), label_pad=0.05)

    text_box_wp_safetyDistFromHub = TextBox(ax_txtbox[17], 'Num Figures', plt.get_fignums(), hovercolor='0.975', label_pad=0.05)

#***************************************************************************
#* FUNCTION - gen_buttons
#***************************************************************************
def gen_buttons(ax_txtbox,ax_3D):
    
    bt_event = ButtonEvent()
    
    #Top View
    but_top_view = Button(ax_txtbox[2], 'Top',color="yellow", hovercolor="blue")
    but_top_view.on_clicked(bt_event.view_Top)
    
    #Side View
    but_side_view = Button(ax_txtbox[5], 'Side',color="yellow", hovercolor="blue")
    but_side_view.on_clicked(bt_event.view_Side)
    
    #3D View
    but_3D_view = Button(ax_txtbox[11], '3D',color="yellow", hovercolor="blue")
    but_3D_view.on_clicked(bt_event.view_3D)
    
    #Front View
    but_front_view = Button(ax_txtbox[8], 'Front',color="yellow", hovercolor="blue")
    but_front_view.on_clicked(bt_event.view_Front)

    but_Submit = Button(ax_txtbox[16], 'Submit',color="red", hovercolor="blue")

#***************************************************************************
#* FUNCTION - Main Function
#***************************************************************************
def main():
    mark = 0

    ds_user_inputs = UserInputs(0,0,75,5,0,6,75,10,8,10,3,4)
    print(ds_user_inputs.ref_lat)
    
    ax_3D, ax_txtbox = format_UI() # Generate Main Plot Format
    gen_textboxes(ax_txtbox,ds_user_inputs)
    gen_buttons(ax_txtbox,ax_3D)
    plt.show()

#***************************************************************************
#* CONSTRUCTER - MAIN NAME - Call Main Function
#***************************************************************************
main()