#===========================================================================
#
# Include files
#
#===========================================================================

from	iv	import	*
import	math
import	numarray

#===========================================================================
#
# ERROR
#
#===========================================================================

acuSgObjectError	= "ERROR from acuSgObject module"

#===========================================================================
#
# AcuSgObject
#
#===========================================================================

class AcuSgObject( SoSeparator ):

    def __init__( 	self,
    			parent		= None,
    			type		= "point",
			center		= [0,0,0],
			normal		= [0,1,0],
                        normalX         = [1,0,0],
                        normalY         = [0,1,0],
                        normalZ         = [0,0,1],
			radius		= None,
			height		= None,
			width		= None,
			depth		= None,
			xangle		= None,
			yangle		= None,
			zangle		= None,
			color		= [1,0,0],
			pntList		= None,
			point		= None,
			point1		= None,
			point2		= None,
			verticesPerRow  = 0,
			verticesPerColumn = 0,
			text		= None,
			fontSize	= None,
			fontName 	= "Times-Roman",
			pointSize	= 2,
			lineWidth	= 2,
			arrowLength	= 1,
			triSize		= 1,
			tetSize		= 1,
                        vis             = False,
                        trans           = False,
                        transVal        = 0.5,
                        points          = None,
                        lnStyle         = "Solid line",
			):
	'''
	This class is useful for building 0D, 1D, 2D and 3D objects
	to be incorporated into scenegraph to provide visual feedback
	to the end user.
	example applications:
	    - drawing an arrow to show a vector
	    - drawing a circle, box, sphere or a cylinder to identify
	      a region for specifying mesh attributes
	'''

	SoSeparator.__init__(			self			)

	self.shpObj	= None

	self.parent	= parent
	self.objType	= type
	self.ctr	= SbVec3f(	center[0], center[1], center[2]	)
	self.nrm	= SbVec3f(	normal[0], normal[1], normal[2]	)
	self.nrmX	= SbVec3f(	normalX[0],normalX[1],normalX[2])
	self.nrmY	= SbVec3f(	normalY[0],normalY[1],normalY[2])
	self.nrmZ	= SbVec3f(	normalZ[0],normalZ[1],normalZ[2])
	self.prvNrm	= SbVec3f(		0, 1, 0 		)
	self.rad	= radius
	self.ht		= height
	self.wd		= width
	self.dp		= depth
	self.pt		= point
	self.pt1	= point1
	self.pt2	= point2
	self.pList	= pntList
	self.clr	= color
        self.lnw	= lineWidth
        self.pntSize	= pointSize
        self.text	= text
        self.fntSize	= fontSize
        self.fntName    = fontName
        self.arrowLen	= arrowLength
        self.triSize	= triSize
        self.tetSize	= tetSize
	self.visFlg	= vis
	self.transFlg   = trans
        self.transValue = transVal
        self.lnStyle    = lnStyle
        self.hLightFlag = None
	self.xangle	= xangle
	self.yangle	= yangle
	self.zangle	= zangle
	self.vrtxPerRow = verticesPerRow
	self.vrtxPerCol = verticesPerColumn


        self.lineStyles                         = {}
        self.lineStyles['Solid line']           = 0xffff
        self.lineStyles['Dash line']            = 0xff00
        self.lineStyles['Dot line']             = 0x1111
        self.lineStyles['Dash Dot Dot line']    = 0x7ff6
        self.lineStyles['Dash Dot line']        = 0x8ff0

	if self.objType == "cylinder" or \
		self.objType == "cone" or \
		self.objType == "box" or \
		self.objType == "sphere" or \
		self.objType == "tet" or \
		self.objType == "triangle" or \
		self.objType == "circle" or \
		self.objType == "brick" or \
		self.objType == "text" or\
		self.objType == "quade":

	    self.material	= SoMaterial(				)
	    self.addChild(			self.material		)
	    self.color(				self.clr		)

	    self.drawStyle	= SoDrawStyle(				)
	    self.drawStyle.style.setValue(	SoDrawStyle.FILLED	)
	    self.addChild(			self.drawStyle		)


	    self.trans	= SoTranslation(				)
	    self.addChild(			self.trans		)
	    self.center(			self.ctr		)

	    self.rot	= SoRotation(					)
	    self.addChild(			self.rot		)

	    self.fntObj	= SoFont(					)
	    self.addChild(			self.fntObj		)
	    self.fontSize(			self.fntSize		)

	    self.txtObj	= SoText2(					)
	    self.addChild(			self.txtObj		)
	    self.setText(			self.text		)
		
	if self.objType == "cylinder":
	    self._createCylinder(					)
	elif self.objType == "sphere":
	    self._createSphere(						)
	elif self.objType == "cone":
	    self._createCone(						)
	elif self.objType == "box":
	    self.boxRotX	= SoRotationXYZ(			)
	    self.boxRotY	= SoRotationXYZ(			)
	    self.boxRotZ	= SoRotationXYZ(			)
	    self.boxRotX.axis.setValue(		SoRotationXYZ.X		)
	    self.boxRotY.axis.setValue(		SoRotationXYZ.Y		)
	    self.boxRotZ.axis.setValue(		SoRotationXYZ.Z		)
	    self.addChild(			self.boxRotX		)
	    self.addChild(			self.boxRotY		)
	    self.addChild(			self.boxRotZ		)
	    self._createBox(						)
	    self.rotateBox(	self.xangle, self.yangle, self.zangle	)
	elif self.objType == "circle":
	    self._createCircle(						)
	elif self.objType == "triangle":
	    self._createTriangle(					)
	elif self.objType == "tet":
	    self._createTet(						)
	elif self.objType == "arrow":
	    self._createArrow(						)
	elif self.objType == "axes":
	    self._createAxes(						)
	elif self.objType == "point":
	    self._createPoint(						)
	elif self.objType == "points":
	    self._createPoints(						)
	elif self.objType == "line":
	    self._createLine(						)
	elif self.objType == "pointsLine":
            self._createPntsLine(                                       )
	elif self.objType == "polyline":
	    self._createPolyLine(					)
	elif self.objType == "brick":
            self._createBrick(                  points                  )
        elif self.objType == "quade":
            self._createQuade(                  points                  )
	elif self.objType == "text":
	    pass # need to add some attributes to the added text
	elif self.objType == "quadmesh":
	    self._createQuadMesh()
	else:
	    raise acuSgObjectError, " Unknown object type  <%s> " % type

        if self.transFlg:
            self.transparencyOn(                                        )

	if not self.visFlg:
	    self.visibilityOff(						)

#-------------------------------------------------------------------------
# _createQuadMesh: private function to create a QuadMesh
#-------------------------------------------------------------------------

    def _createQuadMesh(  self ):

        # Draw Colormap Quadmesh
        self.transform = SoTransform()
        self.transform.translation.setValue( self.ctr )
        self.addChild( self.transform )
		
        self.materialObj = SoMaterial()
        self.materialObj.diffuseColor.setValues(0, self.clr)
        self.addChild( self.materialObj )
		
        self.materialBinding = SoMaterialBinding()
        self.materialBinding.value.setValue(SoMaterialBinding.PER_VERTEX)
        self.addChild( self.materialBinding )
		
		# Using the new SoVertexProperty node is more efficient
        vertexPropertyObj = SoVertexProperty()
        vertexPropertyObj.vertex.setValues(0, self.pList)
		
        # Define the QuadMesh.
        self.quadMeshObj = SoQuadMesh()
        self.quadMeshObj.verticesPerRow.setValue(self.vrtxPerRow)
        self.quadMeshObj.verticesPerColumn.setValue(self.vrtxPerCol)
        self.quadMeshObj.vertexProperty.setValue(vertexPropertyObj)
        self.addChild( self.quadMeshObj )
	
#-------------------------------------------------------------------------
# _createText: private function to create a Text
#-------------------------------------------------------------------------	
    def _createText(  self, parentSep ):
	
        self.fntObj	= SoFont()
        parentSep.addChild(	self.fntObj	)
		
        if self.fntSize != None:
            self.fntObj.size.setValue( self.fntSize )
		
        if self.fntName != None:
            self.fntObj.name.setValue( self.fntName	)
		
        self.txtObj	= SoText2(	)
        parentSep.addChild( self.txtObj )

        if self.text != None:
            self.txtObj.string.setValue( self.text )        
        
		
#-------------------------------------------------------------------------
# _createCylinder: private function to create a Cylinder
#-------------------------------------------------------------------------

    def _createCylinder(  self ):
	'''
	   private function to create a cylinder
	'''

	self.shpObj	= SoCylinder(					)
	self.addChild(				self.shpObj		)

	self.radius(				self.rad		)
	self.height(				self.ht			)
	self.normal(				self.nrm		)
	self.color(				self.clr		)

#-------------------------------------------------------------------------
# _createSphere: private function to create a Sphere
#-------------------------------------------------------------------------

    def _createSphere(  self ):
	'''
	   private function to create a sphere
	'''
	self.shpObj	= SoSphere(					)
	self.addChild(				self.shpObj		)

	self.radius(				self.rad		)

#-------------------------------------------------------------------------
# _createCone: private function to create a Cone
#-------------------------------------------------------------------------

    def _createCone(  self ):
	'''
	   private function to create a cone
	'''
	self.shpObj	= SoCone(					)
	self.addChild(				self.shpObj		)

	self.radius(				self.rad		)
	self.height(				self.ht			)
	self.normal(				self.nrm		)

#-------------------------------------------------------------------------
# _createBox: private function to create a Box
#-------------------------------------------------------------------------

    def _createBox(  self ):
	'''
	   private function to create a box
	'''

	self.shpObj	= SoCube(					)
	self.addChild(				self.shpObj		)


	self.height(				self.ht			)
	self.width(				self.wd			)
	self.depth(				self.dp			)

#-------------------------------------------------------------------------
# _createTriangle: private function to create a Triangle
#-------------------------------------------------------------------------

    def _createTriangle(  self ):
	'''
	   private function to create a triangle
	'''

	self.shHints	= SoShapeHints(					)
	self.shHints.vertexOrdering.setValue( SoShapeHints.CLOCKWISE	)
	self.shHints.shapeType.setValue(SoShapeHints.UNKNOWN_SHAPE_TYPE	)
	self.addChild(			self.shHints			)

	self.vertProp	= SoVertexProperty(				)
	self.shpObj	= SoIndexedFaceSet(				)
	self.shpObj.vertexProperty.setValue(		self.vertProp	)
	self.addChild(			self.shpObj			)

	self.crd	= numarray.zeros( shape=(3,3), type='d'		)
	self.cnn	= numarray.arange(  	4, type='i'		)
	self.cnnFlag	= False
	self.setTriangleData(		self.triSize			)
    	self.normal( 			self.nrm			)

#-------------------------------------------------------------------------
# _createTet: private function to create a Tetrahedron
#-------------------------------------------------------------------------

    def _createTet(  self ):
	'''
	   private function to create a triangle
	'''

	self.shHints	= SoShapeHints(					)
	self.shHints.vertexOrdering.setValue( SoShapeHints.CLOCKWISE	)
	self.shHints.shapeType.setValue(SoShapeHints.UNKNOWN_SHAPE_TYPE	)
	self.addChild(			self.shHints			)

	self.drawStyle	= SoDrawStyle(					)
	self.drawStyle.style.setValue(	SoDrawStyle.FILLED		)
	self.addChild(			self.drawStyle			)

	self.vertProp	= SoVertexProperty(				)
	self.shpObj	= SoIndexedFaceSet(				)
	self.shpObj.vertexProperty.setValue(		self.vertProp	)
	self.addChild(			self.shpObj			)

	self.crd	= numarray.zeros( shape=(4,3), type='d'		)
	self.cnn	= numarray.arange(  	16, type='i'		)
	self.cnnFlag	= False
	self.setTetData(		self.tetSize			)

#-------------------------------------------------------------------------
# _createCircle: private function to create a Circle
#-------------------------------------------------------------------------

    def _createCircle(  self ):
	'''
	   private function to create a circle
	'''

	self.shHints	= SoShapeHints(					)
	self.shHints.vertexOrdering.setValue( SoShapeHints.CLOCKWISE	)
	self.shHints.shapeType.setValue(SoShapeHints.UNKNOWN_SHAPE_TYPE	)
	self.addChild(			self.shHints			)

	self.vertProp	= SoVertexProperty(				)
	self.shpObj	= SoIndexedFaceSet(				)
	self.shpObj.vertexProperty.setValue(		self.vertProp	)
	self.addChild(			self.shpObj			)

	self.nPts	= 24
	self.crd	= numarray.zeros( shape=(self.nPts,3), type='d'	)
	self.cnn	= numarray.arange(  4*(self.nPts-1), type='i'	)
	self.cnnFlag	= False
    	self.radius( 			self.rad			)
    	self.normal( 			self.nrm			)

#-------------------------------------------------------------------------
# _createArrow: private function to create a Arrow
#-------------------------------------------------------------------------

    def _createArrow(  self ):
	'''
	   private function to create an arrow
	'''

	self.arrowSep	= SoSeparator(					)
	self.addChild(				self.arrowSep		)

	self.material	= SoMaterial(					)
	self.arrowSep.addChild(			self.material		)
	self.color(				self.clr		)

	self.drawStyle	= SoDrawStyle(					)
	self.drawStyle.style.setValue(	SoDrawStyle.FILLED		)
	self.arrowSep.addChild(		self.drawStyle			)

	self.vertProp	= SoVertexProperty(				)
	self.shpObj	= SoIndexedLineSet(				)
	self.shpObj.vertexProperty.setValue(		self.vertProp	)
	self.arrowSep.addChild(		self.shpObj			)

	self.crd	= numarray.zeros( shape=(2,3), type='d'	)
	self.cnn	= numarray.arange(  3, type='i'	)
	self.cnnFlag	= False

	if self.pt1 == None and self.pt2 == None:
	    raise acuSgObjectError, \
				"specify atleast one point on the arrow"
	self.ptCal	= None

	if self.pt2 == None:
	    self.ptCal	= "pt2"

	if self.pt1 == None:
	    self.ptCal	= "pt1"

	if self.arrowLen == None:
	    self.arrowLen = 1.0

	if self.pt2 == None:
	    nx, ny, nz	= self.nrm.getValue(				)
	    self.pt2	= [ 0, 0, 0 ]
	    self.pt2[0]	= self.pt1[0] + self.arrowLen * nx
	    self.pt2[1]	= self.pt1[1] + self.arrowLen * ny
	    self.pt2[2]	= self.pt1[2] + self.arrowLen * nz

	if self.pt1 == None:
	    nx, ny, nz	= self.nrm.getValue(				)
	    self.pt1	= [ 0, 0, 0 ]
	    self.pt1[0]	= self.pt2[0] - self.arrowLen * nx
	    self.pt1[1]	= self.pt2[1] - self.arrowLen * ny
	    self.pt1[2]	= self.pt2[2] - self.arrowLen * nz

	self._drawArrowHead(	self.pt1, self.pt2			)
	self.setLineData(	self.pt1, self.pt2			)

	self.fntObj	= SoFont(					)
	self.arrowSep.addChild(		self.fntObj			)
	self.fontSize(			self.fntSize			)
	self.txtObj	= SoText2(					)
	self.arrowSep.addChild(		self.txtObj			)
	self.setText(			self.text			)
	self.lineWidth(			self.lnw			)

#-------------------------------------------------------------------------
# _createAxes: private function to create Axes
#-------------------------------------------------------------------------

######## NOT IMPLEMENTED #############

    def _createAxes(  self ):
	'''
	   private function to create axes
	'''

	self.axesSep	= SoSeparator(					)
	self.addChild(			    self.axesSep		)

	self.drawStyle	= SoDrawStyle(					)
	self.drawStyle.style.setValue(	    SoDrawStyle.FILLED		)
	self.axesSep.addChild(		    self.drawStyle		)

        #----- xAxis
	self.axesSepX	= SoSeparator(					)
	self.axesSep.addChild(		    self.axesSepX		)
	
    	self.xMat	= SoMaterial(					)
	self.xMat.diffuseColor.setValue(    1, 0, 0			)
	self.axesSepX.addChild(		    self.xMat		        )

	self.xVp	= SoVertexProperty(				)
	self.xShpObj	= SoIndexedLineSet(				)
	self.xShpObj.vertexProperty.setValue(self.xVp	                )
	self.axesSepX.addChild(		    self.xShpObj		)

        #----- yAxis
	self.axesSepY	= SoSeparator(					)
	self.axesSep.addChild(		    self.axesSepY		)
	
    	self.yMat	= SoMaterial(					)
	self.yMat.diffuseColor.setValue(    0, 1, 0			)
	self.axesSepY.addChild(		    self.yMat		        )

	self.yVp	= SoVertexProperty(				)
	self.yShpObj	= SoIndexedLineSet(				)
	self.yShpObj.vertexProperty.setValue(self.yVp	                )
	self.axesSepY.addChild(		    self.yShpObj		)

        #----- zAxis
	self.axesSepZ	= SoSeparator(					)
	self.axesSep.addChild(		    self.axesSepZ		)
	
    	self.zMat	= SoMaterial(					)
	self.zMat.diffuseColor.setValue(    0, 0, 1			)
	self.axesSepZ.addChild(		    self.zMat		        )

	self.zVp	= SoVertexProperty(				)
	self.zShpObj	= SoIndexedLineSet(				)
	self.zShpObj.vertexProperty.setValue(self.zVp	                )
	self.axesSepZ.addChild(		    self.zShpObj		)

	self.xCrd	= numarray.zeros( shape=(2,3), type='d'	)
	self.xCnn	= numarray.arange(  3, type='i'	)
	self.xCnnFlag	= False

	self.yCrd	= numarray.zeros( shape=(2,3), type='d'	)
	self.yCnn	= numarray.arange(  3, type='i'	)
	self.yCnnFlag	= False

	self.zCrd	= numarray.zeros( shape=(2,3), type='d'	)
	self.zCnn	= numarray.arange(  3, type='i'	)
	self.zCnnFlag	= False

	if self.pt1 == None:
	    raise acuSgObjectError, \
				"specify atleast one point on the axes"

	self.ptCal	= None

	if self.pList == None:
	    self.ptCal	= "pList"

	if self.arrowLen == None:
	    self.arrowLen = 1.0

	if self.pList == None:
            self.pList	        = [ [0, 0, 0], [0, 0, 0], [0, 0, 0] ]
            
	    nxX, nyX, nzX       = self.nrmX.getValue(			)
	    self.pList[0][0]    = self.pt1[0] + self.arrowLen * nxX
	    self.pList[0][1]    = self.pt1[1] + self.arrowLen * nyX
	    self.pList[0][2]    = self.pt1[2] + self.arrowLen * nzX

	    nxY, nyY, nzY       = self.nrmY.getValue(			)
	    self.pList[1][0]    = self.pt1[0] + self.arrowLen * nxY
	    self.pList[1][1]    = self.pt1[1] + self.arrowLen * nyY
	    self.pList[1][2]    = self.pt1[2] + self.arrowLen * nzY

	    nxZ, nyZ, nzZ       = self.nrmZ.getValue(			)
	    self.pList[2][0]    = self.pt1[0] + self.arrowLen * nxZ
	    self.pList[2][1]    = self.pt1[1] + self.arrowLen * nyZ
	    self.pList[2][2]    = self.pt1[2] + self.arrowLen * nzZ

	self._drawArrowHeadAxes(        self.pt1,       self.pList	)
	self.setLineDataAxes(	        self.pt1,       self.pList	)

	self.fntObj	= SoFont(					)
	self.axesSep.addChild(		self.fntObj			)
	self.fontSize(			self.fntSize			)
	self.txtObj	= SoText2(					)
	self.axesSep.addChild(		self.txtObj			)
	self.setText(			self.text			)
	self.lineWidth(			2				)

#-------------------------------------------------------------------------
# _createPoint: private function to create a Point
#-------------------------------------------------------------------------

    def _createPoint(  self ):
	'''
	   private function to create a point
	'''

	self.material	= SoMaterial(					)
	self.addChild(			self.material			)
	self.color(			self.clr			)

	self.drawStyle	= SoDrawStyle(					)
	self.drawStyle.style.setValue(	SoDrawStyle.FILLED		)
	self.addChild(			self.drawStyle			)

	self.vertProp	= SoVertexProperty(				)
	self.shpObj	= SoPointSet(					)
	self.shpObj.vertexProperty.setValue(	self.vertProp		)
	self.addChild(			self.shpObj			)

	self.trans	= SoTranslation(				)
	self.addChild(			self.trans			)
	self.center(			self.ctr			)

	self.fntObj	= SoFont(					)
	self.addChild(			self.fntObj			)
	self.fontSize(			self.fntSize			)

	self.txtObj	= SoText2(					)
	self.addChild(			self.txtObj			)
	self.setText(			self.text			)


	self.shpObj.numPoints.setValue(		1			)

	self.crd	= numarray.zeros( 	shape=(1,3), type='d'	)
	self.setPointData(		self.pt				)
	self.pointSize(			self.pntSize			)

#-------------------------------------------------------------------------
# _createPoint: private function to create points
#-------------------------------------------------------------------------

    def _createPoints(  self ):
	'''
	   private function to create points
	'''

	self.pointsSep	= SoSeparator(					)
	self.addChild(			self.pointsSep			)

	self.material	= SoMaterial(					)
	self.pointsSep.addChild(	self.material			)
	self.color(			self.clr			)

	self.drawStyle	= SoDrawStyle(					)
	self.drawStyle.style.setValue(	SoDrawStyle.FILLED		)
	self.pointsSep.addChild(	self.drawStyle			)

	self.vertProp	= SoVertexProperty(				)
	self.shpObj	= SoPointSet(				        )
	self.shpObj.vertexProperty.setValue(	self.vertProp		)
	self.pointsSep.addChild(	self.shpObj			)

	self.trans	= SoTranslation(				)
	self.pointsSep.addChild(	self.trans			)
	self.center(			self.ctr			)

	self.fntObj	= SoFont(					)
	self.pointsSep.addChild(	self.fntObj			)
	self.fontSize(			self.fntSize			)

	self.txtObj	= SoText2(					)
	self.pointsSep.addChild(	self.txtObj			)
	self.setText(			self.text			)

	self.setPntListData(		self.pList			)
	self.pointSize(			self.pntSize			)

#-------------------------------------------------------------------------
# _createLine: private function to create a Line
#-------------------------------------------------------------------------

    def _createLine(  self ):
	'''
	   private function to create a line
	'''

	self.lineSep	= SoSeparator(					)
	self.addChild(			self.lineSep			)

	self.material	= SoMaterial(					)
	self.lineSep.addChild(		self.material			)
	self.color(			self.clr			)

	self.drawStyle	= SoDrawStyle(					)
	self.drawStyle.style.setValue(	SoDrawStyle.FILLED		)
	self.drawStyle.linePattern.setValue(
                                        self.lineStyles[ self.lnStyle ] )
	self.lineSep.addChild(		self.drawStyle			)

	self.vertProp	= SoVertexProperty(				)
	self.shpObj	= SoIndexedLineSet(				)
	self.shpObj.vertexProperty.setValue(		self.vertProp	)
	self.lineSep.addChild(		self.shpObj			)

	self.crd	= numarray.zeros( 	shape=(2,3), type='d'	)
	self.cnn	= numarray.arange(  	3, type='i'		)
	self.cnnFlag	= False

	if self.pt1 == None or self.pt2 == None:
	    raise acuSgObjectError, "need two points to draw a line"

	self.trans	= SoTranslation(				)
	self.lineSep.addChild(		self.trans			)

	self.fntObj	= SoFont(					)
	self.lineSep.addChild(		self.fntObj			)
	self.fontSize(			self.fntSize			)

	self.txtObj	= SoText2(					)
	self.lineSep.addChild(		self.txtObj			)
	self.setText(			self.text			)

	self.setLineData(		self.pt1, self.pt2		)

        #----- Misc. 3/07 H2 ; Negar
	#----- changed function Visibility; Navid 6/12/07
	#self.shpObj = self.lineSep

#-------------------------------------------------------------------------
# _createPolyLine: private function to create a PolyLine
#-------------------------------------------------------------------------

    def _createPolyLine(  self ):
	'''
	   private function to create a line
	'''

	self.lineSep	= SoSeparator(					)
	self.addChild(			self.lineSep			)

	self.material	= SoMaterial(					)
	self.lineSep.addChild(		self.material			)
	self.color(			self.clr			)

	self.drawStyle	= SoDrawStyle(					)
	self.drawStyle.style.setValue(	SoDrawStyle.FILLED		)
	self.drawStyle.linePattern.setValue(
                                        self.lineStyles[ self.lnStyle ] )
	self.lineSep.addChild(		self.drawStyle			)

	self.vertProp	= SoVertexProperty(				)
	self.shpObj	= SoIndexedLineSet(				)
	self.shpObj.vertexProperty.setValue(	self.vertProp		)
	self.lineSep.addChild(		self.shpObj			)

	self.trans	= SoTranslation(				)
	self.lineSep.addChild(		self.trans			)
	self.center(			self.ctr			)

	self.fntObj	= SoFont(					)
	self.lineSep.addChild(		self.fntObj			)
	self.fontSize(			self.fntSize			)

	self.txtObj	= SoText2(					)
	self.lineSep.addChild(		self.txtObj			)
	self.lineWidth(                 self.lnw 	                )
	self.setText(			self.text			)
	self.setPntList(		self.pList			)

        #----- Misc. 3/07 H2 ; Negar
	#----- changed function Visibility; Navid 6/12/07
	#self.shpObj = self.lineSep

#-------------------------------------------------------------------------
# _createPntsLine: private function to create a PolyLine
#-------------------------------------------------------------------------

    def _createPntsLine(  self ):
	'''
	   private function to create a line
	'''

	self.lineSep	= SoSeparator(					)
	self.addChild(			self.lineSep			)

	self.material	= SoMaterial(					)
	self.lineSep.addChild(		self.material			)

	self.drawStyle	= SoDrawStyle(					)
	self.drawStyle.style.setValue(	SoDrawStyle.FILLED		)
	self.drawStyle.linePattern.setValue(
                                        self.lineStyles[ self.lnStyle ] )
	self.lineSep.addChild(		self.drawStyle			)

	self.vertProp	= SoVertexProperty(				)
	self.shpObj	= SoIndexedLineSet(				)
	self.shpObj.vertexProperty.setValue(	self.vertProp		)
	self.lineSep.addChild(		self.shpObj			)

	self.trans	= SoTranslation(				)
	self.lineSep.addChild(		self.trans			)
	self.center(			self.ctr			)

	self.fntObj	= SoFont(					)
	self.lineSep.addChild(		self.fntObj			)
	self.fontSize(			self.fntSize			)

	self.txtObj	= SoText2(					)
	self.lineSep.addChild(		self.txtObj			)
	self.setText(			self.text			)
	self.setPntList(		self.pList			)
        #-----
	self.pointsSep	= SoSeparator(					)
	self.addChild(			self.pointsSep			)

	self.pointsSep.addChild(	self.material			)

	self.pointsSep.addChild(	self.drawStyle			)

	self.vertProp	= SoVertexProperty(				)
	self.shpObj	= SoPointSet(				        )
	self.shpObj.vertexProperty.setValue(	self.vertProp		)
	self.pointsSep.addChild(	self.shpObj			)

	self.trans	= SoTranslation(				)
	self.pointsSep.addChild(	self.trans			)
	self.center(			self.ctr			)

	self.fntObj	= SoFont(					)
	self.pointsSep.addChild(	self.fntObj			)
	self.fontSize(			self.fntSize			)

	self.txtObj	= SoText2(					)
	self.pointsSep.addChild(	self.txtObj			)
	self.setText(			self.text			)

	self.setPntListData(		self.pList			)
	self.pointSize(			self.pntSize			)
	self.lineWidth(                 self.lnw 	                )
	self.color(			self.clr			)

#---------------------------------------------------------------------------
# "setVisibility": Set Visibility of actors.
#---------------------------------------------------------------------------

    def setVisibility(  self,   visOption   = 'on'  ):
        ''' set Visibility of actors.'''

        if visOption == 'on':
            self.visibilityOn(                                          )
        else:
            self.visibilityOff(                                         )

#---------------------------------------------------------------------------
# highlight: highlight the actor by their id
#---------------------------------------------------------------------------

    def highlight( self ):
        '''
	    highlight the actor identified by its unique id
	    Arguments:
	        None
	    Output:
	        None
        '''

        self.material.diffuseColor.setValue( 1, 1, 1 )

#---------------------------------------------------------------------------
# unHighlight: highlight the actor by their id
#---------------------------------------------------------------------------

    def unHighlight( self ):
        '''
	    unHighlight the actor identified by its unique id
	    Arguments:
	        None
	    Output:
	        None
        '''

        self.color(             self.clr                )


#---------------------------------------------------------------------------
# lineStyle: change the line styles for the polyline and line or return
#---------------------------------------------------------------------------

    def lineStyle( self, style = None ):
        '''
	    Method to change the line style for the line and polyline.
	    Arguments:
	        style   : The style of line which should be set.
                            "solid", "dash", "dot", ...
	    Output:
	        lineStyle
        '''
        
        retVal  = self.lnStyle

        if style != None:
            self.drawStyle.linePattern.setValue( self.lineStyles[style] )
            self.lnStyle    = style

        return retVal
    
#-------------------------------------------------------------------------
# radius: function to set/get radius of the cylinder, sphere, circle
#-------------------------------------------------------------------------

    def radius( self , r  = None ):
        '''
	    set the radius of the cylinder , circle or a sphere

	    Arguments:
	    	r	-  radius of the cylinder

	    Output:
	    	r	-  current value of the radius
        '''

        retVal	= self.rad

        if r != None:
	    self.rad    = r

	    if self.objType == "sphere" or self.objType == "cylinder":
	        self.shpObj.radius.setValue(		self.rad	)

	    if self.objType == "cone":
	        self.shpObj.bottomRadius.setValue(	self.rad	)

	    if self.objType == "circle":
	        self._buildCircle(		        self.rad	)
	        
        return retVal

#-------------------------------------------------------------------------
# radius: function to set/get height of the cylinder, box or a cone
#-------------------------------------------------------------------------

    def height( self , h = None ):
        '''
	    set the height of the cylinder, box or a cone

	    Arguments:
	    	h	-  height of the cylinder

	    Output:
	    	h	-  current value of the height

        '''

        retVal	= self.ht

        if h != None:
	    self.ht	= h
	    self.shpObj.height.setValue(		self.ht		)

        return retVal

#-------------------------------------------------------------------------
# width: function to set/get width of the box
#-------------------------------------------------------------------------

    def width( self , w = None ):
        '''
	    set the width of the cylinder  or a box

	    Arguments:
	    	w	-  width of the box

	    Output:
	    	w	-  current value of the width
        '''

        retVal	= self.wd

        if w != None:
	    self.wd	= w
	    self.shpObj.width.setValue(			self.wd		)

        return retVal

#-------------------------------------------------------------------------
# depth: function to set/get depth of the box
#-------------------------------------------------------------------------

    def depth( self , d = None ):
        '''
	    set the depth of a box

	    Arguments:
	    	d	-  depth of the box

	    Output:
	    	d	-  current value of the depth
        '''

        retVal	= self.dp

        if d != None:
	    self.dp	= d
	    self.shpObj.depth.setValue(			self.dp		)

        return retVal

#-------------------------------------------------------------------------
# rotateBox: function to rotate the box
#-------------------------------------------------------------------------
    def rotateBox( self, angX, angY, angZ ):
        '''
	    rotate the box by x-degrees, y-degrees and z-degrees

	    Arguments:
	        angX	- rotation about X-Axis in degrees
	        angY	- rotation about Y-Axis in degrees
	        angZ	- rotation about Z-Axis in degrees
        '''
	if self.objType != "box":
	    return

	if angX != None:
	    angX	= angX * math.pi / 180
	    self.boxRotX.angle.setValue(	angX			)
	if angY != None:
	    angY	= angY * math.pi / 180
	    self.boxRotY.angle.setValue(	angY			)
	if angZ != None:
	    angZ	= angZ * math.pi / 180
	    self.boxRotZ.angle.setValue(	angZ			)

#-------------------------------------------------------------------------
# getTransformedPoint: 
#-------------------------------------------------------------------------
    def getTransformedPoint( self, pnt  ):
        '''
        '''
	action	= SoGetMatrixAction(					)
	action.apply(				self			)
	mat	= SbMatrix(						)
	mat	= action.getMatrix(					)
	pt	= SbVec3f( 		pnt[0], pnt[1], pnt[2]		)
	tPnt	= mat.multVecMatrix(		pt			)
	return tPnt


#-------------------------------------------------------------------------
# normal: function to set/get the normal
#          circle, cylinder, triangle
#-------------------------------------------------------------------------

    def normal( self , dir = None ):

        '''
	    set the normal direction for an arrow, cylinder or a circle

	    Arguments:
	    	dir	-  [ dx, dy, dz ]

	    Output:
	    	dir	-  current value of the normal

        '''

	if self.objType != "arrow" or \
		self.objType != "cylinder" or \
		self.objType != "circle" or \
		self.objType != "triangle":
		pass


        retVal	= self.nrm

        if dir != None:
	    if isinstance( dir, SbVec3f ):
	        self.nrm	= dir
	    else:
	        self.nrm	= SbVec3f(	dir[0],dir[1],dir[2]	)


	    if self.objType == "arrow":

	        nx, ny, nz	= self.nrm.getValue(			)

	        if self.ptCal == "pt1":
		    self.pt1	= [ 0, 0, 0 ]
	            self.pt1[0]	= self.pt2[0] - self.arrowLen * nx
	            self.pt1[1]	= self.pt2[1] - self.arrowLen * ny
	            self.pt1[2]	= self.pt2[2] - self.arrowLen * nz

	        else:
		    self.pt2	= [ 0, 0, 0 ]
	            self.pt2[0]	= self.pt1[0] + self.arrowLen * nx
	            self.pt2[1]	= self.pt1[1] + self.arrowLen * ny
	            self.pt2[2]	= self.pt1[2] + self.arrowLen * nz

		x	= self.pt2[0] - self.pt1[0]
		y	= self.pt2[1] - self.pt1[1]
		z	= self.pt2[2] - self.pt1[2]
		mag	= math.sqrt(		x*x + y*y + z*z		)
		self.arrowLen	= mag
		rad			= mag / 15
		ht			= mag / 10
		self.arrowHead.bottomRadius.setValue(	rad		)
		self.arrowHead.height.setValue(		ht		)
		self.setLineData(	self.pt1, self.pt2		)

	    tmpRot	= SbRotation(  self.prvNrm, self.nrm		)
	    q1,q2,q3,q4 = tmpRot.getValue(				)
	    self.rot.rotation.setValue(		q1,q2,q3,q4		)

        return retVal

#-------------------------------------------------------------------------
# center: function to set/get the center
#-------------------------------------------------------------------------

    def center( self , ctr = None ):

        '''
	    set the center of the object

	    Arguments:
	    	ctr	-  [ ctrx, ctry, ctrtz ]

	    Output:
	    	ctr	-  current value of the origin

        '''

	if self.objType != "cylinder" or \
		self.objType != "sphere" or \
		self.objType != "cube" or \
		self.objType != "tet" or \
		self.objType != "circle":
		pass

        retVal	    = self.ctr

	if ctr != None:
	    if isinstance( ctr, SbVec3f ):
	        self.ctr	= ctr
	    else:
	        self.ctr	= SbVec3f(	ctr[0],ctr[1],ctr[2]	)
            
            self.trans.translation.setValue(	self.ctr		)

        return retVal

#-------------------------------------------------------------------------
# setTriangleData: function to set the triangle data
#-------------------------------------------------------------------------

    def setTriangleData( self , size  = None ):
        '''
	    set the size of the triangle

	    Arguments:
	    	size	-  size of the side of equilateral triangle

	    Output:
	    	size	-  size of the side of equilateral triangle
        '''

        retVal	= self.triSize

        if size != None:
	    self.triSize	= size
	    h			= 1.7320508075688772 * 0.5 * size

	    self.crd[0][0]	= 0.0
	    self.crd[0][1]	= 0.0
	    self.crd[0][2]	= 2.0 * h / 3.0

	    self.crd[1][0]	= -0.5 * size
	    self.crd[1][1]	= 0.0
	    self.crd[1][2]	= -1.0 * h / 3.0

	    self.crd[2][0]	= 0.5 * size
	    self.crd[2][1]	= 0.0
	    self.crd[2][2]	= -1.0 * h / 3.0

            if not self.cnnFlag:
	        self.cnn[0]	= 0
	        self.cnn[1]	= 1
	        self.cnn[2]	= 2
	        self.cnn[3]	= -1
		self.cnnFlag	= True
	        self.shpObj.coordIndex.setValues(	0,	self.cnn)
	    self.vertProp.vertex.setValues(		0, 	self.crd)

        return retVal

#-------------------------------------------------------------------------
# setTetData: function to set the tet data
#-------------------------------------------------------------------------

    def setTetData( self , size  = None ):
        '''
	    set the size of the tet

	    Arguments:
	    	size	-  size of the side of equilateral triangle

	    Output:
	    	size	-  size of the side of equilateral triangle
        '''

        retVal	= self.tetSize

        if size != None:

	    self.tetSize	= size
	    h			= 1.7320508075688772 * 0.5 * size

	    self.crd[0][0]	= 0.0
	    self.crd[0][1]	= 0.0
	    self.crd[0][2]	= 2.0 * h / 3.0

	    self.crd[1][0]	= -0.5 * size
	    self.crd[1][1]	= 0.0
	    self.crd[1][2]	= -1.0 * h / 3.0

	    self.crd[2][0]	= 0.5 * size
	    self.crd[2][1]	= 0.0
	    self.crd[2][2]	= -1.0 * h / 3.0

	    self.crd[3][0]	= 0.0
	    self.crd[3][1]	= 0.5 * size
	    self.crd[3][2]	= 0.0

            if not self.cnnFlag:
	        self.cnn[0]	= 0
	        self.cnn[1]	= 1
	        self.cnn[2]	= 2
	        self.cnn[3]	= -1

	        self.cnn[4]	= 0
	        self.cnn[5]	= 2
	        self.cnn[6]	= 3
	        self.cnn[7]	= -1

	        self.cnn[8]	= 0
	        self.cnn[9]	= 3
	        self.cnn[10]	= 1
	        self.cnn[11]	= -1

	        self.cnn[12]	= 1
	        self.cnn[13]	= 2
	        self.cnn[14]	= 3
	        self.cnn[15]	= -1

		self.cnnFlag	= True
	        self.shpObj.coordIndex.setValues(	0,	self.cnn)
	    self.vertProp.vertex.setValues(		0, 	self.crd)

#-------------------------------------------------------------------------
# setText: function to set the text that goes along with objects
#-------------------------------------------------------------------------

    def setText( self , txt  = None ):
        '''
	    Arguments:
	    	txt	-  2D text string

	    Output:
	    	txt	-  2D text string
        '''

	retVal	= self.text

	if txt != None:
	    self.text	= txt
	    self.txtObj.string.setValue(		txt		)

        return retVal

#-------------------------------------------------------------------------
# fontSize: function to set the font size of the text
#-------------------------------------------------------------------------

    def fontSize( self , size  = None ):
        '''
	    Arguments:
	    	size	-  font size

	    Output:
	    	size	-  font size
        '''

	retVal	= self.fntSize

	if size != None:
	    self.fntSize	= size
	    self.fntObj.size.setValue(			size		)

        return retVal

#-------------------------------------------------------------------------
# color: function to set the color of the text
#-------------------------------------------------------------------------

    def color( self , clr = None ):

        '''
	    set the color of the object
	    Arguments:
	    Output:
        '''

        retVal	= self.clr

	if clr != None:
	    self.clr	= clr
	    self.material.diffuseColor.setValue( clr[0], clr[1], clr[2]	)
        return retVal

#-------------------------------------------------------------------------
# pointSize: function to set the point size
#-------------------------------------------------------------------------

    def pointSize( self , size ):

        retVal	= self.pntSize

	if size != None:
	    self.pntSize	= size
	    self.drawStyle.pointSize.setValue( 		self.pntSize 	)
        return retVal

#-------------------------------------------------------------------------
# lineWidth: function to set/get the linewidth
#-------------------------------------------------------------------------

    def lineWidth( self , width = None  ):

        '''
		set the width of the box
        '''

        retVal	= self.lnw

	if width != None:
	    self.lnw	= width
	    self.drawStyle.lineWidth.setValue( 	self.lnw 	)
        return retVal

#-------------------------------------------------------------------------
# show: show the object
#-------------------------------------------------------------------------

    def show( self ):
        '''
	    show the object
        '''

	self.drawStyle.style.setValue(		SoDrawStyle.FILLED	)	

#-------------------------------------------------------------------------
# hide: hide the object
#-------------------------------------------------------------------------

    def hide( self ):
        '''
	    hide the object
        '''

	self.drawStyle.style.setValue(		SoDrawStyle.INVISIBLE	)	

#-------------------------------------------------------------------------
# isShown: 
#-------------------------------------------------------------------------

    def isShown( self ):
        ''' A function to get the visibility of geom.

            Argument:
                None

            Output:
                retVal  - True / False

        '''

        if self.drawStyle.style.getValue() == SoDrawStyle.INVISIBLE:
            return False

        return True

#-------------------------------------------------------------------------
# _buildCircle: private function to build the circle object
#-------------------------------------------------------------------------


    def _buildCircle( self , radius ):
        '''
	   private function to build a circle by creating points
	   along the circumference
	'''

	theta	= 0.0
	angInc	= 2 * math.pi / self.nPts

	for i in range( self.nPts ):
	    self.crd[i][0]	= radius * math.cos(	theta 		)
	    self.crd[i][1]	= 0.0
	    self.crd[i][2]	= radius * math.sin( 	theta 		)
	    theta	+= angInc

        if not self.cnnFlag:
	    for i in range( self.nPts-2 ):
	        self.cnn[4*i]	= 0
	        self.cnn[4*i+1]	= i + 1
	        self.cnn[4*i+2]	= i + 2
	        self.cnn[4*i+3]	= -1

	    self.cnn[4*(self.nPts-2)]	= self.nPts - 2
	    self.cnn[4*(self.nPts-2)+1]	= self.nPts - 1
	    self.cnn[4*(self.nPts-2)+2]	= 0
	    self.cnn[4*(self.nPts-2)+3]	= -1

	    self.cnnFlag	= True

	    self.shpObj.coordIndex.setValues(	0,	self.cnn	)
	self.vertProp.vertex.setValues(		0, 	self.crd	)

#-------------------------------------------------------------------------
# setPointData: function to set the point data
#-------------------------------------------------------------------------

    def setPointData( self , pt	):
        '''
	    function to draw a point
	'''

	self.crd[0][0]	= pt[0]
	self.crd[0][1]	= pt[1]
	self.crd[0][2]	= pt[2]
	self.vertProp.vertex.setValues(		0, 	self.crd	)
	self.trans.translation.setValue(    SbVec3f(pt[0],pt[1],pt[2])	)

#-------------------------------------------------------------------------
# setPntListData: function to set the list of points 
#-------------------------------------------------------------------------

    def setPntListData( self , pList ):
        '''
	    private function to draw points
	'''

	if isinstance( pList, numarray.numarraycore.NumArray ):
	    self.nPoints, self.nVals	= pList.shape
	else:
	    self.nPoints	= len( 		pList 		        )
	    if self.nPoints > 0:
	        self.nVals	= len(		pList[0]	        )

	if self.nPoints < 1 or self.nVals != 3:
	    raise acuSgObjectError, \
	    	"Need at least one point and 3 coords per point."

        self.shpObj.numPoints.setValue(	        self.nPoints		)
        
	self.crd	= []
	self.crd	= numarray.zeros( shape=(self.nPoints,3), type='d')

	for i in range( self.nPoints ):
	    self.crd[i][0]	= pList[i][0]
	    self.crd[i][1]	= pList[i][1]
	    self.crd[i][2]	= pList[i][2]

	self.vertProp.vertex.setValues(		0, 	self.crd	)
	ctr	= SbVec3f(	pList[0][0],pList[0][1],pList[0][2]	)
	self.trans.translation.setValue(   		ctr		)

#-------------------------------------------------------------------------
# setLineData: function to set the line data
#-------------------------------------------------------------------------

    def setLineData( self , pt1, pt2 ):
        '''
	    function to draw a line between two points
	'''

	self.crd[0][0]	= pt1[0]
	self.crd[0][1]	= pt1[1]
	self.crd[0][2]	= pt1[2]

	self.crd[1][0]	= pt2[0]
	self.crd[1][1]	= pt2[1]
	self.crd[1][2]	= pt2[2]

        if not self.cnnFlag:

	    self.cnn[0]		= 0
	    self.cnn[1]		= 1
	    self.cnn[2]		= -1
	    self.cnnFlag	= True
	    self.shpObj.coordIndex.setValues(	0,	self.cnn	)

	self.vertProp.vertex.setValues(		0, 	self.crd	)

	ctr	= SbVec3f(		pt2[0], pt2[1], pt2[2] 		)
	self.trans.translation.setValue(   		ctr		)

#-------------------------------------------------------------------------
# setLineDataAxes: function to set the line data
#-------------------------------------------------------------------------

    def setLineDataAxes( self , pt1, pLst ):
        '''
	    function to draw a line between two points
	'''

        #----------------------------------------------------------------
        # draw xAxis line
        #----------------------------------------------------------------
        
	self.xCrd[0][0]	= pt1[0]
	self.xCrd[0][1]	= pt1[1]
	self.xCrd[0][2]	= pt1[2]
	self.xCrd[1][0]	= pLst[0][0]
	self.xCrd[1][1]	= pLst[0][1]
	self.xCrd[1][2]	= pLst[0][2]

        if not self.xCnnFlag:
	    self.xCnn[0]= 0
	    self.xCnn[1]= 1
	    self.xCnn[2]= -1
	    self.xCnnFlag= True
	    self.xShpObj.coordIndex.setValues(	0,	self.xCnn	)

	self.xVp.vertex.setValues(		0, 	self.xCrd	)

	ctr	= SbVec3f(		        pLst[0][0],
                                                pLst[0][1], pLst[0][2] 	)
	self.transX.translation.setValue(   	ctr		        )

        #----------------------------------------------------------------
        # draw yAxis line
        #----------------------------------------------------------------
        
	self.yCrd[0][0]	= pt1[0]
	self.yCrd[0][1]	= pt1[1]
	self.yCrd[0][2]	= pt1[2]
	self.yCrd[1][0]	= pLst[1][0]
	self.yCrd[1][1]	= pLst[1][1]
	self.yCrd[1][2]	= pLst[1][2]

        if not self.yCnnFlag:
	    self.yCnn[0]= 0
	    self.yCnn[1]= 1
	    self.yCnn[2]= -1
	    self.yCnnFlag= True
	    self.yShpObj.coordIndex.setValues(	0,	self.yCnn	)

	self.yVp.vertex.setValues(		0, 	self.yCrd	)

	ctr	= SbVec3f(		        pLst[1][0],
                                                pLst[1][1], pLst[1][2] 	)
	self.transY.translation.setValue(   	ctr		        )

        #----------------------------------------------------------------
        # draw zAxis line
        #----------------------------------------------------------------
        
	self.zCrd[0][0]	= pt1[0]
	self.zCrd[0][1]	= pt1[1]
	self.zCrd[0][2]	= pt1[2]
	self.zCrd[1][0]	= pLst[2][0]
	self.zCrd[1][1]	= pLst[2][1]
	self.zCrd[1][2]	= pLst[2][2]

        if not self.zCnnFlag:
	    self.zCnn[0]= 0
	    self.zCnn[1]= 1
	    self.zCnn[2]= -1
	    self.zCnnFlag= True
	    self.zShpObj.coordIndex.setValues(	0,	self.zCnn	)

	self.zVp.vertex.setValues(		0, 	self.zCrd	)

	ctr	= SbVec3f(		        pLst[2][0],
                                                pLst[2][1], pLst[2][2] 	)
	self.transZ.translation.setValue(   	ctr		        )

#-------------------------------------------------------------------------
# setPntList: function to set the list of points for a poly line
#-------------------------------------------------------------------------

    def setPntList( self , pList ):
        '''
	    private function to draw a polyline
	'''

	if pList == None:
	    raise acuSgObjectError, \
	    	"need atleat two points to draw a polyline"

	if isinstance( pList,numarray.numarraycore.NumArray ):
	    self.nPoints, self.nVals	= pList.shape
	else:
	    self.nPoints	= len( 			pList 		)
	    if self.nPoints > 0:
	        self.nVals	= len(			pList[0]	)

	if self.nPoints < 2 or self.nVals != 3:
	    raise acuSgObjectError, \
	    	"need two points and 3 coords per point for a polyline "

	self.crd	= []
	self.cnn	= []

	self.crd	= numarray.zeros( shape=(self.nPoints,3), type='d')
	self.cnn	= numarray.arange( 3*(self.nPoints-1), type='i'	)

	for i in range( self.nPoints ):
	    self.crd[i][0]	= pList[i][0]
	    self.crd[i][1]	= pList[i][1]
	    self.crd[i][2]	= pList[i][2]

	for i in range( self.nPoints - 2 ):
	    self.cnn[3*i]	= i
	    self.cnn[3*i+1]	= i+1
	    self.cnn[3*i+2]	= -1

	self.cnn[3*(self.nPoints-2)]	= self.nPoints-2
	self.cnn[3*(self.nPoints-2)+1]	= self.nPoints-1
	self.cnn[3*(self.nPoints-2)+2]	= -1

	self.shpObj.coordIndex.setValues(	0,	self.cnn	)
	self.vertProp.vertex.setValues(		0, 	self.crd	)
	ctr	= SbVec3f(	pList[0][0],pList[0][1],pList[0][2]	)
	self.trans.translation.setValue(   		ctr		)

#-------------------------------------------------------------------------
# _drawArrowHead: private function to draw the arrow head
#-------------------------------------------------------------------------

    def _drawArrowHead( self , pt1, pt2 ):
        '''
	    private function to draw the cone representing arrow head
	'''


	if pt1[0] == pt2[0] and pt1[1] == pt2[1] and pt1[2] == pt2[2]:
	    raise acuSgObjectError, "cannot draw arrow head "

	x,y,z	= pt2[0] - pt1[0], pt2[1] - pt1[1], pt2[2] - pt1[2]
	mag	= math.sqrt(		x*x + y*y + z*z			)
	self.arrowLen	= mag
	self.nrm= SbVec3f( 	x / mag, y / mag , z / mag 		)

	self.trans	= SoTranslation(				)
	self.arrowSep.addChild(		self.trans			)
	self.rot	= SoRotation(					)
	self.arrowSep.addChild(		self.rot			)
	self.arrowHead	= SoCone(					)
	self.arrowSep.addChild(		self.arrowHead			)
	rad			= mag / 15
	ht			= mag / 10
	self.arrowHead.bottomRadius.setValue(	rad			)
	self.arrowHead.height.setValue(		ht			)
	
	tmpRot	= SbRotation(  		self.prvNrm, self.nrm		)
	q1,q2,q3,q4 = tmpRot.getValue(					)
	self.rot.rotation.setValue(		q1,q2,q3,q4		)

#-------------------------------------------------------------------------
# _drawArrowHeadAxes: private function to draw the axes head
#-------------------------------------------------------------------------

    def _drawArrowHeadAxes( self , pt1, pList ):
        '''
	    private function to draw the cone representing arrow head
	'''

        #----------------------------------------------------------------
        # xAxis arrow head
        #----------------------------------------------------------------
        
	xX,yX,zX        = pList[0][0]-pt1[0], pList[0][1]-pt1[1],pList[0][2]-pt1[2]
	magX            = math.sqrt(	xX*xX + yX*yX + zX*zX		)
	self.axesXLen   = magX
	self.nrmX       = SbVec3f( 	xX / magX, yX / magX , zX / magX)

	self.transX	= SoTranslation(				) 
	self.axesSepX.addChild(		self.transX			)
	self.rotX	= SoRotation(					)
	self.axesSepX.addChild(		self.rotX			)
	self.axesHeadX	= SoCone(					)
	self.axesSepX.addChild(		self.axesHeadX			)
	rad			= magX / 15
	ht			= magX / 10
	self.axesHeadX.bottomRadius.setValue(	rad			)
	self.axesHeadX.height.setValue(		ht			)
	
	tmpRot	= SbRotation(  		self.prvNrm, self.nrmX		)
	q1,q2,q3,q4 = tmpRot.getValue(					)
	self.rotX.rotation.setValue(		q1,q2,q3,q4		)

        #----------------------------------------------------------------
        # yAxis arrow head
        #----------------------------------------------------------------
        
	xY,yY,zY        = pList[1][0]-pt1[0], pList[1][1]-pt1[1],pList[1][2]-pt1[2]
	magY            = math.sqrt(	xY*xY + yY*yY + zY*zY		)
	self.axesYLen   = magY
	self.nrmY       = SbVec3f( 	xY / magY, yY / magY , zY / magY)

	self.transY	= SoTranslation(				) 
	self.axesSepY.addChild(		self.transY			)
	self.rotY	= SoRotation(					)
	self.axesSepY.addChild(		self.rotY			)
	self.axesHeadY	= SoCone(					)
	self.axesSepY.addChild(		self.axesHeadY			)
	rad			= magY / 15
	ht			= magY / 10
	self.axesHeadY.bottomRadius.setValue(	rad			)
	self.axesHeadY.height.setValue(		ht			)
	
	tmpRot	= SbRotation(  		self.prvNrm, self.nrmY		)
	q1,q2,q3,q4 = tmpRot.getValue(					)
	self.rotY.rotation.setValue(		q1,q2,q3,q4		)

        #----------------------------------------------------------------
        # zAxis arrow head
        #----------------------------------------------------------------
        
	xZ,yZ,zZ        = pList[2][0]-pt1[0], pList[2][1]-pt1[1],pList[2][2]-pt1[2]
	magZ            = math.sqrt(	xZ*xZ + yZ*yZ + zZ*zZ		)
	self.axesZLen   = magZ
	self.nrmZ       = SbVec3f( 	xZ / magZ, yZ / magZ , zZ / magZ)

	self.transZ	= SoTranslation(				) 
	self.axesSepZ.addChild(		self.transZ			)
	self.rotZ	= SoRotation(					)
	self.axesSepZ.addChild(		self.rotZ			)
	self.axesHeadZ	= SoCone(					)
	self.axesSepZ.addChild(		self.axesHeadZ			)
	rad			= magZ / 15
	ht			= magZ / 10
	self.axesHeadZ.bottomRadius.setValue(	rad			)
	self.axesHeadZ.height.setValue(		ht			)
	
	tmpRot	= SbRotation(  		self.prvNrm, self.nrmZ		)
	q1,q2,q3,q4 = tmpRot.getValue(					)
	self.rotZ.rotation.setValue(		q1,q2,q3,q4		)

#-------------------------------------------------------------------------
# delete: function to delete the object
#-------------------------------------------------------------------------

    def delete(	self ):
        ''' function to delete the object '''

	self.removeAllChildren(						)

#---------------------------------------------------------------------------
# visibility: set/get the visibility of the actor
#---------------------------------------------------------------------------

    def visibility( self, vis = None ):
        '''
	    Function to set the color of the actor

	    Arguments:
	        vis		- True / False

	    Output: ( only if r,g,b input is equal to None )
	'''
        
	retVal	= self.visFlg

        if vis != None:
	    self.visFlg	= vis
	return retVal

#---------------------------------------------------------------------------
# "toggleVisibility" : Toggle Visibility of actor.
#---------------------------------------------------------------------------

    def toggleVisibility( self ):
        ''' Toggle Visibility of actor.'''

        if self.visibility():
            self.visibilityOff(                                         )
        else:
            self.visibilityOn(                                          )

#---------------------------------------------------------------------------
# "visibilityOff" : Set visibility of actor.
#---------------------------------------------------------------------------

    def visibilityOff( self ):
        ''' Set actor invisible.'''

        if self.objType in [ "line" , "polyline" ]:
            if self.findChild( self.lineSep 	) != -1:
                self.removeChild(	    self.lineSep		)

        elif self.objType == "points":
            if self.findChild( self.pointsSep   ) != -1:
                self.removeChild(           self.pointsSep              )

        elif self.objType == "pointsLine" :
            if self.findChild( self.lineSep     ) != -1:
                self.removeChild(           self.lineSep                )
            if self.findChild( self.pointsSep   ) != -1:
                self.removeChild(           self.pointsSep              )

	elif self.findChild( self.shpObj ) != -1:
	    self.removeChild(		    self.shpObj			)

        self.visibility(                    False                       )

#---------------------------------------------------------------------------
# "visibilityOn" : Set visibility of actor.
#---------------------------------------------------------------------------

    def visibilityOn( self ):
        ''' Set actor visible.'''

        self.visibility(                    True                        )

        if self.objType in [ "line" , "polyline" ]:
            if self.findChild( self.lineSep 	) == -1:
                self.addChild(		    self.lineSep		)

        elif self.objType == "points":
            if self.findChild( self.pointsSep   ) == -1:
                self.addChild(              self.pointsSep              )

        elif self.objType == "pointsLine" :
            if self.findChild( self.lineSep     ) == -1:
                self.addChild(              self.lineSep                )
            if self.findChild( self.pointsSep   ) == -1:
                self.addChild(              self.pointsSep              )
        
	elif self.findChild( self.shpObj 	) == -1:
	    self.addChild(		    self.shpObj			)

#---------------------------------------------------------------------------
# transparency: set/get the transparency
#---------------------------------------------------------------------------

    def transparency( self, trans = None ):
        '''
	    Function to set the trnasparenty of the actor

	    Arguments:
	        trans		- True / False

	    Output: ( True/False input is equal to None )
	'''

	retVal	= self.transFlg

        if trans != None:
	    self.transFlg	= trans
        return retVal

#---------------------------------------------------------------------------
# transparencyVal: set/get the transparency value of the actor
#---------------------------------------------------------------------------

    def transparencyVal( self, value = None ):
        '''
	    Function to set transparency to value

	    Arguments:
	        value		- set the transparency value (0-1)

	    Output: ( only if value input is equal to None )
	        value		- current transparency value (0-1)
        '''
        
	retVal	= self.transValue

	if value != None:
	    if value < 0.0 or value > 1.0:
		raise acuSgObjectError, \
			"transparency values should be between 0 and 1 "
	    else:
		self.material.transparency.setValue( 	value		)
		self.transValue	= value
	return retVal

#---------------------------------------------------------------------------
# "toggleTransparency" : Toggle transparency of actor.
#---------------------------------------------------------------------------

    def toggleTransparency( self ):
        ''' Toggle transparency of actor.'''

        if self.transparency():
            self.transparencyOff(                                       )
        else:
            self.transparencyOn(                                        )

#---------------------------------------------------------------------------
# "transparencyOff" : Set transparency of actor.
#---------------------------------------------------------------------------

    def transparencyOff( self ):
        ''' Set actor invisible.'''

        self.material.transparency.setValue( 	        0.0		)
        self.transparency(                              False           )

#---------------------------------------------------------------------------
# "transparencyOn" : Set transparency of actor.
#---------------------------------------------------------------------------

    def transparencyOn( self ):
        ''' Set actor visible.'''

        self.transparency(                              True            )
        self.material.transparency.setValue( 	        self.transValue	)

#************************** For MeshZone ***********************************
#***************************************************************************

#-------------------------------------------------------------------------
# setQuadData: function to set the quad data
#-------------------------------------------------------------------------

    def setQuadData( self , points ):
            '''
                set the size of the triangle

                Arguments:
                    size	-  size of the side of equilateral triangle

                Output:
                    size	-  size of the side of equilateral triangle
            '''

	    self.crd[0][0]	= points[0][0]
	    self.crd[0][1]	= points[0][1]
	    self.crd[0][2]	= points[0][2]

	    self.crd[1][0]	= points[1][0]
	    self.crd[1][1]	= points[1][1]
	    self.crd[1][2]	= points[1][2]

	    self.crd[2][0]	= points[2][0]
	    self.crd[2][1]	= points[2][1]
	    self.crd[2][2]	= points[2][2]

	    self.crd[3][0]	= points[3][0]
	    self.crd[3][1]	= points[3][1]
	    self.crd[3][2]	= points[3][2]	    

            if not self.cnnFlag:
	        self.cnn[0]	= 0
	        self.cnn[1]	= 1
	        self.cnn[2]	= 2
	        self.cnn[3]	= 3
		self.cnnFlag	= True
	        self.qudObj.coordIndex.setValues(	0,	self.cnn)
	    self.vertProp.vertex.setValues(		0, 	self.crd)

#-------------------------------------------------------------------------
# _createQuade: 
#-------------------------------------------------------------------------

    def _createQuade(  self , points ):
	'''
	   private function to create a triangle
	'''

        if not self.shpObj:
            self.shpObj    = SoSeparator(			        )
            self.addChild(	                        self.shpObj	)

	self.shHints	= SoShapeHints(					)
	self.shHints.vertexOrdering.setValue( SoShapeHints.CLOCKWISE	)
	self.shHints.shapeType.setValue(SoShapeHints.UNKNOWN_SHAPE_TYPE	)
	self.shpObj.addChild(		self.shHints			)

	self.vertProp	= SoVertexProperty(				)
	self.qudObj	= SoIndexedFaceSet(				)
	self.qudObj.vertexProperty.setValue(		self.vertProp	)
	self.shpObj.addChild(		    self.qudObj			)

	self.crd	= numarray.zeros( shape=(4,3), type='d'		)
	self.cnn	= numarray.arange(  	4, type='i'		)
	self.cnnFlag	= False
	self.setQuadData(               points                          )
    	self.normal( 			self.nrm			)

    	return self.shHints

#-------------------------------------------------------------------------
# _createBrick: 
#-------------------------------------------------------------------------

    def _createBrick(  self , points ):
	'''
	   private function to create a triangle
	'''

        p1  = points[0]
        p2  = points[1]
        p3  = points[2]
        p4  = points[3]
        
        Q1 = p1
        Q2 = p2
        Q3 = [ 0, 0, 0 ]
        Q4 = [ 0, 0, 0 ]
        Q5 = [ 0, 0, 0 ]
        Q6 = [ 0, 0, 0 ]
        Q7 = [ 0, 0, 0 ]
        Q8 = [ 0, 0, 0 ]
        
        d1  = self.norm(        Q2,     Q1  )
        r   = self.dotProduct(  p3 ,    d1  )

        for i in range( 3 ):

            Q3[i] = p3[i] - r * d1[i]
            Q4[i] = Q2[i] + Q3[i] - Q1[i]
            
        d2  = self.norm(        Q3,     Q1 )
        
        r1  = self.dotProduct(  p4 ,    d1 )
        r2  = self.dotProduct(  p4 ,    d2 )

        for i in range( 3 ):
            Q5[i] = p4[i] - (r1 * d1[i]) - (r2 * d2[i])
            Q6[i] = Q5[i] + Q2[i] - Q1[i]
            Q7[i] = Q5[i] + Q3[i] - Q1[i]
            Q8[i] = Q5[i] + Q4[i] - Q1[i]

	self.shpObj    = SoSeparator(			)
	

        self._createQuade(      ( Q1, Q2, Q4, Q3 )      )
        self._createQuade(      ( Q5, Q6, Q8, Q7 )      )
        self._createQuade(      ( Q1, Q3, Q7, Q5 )      )
        self._createQuade(      ( Q2, Q1, Q5, Q6 )      )
        self._createQuade(      ( Q4, Q2, Q6, Q8 )      )
        self._createQuade(      ( Q3, Q4, Q8, Q7 )      )

        self.addChild(	        self.shpObj		)
        
#-------------------------------------------------------------------------
# norm: 
#-------------------------------------------------------------------------

    def norm( self, p1, p2 ):

        p3 = ( p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2] )
        r  = math.sqrt( p3[0]*p3[0] + p3[1]*p3[1] + p3[2]*p3[2] )
        if r== 0 :
            return
        return ( p3[0]/r , p3[1]/r ,p3[2]/r )

    
#-------------------------------------------------------------------------
# dotProduct: 
#-------------------------------------------------------------------------

    def dotProduct( self, p1 , p2 ):

        result = 0
        for i in range( 3 ):
            result += p1[i]*p2[i]
        return result
             
#****************************************************************************
#************************** For MeshZone ************************************

#---------------------------------------------------------------------------
# Test
#---------------------------------------------------------------------------

if __name__ == '__main__':
    from	acuSgViewer	import	AcuSgViewer
    import  sys
    import	acuQt

    myWindow	= SoQt.init(	sys.argv[0]				)
    if not myWindow:
    	sys.exit(							)

    root	= SoSeparator(						)

    acuQt.initSettings(			'AcuConsole'			)

    rad		= 4
    height	= 10
    center	= [0,15,0]

    x,y,z	= 0,1,0
    mag		= math.sqrt( x*x + y*y + z*z )
    normal	= [ x/mag,y/mag,z/mag ]

    pnt0	= [0,0,0]
    pnt1	= [0,10,0]
    pntList	= [ [-10,-20,0], [-20,-30,0], [-10,-40,0], [0,-20,0] ]

    '''
    
    for i in range( 30 ):
        mag	= abs( 100 - i * i * 0.1 ) * 0.1
	b	= abs( 10 - 0.9*mag )
	r	= abs( mag * 0.5 )
	if i < 10:
	    g	= r * 0.5
	else:
	    g	= r * 1.5
	nm	= math.sqrt( r*r + b*b + g*g )
	color	= [ r / nm, g / nm, b / nm ]
	
        obj	= AcuSgObject(	type	= "arrow",
				point1	= [1,i,0],
				normal	= [1,0,0],
				color	= color,
                                arrowLength = mag   )#My changes
				#arrowLen= mag				)

        root.addChild(				obj			)

    '''
    point	= AcuSgObject(	type	= "point",
    				text	= "POINT",
    				fontSize	= 20,
    				pointSize	= 10,
				point	= [ 0,0,0]			)

    root.addChild(			point				)

    triangle	= AcuSgObject(	type	= "triangle",
    				center	= [30,10,10],
				text	= "TRIANGLE",
				vis	= True,
    				normal	= [0,0,1],
    				triSize	= 10				)
    root.addChild(			triangle			)

    tet		= AcuSgObject(	type	= "tet",
    				text	= "TET",
    				center	= [30,-20,10],
    				color	= [0.0,0.3,1.0],
				vis	= True,
    				tetSize	= 15				)
    root.addChild(			tet				)

    text	= AcuSgObject(	type	= "text",
				text	= "ACUSIM SOFTWARE INC",
				fontSize	= 24.0,
				color	= [1,0,0],
				center	= [30,50,10]			)
    root.addChild(			text				)

    line	= AcuSgObject(	type	= "line",
				text	= "LINE",
				lineWidth	= 3,
				vis	= True,
				point1	= [-25,10,0],
				point2	= [-30,0,10]			)

    root.addChild(			line				)

    polyline	= AcuSgObject(	type	= "polyline",
				text	= "polyline",
				lineWidth	= 3,
				color	= [ 0.1, 1, 0.2 ],
				vis	= True,
				pntList	= pntList			)
    root.addChild(			polyline			)

    circle	= AcuSgObject(	type	= "circle",
				text	= "CIRCLE",
    				radius	= rad,
				vis	= True,
				center	= [-10,-5,0],
				color	= [ 0.5, 0.9 , 0],
				normal	= [0,0,1]  			)
    root.addChild(			circle				)

    cylinder	= AcuSgObject(	type	= "cylinder",
    				radius	= 4,
    				height	= 4,
				vis	= True,
    				text	= "CYLINDER",
				center	= [-15,20,0],
				color	= [ 0,0,1],
				normal	= [1,0,0]  			)
    root.addChild(			cylinder			)

    sphere	= AcuSgObject(	type	= "sphere",
    				radius	= 4,
    				text	= "SPHERE",
				vis	= True,
				center	= [-35,-5,0]  			)
    root.addChild(			sphere				)

    arrow	= AcuSgObject(	type	= "arrow",
    				text	= "arrow",
				vis	= True,
				point1	= [-20,0,0],
				point2	= [-20,15,0]  			)

    root.addChild(			arrow				)

    box		= AcuSgObject(	type	= "box",
    				text	= "box",
				vis	= True,
				center	= [20,20,20],
				color	= [0.8,0.5,0.2],
				height	= 5,
				width	= 5,
				depth	= 5				)
    root.addChild(			box				)
    box.delete()

    points	= AcuSgObject(	type	= "points",
				text	= "points",
				pointSize= 3,
				color	= [ 1, 1, 0.2 ],
                                vis     = True,
				pntList	= pntList			)
    root.addChild(		points			                )
    
    axes	= AcuSgObject(	type	= "axes",
    				text	= "axes",
                                color   = [1,1,0],
				point1	= [0,0,0],
                                vis     = True                          )

    root.addChild(		axes				        )

    myViewer	= AcuSgViewer(			myWindow		)
    myViewer.color(		0, 0.5, 0.5				)
    myViewer.setSceneGraph(			root			)
    myViewer.show(							)
    camera	= myViewer.getCamera(					)
    camera.viewAll(		root,myViewer.getViewportRegion()	)
    SoQt.show(			myWindow				)
    SoQt.mainLoop(							)
