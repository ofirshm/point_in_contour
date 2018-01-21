import numpy as np
import matplotlib.pyplot as plt
def onclick(event):
    '''
    This function defines the real-time answer for each mouse event  
    :param event: contains the mouse information
    :return: refresh the figure title with the information for the coordinates and whether it is the contour
    '''
    # out of border make errors
    try:
        #Get the mouse coordinates
        x_pos = int(event.xdata)
        y_pos = int(event.ydata)
        answer = "Point (" + str(x_pos) + ", " + str(y_pos) + ") is "
        #concrate if the point is in the conour using pnpoly
        if pnpoly(point(x_pos, y_pos), img):
            answer += "in"
        else:
            answer += "not in "

        plt.title(answer)
        fig.canvas.draw()


    #reset the title for error
    except:
        plt.title('')
        fig.canvas.draw()
        pass

    # print('%s click: button=%d,  xdata=%f, ydata=%f' %
    #       ('double' if event.dblclick else 'single', event.button,
    #        event.xdata, event.ydata))
    # p=point(int(event.xdata),int(event.ydata))
    # print("IS IN") if pnpoly(p, img) else print("NOT IN")


def pnpoly(p,img):
    '''
    This function checks if point p is in image I
    :param p:     point object with p.x and p.y value within the image region
    :param i:     The image 

    :return: True if the point is in the contour and False if the point outside the contour
    
    '''
    state=False
    #If the point on the contour, we are outside the function
    if img[p.x,p.y]==0:
        return state
    #Set our region of interest, as the x coordinate of the point , extract i value for this points.
    x_i=img[int(p.x),0:int(p.y)]
    #define intersect as the points where we meet the contour
    intersects=np.asarray(np.where( x_i==0)[0])
    #next code checks the suspected area contour and decide about the out put
    #We use 2 flags to catch which type of border we encounter ,
    flag_r=False
    flag_l=False
    for y_suspect in intersects:
        suspected_point=point(x=p.x,y=y_suspect)
        #crop region of interest for every suspected point 3x3
        suspected_area= img[(suspected_point.x-1):(suspected_point.x+2),
                        (suspected_point.y-1):(suspected_point.y+2) ]
        #is_border function decide the area type
        border_type=is_border(suspected_area)

        if border_type=='border':#Change state for defined border type
            state= not state
        elif border_type=='Right':
            if flag_r==True:# in this case we already saw a right border
                flag_r=False#That means we didnt pass any border, we reset the flag and continue
                continue
            elif flag_l==True:# in this case we saw a half left border , which means we passed a  border;reset flags and change state
                flag_r=False
                flag_l=False
                state = not state
            else:#we didn't see any other flag yet
                flag_r=True
        elif type == 'Left':#same logic.
            if flag_l==True:
                flag_l=False
                continue
            elif flag_r==True:
                flag_r=False
                flag_l=False
                state = not state
            else:
                flag_l=True

    return state

def is_border(suspected_area):#
    '''
    This function output the border type for each suspected area, there are 4 defined option
    :param suspected_area: 3x3 np array , must contain 3 pixels(0 value, rest is 255) in total
    :return: specific string, one might choose enum 
    'border -if the suspected area is border
    False if the state is a cornered state- left or right
    'Right' /'Left' if the pattern correspond to right\corner corner
    'line' and False indicate about state but shouldn't be considered during implementation
    '''
    sum_area = np.sum(suspected_area == 0, 1)#the shape depends only over the sum over x axis of the suspected area
    if (sum_area==[1,1,1]).all():
        return 'border'
    if (sum_area == [0, 1, 2]).all():#corner
        return False
    if (sum_area == [2, 1, 0]).all():#corner
        return False
    if (sum_area == [0, 3, 0]).all():
        return 'line'
    if (sum_area == [1, 2, 0]).all():
        return 'Right'
    if (sum_area == [0, 2, 1]).all():
        return 'Left'

class point(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y


if __name__=='__main__':

    #Select for image visualization
    visualization=True

    #Load input sample
    img=np.load('input_sample.npy')
    #image x,y limits
    (i_x_size,i_y_size)=img.shape

    if visualization:
        fig = plt.figure()
        implot = plt.imshow(img,cmap='gray',vmin=0,vmax=255,origin='lower')
        fig.suptitle('Given contour image', fontsize=14, fontweight='bold')
        plt.gca().set_xlim([0,i_x_size])
        plt.gca().set_ylim([0,i_y_size])
        plt.colorbar()
        cid = fig.canvas.mpl_connect('motion_notify_event', onclick)
        plt.show()




