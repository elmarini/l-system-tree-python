import maya.cmds as cmds
import math
import random


#VECTORS#
#-------#
# correct vector length - find unit vector
def unitVect(_vect):
    unitVect = []                                                        #create empty list to store unit vector
    magnitude = math.sqrt( (_vect[0]**2 + _vect[1]**2 + _vect[2]**2) )      #find magnitude
    if magnitude == 0:                                                   #if magnitude is 0, do not change vector.
        return _vect
    for i in range(3):
       unitVect.append (_vect[i] / magnitude)                             #divide vector by its magnitude, modifying the vector's elements
    return unitVect


#CREATE TURTLE#
#-------------#
    #init turtle#
    #Creates a turtle data record, which keeps track of the turtle's current state
    #position = vector from the origin to the turtle's current position (P1).
    #heading = direction of travel (UNIT vector P1 to P2)
    #fill = extrudes along curves with either polygons or nurbs surfaces.
    #size = (width, height) of fill
    #sf = constant that the top of the branch decrements by. sf should increase according with level.
    
    #turn Z/Y/X#    
    #rotates turtle heading vector 
    #angle = angle of rotation    
    
    #forward#
    #draws in curves and extrudes along them with either nurbs surfaces or polyplanes depending on turtle.fill
    #new position = current position + (direction of travel * distance to travel in that direction) = turtle.position + (turtle.heading * length)
    #Current position is the vector from O --> P1, (heading*length) is vector from P1--> P2. 
    #Add together to get vector from O --> P2 (origin to new position).

#create empty object/class
class Turtle():    
    pass
    
#set object layout procedure
def init( turtle, _position = [0.0,0.0,0.0],  _heading = [0.0,1.0,0.0], _pen = True, _fill = ['poly'], _size = 0.5, _sf = 0.85, _curveNum = 0 ):
    turtle.position = _position 
    turtle.heading = _heading 
    turtle.pen = _pen  
    turtle.fill = _fill
    turtle.size = _size
    turtle.sf = _sf
    turtle.curveNum = _curveNum

#turn along z-axis      
def turnZ ( turtle, _angle):                   
    theta = math.radians(_angle)      
    #rotates old heading vector to find new heading. 
    px = turtle.heading[0] * math.cos(theta)  -  turtle.heading[1] * math.sin(theta) 
    py = turtle.heading[0] * math.sin(theta) +  turtle.heading[1] * math.cos(theta)
    #update turtle heading     
    turtle.heading = unitVect([ px,  py, turtle.heading[2] ])

#turn along y-axis (twisting)
def turnY( turtle, _angle):    
    theta = math.radians(_angle)  
    px = turtle.heading[0] * math.cos(theta)  +  turtle.heading[2] * math.sin(theta) 
    pz = -turtle.heading[0] * math.sin(theta) +  turtle.heading[2] * math.cos(theta)    
    turtle.heading = unitVect([ px,  turtle.heading[1], pz ])

#turn along x-axis (elevate and lower)
def turnX( turtle, _angle):    
    theta = math.radians(_angle)     
    py = turtle.heading[1] * math.cos(theta)  -  turtle.heading[2] * math.sin(theta) 
    pz = turtle.heading[1] * math.sin(theta) +  turtle.heading[2] * math.cos(theta)
    turtle.heading = unitVect([ turtle.heading[0], py, pz ]) 

#draws curve and updates position
def forward ( turtle, _length):        
    newPosition = [ turtle.position[0] + (turtle.heading[0]* _length)  , turtle.position[1] + (turtle.heading[1] * _length), turtle.position[2] + (turtle.heading[2] * _length)]   
    if turtle.pen == True:
        cmds.curve(p = [turtle.position, newPosition ], d = 1, name = 'curve' + str(turtle.curveNum) ) 
        if turtle.fill[0] == 'poly':
            cmds.polyPlane (name = 'plane' + str(turtle.curveNum), w = turtle.size, h = turtle.size, sx = 1, sy = 1)           
            cmds.setAttr ( 'plane' + str(turtle.curveNum) + '.translate', turtle.position[0], turtle.position[1], turtle.position[2], type = 'double3' )   
            cmds.polyExtrudeFacet ( 'plane' + str(turtle.curveNum) , inc = 'curve'+ str(turtle.curveNum) )
            cmds.setAttr ( 'polyExtrudeFace'+ str(turtle.curveNum + 1) + '.taper' , turtle.sf)    #taper branch
        elif turtle.fill[0] == 'nurbs':
            cmds.circle( center = turtle.position, radius = turtle.size, normal = turtle.heading, sections = 1,  name = 'circle' + str(turtle.curveNum) )
            cmds.extrude ( 'circle' + str(turtle.curveNum), 'curve' + str(turtle.curveNum), et = 2, upn = True, scale = turtle.sf, name = 'plane' + str(turtle.curveNum))         
    turtle.curveNum += 1            #increment curve num        
    turtle.position = newPosition   #update position 


#LEAVES#
#------#

#draws leaves with curves along the last branch
def planLeaves( turtle, _leafNum, _leafWidth, _leafHeight, _leafType = 'standard'):    
    tpos1 = cmds.getAttr( 'curve' + str(turtle.curveNum - 1) + '.cv[0]')        #get coordinates of last coord of the previous curve
    tpos1 = tpos1[0]  #getattr will return a list. To get the coordinates of cv[1] only, store only the first element in tpos.
    tpos2 = cmds.getAttr( 'curve' + str(turtle.curveNum - 1) + '.cv[1]')
    tpos2 = tpos2[0]     
    for i in range(_leafNum):   
        x = random.uniform(tpos1[0], tpos2[0])            #choose a random x coordinate between the start and end of the branch
        y = random.uniform(tpos1[1], tpos2[1])
        z = random.uniform(tpos1[2], tpos2[2])    
        if _leafType == 'standard':
            #create a leaf with a curve
            cmds.curve(p=[(x,y,z),  (x+ _leafWidth/2.0, y + _leafHeight/2.0, z),  (x, y + _leafHeight, z),  ( x - (_leafWidth/2.0), y + _leafHeight/2.0, z), (x,y,z) ] , d = 3, name = 'lCurve' + str(turtle.curveNum - 1) + '_' + str(i) )           
        elif _leafType == 'oblong':
            #obovate leaf       
            cmds.curve(p=[ (x, y, z), (x - (_leafWidth/2.0), y, z),  (x + _leafWidth , y , z),  (x - (_leafWidth/2.0), y + _leafHeight, z), (x + _leafWidth, y + _leafHeight, z), (x , y, z) ] , d = 5, name = 'lCurve' + str(turtle.curveNum - 1) + '_' + str(i))    
        elif _leafType == 'sagitate':   
            #sagitate leaf
            cmds.curve(p=[(x, y, z), (x + _leafWidth/2.0, y - (_leafHeight/3.0), z), (x, y + _leafHeight, z),  (x - (_leafWidth/2.0) , y - (_leafHeight/3.0), z), (x,y, z) ] , d = 3, name = 'lCurve' + str(turtle.curveNum - 1) + '_' + str(i) ) 

#creates nurbs planes out of leaf curves & rotates leaves randomly
def makeLeaves( turtle, _leafNum ):
    tpos = cmds.getAttr( 'curve' + str(turtle.curveNum - 1) + '.cv[1]')
    tpos = tpos[0]  
    for i in range (_leafNum):
        leafName = 'leaf' + str(turtle.curveNum - 1) + '_' + str(i)
        cmds.planarSrf( 'lCurve' + str(turtle.curveNum - 1) + '_' + str(i), name = leafName , d=1, ch = False)     #create plane from curve
        #set pivot to ending point of leaf branch
        cmds.setAttr (leafName + '.scalePivot'  , tpos[0], tpos[1], tpos[2], type = 'double3' )
        cmds.setAttr (leafName + '.rotatePivot' , tpos[0], tpos[1], tpos[2], type = 'double3' )
        #place leaf
        cmds.rotate(0, 0, random.randint(-85, 85), leafName, os = True, r = True )  
        cmds.rotate(0, random.randint(-15, 15), 0, leafName, os = True, r = True ) 
        cmds.rotate(random.randint(-40, 40), 0, 0, leafName, os = True, r = True ) 



#CREATE STRING#
#--------------#
#F --> F[+F]F[-F]F
#ruleIn  --- initiator --- the thing which will be replaced 
#ruleOut  --- generator --- the thing it will be replaced WITH

def createString(_axiom, _lvl, _rule):
    temp = list(_axiom)                            # creates a list 'temp' with one element, 'axiom' 
    for i in range (_lvl):                         # for each level
        output = ''                               # reset output           
        for j in temp:                            # traverse 'temp'
            if j == _rule[0]:                      # if current element in temp matches the input of rule:
                output += _rule[1]                 # add rule output (F[+F]F[-F]F) to 'output'
            else:
                output += j                       # add current element in temp to 'output'           
        temp = output                             # set new value of temp after it has finished traversing for next level.          
    return output                                 # return string at the end


#SET COMMANDS TO EACH LETTER:
#-------------------------#
#http://algorithmicbotany.org/papers/abop/abop-ch1.pdf

#turtle -> name of turtle to use
#string -> string of instructions to interpret
#sfDecr -> amount side branches are scaled down
#aZ -> angle decrement/increment in Z axis

#F calls the forward() procedure  with arguments t0 and 1. This draws a curve from the values stored in t0.position to one unit along in the direction of t0.heading. The curve is then extruded along with nurbs or polygons depending on t0.fill.
#'+' and '-' rotate the vector describing the direction the turtle is facing (t0.heading) along the z axis. + rotates to the left, - to the right.
#'<' and '>' rotate t0.heading along the y-axis.
#'^' and '&' rotate t0.heading along the x-axis.
#'[' stores the position, heading, size and scale factor of t0 into 4 respective empty lists called 'positionStack', 'headingStack', 'sizeStack' and 'sfStack'.
#']' reads the last values stored in the 4 stack lists, deletes them and stores them into t0's position, heading, size and scale factor respectively.
#'L' calls the planLeaves() and makeLeaves() procedure with a list of values (leafInfo) passed into the interpretString() procedure.


def interpretString( turtle, string, leafInfo, _sfDecr = 0.005, _aZ=20, _aY=0, _aX=0, positionStack=[], headingStack=[], sizeStack =[], sfStack=[] ): 
    for i in range (len(string)):  
        if  string[i] == 'F' :
            forward( turtle, 5)  
            turtle.size =  turtle.size * turtle.sf #set topsize of last branch as  bottomsize of new branch   

        elif string[i] == 'L' :
            planLeaves(turtle, leafInfo[0], leafInfo[1], leafInfo[2], leafInfo[3] )
            makeLeaves(turtle, leafInfo[0])
            
        elif string[i] == '[' :
            positionStack.append(turtle.position)
            headingStack.append(turtle.heading) 
            sizeStack.append(turtle.size)
            sfStack.append(turtle.sf)  

        elif string[i] == ']':
            turtle.position = positionStack.pop(-1)
            turtle.heading = headingStack.pop(-1) 
            turtle.size = sizeStack.pop(-1)
            turtle.sf = sfStack.pop(-1)    

        elif string[i] == '-':        #turn right
            turtle.sf -= _sfDecr
            turnZ(turtle, -_aZ) 
                  
        elif string[i] == '+':        #turn left
            turtle.sf -= _sfDecr
            turnZ(turtle, _aZ)          
     
        elif string[i] == '|':       #turn around
            turnZ(turtle, 180)
       
        elif string[i] == '<':        #twist left
            turnY (turtle, -_aY) 
                   
        elif string[i] == '>':       #twist right
            turnY(turtle, _aY )  
       
        elif string[i] == '^':        #pitch up
            turnX (turtle, -_aX)    
       
        elif string[i] == '&':        #pitch down
            turnX (turtle, _aX)

           
#SHADERS#
#-------#
#create and assign a material to an object

def assignShaderColour( _objName, _shaderType = 'lambert', _colour = [ 0.5, 0.5, 0.5 ] ):  
    shadingGroup = cmds.sets( empty = True, renderable = True)    #creates empty set, stored in variable shadingGrop
    shaderName = cmds.shadingNode (_shaderType, asShader = True)                          #creates lambert shading node, stored in variable shader name
    cmds.setAttr( shaderName + '.color', _colour[0], _colour[1], _colour[2], type = 'double3' )    #changes shader node's color attribute
    cmds.surfaceShaderList( shaderName , add = shadingGroup)           #adds the shader node to the shadingGroup 
    cmds.sets( _objName , edit = True, forceElement = shadingGroup)     #adds object to shading group


