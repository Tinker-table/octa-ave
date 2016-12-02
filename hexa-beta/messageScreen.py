#screen = 0 vendor,screen = 1 customer.

import GLCD as g


fontWidth = 6
lineLength = 21

def msg(m = 'Error!!!',linenum = 7):
    #vendor Screen
    g.clearDisplay(0)
    string = ("{:^%d}" % lineLength).format(m)
    g.displayText(string,linenum,0,0)
   

    #User Screen
    g.clearDisplay(1)
    string = ("{:^%d}" % lineLength).format(m)
    g.displayText(string,linenum,0,1)
