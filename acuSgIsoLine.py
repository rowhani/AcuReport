#===========================================================================
#
# Include files
#
#===========================================================================

import  types
import  numarray

import  acuQt

from    qt          import  QColor

from    acuSgActor  import  AcuSgActor
from    acuItemObj  import  AcuItemObj

#===========================================================================
#
# Errors
#
#===========================================================================

acuSgIsoLineError   = "ERROR from acuSgIsoLine module"

#===========================================================================
#
# "acuSgIsoLine": IsoLine actor
#
#===========================================================================
      
class AcuSgIsoLine:
    '''
	Class acuSgIsoLine creates objects of IsoLine actors
    '''

    def __init__( self, parent  ):
	'''
	    AcuSgIsoLine is used to create Iso-line actors.

	    Arguments:
	        parent  - parent object				
		
	'''
	
        self.parent         = parent
            
        self.sceneGraph     = parent.asg
        self.actList        = []

        self.disp           = "solid"
        self.clr            = QColor( 255, 0, 0 )
        self.trans          = True
        self.visibil        = True
        self.transVal       = 0.5
        self.lineWdth       = 0
        self.pntSize        = 2
        self.isoVecName     = None

        self.velDisplayed   = False

#---------------------------------------------------------------------------
# addIsoLnSet: Add an iso-line actor to the scene graph
#---------------------------------------------------------------------------

    def addIsoLnSet( self, isoLnObj, isoVec, isoVal, name  ):
        '''
	    Add an iso-line actor to the scene graph

	    Arguments:
	        isoLnObj    - acuisl object
		isoVec	    - iso-line vector
		isoVal	    - iso-line value
		name	    - an optional name for iso-line actor

	    Output:
	        actor       - iso-line actor
        '''

        self.isoLnObj   = isoLnObj
	self.isoVal     = isoVal
	self.name       = name

	if type( isoVec ) == types.StringType and \
           isoVec in self.parent.sclrVarNames:
            self.isoVecName = isoVec
            isoVec          = self.parent.varValues[    isoVec          ]

        if type( isoVec ) != numarray.numarraycore.NumArray or \
           isoVec.shape[0] != self.parent.crd.shape[0]:
            raise acuSgIsoLineError, "Invalid type or name for isoVec."        
    
	self.isoVec     = isoVec
        (isoCrd,isoLine,isoPrj) = \
                                isoLnObj.getIsoLines( isoVec, isoVal    )
        
        item        = AcuItemObj(           name,           self.disp,
                                            self.visibil ,  self.trans,
                                            self.transVal,  self.clr    )
        if len(isoLine) != 0:
            actor       = self.sceneGraph.addLinSet(    isoCrd,
                                                        isoLine,
                                                        'line',
                                                        item            )

            actor.isoPrj = isoPrj

            self.actList.append(                        actor           )

        else:
            raise acuSgIsoLineError, "Invalid isoVec or isoVal."
        
#---------------------------------------------------------------------------
# removeIsoLnSet: Remove an iso-line actor from the scene graph
#---------------------------------------------------------------------------

    def removeIsoLnSet( self  ):
        '''
        Remove an iso-line actors from the scene graph
	    
	    Arguments:
	        None

	    Output:
	        None
        '''

        for remActor in self.actList:
            self.sceneGraph.remIsoLnActor(          remActor           )
        self.actList    = [] 

#---------------------------------------------------------------------------
# setIsoVal: Change\Set the value of the iso-line
#---------------------------------------------------------------------------

    def setIsoVal( self, newVal  ):
        '''
	    Change\Set the value of the iso-line
	    
	    Arguments:
	        newVal  - The new value that the iso-line is set to

	    Output:
	        None
        '''

        self.removeIsoLnSet(                                            )
        self.addIsoLnSet(           self.isoLnObj,  self.isoVec,
                                    newVal,         self.name           )

#---------------------------------------------------------------------------
# display: Get\Set the display type of the iso-line actor
#---------------------------------------------------------------------------

    def display( self, style = None ):
        '''
	    Get\Set the display type of the iso-line actor
	    
	    Arguments:
	        style   - The desired display type of the iso-line actor

	    Output:
	        ( only if style input is equal to None )
	        style	- current style ("outline", "solid", "wireframe" ...)
        '''

        if style:
            self.disp   = style

            for actor in self.actList:
                actor.display(                  style                   )

        return self.disp

#---------------------------------------------------------------------------
# transparencyVal: Get\Set the transparency value of the iso-line actor
#---------------------------------------------------------------------------

    def transparencyVal( self, value = None ):
        '''
	    Get\Set the transparency value of the iso-line actor
	    
	    Arguments:
	        value   - The desired transparency value of the iso-line actor

	    Output:
	        ( only if value input is equal to None )
	        value	- current transparency value (0-1)
        '''

        if value != None:
            self.transVal  = value

            for actor in self.actList:
                actor.transparencyVal(          value                   )

        return self.transVal

#---------------------------------------------------------------------------
# transparency: Get\Set the transparency of the iso-line actor
#---------------------------------------------------------------------------

    def transparency( self, trans = None ):
        '''
	    Get\Set the transparency of the iso-line actor
	    
	    Arguments:
	        trans	- True / False

	    Output:
	        ( only if trans input is equal to None )
	        trans	- current transparency flag
        '''

        if trans != None:
            self.trans  = trans

            for actor in self.actList:
                actor.transparency(             trans                   )

        return self.trans

#---------------------------------------------------------------------------
# color: Get\Set the color of the iso-line actor
#---------------------------------------------------------------------------

    def color( self, r = None, g = None, b = None ):
        '''
	    Get\Set the color of the iso-line actor
	    
	    Arguments:
	        r,g,b	- red, blue, green values

	    Output:
	        ( only if r,g,b input is equal to None )
	        [ r, g, b ] - red, blue, green values
        '''

        if r != None and g != None and b != None:
            self.clr    = [ r, g, b ]

            for actor in self.actList:
                actor.color(                    r, g, b                 )

        return self.clr

#---------------------------------------------------------------------------
# visibility: Get\Set the visibility of the iso-line actor
#---------------------------------------------------------------------------

    def visibility( self, vis = None ):
        '''
	    Get\Set the visibility of the iso-line actor
	    
	    Arguments:
	        vis	- True / False

	    Output:
	        ( only if vis input is equal to None )
	        vis	- current visibility flag
        '''

        if vis != None:
            self.visibil    = vis

            for actor in self.actList:
                actor.visibility(               vis                     )

        return self.visibil
        
#---------------------------------------------------------------------------
# setVisibility: Set the visibility of the iso-line actor
#---------------------------------------------------------------------------

    def setVisibility( self, vis = None ):
        '''
	    Get\Set the visibility of the iso-line actor
	    
	    Arguments:
	        vis	- 'On' or 'Off'

	    Output:
	        vis     - Current visibility
	        ( only if vis input is equal to None )
        '''

        if vis != None:
            if vis == 'on':
                self.visibil    = True
            elif vis == 'off':
                self.visibil    = False

        for actor in self.actList:
            actor.setVisibility(                            vis         )

#---------------------------------------------------------------------------
# lineWidth: Get\Set the line width of the iso-line actor
#---------------------------------------------------------------------------

    def lineWidth( self, width = None ):
        '''
	    Get\Set the line width of the iso-line actor
	    
	    Arguments:
	        width	- line width value

	    Output:
	        ( Only if width equal to None )
	        width	- line width value
        '''

        if width != None:
            self.lineWdth  = width
            
            for actor in self.actList:
                actor.lineWidth(                            width       )

        return self.lineWdth

#---------------------------------------------------------------------------
# pointSize: Get\Set the point size of the iso-line actor
#---------------------------------------------------------------------------

    def pointSize( self, size = None ):
        '''
	    Get\Set the point size of the iso-line actor
	    
	    Arguments:
	        size	- point size value

	    Output:
	        ( Only if size equal to None )
	        size	- point size
        '''

        if size != None:
            self.pntSize    = size

            for actor in self.actList:
                actor.pointSize(                            size        )

        return self.pntSize

#---------------------------------------------------------------------------
# setScalar: set the scalar vector
#---------------------------------------------------------------------------

    def setScalar( self,    scalar      = None,  name       = "",
                            sclrMinVal  = None,  sclrMaxVal = None ):
                   
        """
            Function to store a scalar vector in the scene graph.

	    Arguments:
                scalar      - Scaler vector value
                name        - Scaler name
                sclrMinVal  - Set scaler vector minimum value
                sclrMaxVal  - Set scaler vector maximum value                
                
	    Output: 
	        None
	"""        
        
        for actor in self.actList:
            prjScalar  = actor.isoPrj.project( scalar                   )
	    actor.setScalar( prjScalar, name, sclrMinVal, sclrMaxVal    )

#---------------------------------------------------------------------------
# setSclrLimits: get/set the scalar Min/Max value
#---------------------------------------------------------------------------

    def setSclrLimits( self, sclrMinVal = None, sclrMaxVal = None ):

        """
            Function to get/set the scalar min/max value.

	    Arguments:
	        sclrMinVal  - The minimum value of the scalar
	        sclrMaxVal  - The maximum value of the scalar

	    Output:
                The current scaler min/max value
	"""

        minVal =  1e308
        maxVal = -1e308

        for actor in self.actList:           
	    val1, val2 = actor.setSclrLimits( sclrMinVal, sclrMaxVal    )

	    if val1 < minVal:
                minVal = val1
            if val2 > maxVal:
                maxVal = val2

        return ( minVal, maxVal )

#---------------------------------------------------------------------------
# setSclrMinVal: get/set the scalar Min value
#---------------------------------------------------------------------------

    def setSclrMinVal( self, sclrMinVal = None ):
        
        """
            Function to get/set the scalar minimum value.

	    Arguments:
	        sclrMinVal  - The minimum value of the scalar

	    Output:
                The current scaler minimum value
	"""

        minVal = 1e308

        for actor in self.actList:           
	    val = actor.setSclrMinVal( sclrMinVal                       )
	    if val < minVal:
                minVal = val

        return minVal

#---------------------------------------------------------------------------
# setSclrMaxVal: get/set the scalar Max value
#---------------------------------------------------------------------------

    def setSclrMaxVal( self, sclrMaxVal = None ):

        """
            Function to get/set the scalar maximum value.

	    Arguments:
	        sclrMaxVal  - The maximum value of the scalar

	    Output:
                The current scaler maximum value
	"""

        maxVal = -1e308

        for actor in self.actList:           
	    val = actor.setSclrMaxVal( sclrMaxVal                       )
	    if val > maxVal:
                maxVal = val

        return maxVal

#---------------------------------------------------------------------------
# setCmap: set the colormap 
#---------------------------------------------------------------------------

    def setCmap( self, cmap = "default" ):
        
        """
            Function to set the color map.

	    Arguments:
	        cmap    - The cmap value
	        
	    Output: 
	        None 
	"""

        for actor in self.actList:           
	    actor.setCmap( cmap                                         )
	    
#---------------------------------------------------------------------------
# setVel: set the velocity vectors 
#---------------------------------------------------------------------------

    def setVel( self,   vel         = None, name = "",
                        velScale    = None              ):

        """
	    Function to set the velocity vectors 

	    Arguments:
                vel	    - Velocity vectors 
                name        - Velocity vectors name
                velScale    - Velocity vectors Scale               
                
	    Output: 
	        None
	"""        

        for actor in self.actList:
            prjVel  = actor.isoPrj.project( vel                         )
	    actor.setVel( prjVel, name, velScale                        )

#---------------------------------------------------------------------------
# setVelScale: get/set the velocity vectors scale 
#---------------------------------------------------------------------------

    def setVelScale( self, velScale = None ):

        """
	    Function to get/set the velocity vectors scale

	    Arguments:
                velScale    - Velocity vectors scale            
                
	    Output: 
	        The current velScale value
	"""

        for actor in self.actList:
            actor.setVelScale( velScale                                 )

#---------------------------------------------------------------------------
# setVelScalar: set the velocity vector color scalar 
#---------------------------------------------------------------------------

    def setVelScalar( self, velScalar       = None,
                            velScalarType   = "magnitude",
                            velSclrMinVal   = None,
                            velSclrMaxVal   = None          ):

        """
	    Function to set the velocity vector color scalar

	    Arguments:
	        velScalar       - Velocity color scalar value
	        velScalarType   - Velocity color scalar type
		velSclrMinVal   - Set velocity color scalar minimum value
		maxVal          - Set velocity color scalar maximum value
		
	    Output: 
	        None
	"""

        if velScalar != None:
            for actor in self.actList:
                prjVelScalar  = actor.isoPrj.project( velScalar         )
                actor.setVelScalar( prjVelScalar,   velScalarType,
                                    velSclrMinVal,  velSclrMaxVal       )

#---------------------------------------------------------------------------
# setVelSclrLimits: set the velScalar Min/Max value
#---------------------------------------------------------------------------

    def setVelSclrLimits( self, velSclrMinVal = None, velSclrMaxVal = None ):

        """
            Function to set/get the velScalar min/max value.

	    Arguments:
	        velSclrMinVal  - The minimum value of the velScalar
	        velSclrMaxVal  - The maximum value of the velScalar

	    Output:
                The current velScalar min/max value
	"""

        minVal =  1e308
        maxVal = -1e308

        for actor in self.actList:
            val1, val2 = actor.setVelSclrLimits( velSclrMinVal, velSclrMaxVal )

            if val1 < minVal:
                minVal = val1
            if val2 > maxVal:
                maxVal = val2

        return ( minVal, maxVal )

#---------------------------------------------------------------------------
# setVelSclrMinVal: set the velScalar Min value
#---------------------------------------------------------------------------

    def setVelSclrMinVal( self, velSclrMinVal = None ):
        
        """
            Function to set/get the velScalar minimum value.

	    Arguments:
	        velSclrMinVal  - The minimum value of the velScalar

	    Output:
                The current velScalar minimum value
	"""

        minVal = 1e308

        for actor in self.actList:
            val = actor.setVelSclrMinVal( velSclrMinVal                 )
            if val < minVal:
                minVal = val

        return minVal

#---------------------------------------------------------------------------
# setVelSclrMaxVal: set the velScalar Max value
#---------------------------------------------------------------------------

    def setVelSclrMaxVal( self, velSclrMaxVal = None ):
        
        """
            Function to set/get the velScalar maximum value.

	    Arguments:
	        velSclrMaxVal  - The maximum value of the velScalar

	    Output:
                The current velScalar maximum value
	"""

        maxVal = -1e308

        for actor in self.actList:
            val = actor.setVelSclrMaxVal( velSclrMaxVal                 )

            if val > maxVal:
                maxVal = val

        return maxVal

#---------------------------------------------------------------------------
# setVelWidth: get/set the velocity vectors width 
#---------------------------------------------------------------------------

    def setVelWidth( self, velWidth = 1.0 ):

        """
	    Function to get/set the velocity vectors width

	    Arguments:
                velWidth    - Velocity vectors width            
                
	    Output: 
	        The current velWidth value
	"""

        for actor in self.actList:
            actor.setVelWidth( velWidth                                 )

#---------------------------------------------------------------------------
# setVelArrowType: get/set the velocity vector arrow type
#---------------------------------------------------------------------------

    def setVelArrowType( self, velArrowType = "none" ):

        """
	    Function to get/set the velocity vector arrow type

	    Arguments:
                velArrowType    - Velocity vectors arrow type            
                
	    Output: 
	        The current velArrowType value
	"""

        for actor in self.actList:
            actor.setVelArrowType( velArrowType                         )

#---------------------------------------------------------------------------
# setVelColorType: get/set the velocity vector color type
#---------------------------------------------------------------------------

    def setVelColorType( self, velColorType = "constant" ):

        """
	    Function to get/set the velocity vector color type

	    Arguments:
                velColorType    - Velocity vectors color type            
                
	    Output: 
	        The current velColorType value
	"""

        for actor in self.actList:
            actor.setVelColorType( velColorType                         )
            
#---------------------------------------------------------------------------
# setVelColor: get/set the velocity vector constant color
#---------------------------------------------------------------------------

    def setVelColor( self, velColor = (1, 1, 1) ):

        """
	    Function to get/set the velocity vector constant color

	    Arguments:
                velColor    - Velocity vector constant color            
                
	    Output: 
	        The current velColor value
	"""

        for actor in self.actList:
            actor.setVelColor( velColor                                 )

#---------------------------------------------------------------------------
# setVelCmap: get/set the velocity vector per_node colormap 
#---------------------------------------------------------------------------

    def setVelCmap( self, velCmap = "default" ):
        
        """
	    Function to get/set the velocity vector per_node colormap

	    Arguments:
                velCmap - The velocity vector per_node colormap
                
	    Output: 
	        The current velCmap
	"""

        for actor in self.actList:
            actor.setVelCmap( velCmap                                   )
            
#---------------------------------------------------------------------------
# velDisplay: set the velocity vector 
#---------------------------------------------------------------------------

    def velDisplay( self, display = True ):

        self.velDisplayed = display
        
        for actor in self.actList:
            actor.velDisplay( display                                   )            
