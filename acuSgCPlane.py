#===========================================================================
#
# Include files
#
#===========================================================================

import  types
import  sys
import  math
import  numarray
import  acupc
import  acuiso

from    iv		import *
import	acuSgViewer

SO_SWITCH_ALL	= -3
SO_SWITCH_NONE	= -1

#===========================================================================
#
# ERRORS: error from acuCutPlane module
#
#===========================================================================

ERROR = "error from acuCutPlane module"

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

_disStyles	= {}
_disStyles["none"] 	= "none"
_disStyles["mesh"] 	= "mesh"
_disStyles["mesh line"]	= "mesh line"

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
_mouseActionMap[SHIFTDOWN+B1DOWN]	= "NONE"		# 9
_mouseActionMap[SHIFTDOWN+B2DOWN]	= "NONE"		# 10
_mouseActionMap[SHIFTDOWN+B3DOWN]	= "NONE"		# 12
_mouseActionMap[SHIFTDOWN+B1DOWN+B2DOWN] = "NONE" 		# 11
_mouseActionMap[SHIFTDOWN+B1DOWN+B3DOWN] = "NONE" 		# 13
_mouseActionMap[SHIFTDOWN+B2DOWN+B3DOWN] = "NONE" 		# 14
_mouseActionMap[SHIFTDOWN+B1DOWN+B2DOWN+B3DOWN] = "NONE" 	# 15

_mouseActionMap[CTRLDOWN]		= "NONE"		# 16
_mouseActionMap[CTRLDOWN+B1DOWN]		= "SPIN"		# 17
_mouseActionMap[CTRLDOWN+B2DOWN]		= "ZOOM"		# 18
_mouseActionMap[CTRLDOWN+B3DOWN]		= "PAN"			# 20
_mouseActionMap[CTRLDOWN+B1DOWN+B2DOWN] 	= "NONE" 		# 19
_mouseActionMap[CTRLDOWN+B1DOWN+B3DOWN] 	= "NONE" 		# 21
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

TRUE	= 1
True	= 1
FALSE	= 0
False	= 0

class AcuSgCPlane:

    def __init__( self , sceneGraph ):
        ''' class to render cut plane and the actors '''

	self.mainWin		= sceneGraph.settingObj
	self.db			= self.mainWin.db
	self.sceneGraph		= sceneGraph
	self.viewer		= sceneGraph.viewer

	self.lastMousePos	= self.viewer.lastMousePos
	self.pt0		= self.viewer.pt0
	self.pt1		= self.viewer.pt1
	self.nPtsStored		= self.viewer.nPtsStored
	self.spinProj		= self.viewer.spinProj

	self.eventMode		= "NONE"
	self.button1down	= False
	self.button2down	= False
	self.button3down	= False
	self.button4down	= False
	self.button5down	= False

	self.ctrlDown		= False
	self.shiftDown		= False

	( self.xmax, self.ymax, self.zmax, self.xmin, self.ymin, self.zmin ) = \
		sceneGraph.getBoundingBox( sceneGraph.dynObjects	)
	self.xmid	= ( self.xmin + self.xmax ) / 2.
	self.ymid	= ( self.ymin + self.ymax ) / 2.
	self.zmid	= ( self.zmin + self.zmax ) / 2.
	pntList	= [ [self.xmin,self.ymin,self.zmid],
                    [self.xmax,self.ymin,self.zmid],
		    [self.xmax,self.ymax,self.zmid] ]

	self.cpnts	= numarray.array(	type='d',shape=(4,3)	)
	self.buildRectangle(			pntList			)

	self.cnn	= numarray.arange(	5, type = 'i'		)
	self.cnn[4] 	= 0 

	self.transVal		= 0.3
	self.r			= 0.0
	self.g			= 0.0
	self.b			= 0.0

	self.createCutPlane(						)
	self.clipFlg	= False
	self.clrCrit	= "gray"

	ctr	= self.getCenter(					)
	cvec	= SbVec3f( 		ctr[0],ctr[1],ctr[2]		)
	self.transform.center.setValue(		cvec			)

        self.ctrSensor		= None
        self.nrmSensor		= None
	self.szSensor		= None

	### build acupc stuff...lazy binding
	self.crd	= self.db.getArrayPar( 'crd',
                                               self.db.coordinates      )

	cnnList	= []

	path		= self.db.modelVol
	volumes		= self.db.childNodes(		path, 1		)

	for volume in volumes:
	    childPath 	= path + self.db.RS + volume
	    clr1	= self.db.getArrayPar( 'color', childPath, None )
	    clr		= [ float(clr1[0]),float(clr1[1]),float(clr1[2])]
	    clr		= [ clr[0]/255, clr[1]/255, clr[2]/255 ]
	    meshSets	= self.db.getListPar( 'meshSets', childPath, []	)
	    for mesh in meshSets:
	        node	= self.db.meshVol + self.db.RS + mesh
		cnn	= self.db.getArrayPar(		'cnn', node	)
		cnnList.append(			(cnn,clr)		)

	self.cplane	= acupc.Acupc(		self.crd, cnnList	)

        ### build acuiso stuff...lazy binding
	self.isos       = {}
	usrIds          = self.db.getArrayPar(  'usrIds',
                                                self.db.coordinates     )
	for volume in volumes: 
	    childPath 	= path + self.db.RS + volume
	    meshSets	= self.db.getListPar( 'meshSets', childPath, []	)
	    cnnList     = []
	    for mesh in meshSets:
	        node	= self.db.meshVol + self.db.RS + mesh
		cnn	= self.db.getArrayPar(		'cnn', node	)
		cnnList.append(			cnn		        )
	    self.isos[ volume ] = acuiso.Acuiso(usrIds, self.crd,cnnList)

	self.actors	= {}
	self.meshFlag	= False # Is any mesh displayed
	self.style	= "none"
	self.direction	= "Up"
	self.wheelVal	= 0.0
	self.plnVisFlag	= True

#---------------------------------------------------------------------------
# buildRectangle:
#---------------------------------------------------------------------------
    def buildRectangle( self, pntOrg ):
        ''' build the rectangle representing the plane from a 3 points '''

	pnt	= None

	if type(pntOrg) == types.ListType or type(pntOrg) == types.TupleType:
	    if len(pntOrg) != 3:
	        raise ERROR, "invalid data passed to buildRectangle"
	    if len(pntOrg[0]) != 3 or len(pntOrg[1]) != 3 or \
	       len(pntOrg[2]) != 3:
	        raise ERROR, "invalid data passed to buildRectangle"
            pnt	= pntOrg
	    pnt.append(				1*pnt[0]		)

	elif isinstance( pntOrg, numarray.numarraycore.NumArray ):
	    try:
	        ( nDim1 , nDim2 ) = pntOrg.shape
		if nDim1 != 3 or nDim2 != 3:
	            raise ERROR, "invalid data passed to buildRectangle"
	    except:
	        raise ERROR, "invalid data passed to buildRectangle"
	    pnt	= numarray.array(	type='d', shape=(4,3)		)
	    pnt[0]	= pntOrg[0]
	    pnt[1]	= pntOrg[1]
	    pnt[2]	= pntOrg[2]
	    pnt[3]	= pntOrg[0]
	else:
	    raise ERROR, "invalid data passed to buildRectangle"


	aDir1	= pnt[1][0] - pnt[0][0]
	aDir2	= pnt[1][1] - pnt[0][1]
	aDir3	= pnt[1][2] - pnt[0][2]


	tmp	= math.sqrt(	aDir1**2 + aDir2**2 + aDir3**2		)
	if tmp == 0:
	    tmp	= 1.0
	aDir1	= aDir1 / tmp
	aDir2	= aDir2 / tmp
	aDir3	= aDir3 / tmp

	tmp	= aDir1 * ( pnt[2][0] - pnt[1][0]  ) \
		+ aDir2 * ( pnt[2][1] - pnt[1][1]  ) \
		+ aDir3 * ( pnt[2][2] - pnt[1][2]  )

	pnt[2][0]	-= aDir1 * tmp
	pnt[2][1]	-= aDir2 * tmp
	pnt[2][2]	-= aDir3 * tmp

	pnt[3][0] = pnt[0][0] - pnt[1][0] + pnt[2][0]
	pnt[3][1] = pnt[0][1] - pnt[1][1] + pnt[2][1]
	pnt[3][2] = pnt[0][2] - pnt[1][2] + pnt[2][2]

	self.cpnts[0][0]	= pnt[0][0]
	self.cpnts[0][1]	= pnt[0][1]
	self.cpnts[0][2]	= pnt[0][2]

	self.cpnts[1][0]	= pnt[1][0]
	self.cpnts[1][1]	= pnt[1][1]
	self.cpnts[1][2]	= pnt[1][2]

	self.cpnts[2][0]	= pnt[2][0]
	self.cpnts[2][1]	= pnt[2][1]
	self.cpnts[2][2]	= pnt[2][2]

	self.cpnts[3][0]	= pnt[3][0]
	self.cpnts[3][1]	= pnt[3][1]
	self.cpnts[3][2]	= pnt[3][2]

#---------------------------------------------------------------------------
# getCenter: 
#---------------------------------------------------------------------------

    def getCenter( self ):
        x = ( self.cpnts[0][0] + self.cpnts[1][0] + self.cpnts[2][0] + \
		self.cpnts[3][0] ) / 4.0
        y = ( self.cpnts[0][1] + self.cpnts[1][1] + self.cpnts[2][1] + \
		self.cpnts[3][1] ) / 4.0
        z = ( self.cpnts[0][2] + self.cpnts[1][2] + self.cpnts[2][2] + \
		self.cpnts[3][2] ) / 4.0
        return [x,y,z] 

#---------------------------------------------------------------------------
# createCutPlane:
#---------------------------------------------------------------------------

    def createCutPlane( self ):

	self.planeSep	= SoSeparator(					)

	self.eventCB	= SoEventCallback(				)
	self.planeSep.addChild(			self.eventCB		)
	self.eventCB.addEventCallback( SoKeyboardEvent.getClassTypeId(),
				self.processEvent, None		)
	self.eventCB.addEventCallback( SoMouseButtonEvent.getClassTypeId(),
				self.processEvent, None		)
	self.eventCB.addEventCallback( SoLocation2Event.getClassTypeId(),
				self.processEvent, None		)
			
	self.shapeHints	= SoShapeHints(					)
	self.shapeHints.vertexOrdering.setValue( SoShapeHints.CLOCKWISE	)
	self.shapeHints.shapeType.setValue( SoShapeHints.UNKNOWN_SHAPE_TYPE )
	self.planeSep.addChild(			self.shapeHints		)

	self.drawStyle	= SoDrawStyle(					)
	self.drawStyle.style.setValue(		SoDrawStyle.FILLED	)
	self.planeSep.addChild(			self.drawStyle		)


	self.material	= SoMaterial(					)
	self.transparency(		self.transVal			)
	self.planeSep.addChild(			self.material		)

	self.transform	= SoTransform(					)
	self.planeSep.addChild(			self.transform		)

	self.switch	= SoSwitch(					)
	self.switch.whichChild.setValue(	SO_SWITCH_ALL		)

	self.meshSet	= SoIndexedFaceSet(				)

	self.vertProp	= SoVertexProperty(				)
	self.vertProp.vertex.setValues(			0, self.cpnts	)
	self.meshSet.vertexProperty.setValue(		self.vertProp	)
	self.meshSet.coordIndex.setValues(		0, self.cnn	)
	self.switch.addChild(			self.meshSet		)

	#self.planeSep.addChild(			self.meshSet	)
	self.planeSep.addChild(			self.switch		)

#---------------------------------------------------------------------------
# setCutPlaneVisibility:
#---------------------------------------------------------------------------

    def cutPlaneVisibility( self, flag  = None ):

        if flag == None:
	    return self.plnVisFlag

        if not flag:
	    self.switch.whichChild.setValue(	SO_SWITCH_NONE		)
        else:
	    self.switch.whichChild.setValue(	SO_SWITCH_ALL		)

	self.plnVisFlag = flag
        

#---------------------------------------------------------------------------
# transparency:
#---------------------------------------------------------------------------
    def transparency( self, value = None ):
        ''' set/get the transparency value of the plane'''

        if value == None:
	    return self.transVal

        if value < 0:
	    value = 0

        if value > 1:
	    value = 1

        self.material.transparency.setValue(		value		)
	self.transVal	= value

#---------------------------------------------------------------------------
# color:
#---------------------------------------------------------------------------
    def color( self, r = None, g = None, b = None ):
        ''' set/get the color of the plane'''

        if r != None and g != None and b != None:
	    self.r	= r
	    self.g	= g
	    self.b	= b
	    self.material.diffuseColor.setValue(	r, g, b		)
        else:
	    return ( self.r, self.g, self.b )

#---------------------------------------------------------------------------
# setViewer:
#---------------------------------------------------------------------------
    def getActor( self ):
        ''' get the container  of the entire cut plane data'''
        return self.planeSep

#---------------------------------------------------------------------------
# saveLog:
#---------------------------------------------------------------------------
    def saveLog( self, pos ):
        ''' save the previous two mouse positions'''

        if self.nPtsStored == 0:
	    self.pt1.setValue(			pos.getValue()		)
	    self.nPtsStored	+= 1
        elif self.nPtsStored == 1:
	    self.pt0.setValue(			pos.getValue()		)
	    self.nPtsStored	+= 1
        else:
	    self.pt1.setValue(		self.pt0.getValue()		)
	    self.pt0.setValue(			pos.getValue()		)


#---------------------------------------------------------------------------
# processEvent: Handling QEvent object
#---------------------------------------------------------------------------

    def processEvent( self, userData, eventCB ):
        ''' Handle processEvent before you go to a viewer '''

	event	= eventCB.getEvent(					)

	if self.viewer == None:
	    return False

        sx, sy		= self.viewer.getGLSize().getValue(		)
	prev		= self.lastMousePos

	curMode		= self.eventMode
	newMode		= curMode
	combEvents	= 0
	processed	= False

	if event.wasCtrlDown():
	    self.ctrlDown	= True
	else:
	    self.ctrlDown	= False

	if event.wasShiftDown():
	    self.shiftDown	= True
	else:
	    self.shiftDown	= False

	px, py		= event.getPosition().getValue(	)
	px			= float( px ) / float(max(int(sx-1),1)	)
	py			= float( py ) / float(max(int(sy-1),1)	)
	posn		= SbVec2f(		px,py		)
	self.lastMousePos	= posn

	if event.getTypeId() == SoMouseButtonEvent.getClassTypeId():
	    if event.getState() == SoButtonEvent.DOWN:
	        press	= True
		self.delMesh(						)
	    else:
	        press	= False
		if self.style == "mesh":
		    self.delMesh(					)
		    self.showMesh(					)

                elif self.style == "mesh line":
                    self.delMesh(					)
                    self.showMeshLine(                                  )
		    
            processed	= True
	    button		= event.getButton(			)
	    if button == SoMouseButtonEvent.BUTTON1:
	        self.button1down	= press
		self.viewer.button1down	= press
	    elif button == SoMouseButtonEvent.BUTTON2:
	        self.button2down	= press
		self.viewer.button2down	= press
	    elif button == SoMouseButtonEvent.BUTTON3:
	        self.button3down	= press
		self.viewer.button3down	= press
	    elif button == SoMouseButtonEvent.BUTTON4:
	        self.button4down	= press
		self.viewer.button4down	= press
	        if not self.ctrlDown:
	            self.zoom(			-0.1			)
	    elif button == SoMouseButtonEvent.BUTTON5:
	        self.button5down	= press
		self.viewer.button5down	= press
	        if not self.ctrlDown:
		        self.zoom(			0.1		)
	    else:
	        self.eventMode	= "NONE"
		processed		= False

	if event.getTypeId() == SoLocation2Event.getClassTypeId():
	    self.button1down	= self.viewer.button1down
	    self.button2down	= self.viewer.button2down
	    self.button3down	= self.viewer.button3down
	    self.button4down	= self.viewer.button4down
	    self.button5down	= self.viewer.button5down
	    processed	= True
	    if not self.ctrlDown:
	        self.saveLog(		event.getPosition())
	    if self.eventMode	== "ZOOM":
	        if not self.ctrlDown:
		    self.zoomByCursor(		posn,	prev	)
	    elif self.eventMode	== "PAN":
	        if not self.ctrlDown:
		    self.pan(			posn,	prev	)
	    elif self.eventMode	== "SPIN":
		if not self.ctrlDown:
		    self.spin(			posn		)
	    else:
	        self.eventMode	= "NONE"
	        #processed		= False

	if self.ctrlDown:
	    combEvents	+= CTRLDOWN
	if self.shiftDown:
	    combEvents	+= SHIFTDOWN

        if self.button1down:
	    combEvents	+= B1DOWN

        if self.button2down:
	    combEvents	+= B2DOWN

        if self.button3down:
	    combEvents	+= B3DOWN

        if combEvents > ( CTRLDOWN + SHIFTDOWN):
	    newMode	= "NONE"
        else:
	    newMode	= _mouseActionMap[combEvents]

        if newMode != curMode:
	    self._setMode(		newMode				)

        if self.ctrlDown:
	    return False

        if processed:
	    return True
        else:
	    return False

#---------------------------------------------------------------------------
# _setMode:
#---------------------------------------------------------------------------

    def _setMode( self, newMode ):
        ''' set the camera transformation mode'''

	if newMode == self.eventMode:
	    return

        if newMode == "SPIN":
	    self.spinProj.project(		self.lastMousePos	)

        self.eventMode = newMode
	if self.viewer  != None:
	    self.viewer.setMouseRepresentation(				)

#---------------------------------------------------------------------------
# clip:
#---------------------------------------------------------------------------
    def clip( self, flag ):
        ''' set/get the clip plane flag'''

        if flag != None:
	    self.clipFlg	= flag
	    self.clipDir(			self.direction		)
	    self.sceneGraph.clip(			flag		)
	else:
	    return self.clipFlg

#---------------------------------------------------------------------------
# colorCriteria:
#---------------------------------------------------------------------------
    def colorCriteria( self, clrCrit ):
        ''' set/get the color criteria '''

        if clrCrit != None:
	    if self.clrCrit != clrCrit:
	        self.clrCrit	= clrCrit
		self.delMesh(						)
		if self.style == "mesh":
		    self.showMesh(					)
                elif self.style == "mesh line":
                    self.showMeshLine(                                  )
		    
	else:
	    return self.clrCrit

#---------------------------------------------------------------------------
# clipDir:
#---------------------------------------------------------------------------
    def clipDir( self, direction ):
        ''' set the clip direction''' 

        if direction != None:

	    points	= self.getPlaneData(				)
	    p0 = SbVec3f( points[0][0],points[0][1],points[0][2] )
	    p1 = SbVec3f( points[1][0],points[1][1],points[1][2] )
	    p2 = SbVec3f( points[2][0],points[2][1],points[2][2] )
	    self.direction	= direction

	    if direction == "Up":
	        plane	= SbPlane( 	p0, p1, p2			)

	    elif direction == "Down":
	        plane	= SbPlane( 	p0, p2, p1			)
	    else:
	        raise ERROR, "Undefined clip direction"

	    self.sceneGraph.setClipPlane(	plane			)

#---------------------------------------------------------------------------
# setTransformData:
#---------------------------------------------------------------------------
    def setTransformData( self, data ):
        ''' set the new plane data'''

	self.buildRectangle(			data			)
	self.vertProp.vertex.setValues(		0, self.cpnts		)
	matrix	= SbMatrix(						)
	matrix.makeIdentity(						)
	self.transform.setMatrix(		matrix			)

	ctr	= self.getCenter(					)
	cvec	= SbVec3f( 		ctr[0],ctr[1],ctr[2]		)
	self.transform.center.setValue(		cvec			)

	if self.style == "mesh":
	    self.delMesh(						)
	    self.showMesh(						)
	elif self.style == "mesh line":
	    self.delMesh(						)
	    self.showMeshLine(                                          )

	if self.clipFlg:
	    points	= self.getPlaneData(				)
	    p0 = SbVec3f( points[0][0],points[0][1],points[0][2] )
	    p1 = SbVec3f( points[1][0],points[1][1],points[1][2] )
	    p2 = SbVec3f( points[2][0],points[2][1],points[2][2] )

	    if self.direction == "Up":
	        plane	= SbPlane( 	p0, p1, p2			)
	    elif self.direction == "Down":
	        plane	= SbPlane( 	p0, p2, p1			)
	    else:
	        raise ERROR, "Invalid clip direction"

	    self.sceneGraph.setClipPlane(	plane			)

#---------------------------------------------------------------------------
# setTransformSensor:
#---------------------------------------------------------------------------

    def setTransformSensor( self, cbObj ):
        ''' attach sensors to each of the transformation fields'''

        if self.szSensor != None:
	    self.szSensor	= None

        self.szSensor	= SoFieldSensor( self.trnChangedCb, cbObj	)
	self.szSensor.attach(		self.transform.scaleFactor	)

        if self.ctrSensor != None:
	    self.ctrSensor	= None

        self.ctrSensor	= SoFieldSensor( self.trnChangedCb, cbObj	)
	self.ctrSensor.attach(		self.transform.translation	)

        if self.nrmSensor != None:
	    self.nrmSensor	= None

        self.nrmSensor	= SoFieldSensor( self.trnChangedCb, cbObj	)
	self.nrmSensor.attach(		self.transform.rotation		)

#---------------------------------------------------------------------------
# trnChangedCb:
#---------------------------------------------------------------------------

    def trnChangedCb( self, cbObj, sensor ):
        ''' callback on the sensors attached to the transformation object'''

        pts	= self.getPlaneData(					)
	cbObj.setData(				pts			)

	if self.clipFlg:
	    points	= self.getPlaneData(				)
	    p0 = SbVec3f( points[0][0],points[0][1],points[0][2] )
	    p1 = SbVec3f( points[1][0],points[1][1],points[1][2] )
	    p2 = SbVec3f( points[2][0],points[2][1],points[2][2] )

	    if self.direction == "Up":
	        plane	= SbPlane( 	p0, p1, p2			)
	    elif self.direction == "Down":
	        plane	= SbPlane( 	p0, p2, p1			)
	    else:
	        raise ERROR, "Invalid clip direction"
	    self.sceneGraph.setClipPlane(	plane			)

#---------------------------------------------------------------------------
# getNormal:
#---------------------------------------------------------------------------
    def getNormal( self ):
        ''' get the normal from the plane corners and transformation object'''

        ### Use three corners o,a,b of the plane and compute
	### oa and ob vectors. Take their cross product and normalize it.

	oax	= self.cpnts[1][0] - self.cpnts[0][0]
	oay	= self.cpnts[1][1] - self.cpnts[0][1]
	oaz	= self.cpnts[1][2] - self.cpnts[0][2]

	obx	= self.cpnts[2][0] - self.cpnts[0][0]
	oby	= self.cpnts[2][1] - self.cpnts[0][1]
	obz	= self.cpnts[2][2] - self.cpnts[0][2]

	abx	=  oay * obz - oaz * oby
	aby	=  oaz * obx - oax * obz
	abz	=  oax * oby - oay * obx

	mag	= math.sqrt( abx*abx + aby*aby + abz*abz )
	if mag == 0:
	    mag	= 1.0
	abx,aby,abz	= abx/mag, aby/mag, abz/mag
	abx,aby,abz	= self.rotateVector( SbVec3f(abx,aby,abz))

	return ( abx, aby , abz )

#---------------------------------------------------------------------------
# rotateVector:
#---------------------------------------------------------------------------

    def rotateVector( self, orgAxis ):
        ''' rotate a given point using quaternions '''

	x,y,z,w= self.transform.rotation.getValue().getValue(	)
	nx,ny,nz	= orgAxis

	ax	= w*w*nx + 2*y*w*nz - 2*z*w*ny + x*x*nx + 2*y*x*ny + \
		  2*z*x*nz - z*z*nx - y*y*nx

	ay	= 2*x*y*nx + y*y*ny + 2*z*y*nz + 2*w*z*nx - z*z*ny + \
		  w*w*ny - 2*x*w*nz - x*x*ny

	az	= 2*x*w*nx + 2*y*z*ny + z*z*nz - 2*w*y*nx - y*y*nz + \
		  2*w*x*ny - x*x*nz + w*w*nz

	if ax == 0 and ay == 0 and az == 0:
	    ax, ay, ay	= 0, 0, 1
	else:
	   #normalize ax,ay,az
	   mag	= math.sqrt(	ax*ax + ay*ay + az*az			)
	   ax	= ax / mag
	   ay	= ay / mag
	   az	= az / mag

	return (  ax, ay, az 	)

#---------------------------------------------------------------------------
# display:
#---------------------------------------------------------------------------

    def display( self, style = None ):
        ''' set the display to either mesh, mesh_line or none'''

        if style == None:
	    return self.style

        if style not in _disStyles:
	    return

        self.style  = style

	if self.style == "mesh":
	    self.delMesh(						)
	    self.showMesh(						)
	elif self.style == "mesh line":
	    self.delMesh(						)
	    self.showMeshLine(                                          )
	else:
	    self.middleX(						)
	    self.meshFlag	= False
	    self.delMesh(						)

#---------------------------------------------------------------------------
# delMesh:
#---------------------------------------------------------------------------

    def delMesh( self ):
        ''' delete the mesh actors as well as the vals from the dictionary'''

	self.sceneGraph.cutPlnSwt1.whichChild.setValue(	SO_SWITCH_NONE	)

        for i in self.actors:
	    self.sceneGraph.remCPlnActor(	self.actors[i]		)

        self.actors	= {}
	self.sceneGraph.cutPlnSwt1.whichChild.setValue(	SO_SWITCH_ALL	)

#---------------------------------------------------------------------------
# showMesh:
#---------------------------------------------------------------------------

    def showMesh( self ):
        ''' show the mesh on the cut plane '''

        points	= self.getPlaneData(					)

	srfs = self.cplane.getCutSrfs(		points, self.clrCrit	)

	if srfs == None:
	    return

	nSrfs	= len(				srfs			)

	if nSrfs == 0:
	    self.meshFlag	= False
	    return
	
	self.meshFlag	= True

	for i in range( nSrfs ):
	    ( scrd, srf, clr ) = srfs[i]
	    ( nElems, nElemNodes ) = srf.shape
	    topology = "unknown"
	    name	= "cutplane%d"%i
	    if nElemNodes == 3:
	        topology	= "three_node_triangle"
	    elif nElemNodes == 4:
	        topology	= "four_node_quad"
	    else:
	        raise ERROR, "unknow srf element type"

	    actor = self.sceneGraph.addCPlaneActor(	self.crd, srf,\
	    				topology, name, clr		)
	    self.actors[i]	= actor
	self.sceneGraph.cutPlnSwt1.whichChild.setValue(	SO_SWITCH_ALL	)

#---------------------------------------------------------------------------
# showMeshLine:
#---------------------------------------------------------------------------

    def showMeshLine( self ):
        ''' show the mesh on the cut plane '''

        crd         = self.crd
        nx, ny, nz  = self.getNormal(	                                )
        isoVec      = nx * crd[:,0] + ny * crd[:,1] + nz * crd[:,2]

        cpnts	    = self.getPlaneData(				)
        isoVal      = nx * cpnts[0][0] + ny * cpnts[0][1] + nz * cpnts[0][2]

	path	    = self.db.modelVol
	volumes	    = self.db.childNodes(	path,   1		)
	for volume in volumes:
	    #### RAVI: LHS has four values to unpack: Date: May 12th 2009
            isoCrd,isoTris,isoQuads,isoPrj = self.isos[ volume ].getIsoSurfaces(
                                                isoVec, isoVal          )

            if self.clrCrit == "volumes":
                childPath   = path + self.db.RS + volume
                clr1	    = self.db.getArrayPar( 'color',childPath, None )
                clr	    = [ float(clr1[0]),float(clr1[1]),float(clr1[2])]
                clr	    = [ clr[0]/255, clr[1]/255, clr[2]/255 ]
            else:
                clr         = [ 0.5, 0.5, 0.5 ]

            if len( isoTris ) != 0:
                self.meshFlag= True
                name	    = "cutplane%s" %volume
                topology    = "three_node_triangle"
                actor       = self.sceneGraph.addCPlaneActor(isoCrd,
                                                             isoTris,
                                                             topology,
                                                             name, clr  )
                self.actors[ volume ] = actor

            if len( isoQuads ) != 0:
                self.meshFlag= True
                name	    = "cutplane%s" %volume
                topology    = "four_node_quad"
                actor       = self.sceneGraph.addCPlaneActor(isoCrd,
                                                             isoQuads,
                                                             topology,
                                                             name, clr  )
                self.actors[ volume ] = actor


	self.sceneGraph.cutPlnSwt1.whichChild.setValue(	SO_SWITCH_ALL	)

#---------------------------------------------------------------------------
# getPlaneCenter:
#---------------------------------------------------------------------------
    def getPlaneCenter(	self ):
        ''' get the plane center in world space '''
        vp	= self.viewer.getViewportRegion(			)
	gma	= SoGetMatrixAction(			vp		)
	gma.apply(			self.transform			)

	matrix	= SbMatrix(						)
	matrix	= gma.getMatrix(					)

        pts	= [0,0,0]

	for  i in range(4):

	    svec = SbVec3f( self.cpnts[i][0],self.cpnts[i][1],\
	    			self.cpnts[i][2] 			)
	    dvec = SbVec3f(						)

	    matrix.multVecMatrix(		svec,svec		)
	    dvec = svec
	    x,y,z	= dvec.getValue(				)
	    pts[0] = pts[0] + x
	    pts[1] = pts[1] + y
	    pts[2] = pts[2] + z

	pts[0] = pts[0] / 4.
	pts[1] = pts[1] / 4.
	pts[2] = pts[2] / 4.

	return pts

#---------------------------------------------------------------------------
# getPlaneData:
#---------------------------------------------------------------------------

    def getPlaneData(	self ):
        ''' get the three corners of the plane in world space '''

        vp	= self.viewer.getViewportRegion(			)
	gma	= SoGetMatrixAction(			vp		)
	gma.apply(			self.transform			)

	matrix	= SbMatrix(						)
	matrix	= gma.getMatrix(					)

        pts	= numarray.array( type='d', shape=(3,3)			)

	for  i in range(3):
	    svec = SbVec3f( self.cpnts[i][0],self.cpnts[i][1],\
	    			self.cpnts[i][2] 			)
	    dvec = SbVec3f(						)

	    matrix.multVecMatrix(		svec,svec		)
	    dvec = svec
	    pts[i][0], pts[i][1],pts[i][2] = dvec.getValue()

	return pts

#---------------------------------------------------------------------------
# middleX:
#---------------------------------------------------------------------------

    def middleX( self, offset = 0.0 ):
        ''' Locate the plane with x-axis as normal and at xmid '''

	xm	= self.xmid
	xm	+= offset

	pntList	= [ [xm,self.ymin,self.zmin],
	            [xm,self.ymin,self.zmax],
		    [xm,self.ymax,self.zmax] ]
	self.setTransformData( 			pntList 		)

#---------------------------------------------------------------------------
# middleY:
#---------------------------------------------------------------------------

    def middleY( self, offset = 0.0 ):
        ''' Locate the plane with y-axis as normal and at ymid '''

	ym	= self.ymid

	ym	+= offset

	pntList	= [ [self.xmin,ym,self.zmin],
	            [self.xmin,ym,self.zmax],
		    [self.xmax,ym,self.zmax] ]
	self.setTransformData( 			pntList 		)

#---------------------------------------------------------------------------
# middleZ:
#---------------------------------------------------------------------------

    def middleZ( self, offset = 0.0 ):
        ''' Locate the plane with z-axis as normal and at zmid '''

	zm	= self.zmid
	zm	+= offset

	pntList	= [ [self.xmin,self.ymin,zm],
	            [self.xmin,self.ymax,zm],
		    [self.xmax,self.ymax,zm] ]
	self.setTransformData( 			pntList 		)

#---------------------------------------------------------------------------
# translateAlongNormal:
#---------------------------------------------------------------------------

    def translateAlongNormal( self, value ):
        ''' Translate along the normal by value'''

	v		= value - self.wheelVal
	self.wheelVal	= value

	nx, ny, nz	= self.getNormal(				)
	pts		= self.getPlaneData(				)

        r1	= [ pts[0,0] , pts[0,1] , pts[0,2] ]
        r2	= [ pts[1,0] , pts[1,1] , pts[1,2] ]
        r3	= [ pts[2,0] , pts[2,1] , pts[2,2] ]

	r1[0]	= r1[0] + v * nx
	r1[1]	= r1[1] + v * ny
	r1[2]	= r1[2] + v * nz

	r2[0]	= r2[0] + v * nx
	r2[1]	= r2[1] + v * ny
	r2[2]	= r2[2] + v * nz

	r3[0]	= r3[0] + v * nx
	r3[1]	= r3[1] + v * ny
	r3[2]	= r3[2] + v * nz

	pntList	= [ r1, r2, r3 ]

	self.setTransformData(			pntList			)

#---------------------------------------------------------------------------
# alignAxis: align the cut plane to closest principal axis
#---------------------------------------------------------------------------

    def alignAxis( self, ax, ay, az ):
        '''
	    returns the closest principal axes to ax,ay,az
	    Arguments:
	        ax	- normalized direction of the x-vector
	        ay	- normalized direction of the y-vector
	        az	- normalized direction of the z-vector
	    Output:
	        ( ax,ay,az )	- closest principal axes
        '''

        if abs(ax) >= abs(ay):
	    if abs(ax) >= abs(az):
		if ax >= 0:
		    ax, ay, az = +1, 0, 0
		else:
		    ax, ay, az = -1, 0, 0
	    else:
		if az >= 0:
		    ax, ay, az = 0, 0, +1
		else:
		    ax, ay, az = 0, 0, -1
	else:
	    if abs(ay) >= abs(az):
	        if ay >= 0:
		    ax, ay, az = 0, +1, 0
		else:
		    ax, ay, az = 0, -1, 0
	    else:
	        if az >= 0:
		    ax, ay, az = 0, 0, +1
		else:
		    ax, ay, az = 0, 0, -1
	return( ax, ay, az )

#---------------------------------------------------------------------------
# snap: compute and align the cut plane to closest principal axis
#---------------------------------------------------------------------------

    def snap( self , zsnap = False ):
        '''
	    snaps the cut plane to to the closest principal axes
	    Arguments:
	        zsnap	 - if True snaps only in the z-plane ( default=False)
	    Output:
	        None
        '''

	nx, ny, nz	= self.getNormal(				)
	pts		= self.getPlaneData(				)

        xmax	= max ( pts[0,0] , pts[1,0] , pts[2,0] ) 
        xmin	= min ( pts[0,0] , pts[1,0] , pts[2,0] ) 
        ymax	= max ( pts[0,1] , pts[1,1] , pts[2,1] ) 
        ymin	= min ( pts[0,1] , pts[1,1] , pts[2,1] ) 
        zmax	= max ( pts[0,2] , pts[1,2] , pts[2,2] ) 
        zmin	= min ( pts[0,2] , pts[1,2] , pts[2,2] ) 

        xc	= ( xmin + xmax ) / 2.0
        yc	= ( ymin + ymax ) / 2.0
        zc	= ( zmin + zmax ) / 2.0



	ax, ay, az	= self.alignAxis( 		nx, ny, nz 	)

	#t		= ax * nx + ay * ny + az * nz
	#print t
	#nx, ny, nz	= nx - t * ax, ny - t * ay, nz - t * az

	if zsnap:
	    t		= math.sqrt( ax*ax + ay*ay + az*az )
	    if t == 0:
	        return
	    nx,ny,nz	= ax / t, ay / t, az / t
	else:
	    nx,ny,nz	= self.alignAxis( ax, ay, az )

	if nx == 1:
	    pntList = [ [xc,ymin,zmin],[xc,ymin,zmax],[xc,ymax,zmax] ]
	elif ny == 1:
	    pntList = [ [xmin,yc,zmin],[xmin,yc,zmax],[xmax,yc,zmax] ]
	else:
	    pntList = [ [xmin,ymin,zc],[xmin,ymax,zc],[xmax,ymax,zc] ]
	
	self.setTransformData(			pntList			)

#---------------------------------------------------------------------------
# snapz: compute and align the camera to closest z plane
#---------------------------------------------------------------------------

    def snapz( self ):
        '''
	    snaps the camera to to the closest z plane.
	    calls snap( True )
	    Arguments:
	        None
	    Output:
	        None
        '''
        self.snap( True )

#---------------------------------------------------------------------------
# zoom: sets the scaleFactor value of Transformation to zoom the object
#---------------------------------------------------------------------------

    def zoom( self, amp ):
        ''' zoom the plane by adjusting scale factor'''
	amp	= amp
        sF	= self.transform.scaleFactor.getValue(			)
	sx,sy,sz= sF.getValue(						)
	sx,sy,sz= sx + sx * amp, sy + sy * amp , sz + sz * amp
	if sx != 0 and sy != 0 and sz != 0:
	    sF	= SbVec3f(			sx,sy,sz		)
	    self.transform.scaleFactor.setValue(		sF	)

#---------------------------------------------------------------------------
# pan: pans the object based on previous and current mouse positions.
#---------------------------------------------------------------------------

    def pan( self, currPos, prevPos ):
        ''' pan plane '''
	if not self.viewer:
	    return
	camera	= self.viewer.getCamera(				)
	vv	= camera.getViewVolume( self.viewer.getGLAspectRatio()	)
	line	= SbLine(						)
	fD	= camera.focalDistance.getValue(			)
	panPln	= vv.getPlane(			fD			)

	vv.projectPointToLine(		currPos,	line		)
	curPt	= SbVec3f(						)
	panPln.intersect(		line, curPt			)

	vv.projectPointToLine(		prevPos,	line		)
	oldPt	= SbVec3f(						)
	panPln.intersect(		line,	oldPt			)

	#px,py,pz	= camera.position.getValue(			)
	tx,ty,tz	= self.transform.translation.getValue(		)
	cx,cy,cz	= curPt.getValue(				)
	ox,oy,oz	= oldPt.getValue(				)
	#px,py,pz	= px + ( ox-cx ), py + ( oy-cy ), pz + ( oz-cz )
	tx,ty,tz	= tx + ( cx-ox ), ty + ( cy-oy ), tz + ( cz-oz )
	self.transform.translation.setValue(	SbVec3f(tx,ty,tz)	)

#---------------------------------------------------------------------------
# spin: spins the transf. object based on the current and previous 
#       positions.The previous position is used in the projector and is not
#       required by this function.
#---------------------------------------------------------------------------

    def spin( self, pos ):
        ''' spin plane '''
	if not self.viewer:
	    return

	if self.nPtsStored < 2:
	    return

	px,py	= pos.getValue(						)
	lx,ly	= self.pt1.getValue(				)
	sx,sy	= self.viewer.getGLSize().getValue(			)
	lx	= float( lx ) / float( 	max( 	int(sx-1),1 	)	)
	ly	= float( ly ) / float( 	max( 	int(sy-1),1 	)	)

	self.spinProj.project(		SbVec2f(lx,ly)			)
	rot	= SbRotation(						)
	rot.invert(							)
	self.spinProj.projectAndGetRotation(	pos, rot		)

	### reorient camera equivalent to object

	oldOrient	= self.transform.rotation.getValue()
	(ox,oy,oz,ow)	= ( rot * oldOrient ).getValue(			)
	#(ox,oy,oz,ow)	= ( oldOrient * rot ).getValue(			)
	self.transform.rotation.setValue( 	ox,oy,oz,ow		)

#---------------------------------------------------------------------------
# zoomByCursor: calls zoom by computing amplification value from cursor
#                positions ( previous and current ).
#---------------------------------------------------------------------------

    def zoomByCursor( self, currPos, prevPos ):
        ''' zoom the plane by adjusting scale factor with cursor movement'''
	cx,cy	= currPos.getValue(					)
	px,py	= prevPos.getValue(					)
	amp	= ( py - cy ) * 2.0
	self.zoom(			amp				)

#---------------------------------------------------------------------------
# Test:
#---------------------------------------------------------------------------

if __name__ == '__main__':

    myWindow	= SoQt.init(		sys.argv[0]			)
    if not myWindow:
    	sys.exit(							)
