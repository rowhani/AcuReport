#===========================================================================
#
# Include files
#
#===========================================================================

from    iv          import *

import  types
import  sys
import  math
import  acuQt
import	qt
import  os

TRUE	= 1
True	= 1
FALSE	= 0
False	= 0

MODE_VIEWING			= 0
MODE_PICKING			= 1


#===========================================================================
#
# Transparency types map
#
#===========================================================================

_transType                              = {}
_transType["SCREEN_DOOR"]               = SoGLRenderAction.SCREEN_DOOR
_transType["ADD"]                       = SoGLRenderAction.ADD
_transType["DELAYED_ADD"]               = SoGLRenderAction.DELAYED_ADD
_transType["SORTED_OBJECT_ADD"]         = SoGLRenderAction.SORTED_OBJECT_ADD
_transType["BLEND"]                     = SoGLRenderAction.BLEND
_transType["DELAYED_BLEND"]             = SoGLRenderAction.DELAYED_BLEND
_transType["SORTED_OBJECT_BLEND"]       = SoGLRenderAction.SORTED_OBJECT_BLEND


#===========================================================================
#
# Useful mouseAction mapping
#
#===========================================================================

B1DOWN		= 1
B2DOWN		= 2
B3DOWN		= 4
SHIFTDOWN	= 8
CTRLDOWN	= 16

_mouseActionMap	= {}
_mouseActionMap[0]			= "NONE"		# 0
_mouseActionMap[B1DOWN]			= "SPIN"		# 1
_mouseActionMap[B2DOWN]			= "ZOOM"		# 2
_mouseActionMap[B3DOWN]			= "PAN"			# 4

_mouseActionMap[B1DOWN+B2DOWN]		= "NONE"		# 3
_mouseActionMap[B1DOWN+B3DOWN]		= "NONE"		# 5
_mouseActionMap[B2DOWN+B3DOWN]		= "NONE"		# 6
_mouseActionMap[B1DOWN+B2DOWN+B3DOWN]	= "NONE" 		# 7

_mouseActionMap[SHIFTDOWN]		= "NONE"		# 8
_mouseActionMap[SHIFTDOWN+B1DOWN]	= "SPIN"		# 9
_mouseActionMap[SHIFTDOWN+B2DOWN]	= "ZOOM"		# 10
_mouseActionMap[SHIFTDOWN+B3DOWN]	= "PAN"			# 12
_mouseActionMap[SHIFTDOWN+B1DOWN+B2DOWN] = "NONE" 		# 11
_mouseActionMap[SHIFTDOWN+B1DOWN+B3DOWN] = "NONE" 		# 13
_mouseActionMap[SHIFTDOWN+B2DOWN+B3DOWN] = "NONE" 		# 14
_mouseActionMap[SHIFTDOWN+B1DOWN+B2DOWN+B3DOWN] = "NONE" 	# 15

_mouseActionMap[CTRLDOWN]		= "NONE"		# 16
_mouseActionMap[CTRLDOWN+B1DOWN]		= "SPIN"		# 17
_mouseActionMap[CTRLDOWN+B2DOWN]		= "ZOOM"		# 18
_mouseActionMap[CTRLDOWN+B3DOWN]		= "PAN"			# 20
_mouseActionMap[CTRLDOWN+B1DOWN+B2DOWN] 	= "NONE" 		# 19
_mouseActionMap[CTRLDOWN+B2DOWN+B3DOWN] 	= "NONE" 		# 22
_mouseActionMap[CTRLDOWN+B1DOWN+B2DOWN+B3DOWN] = "NONE" 		# 23

_mouseActionMap[CTRLDOWN+SHIFTDOWN] 	= "NONE" 		# 24

#---- Create a map for BUTTON names to their location in the action map

_mouseButtonString	= {}
_mouseButtonString["BUTTON1"]				= 1
_mouseButtonString["BUTTON2"]				= 2
_mouseButtonString["BUTTON1_BUTTON2"]			= 3
_mouseButtonString["BUTTON3"]				= 4
_mouseButtonString["BUTTON1_BUTTON3"]			= 5
_mouseButtonString["BUTTON2_BUTTON3"]			= 6
_mouseButtonString["BUTTON1_BUTTON2_BUTTON3"]		= 7
_mouseButtonString["SHIFT"]				= 8
_mouseButtonString["SHIFT_BUTTON1"]			= 9
_mouseButtonString["SHIFT_BUTTON2"]			= 10
_mouseButtonString["SHIFT_BUTTON1_BUTTON2"]		= 11
_mouseButtonString["SHIFT_BUTTON3"]			= 12
_mouseButtonString["SHIFT_BUTTON1_BUTTON3"]		= 13
_mouseButtonString["SHIFT_BUTTON2_BUTTON3"]		= 14
_mouseButtonString["SHIFT_BUTTON1_BUTTON2_BUTTON3"]	= 15
_mouseButtonString["CTRL"]				= 16
_mouseButtonString["CTRL_BUTTON1"]			= 17
_mouseButtonString["CTRL_BUTTON2"]			= 18
_mouseButtonString["CTRL_BUTTON1_BUTTON2"]		= 19
_mouseButtonString["CTRL_BUTTON3"]			= 20
_mouseButtonString["CTRL_BUTTON1_BUTTON3"]		= 21
_mouseButtonString["CTRL_BUTTON2_BUTTON3"]		= 22
_mouseButtonString["CTRL_BUTTON1_BUTTON2_BUTTON3"]	= 23
_mouseButtonString["SHIFT_CTRL"]			= 24

_mouseActionString	= {}
_mouseActionString[0]	= "SPIN"
_mouseActionString[1]	= "PAN"
_mouseActionString[2]	= "ZOOM"
_mouseActionString[3]	= "NONE"



#----- Mouse Wheel Motion, BUTTON4 Towards user, 5..Away
#mouseActionMap['BUTTON4']	= "ZOOM_UP"
#mouseActionMap['BUTTON5']	= "ZOOM_DOWN"



#===========================================================================
#
# Useful keyAction mapping
#    * Primarily to Overwrite some of the default actions.
#    * For Example, we don't want q to quit and ESC to change the modes
#
#===========================================================================

keyActionMap	= {}
keyActionMap['ESCAPE']	= "NONE"  # default is to switch modes
keyActionMap['Q']	= "NONE"  # default is to quit
keyActionMap['S']	= "NONE"  # default is to seek

#===========================================================================
#
# Errors
#
#===========================================================================

acuSgViewerError	= "ERROR in AcuSgViewer Module "

#===========================================================================
#
# AcuSgViewer
#
#===========================================================================

class AcuSgViewer( SoQtExaminerViewer ):
    '''
	It is derived from  one of the  viewer classes  and overwrites
	the mouse and keyboard events. The mouse bindings are dynamic
	as the user can specify the appropriate behavior through API
	calls
    '''

    def __init__( self, parent, settingObj = None):
        '''
	    Constructor

	    Arguments:
	        parent		- parent object
	        settingObj	- settings object containing user settings
	    Output:
	        None
        '''

	self.sizeChangedCb	= None


	SoQtExaminerViewer.__init__( 	self,	parent 			)
	self.setDecoration(			FALSE			)
	self.setFullScreen(			FALSE			)
	self.setAnimationEnabled(		FALSE			)
	self.setPopupMenuEnabled(		FALSE			)

	self.setCameraType(	SoOrthographicCamera.getClassTypeId()	)
	self.setFeedbackVisibility(		TRUE			)
	self.setFeedbackSize(			15			)

	#self.setAutoClippingStrategy( SoQtViewer.CONSTANT_NEAR_PLANE,1.0 )

	self.axisFlag		= TRUE
	self.modeFlag		= MODE_VIEWING

	self.noneCursor         = SoQtCursor( SoQtCursor.DEFAULT        )
        self.rotateCursor       = SoQtCursor(
                                            SoQtCursor.getRotateCursor())
        self.zoomCursor         = SoQtCursor( SoQtCursor.getZoomCursor())
        self.panCursor          = SoQtCursor( SoQtCursor.getPanCursor() )

	self.ctrldown		= FALSE
	self.shiftdown		= FALSE
	self.button1down	= FALSE
	self.button2down	= FALSE
	self.button3down	= FALSE
	self.button4down	= FALSE
	self.button5down	= FALSE
	self.eventMode		= "NONE"

	self.lastMousePos	= SbVec2f(				)
	self.spinProj		= \
		SbSphereSheetProjector( SbSphere(SbVec3f(0,0,0), 0.8)	)
	volume			= SbViewVolume(				)
	volume.ortho(		-1,1,-1,1,-1,1				)
	self.spinProj.setViewVolume(		volume			)
	self.nPtsStored 	= 0
	self.pt0		= SbVec2s(				)
	self.pt1		= SbVec2s(				)
	self.setComponentCursor(  		self.noneCursor		)
	self.r		= 1.0
	self.g		= 1.0
	self.b		= 1.0

        #----- Misc 4/08 : E9
        self.win        = settingObj
        self.lstVal     = None

        #----- Background
        
        self.renderBG = self.getGLRenderAction(                         )        
        self.setClearBeforeRender(          False, True                 )
        
	self.backgroundSep = SoSeparator(                               )
	self.backgroundSep.addChild(        SoDirectionalLight()        )

        self.gradientBgSep  = SoSeparator(                              )
	self.backgroundSep.addChild(        self.gradientBgSep          )
	
	self.imageBgSep     = SoSeparator(                              )
        self.backgroundSep.addChild(        self.imageBgSep             )

        self.bgType = None
        
#---------------------------------------------------------------------------
# actualRedraw
#---------------------------------------------------------------------------

    def actualRedraw( self ):
        
	#OpenGL.GL.glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT   )

        self.getSceneManager().render(          True, True              )
        
	self.renderBG.apply(                    self.backgroundSep      )
	
	SoQtExaminerViewer.actualRedraw(        self                    )

#---------------------------------------------------------------------------
# bgColor: function to set/get background of the window
#---------------------------------------------------------------------------

    def bgColor( self,  type        = "solid",
                        red         = 1.,
                        green       = 1.,
                        blue        = 1.,
                        red_bot     = 0.,
                        green_bot   = 0.,
                        blue_bot    = 0.,
                        fileName    = None,
                        image       = None      ):

        self.bgType = type

        retVal  = self.getBackgroundColor().getValue(                   )

        self.gradientBgSep.removeAllChildren(                           )
        self.imageBgSep.removeAllChildren(                              )
                
        if type == "solid":                             
            self.setBackgroundColor( SbColor( red, green, blue)         )
            
        else:

            r   = acuQt.getSettingReal(   "colorRed",   1               )
            g   = acuQt.getSettingReal(   "colorGreen", 1               )
            b   = acuQt.getSettingReal(   "colorBlue",  1               )
            self.setBackgroundColor( SbColor( r, g, b )                 )

            xL  = -1
            xR  =  1
            yL  = -1
            yR  =  1            
            z   =  -0.999999
            
            crd = ( (xL, yL, z) , (xR, yL, z), (xR, yR, z), (xL, yR, z) )
                
            vertProp = SoVertexProperty(                                )
            vertProp.vertex.setValues(          0, crd                  )
            
            bgRect = SoIndexedFaceSet(                                  )
            bgRect.coordIndex.setValues(    0, ( 0, 1, 2, 3 )           )
            bgRect.vertexProperty.setValue(     vertProp                )

            if type == "two-tone":
                
                c1 = SbColor(           red, green, blue                )
                c1 = c1.getPackedValue(                                 )
                c2 = SbColor(           red_bot, green_bot, blue_bot    )
                c2 = c2.getPackedValue(                                 )

                vertProp.orderedRGBA.setValues(  0, ( c2, c2, c1, c1 )  )
                vertProp.materialBinding.setValue(
                                   SoMaterialBinding.PER_VERTEX_INDEXED )

                self.gradientBgSep.addChild(        bgRect              )

            elif type == "filename" or type == "image":        

                bgImage = SoTexture2(                                   )
                
                if fileName != None:
                    bgImage.filename.setValue(      fileName            )                    
                elif image != None:
                    bgImage.image.setValue(      image                  )                    
                else:
                    raise acuSgViewerError, "Invalid background"

                trans = SoTransform(                                    )
                trans.rotation.setValue( SbVec3f(0, 0, 1), math.pi / 2  )
                trans.scaleFactor.setValue(     1, -1, 1                )                                        

                self.imageBgSep.addChild(       bgImage                 )
                self.imageBgSep.addChild(       trans                   )
                self.imageBgSep.addChild(       bgRect                  )            
                   
        self.actualRedraw(                                              )
        self.redraw(													)
        
        return retVal   
              	 
#---------------------------------------------------------------------------
# setFocalPoint:
#---------------------------------------------------------------------------

    def setFocalPoint( self, fP ):
        ''' set the focal point or the center of rotation '''

	camera	= self.getCamera(					)
	px,py,pz= camera.position.getValue(				)
	dir	= SbVec3f(						)
	camera.orientation.getValue().multVec(	SbVec3f(0,0,-1), dir	)

	dx,dy,dz	= dir.getValue(					)

	try:
	    fx, fy, fz	= fP[0], fP[1], fP[2]
	except:
	    print "focal point values is not a list of 3 values"
	    return

	if dx != 0:
	    fD	= ( fx - px ) / dx
	elif dy != 0:
	    fD	= ( fy - py ) / dy
	elif dz != 0:
	    fD	= ( fz - pz ) / dz
	else:
	    print "camera orientation is [0,0,0] "
	    return

	camera.focalDistance.setValue(			fD		)
  

#---------------------------------------------------------------------------
# setSizeChangedCb:
#---------------------------------------------------------------------------

    def setSizeChangedCb( self,  sizeChangedCb ):
        self.sizeChangedCb	= sizeChangedCb

#---------------------------------------------------------------------------
# setSizeChanged:
#---------------------------------------------------------------------------

    def sizeChanged( self,  size ):

        SoQtExaminerViewer.sizeChanged(		self, size		)
	if self.sizeChangedCb:
	    self.sizeChangedCb(			size			)

#---------------------------------------------------------------------------
# mode: sets the event mode of the graphical window ( VIEWING/PICKING )
#---------------------------------------------------------------------------

    def mode( self, mode = None ):
        '''
	    sets the mode to either viewing/selection. If mode == None,
	    the current mode is returned.

	    Arguments:
	        mode		- "PICKING","VIEWING"

	    Output: ( only if input mode == None )
	        mode		- "PICKING","VIEWING"
        '''

	retVal	= self.modeFlag

	if mode != None:
	    if mode != MODE_VIEWING and mode != MODE_PICKING:
		raise acuSgViewerError,"MODE_VIEWING(0), MODE_PICKING(1)"
	    else:
		self.modeFlag	= mode
		if mode == MODE_VIEWING:
		    if not self.isViewing():
		        self.setViewing(		TRUE		)

		if mode == MODE_PICKING:
		    if self.isViewing():
		        self.setViewing(		FALSE		)
	return retVal

#---------------------------------------------------------------------------
# zoom: sets the height of orthographic camera by amplification value
#       [ Implemented only for an orthographic camera  ]
#---------------------------------------------------------------------------

    def zoom( self, amplification ):
        '''
	    sets the orthographic camera's height value to the amplification
	    factor times the current value of the height,

	    Arguments:
	        amplification	- float value for amplifying camera height

	    Output:
	        None
        '''

	camera	= self.getCamera(					)
	camType	= camera.getTypeId(					)

	if camType.isDerivedFrom( SoOrthographicCamera.getClassTypeId()	):
	    multiFactor	= float( 	math.exp( amplification )	)
	    height	= camera.height.getValue() * multiFactor
	    camera.height.setValue(		height			)

	elif camType.isDerivedFrom( SoPerspectiveCamera.getClassTypeId() ):
	    oldFd	= camera.focalDistance.getValue(		)
	    newFd	= oldFd * multiFactor
	    dir	= SbVec3f(						)
	    camera.orientation.getValue().multVec( SbVec3f(0,0,-1),dir	)

	    oldPos	= SbVec3f(					)
	    newPos	= SbVec3f(					)
	    oldPos	= camera.position.getValue(			)
	    px,py,pz	= oldPos.getValue(				)
	    dx,dy,dz	= dir.getValue(					)

	    pnx	= px + ( newFd - oldFd ) * -dx
	    pny	= py + ( newFd - oldFd ) * -dy
	    pnz	= pz + ( newFd - oldFd ) * -dz

	    camera.position.setValue(	SbVec3f(pnx,pny,pnz)		)
	    camera.focalDistance.setValue(		newFd		)
	else:
	    return

#---------------------------------------------------------------------------
# zoomByCursor: calls zoom by computing amplification value from cursor
#                positions ( previous and current ).
#       [ Implemented only for an orthographic camera  ]
#---------------------------------------------------------------------------

    def zoomByCursor( self, currPos, prevPos ):
        '''
	    sets the orthographic camera's height value to the amplification
	    factor times the current value of the height,
	    amplification factor = ( currPos[1] - prevPos[1] ) * 20
	    currPos[1]  = y value of the current position
	    prevPos[1]  = y value of the previous position

	    Arguments:
	        currPos		- SbVec2f() or y location as float
	        prevPos		- SbVec2f() or y location as float

	    Output:
	        None
        '''
	#---- Need to check for currPos type and prevPos type
	# isinstance( SbVec2f() ) should also support two y float values

	cx,cy	= currPos.getValue(					)
	px,py	= prevPos.getValue(					)
	amp	= ( cy - py ) * 2.0
	self.zoom(			amp				)


#---------------------------------------------------------------------------
# pan: pans the camera based on previous and current mouse positions.
#---------------------------------------------------------------------------

    def pan( self, currPos, prevPos ):
        '''
	    translates the camera from previous cursor location to the
	    current location.

	    Arguments:
	        currPos		- SbVec2f()
	        prevPos		- SbVec2f()

	    Output:
	        None
        '''

	camera	= self.getCamera(					)
	vv	= camera.getViewVolume( self.getGLAspectRatio()		)
	line	= SbLine(						)
	fD	= camera.focalDistance.getValue(			)
	panPln	= vv.getPlane(			fD			)

	vv.projectPointToLine(		currPos,	line		)
	curPt	= SbVec3f(						)
	panPln.intersect(		line, curPt			)

	vv.projectPointToLine(		prevPos,	line		)
	oldPt	= SbVec3f(						)
	panPln.intersect(		line,	oldPt			)

	px,py,pz	= camera.position.getValue(			)
	cx,cy,cz	= curPt.getValue(				)
	ox,oy,oz	= oldPt.getValue(				)
	px,py,pz	= px + ( ox-cx ), py + ( oy-cy ), pz + ( oz-cz )
	camera.position.setValue(	SbVec3f(px,py,pz)		)

#---------------------------------------------------------------------------
# RollZ: NOT IMPLEMENTED YET...THIS IS A PLACE HOLDER FOR FUTURE
#---------------------------------------------------------------------------

    def RollZ( self, pos, prev ):
        '''
	   NOT IMPLEMENTED YET....
	   Testing RollZ functionality
        '''
        camera	= self.getCamera()
	q0,q1,q2,q3	= camera.orientation.getValue().getValue()
	radians	= float( math.acos(q3)) * 2.0
	scale	= float( math.sin( radians / 2.0 ) )
	if scale != 0.0:
	    ax	= q0 / scale
	    ay	= q1 / scale
	    az	= q2 / scale
	    nA	= radians + 0.01
	    scale	= float( math.sin( nA/2.0 ))
	    if scale != 0.0:
	        q0	= ax * scale
	        q1	= ay * scale
	        q2	= az * scale
		q3	= math.cos( 2.0 * nA )
		camera.orientation.setValue( q0, q1, q2, q3 )

#---------------------------------------------------------------------------
# spin: spins the camera based on the current and previous positions
#       The previous position is used in the projector and is not
#       required by this function.
#---------------------------------------------------------------------------

    def spin( self, pos ):
        '''
	    Uses the sphere sheet projector to map the mouse position unto
	    a 3D point and find a rotation from this and the last
	    calculated point.

	    Arguments:
	        position	- SbVec2f()

	    Output:
	        None
        '''

	if self.nPtsStored < 2:
	    return

	px,py	= pos.getValue(						)
	lx,ly	= self.pt1.getValue(				)

	sx,sy	= self.getGLSize().getValue(				)
	lx	= float( lx ) / float( 	max( 	int(sx-1),1 	)	)
	ly	= float( ly ) / float( 	max( 	int(sy-1),1 	)	)

	self.spinProj.project(		SbVec2f(lx,ly)			)
	rot	= SbRotation(						)
	self.spinProj.projectAndGetRotation(	pos, rot		)
	rot.invert(							)
	self._reorientCamera(			rot			)

#---------------------------------------------------------------------------
# _reorientCamera: reorients the camera based on SbRotation() object
#---------------------------------------------------------------------------

    def _reorientCamera( self, rot ):
        camera	= self.getCamera(					)
	dir	= SbVec3f(						)
	camera.orientation.getValue().multVec(	SbVec3f(0,0,-1),dir	)

	px,py,pz	= camera.position.getValue(			)
	fD		= camera.focalDistance.getValue(		)
	dx,dy,dz	= dir.getValue(					)
	fx,fy,fz	= px + fD * dx, py + fD * dy, pz + fD * dz

	oldOrient	= camera.orientation.getValue()
	(ox,oy,oz,ow)	= ( rot * oldOrient ).getValue(			)
	camera.orientation.setValue( 		ox,oy,oz,ow		)
	camera.orientation.getValue().multVec(	SbVec3f(0,0,-1),dir	)
	fD		= camera.focalDistance.getValue(		)
	dx,dy,dz	= dir.getValue(					)
	px,py,pz	= fx - fD*dx , fy - fD*dy, fz - fD*dz
	camera.position.setValue(	SbVec3f( px,py,pz)		)
	

#---------------------------------------------------------------------------
# getMouseBinding: returns the action on the button provided
#---------------------------------------------------------------------------

    def getMouseBinding( self, whichButton ):
        '''
	    Arguments:
	        whichButton	- "BUTTON1", BUTTON2...BUTTON3,
		                  BUTTON1_CTRL,...,BUTTON1_SHIFT,
				  BUTTON1_ALT....
	    Output:
	        whatAction	- SPIN, ZOOM, PAN,NONE
        '''

	if whichButton == None:
	    raise acuSgViewerError, " button string is none "

	if whichButton not in _mouseButtonString:
	    raise acuViewError, "Unidentified button name " % whichButton

	val	= _mouseButtonString[whichButton]
	return	_mouseActionMap[val]

#---------------------------------------------------------------------------
# setMouseBinding: sets the action on the button provided
#---------------------------------------------------------------------------

    def setMouseBinding( self, whichButton, whatAction ):
        '''
	    Each of the Mouse buttons with ctrl, shift and alt
	    combinations can be set to have certain action. For now
	    these actions are one of spin, zoom ,pan, zoom_up,
	    zoom_down and pick. All the actions are defined in this
	    class. For pick action, AcuSceneGraph class that has
	    the SoExtSelection objects ( one each for volumes, surfaces,
	    lines and points ) handle the selection mechanism.


	    Arguments:
	        whichButton	- "BUTTON1", BUTTON2...BUTTON3,
		                  BUTTON1_CTRL,...,BUTTON1_SHIFT,
				  BUTTON1_ALT....
	        whatAction	- SPIN, ZOOM, PAN,NONE

	    Output:
	        None
	
        '''

	if whichButton == None:
	    raise acuSgViewerError, " button string is none "

	if whatAction == None:
	    raise acuSgViewerError, " action string is none "

	if whichButton not in _mouseButtonString:
	    raise acuViewError, "Unidentified button name " % whichButton

	if whatAction not in _mouseActionString.values():
	    raise acuViewError, \
	    	"Unidentified action string <%s>" % whatAction

	val	= _mouseButtonString[whichButton]
	_mouseActionMap[val]	= whatAction



#---------------------------------------------------------------------------
# setKeyBinding: sets the action on the key provided
#---------------------------------------------------------------------------

    def setKeyBinding( self, whichButton, whatAction ):
        '''
	    set the actions on the some of the keys. Primarily used
	    to overwrite the default functionality provided by the
	    viewers.
	    For example,
	        we don't want 'q' to quit the application and 'ESC' to
		change the modes between viewing and selection.

	    Arguments:
	        whichButton	- BUTTON1, BUTTON2...BUTTON5,
		                  BUTTON1_CTRL,...,BUTTON1_SHIFT,
				  BUTTON1_ALT....
	        whatAction	- SPIN, ZOOM, PAN, ZOOM_UP, ZOOM_DOWN,PICK

	    Output:
	        None
	
        '''
	pass

#---------------------------------------------------------------------------
# axis: sets/gets the visibility of the axis
#---------------------------------------------------------------------------

    def axis( self, visible = None ):
        '''
	    sets the axis visibility. If visible == None,
	    the current axis state is returned.

	    Arguments:
	        visible		- TRUE/FALSE

	    Output: ( only if input visible == None )
	        visible		- TRUE/FALSE
        '''

	retVal	= self.axisFlag

	if visible != None:
	    if visible != TRUE and visible != FALSE:
	        raise acuSgViewerError, "axis function takes TRUE/FALSE"
	    else:
	        self.axisFlag	= visible
		self.setFeedbackVisible( 		visible 	)	
	
	return retVal

#---------------------------------------------------------------------------
# axisSize: sets/gets the size of the axis
#---------------------------------------------------------------------------

    def axisSize( self, size = None ):
        '''
	    Function to set the size of axis in the graphical window
	    Argument:
		size             - value/None, axis size
	    Output: ( if size input = None )
		size             - current axis size
	'''

	retVal	= self.viewer.getFeedbackSize().getValue(		)

	if size != None:
	    self.viewer.setFeedbackSize(        size                    )
	return retVal

#---------------------------------------------------------------------------
# _setMode: sets the event mode
#---------------------------------------------------------------------------

    def _setMode( self, newMode ):
        '''
	    sets the event mode to newMode ,

	    Arguments:
	        newMode		- "SPIN","ZOOM","PAN" and "NONE"
	    Output:
	        None
        '''

        oldMode	= self.eventMode
	if newMode == oldMode:
	    return

	if newMode == "SPIN":
	    self.spinProj.project(		self.lastMousePos	)

	self.eventMode	= newMode
	self.setMouseRepresentation(					)

#---------------------------------------------------------------------------
# saveLog: stores the previous mouse position
#---------------------------------------------------------------------------

    def saveLog( self, pos ):
        '''
	    saves the current mouse position

	    Arguments:
	        pos		- SbVec2s() object of current mouse posn.
	    Output:
	        None
        '''

	if self.nPtsStored == 0:
	    self.pt1.setValue(			pos.getValue()		)
	    self.nPtsStored	+= 1
	elif self.nPtsStored == 1:
	    self.pt0.setValue(			pos.getValue()		)
	    self.nPtsStored	+= 1
	else:
	    self.pt1.setValue(			self.pt0.getValue()	)
	    self.pt0.setValue(			pos.getValue()		)


#---------------------------------------------------------------------------
# processSoEvent: Point of entry for all graphical window actions
#---------------------------------------------------------------------------

    def processSoEvent( self, ev ):
        '''
	    Function to overwrite the action callbacks
	    Arguments:
	        ev		- SoEvent object
	    Output:
	        success		- returns True else passes control to
					SoQtExaminerViewer( self,ev)
				
        '''

	sx,sy	= self.getGLSize().getValue(				)
	prev	= self.lastMousePos
	px,py	= ev.getPosition().getValue(				)
	px	= float( px ) / float( max( int(sx-1),1) )
	py	= float( py ) / float( max( int(sy-1),1) )

	posn	= SbVec2f(		px,py				)
	self.lastMousePos = posn
	processed	= FALSE

	if ev.wasAltDown():
	    if self.modeFlag != MODE_PICKING and self.isViewing():
	        self.setViewing(		FALSE			)
	    if self.modeFlag != MODE_PICKING:
	        return SoQtExaminerViewer.processSoEvent( self, ev	)
	else:
	    if self.modeFlag != MODE_PICKING and not self.isViewing():
	        self.setViewing(		TRUE			)

	self.ctrldown	= ev.wasCtrlDown(				)
	self.shiftdown	= ev.wasShiftDown(				)

	if self.modeFlag == MODE_PICKING:
	    if self.ctrldown and not self.shiftdown:
		if not self.isViewing():
		    self.setViewing(		TRUE			)
	    else:
	        if self.isViewing():
		    self.setViewing(		FALSE			)
		return SoQtExaminerViewer.processSoEvent( self, ev	)

	if self.modeFlag == MODE_VIEWING:
	    if not self.isViewing():
		self.setViewing(		TRUE			)
	

	curMode	= self.eventMode
	newMode	= curMode

	combEvents	= 0
	if self.ctrldown:
	    combEvents		+= CTRLDOWN
	if self.shiftdown:
	    combEvents		+= SHIFTDOWN


	if( ev.getTypeId() == SoMouseButtonEvent.getClassTypeId() ):

	    #---Handle mouse button events
	    event	= SoMouseButtonEvent(		ev		)

	    if event.getState() == SoButtonEvent.DOWN:
	        press	= TRUE
                #----- Misc 4/08 : E9 
                self.lstVal  = (self.getCameraPosition(),
                                self.getCameraOrientation(),
                                self.getCameraHeight()                  )
	    else:
                press	= FALSE
                #----- Misc 4/08 : E9 
##                newVal  = ( self.getCameraPosition(),
##                                self.getCameraOrientation(),
##                                self.getCameraHeight()                  )
##	        if self.lstVal and newVal != self.lstVal :
##
##                    tag     = self.win.undoStn.UNDO_TAG_HAND_TRANS
##                    self.win.addSettingMarker(  tag,
##                                                par     = 'handTransform',
##                                                lastVal = self.lstVal,
##                                                newVal  = newVal,
##                                                func    = self.refreshUndoSett)
                #----- End of Misc 4/08 : E9 
                
	        
	    #press	= event.getState() == SoButtonEvent.DOWN

	    processed	= TRUE

	    button	= event.getButton(				)

	    if button == SoMouseButtonEvent.BUTTON1:
	        self.button1down	= press
	    elif button == SoMouseButtonEvent.BUTTON2:
	        self.button2down	= press
	    elif button == SoMouseButtonEvent.BUTTON3:
	        self.button3down	= press
	    elif button == SoMouseButtonEvent.BUTTON4:
	        self.button4down	= press
		self.zoom(			0.1			)
	    elif button == SoMouseButtonEvent.BUTTON5:
	        self.button5down	= press
		self.zoom(			-0.1			)
	    else:
	        self.eventMode 	= "NONE"
		processed	= FALSE

	
	if ( ev.getTypeId() == SoKeyboardEvent.getClassTypeId() ):
	    #--- handle key board events

	    event	= SoKeyboardEvent(		ev		)
	    press	= event.getState() == SoButtonEvent.DOWN
	    keyVal	= event.getKey(					)

	    if keyVal == SoKeyboardEvent.ESCAPE or \
	       keyVal == SoKeyboardEvent.Q:
		   processed	= TRUE

	if ( ev.getTypeId() == SoLocation2Event.getClassTypeId() ):
	    event	= SoLocation2Event(		ev		)
	    processed	= TRUE

	    self.saveLog(	event.getPosition()		)
	    if self.eventMode == "ZOOM":
		self.zoomByCursor(		posn,	prev		)
	    elif self.eventMode == "PAN":
		self.pan(			posn,	prev		)
	    elif self.eventMode == "SPIN":
		self.spin(			posn			)
	    else:
	        self.eventMode	= "NONE"
		processed	= FALSE

	if self.button1down:
	    combEvents	+= B1DOWN

	if self.button2down:
	    combEvents	+= B2DOWN

	if self.button3down:
	    combEvents	+= B3DOWN

	if combEvents > ( CTRLDOWN + SHIFTDOWN ):
	    newMode = "NONE"
	else:
	    newMode	= _mouseActionMap[ combEvents ]

	if newMode != curMode:
	    self._setMode(			newMode			)
	
	if not processed:
	    return SoQtExaminerViewer.processSoEvent( self,ev	)
	else:
	    return 1

#---------------------------------------------------------------------------
# setMouseRepresentation: Mouse cursor types are specified here
#---------------------------------------------------------------------------

    def setMouseRepresentation(	 self ):
        '''
	    Function to set the mouse representation based on the
	    current event mode.
	    Arguments:
	        None
	    Output:
	        None
				
        '''

        if self.eventMode == "NONE":
	    self.setComponentCursor(  		self.noneCursor		)
        elif self.eventMode == "SPIN":
	    self.setComponentCursor(  		self.rotateCursor	)
        elif self.eventMode == "PAN":
	    self.setComponentCursor(  		self.panCursor		)
        elif self.eventMode == "ZOOM":
	    self.setComponentCursor(  		self.zoomCursor		)
	else:
	    self.setComponentCursor(  		self.noneCursor		)

#---------------------------------------------------------------------------
# setTransType:
#---------------------------------------------------------------------------

    def setTransType(    self, tType ):
            '''
	        Function to set the transparency type to be used
		Arguments:
		tType   - "SCREEN_DOOR","ADD","DELAYED_ADD",
			"SORTED_OBJECT_ADD","BLEND",DELAYED_BLEND" and
			"SORTED_OBJECT_BLEND"
		Output:
			None
	    '''

	    if tType not in _transType:
		raise acuSgViewerError, \
			"Unrecognized transparency type <%s> " % tType
	    self.setTransparencyType(       _transType[tType]               )

#---------------------------------------------------------------------------
# setCameraPosition: Set the camera position
#---------------------------------------------------------------------------

    def setCameraPosition( self, pos ):
        '''
	    Set the initial camera position when the model is render.
	    
	    Arguments:
	        pos    - The init. position
	        
	    Output:
	        None
				
        '''

	camera	= self.getCamera(					)
        camera.position.setValue(	SbVec3f( pos[0],
                                                 pos[1],    pos[2]      ))

#---------------------------------------------------------------------------
# getCameraPosition: Get the position of camera.
#---------------------------------------------------------------------------

    def getCameraPosition( self ):
        '''
	    Get the position of the camera.
	    
	    Arguments:
	        None
	        
	    Output:
	        x, y, z     - The camera position
				
        '''

	camera	= self.getCamera(					)
        return camera.position.getValue().getValue(                     )

#---------------------------------------------------------------------------
# setCameraOrientation : Set the camera orientation 
#---------------------------------------------------------------------------

    def setCameraOrientation( self, orint ):
        '''
	    Set the camera orientation when the model is render.
	    
	    Arguments:
	        orint     - The orientation
	        
	    Output:
	        None
				
        '''

	camera	= self.getCamera(					)
        camera.orientation.setValue(    SbRotation( orint[0],   orint[1],
                                                    orint[2],   orint[3]))

#---------------------------------------------------------------------------
# getCameraOrientation: Get the position of camera.
#---------------------------------------------------------------------------

    def getCameraOrientation( self ):
        '''
	    Get the orientation of the camera.
	    
	    Arguments:
	        None
	        
	    Output:
	        x, y, z     - The camera position
				
        '''

	camera	= self.getCamera(					)
        return camera.orientation.getValue().getValue(                  )

#---------------------------------------------------------------------------
# setCameraOrientation : Set the camera orientation 
#---------------------------------------------------------------------------

    def setCameraHeight( self, height ):
        '''
	    Set the camera height when the model is render.
	    
	    Arguments:
	        height     - The height
	        
	    Output:
	        None
				
        '''

	camera	= self.getCamera(					)
        camera.height.setValue(                height                   )   

#---------------------------------------------------------------------------
# getCameraOrientation: Get the position of camera.
#---------------------------------------------------------------------------

    def getCameraHeight( self ):
        '''
	    Get the aspectRatio of the camera.
	    
	    Arguments:
	        None
	        
	    Output:
	        aspectRatio    - The camera aspectRatio
				
        '''

	camera	= self.getCamera(					)
        return camera.height.getValue(                                  )

#----- Misc. 8/07 E4
#---------------------------------------------------------------------------
# setAllSettings: set the window background info. from the settings object
#---------------------------------------------------------------------------

    def setAllSettings( self ):
        '''
	    set the settings of graphical window
	    Arguments:
	        None
	    Output:
	        None
        '''

        viewerClr= self.getBackgroundColor().getValue(                  )

        acuQt.setSetting(         'mainBack/red',     viewerClr[0]	)
	acuQt.setSetting(         'mainBack/green',   viewerClr[1]	)
	acuQt.setSetting(         'mainBack/blue',    viewerClr[2]	)

#----- Misc 4/08 : E9    
#---------------------------------------------------------------------------
# refreshUndoSett: 
#---------------------------------------------------------------------------

##    def refreshUndoSett( self, values ):
##        '''
##	    refresh the values of camera by undo/redo.
##	    Arguments:
##	        values   - values of camera.
##	    Output:
##	        None
##        '''
##
##        pos, orint, height  = values
##	
##        self.setCameraPosition(              pos                 )
##        self.setCameraOrientation(           orint               )
##        self.setCameraHeight(                height              )

#---------------------------------------------------------------------------
# Test
#---------------------------------------------------------------------------

from	iv import *

if __name__ == '__main__':
    myWindow	= SoQt.init(	sys.argv[0]				)
    if not myWindow:
    	sys.exit(							)

    #
    #   Use the file in this folder, two_tubes.iv for testing.
    #   python acuSgViewer two_tubes.iv
    #


    if len( sys.argv ) == 2:
	filename	= sys.argv[1]
	mySceneInput = SoInput()
	if not mySceneInput.openFile(filename):
	    raise acuSceneGraphError, "Cannot open file %s" % filename
	
	root = SoDB.readAll(			mySceneInput		)
	if not root:
	    raise acuSceneGraphError, "Problem reading file"
	mySceneInput.closeFile(						)
    else:
	root	= SoCone(						)

    myViewer	= AcuSgViewer(			myWindow		)
    myViewer.setSceneGraph(			root			)
    myViewer.show(							)
    #myViewer.setMouseBinding( "CTRL_BUTTON1_BUTTON2", "NONE"		)
    camera	= myViewer.getCamera(					)
    camera.viewAll(		root,myViewer.getViewportRegion()	)
    SoQt.show(			myWindow				)
    SoQt.mainLoop(							)
