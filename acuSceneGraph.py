#===========================================================================
#
# Include files
#
#===========================================================================

import  sys
import  numarray
import  types
import	acuQt
import	qt
import  math
import  gzip
import  os
import  string
import  time

from    iv      	import	*
from    acuSgActor	import	AcuSgActor
from    acuSgTform	import	AcuSgTform
from    acuSgObject	import	AcuSgObject
from    acuSgCPlane	import	AcuSgCPlane
from    acuCmap         import  AcuCmap

from    acuSgCmapLegend import  AcuSgCmapLegend
from    acuSgClipShape  import  AcuSgClipShape

# Pyrex - acuhdf : Task 2
from    acuUtil         import  str

import  acuSgViewer
import  acuConvertU3D

TRUE    = 1
True    = 1
FALSE   = 0
False   = 0

SO_SWITCH_NONE	= -1
SO_SWITCH_ALL	= -3

#===========================================================================
#
# Errors
#
#===========================================================================

acuSceneGraphError   = "ERROR from acuSceneGraphError module"

#===========================================================================
#
# "AcuSceneGraph": Scene graph
#
#===========================================================================

class AcuSceneGraph:

    '''
	Top level class to create Coin/SoQt related objects to
	create a graphical window and add actors to it. The actors
	can be 3D, 2D, 1D or 0D AcuSolve Mesh objects.
    '''

    def __init__( self, parent, settingObj ):
        '''

	    Argument:
	        parent		- parent holding acuSceneGraph viewer object
		                  In AcuConsole it is the hBox.
		settingObj	- settingObj has information about user
		                  settings for the graphical window

	    This class has to be appropriately modified to account for
	    the co-existence of actors of geometry and mesh
        '''
        self.parent		= parent
        self.settingObj		= settingObj

	self.nPntActors		= 0
	self.nLinActors		= 0
	self.nSrfActors		= 0
	self.nVolActors		= 0
	self.nIsoSrfActors      = 0
	self.nIsoLinActors      = 0
	#----- Misc. 04/09 H1 SH
	self.nEdgActors		= 0

	## Actors like arrows, cylinders, boxes etc
	self.nGeomActors	= 0

	## Cut plane
        self.cutPlane		= None

	## Cut plane actors 
	self.nCPlnActors	= 0

	## Locate actors 10/6/2007
	self.nLoctActors	= 0

	## Text and Image and Colormap
	self.nTxtActors		= 0
	self.nImgActors		= 0
	self.nCmapActors		= 0

	## Eigenmode
	self.nEignmodeActors    = 0

	## JMAG
	self.nJmagActors        = 0

	self.actors		= {}

	self.pntActors		= {}
	self.linActors		= {}
	self.srfActors		= {}
	self.volActors		= {}
	self.isoSrfActors	= {}
	self.isoLinActors	= {}
	
	#----- Misc. 04/09 H1 SH
	self.edgActors		= {}

        #----- Misc. 4/08 D4
        self.visVolFlag         = False
        self.visSrfFlag         = False
        self.visEdgFlag         = False

	## Actors like arrows, cylinders, boxes etc
	self.geomActors		= {}

	## Cut plane actors 
	self.cPlnActors		= {}

	## Locate actors 10/6/2007
	self.loctActors         = {}

	## Eignmode
	self.eignmodeActors     = {}

	## JMAG
	self.jmagActors         = {}

	## Text and Image Actors
	self.txtActors		= {}
	self.txtPos		= {}
	self.txtLoc		= {}
	self.imgActors		= {}
	self.imgPos		= {}
	self.imgLoc		= {}
	self.cmapActors		= {}
	self.cmapPos		= {}

        #----- Misc 4/08 : E9
  	self.viewer		= acuSgViewer.AcuSgViewer( parent,
                                                           settingObj   )
	self.viewer.setSizeChangedCb(		self.sizeChangedCb	)

  	self.root		= SoSeparator(				)
  	self.root.setName( "Model" )

	# Create two top level branches in the scenegraph
	#   + dynObjects => objects that respond to mouse motion
	#   + stcObjects => static objects like text and images

  	self.grLight = SoSpotLight()
  	self.grLight.setName( "Model_Spot_Light" )
	self.lightModel  = SoLightModel()
	self.grLight.intensity.setValue(0.1)
	self.grLight.on.setValue(False)
	self.lightModel.model.setValue( SoLightModel.PHONG )
	
	self.root.addChild( self.grLight )
	self.root.addChild( self.lightModel )
	
	self.dynObjects		= SoSeparator(				)
	self.dynObjects.boundingBoxCaching.setValue(SoSeparator.OFF	)

	self.stcObjects		= SoSeparator(				)
	self.stcObjects.setName( "stc_objects"                          )

	self.root.addChild(		self.dynObjects			)
	self.root.addChild(		self.stcObjects			)

	self.cutPlnSep	= SoSeparator(					)
	self.cutPlnSep.setName(		"cut_plane_objects"		)
	self.dynObjects.addChild(		self.cutPlnSep		)

	self.miscSep	= SoSeparator(					)
	self.miscSep.setName(		"misc_objects" 			)
	self.dynObjects.addChild(	self.miscSep			)

	self.eventCB		= SoEventCallback(			)
	self.dynObjects.addChild(	self.eventCB			)

	self.geomSep	= SoSeparator(					)
	self.geomSep.setName(		"geom_objects" 			)
	self.dynObjects.addChild( 	self.geomSep 			)

	#----- Look up (locate) 10/6/2007
	self.loctSep	= SoSeparator(					)
	self.loctSep.setName(		"locate_objects"		)
	self.dynObjects.addChild(	self.loctSep		        )

	#----- Eigenmodes
	self.eignmodeSep= SoSeparator(					)
	self.eignmodeSep.setName(	"eigenmodes_objects"		)
	self.dynObjects.addChild(	self.eignmodeSep		)

	#----- JMAG
	self.jmagSep    = SoSeparator(					)
	self.jmagSep.setName(	        "jmags_objects"		        )
	self.dynObjects.addChild(	self.jmagSep		        )

	#### Clip plane is a special node #####
	self.clipPlane	= SoClipPlane(					)
	self.clipPlane.on.setValue(		False			)
	#self.dynObjects.addChild(		self.clipPlane		)

	#---------------------------------------------------------------
	# Create Four ExtSelection Objects to hold actors
	# corresponding to each of the volume_set, surface_set,
	# line_set and point set actors
	#---------------------------------------------------------------

	#---------------------------------------------------------------
	# LassoType has to be RECTANGLE for zooming and rbPicking
	#---------------------------------------------------------------

	self.pntSelection	= SoExtSelection(			)
	self.pntSelection.setName(		"Points" 		)
	self.pntSelection.lassoPolicy.setValue(SoExtSelection.FULL	)
	self.pntSelection.lassoType.setValue(SoExtSelection.NOLASSO	)
	self.pntSelection.setLassoColor( SbColor( 1.0, 0.0, 0.0 )	)
	self.pntSelection.setLassoWidth( 		2.0		)

	self.linSelection	= SoExtSelection(			)
	self.linSelection.setName(		"Lines" 		)
	self.linSelection.lassoPolicy.setValue(SoExtSelection.FULL	)
	self.linSelection.lassoType.setValue(SoExtSelection.NOLASSO	)
	self.linSelection.setLassoColor( SbColor( 1.0, 0.0, 0.0 )	)
	self.linSelection.setLassoWidth( 		2.0		)

	#----- Misc. 04/09 H1 SH
        self.edgSelection	= SoExtSelection(			)
	self.edgSelection.setName(		"edge_set" 		)
	self.edgSelection.lassoPolicy.setValue(SoExtSelection.FULL	)
	self.edgSelection.lassoType.setValue(SoExtSelection.NOLASSO	)
	self.edgSelection.setLassoColor( SbColor( 1.0, 0.0, 0.0 )	)
	self.edgSelection.setLassoWidth( 		2.0		)
	
	self.srfSelection	= SoExtSelection(			)
	self.srfSelection.addChild(		self.clipPlane		)
	self.srfSelection.setName(		"Surfaces" 		)
	self.srfSelection.lassoPolicy.setValue(SoExtSelection.FULL	)
	self.srfSelection.lassoType.setValue(SoExtSelection.NOLASSO	)
	self.srfSelection.setLassoColor( SbColor( 1.0, 0.0, 0.0 )	)
	self.srfSelection.setLassoWidth( 		2.0		)

	self.volSelection	= SoExtSelection(			)
	self.volSelection.addChild(		self.clipPlane		)
	self.volSelection.setName(		"Volumes" 		)
	self.volSelection.lassoPolicy.setValue(SoExtSelection.FULL	)
	self.volSelection.lassoType.setValue(SoExtSelection.NOLASSO	)
	self.volSelection.setLassoColor( SbColor( 1.0, 0.0, 0.0 )	)
	self.volSelection.setLassoWidth( 		2.0		)

	self.isoSrfSelection	= SoExtSelection(			)
	self.isoSrfSelection.setName(		"iso_surface_set" 	)
	self.isoSrfSelection.lassoPolicy.setValue(SoExtSelection.FULL	)
	self.isoSrfSelection.lassoType.setValue(SoExtSelection.NOLASSO	)
	self.isoSrfSelection.setLassoColor( SbColor( 1.0, 0.0, 0.0 )	)
	self.isoSrfSelection.setLassoWidth( 		2.0		)

	self.isoLinSelection	= SoExtSelection(			)
	self.isoLinSelection.setName(		"iso_line_set" 	)
	self.isoLinSelection.lassoPolicy.setValue(SoExtSelection.FULL	)
	self.isoLinSelection.lassoType.setValue(SoExtSelection.NOLASSO	)
	self.isoLinSelection.setLassoColor( SbColor( 1.0, 0.0, 0.0 )	)
	self.isoLinSelection.setLassoWidth( 		2.0		)

	self.dynObjects.addChild( 	self.pntSelection 		)
	self.dynObjects.addChild( 	self.linSelection 		)
	self.dynObjects.addChild( 	self.srfSelection 		)
	self.dynObjects.addChild( 	self.volSelection 		)
	self.dynObjects.addChild( 	self.isoSrfSelection 		)
	self.dynObjects.addChild( 	self.isoLinSelection 		)
	
#----- Misc. 04/09 H1 SH
	self.dynObjects.addChild( 	self.edgSelection 		)

        self.viewer.setSceneGraph( 	self.root 			)
	self.viewer.viewAll(						)

	### Build the necessary nodes in the static branch

	## Annotation node makes sure that the geometry associated with
	## static objects is rendered over other geometry in the scene
	##

	self.txtSep	= SoAnnotation(					)
	self.txtSep.setName(		"text_objects"			)
	self.stcObjects.addChild(	self.txtSep			)

	### camera associated with the 2D text objects

	self.txtCam	= SoOrthographicCamera(				)
	self.txtCam.viewportMapping.setValue( SoCamera.LEAVE_ALONE	)
	#self.txtCam.position.setValue(		SbVec3f(0,0,1)		)
	self.txtCam.height.setValue(			1.0		)

	self.txtSep.addChild(		self.txtCam			)
	self.txtCam.viewAll(self.txtSep, self.viewer.getViewportRegion())

	### Now add 2d image separator node

	self.imgSep	= SoAnnotation(					)
	self.imgSep.setName(		"image_objects"			)
	self.stcObjects.addChild(	self.imgSep			)

	self.imgCam	= SoOrthographicCamera(				)
	self.imgCam.viewportMapping.setValue( SoCamera.LEAVE_ALONE	)
	self.imgSep.addChild(		self.imgCam			)
	self.imgCam.viewAll( self.imgSep, self.viewer.getViewportRegion())

	### Add 2d colormap separator node

	self.cmapSep	= SoAnnotation(					)
	self.cmapSep.setName(		"colormap_objects"		)
	self.stcObjects.addChild(	self.cmapSep			)

	self.cmapCam	= SoOrthographicCamera(	)
	self.cmapCam.viewportMapping.setValue( SoCamera.LEAVE_ALONE	)
	self.cmapSep.addChild(	self.cmapCam )
	self.cmapCam.viewAll( self.cmapSep, self.viewer.getViewportRegion())

	### Add 2d line plot separator node (test)
	'''import acuSgLinePlot
	
	self.plotSep	= SoAnnotation(		                        )
	self.plotSep.setName(		"plot_objects"			)
	self.stcObjects.addChild(self.plotSep)

	self.plotCam	= SoOrthographicCamera(	)
	self.plotCam.viewportMapping.setValue( SoCamera.LEAVE_ALONE	)
	self.plotSep.addChild(	self.plotCam )
	self.plotCam.viewAll( self.plotSep, self.viewer.getViewportRegion())	
	
	linePlot = acuSgLinePlot.AcuSgLinePlot()
	linePlot.test()
	self.plotSep.addChild(linePlot)'''
  
	### Set up other attributes and objects

	self.explodedView       = False

	self.globalCrdFlag	= False
	self.crd                = []

	#----- Color Contour and Velocity Vector
	
	self.nNodes         = 0	
	self.scalar         = None 
	self.scalarName     = None
	self.sclrMinVal     = None
	self.sclrMaxVal     = None
	self.tmpSclrMin     = None
	self.tmpSclrMax     = None
	self.cmap           = None	
	self.vel            = None
	self.velScale       = None
	self.tmpVelScale    = None	
	self.velScalar      = None
	self.velScalarType  = None
	self.velSclrMinVal  = None
	self.velSclrMaxVal  = None
	self.tmpVelSclrMin  = None
	self.tmpVelSclrMax  = None
	self.velWidth       = None
	self.velArrowType   = None
	self.velColorType   = None
	self.velColor       = None
	self.velCmap        = None	
	self.velNormal      = SbVec3f(1, 0, 0)

	self._setOffscreenRenderer(					)

	self.acuTform	= AcuSgTform(	self,	settingObj		)
	self.setMouseEventCallback( self.acuTform.eventCallback, None	)
	self.setPntSelCallback( self.acuTform.pntSelCallback, None	)
	self.setLinSelCallback( self.acuTform.linSelCallback, None	)
	self.setSrfSelCallback( self.acuTform.srfSelCallback, None	)
	self.setVolSelCallback( self.acuTform.volSelCallback, None	)
	#----- Misc. 04/09 H1 SH
	self.setEdgSelCallback( self.acuTform.edgSelCallback, None	)

	self.pntSizeLimits	= SbVec2f(				)
	self.viewer.getPointSizeLimits(		self.pntSizeLimits	)
	(lSz, hSz )	= self.pntSizeLimits.getValue(			)

	acuQt.setSetting( 'preferences/lowPntSize'	, lSz		)
	acuQt.setSetting( 'preferences/hghPntSize'	, hSz		)

	self.linWidthLimits	= SbVec2f()
	self.viewer.getLineWidthLimits(		self.linWidthLimits	)
	(lWd, hWd )	= self.linWidthLimits.getValue(			)
	acuQt.setSetting( 'preferences/lowLinWidth'	, lWd		)
	acuQt.setSetting( 'preferences/hghLinWidth'	, hWd		)

	#----- Misc 11/09 B1-B5
	self.clipShapeActorList = None
        self.clipShapeActorSep  = None
        self.clipTranMat        = None
        self.clipOpaqMat        = None
        self.clipNestedMats     = None

	#----- U3D
	self.binDir = os.path.join( os.environ["ACUSIM_HOME"],
                                    os.environ["ACUSIM_MACHINE"],
                                    os.environ["ACUSIM_VERSION"],
                                    "base",
                                    "bin"                               )                                     
                        
#---------------------------------------------------------------------------
# loadBackground: 
#---------------------------------------------------------------------------

    def loadBackground( self ):
       
        type   = acuQt.getSettingStr(   "type",  'solid'                )
        
        if type == "solid":
            r   = acuQt.getSettingReal(   "colorRed",   1               )
            g   = acuQt.getSettingReal(   "colorGreen", 1               )
            b   = acuQt.getSettingReal(   "colorBlue",  1               )
            
            self.viewer.bgColor(  type,
                                  red    = r,
                                  green  = g,
                                  blue   = b                            )
            
        elif type == "two-tone":           
            r       = acuQt.getSettingReal(  "color2Red",   1           )
            g       = acuQt.getSettingReal(  "color2Green", 1           )
            b       = acuQt.getSettingReal(  "color2Blue",  1           )
            r_bot   = acuQt.getSettingReal(  "color1Red",   1           )
            g_bot   = acuQt.getSettingReal(  "color1Green", 1           )
            b_bot   = acuQt.getSettingReal(  "color1Blue",  1           )
            
            self.viewer.bgColor(  type,
                                  red        = r,
                                  green      = g,
                                  blue       = b,
                                  red_bot    = r_bot,
                                  green_bot  = g_bot,
                                  blue_bot   = b_bot                    )
           
        elif type == "filename":
            image  = acuQt.getSettingStr(   "image", ''                 )
            
            if os.path.exists(image):                              
                self.viewer.bgColor( type, fileName   = image           )
                
        else:
            self.viewer.bgColor( "solid",
                                 red    = 1.0,
                                 green  = 1.0,
                                 blue   = 1.0                           )

#---------------------------------------------------------------------------
# addStaticCameras: 
#---------------------------------------------------------------------------
    def addStaticCameras( self ):
        ''' add the cameras associated with the static objects'''

	indx = self.txtSep.findChild( 		self.txtCam 		)
	if indx == -1:
	    self.txtSep.insertChild(		self.txtCam,0		)

	indx = self.imgSep.findChild( 		self.imgCam 		)
	if indx == -1:
	    self.imgSep.insertChild(		self.imgCam,0		)

	indx = self.cmapSep.findChild( 	self.cmapCam )
	if indx == -1:
	    self.cmapSep.insertChild(	self.cmapCam,0	)

#---------------------------------------------------------------------------
# addStaticObjects: 
#---------------------------------------------------------------------------
    def addStaticObjects( self ):

	indx = self.root.findChild( 		self.stcObjects		)
        if indx == -1:
	    self.root.addChild(			self.stcObjects		)

#---------------------------------------------------------------------------
# remStaticObjects: 
#---------------------------------------------------------------------------
    def remStaticObjects( self ):

	indx = self.root.findChild( 		self.stcObjects		)
        if indx != -1:
	    self.root.removeChild(		self.stcObjects		)

#---------------------------------------------------------------------------
# remStaticCameras: 
#---------------------------------------------------------------------------
    def remStaticCameras( self ):
        ''' remove the cameras associated with the static objects'''

	indx = self.txtSep.findChild( 		self.txtCam 		)
	if indx != -1:
	    self.txtSep.removeChild(		self.txtCam		)

	indx = self.imgSep.findChild( 		self.imgCam 		)
	if indx != -1:
	    self.imgSep.removeChild(		self.imgCam		)

	indx = self.cmapSep.findChild( 		self.cmapCam 		)
	if indx != -1:
	    self.cmapSep.removeChild(		self.cmapCam		)

#---------------------------------------------------------------------------
# resetLassoTypes: 
#---------------------------------------------------------------------------

    def resetLassoTypes( self ):
        ''' reset lasso type of all selection nodes'''

	self.pntSelection.lassoType.setValue(SoExtSelection.NOLASSO	)
	self.linSelection.lassoType.setValue(SoExtSelection.NOLASSO	)
	self.srfSelection.lassoType.setValue(SoExtSelection.NOLASSO	)
	self.volSelection.lassoType.setValue(SoExtSelection.NOLASSO	)
	self.isoSrfSelection.lassoType.setValue(SoExtSelection.NOLASSO	)
        self.isoLinSelection.lassoType.setValue(SoExtSelection.NOLASSO	)

	#----- Misc. 04/09 H1 SH
        self.edgSelection.lassoType.setValue(SoExtSelection.NOLASSO	)

#---------------------------------------------------------------------------
# setKeyboardEventCallback: Use processSoEvent in AcuSgViewer class
#---------------------------------------------------------------------------

    def setKeyboardEventCallback( self, callback, userData ):
        '''
	   Function to set KeyboardEvent Callback for the SoEventCallback
	   node inside the scenegraph

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''

        self.eventCB.addEventCallback( \
		SoKeyboardEvent.getClassTypeId(),
		callback, userData					)

#---------------------------------------------------------------------------
# remKeyboardEventCallback: Use processSoEvent in AcuSgViewer class
#---------------------------------------------------------------------------

    def remKeyboardEventCallback( self, callback, userData ):
        '''
	   Function to remove KeyboardEvent Callback for the SoEventCallback
	   node inside scenegraph

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''

        self.eventCB.removeEventCallback( \
		SoKeyboardEvent.getClassTypeId(),
		callback, userData					)

#---------------------------------------------------------------------------
# setMouseEventCallback: set the callback that handles the mouse events
#                        captured by the eventCB node in scenegraph
#---------------------------------------------------------------------------

    def setMouseEventCallback( self, callback, userData ):
        '''
	   Function to set MouseEvent Callback for the graphical window

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''
        self.eventCB.addEventCallback( \
		SoMouseButtonEvent.getClassTypeId(),
		callback,  userData					)

#---------------------------------------------------------------------------
# remMouseEventCallback: remove the mouse callback on eventCB node
#---------------------------------------------------------------------------

    def remMouseEventCallback( self, callback, userData ):
        '''
	   Function to remove MouseEvent Callback for the graphical window

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''
        self.eventCB.removeEventCallback( \
		SoMouseButtonEvent.getClassTypeId(),
		callback,  userData					)

#---------------------------------------------------------------------------
# setVolSelCallback: set the selection callback on the volume selection
#---------------------------------------------------------------------------

    def setVolSelCallback( self, callback, userData ):
        '''
	   Function to set Volume Selection Callback

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''
        self.volSelection.addSelectionCallback( callback, userData	)

#---------------------------------------------------------------------------
# setSrfSelCallback: set the selection callback on the surface selection
#---------------------------------------------------------------------------

    def setSrfSelCallback( self, callback, userData ):
        '''
	   Function to set Surface Selection Callback

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''
        self.srfSelection.addSelectionCallback( callback, userData	)

#---------------------------------------------------------------------------
# setLinSelCallback: set the selection callback on the line selection
#---------------------------------------------------------------------------

    def setLinSelCallback( self, callback, userData ):
        '''
	   Function to set Line Selection Callback

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''
        self.linSelection.addSelectionCallback( callback, userData	)

#---------------------------------------------------------------------------
# setPntSelCallback: set the selection callback on the point selection
#---------------------------------------------------------------------------

    def setPntSelCallback( self, callback, userData ):
        '''
	   Function to set Line Selection Callback

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''

        self.pntSelection.addSelectionCallback( callback, userData	)

#----- Misc. 04/09 H1 SH
#---------------------------------------------------------------------------
# setEdgSelCallback: set the selection callback on the edge selection
#---------------------------------------------------------------------------

    def setEdgSelCallback( self, callback, userData ):
        '''
	   Function to set Edge Selection Callback

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''

        self.edgSelection.addSelectionCallback( callback, userData	)
        
#---------------------------------------------------------------------------
# remVolSelCallback: remove the selection callback on the volume selection
#---------------------------------------------------------------------------

    def remVolSelCallback( self, callback, userData ):
        '''
	   Function to remove Volume Selection Callback

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''
        self.volSelection.removeSelectionCallback( callback, userData	)

#---------------------------------------------------------------------------
# remSrfSelCallback: remove the selection callback on the surface selection
#---------------------------------------------------------------------------

    def remSrfSelCallback( self, callback, userData ):
        '''
	   Function to remove Surface Selection Callback

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''

        self.srfSelection.removeSelectionCallback( callback, userData	)

#---------------------------------------------------------------------------
# remLinSelCallback: remove the selection callback on the line selection
#---------------------------------------------------------------------------

    def remLinSelCallback( self, callback, userData ):
        '''
	   Function to remove Line Selection Callback

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''

        self.linSelection.removeSelectionCallback( callback, userData	)

#---------------------------------------------------------------------------
# remPntSelCallback: remove the selection callback on the point selection
#---------------------------------------------------------------------------

    def remPntSelCallback( self, callback, userData ):
        '''
	   Function to remove Point Selection Callback

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''

        self.pntSelection.removeSelectionCallback( callback, userData	)

#----- Misc. 04/09 H1 SH
#---------------------------------------------------------------------------
# remEdgSelCallback: remove the selection callback on the edge selection
#---------------------------------------------------------------------------

    def remEdgSelCallback( self, callback, userData ):
        '''
	   Function to remove Edge Selection Callback

	   Argument:
	       callback		-	callback function
	       userData		-	argument to the callback function
        '''

        self.edgSelection.removeSelectionCallback( callback, userData	)
        
#---------------------------------------------------------------------------
# axis: function to set/get axis visibility
#---------------------------------------------------------------------------

    def axis( self, visible = None ):
        '''
	   Function to set the visibility of axis in the graphical window

	   Argument:
	       visible		- True/False/None, visibility value	

	   Output:
	       returns the current state of visibility
        '''

	retVal	= self.viewer.isFeedbackVisible(			)

        if visible != None:
	    if visible != True and visible != False:
	        raise acuSceneGraphError, "visible should be True/False"
	    self.viewer.setFeedbackVisibility(		visible		)
	return retVal

#---------------------------------------------------------------------------
# axisSize: function to set/get axis size
#---------------------------------------------------------------------------

    def axisSize( self, size = None ):
        '''
	   Function to set the size of axis in the graphical window

	   Argument:
	       size		- value/None, axis size

	   Output:
	       returns the current size of axis
        '''

	retVal	= self.viewer.getFeedbackSize(		                )

        if size != None:
	    self.viewer.setFeedbackSize(	size			)
	return retVal
        
#---------------------------------------------------------------------------
# redraw: redraw the scenegraph by adding all the selection objects
#---------------------------------------------------------------------------

    def redraw( self ):
        '''
	    redraws the entire scenegraph in the graphical window.
	    Arguments:
	        None
	    Output:
	        None
        '''

        indx = self.dynObjects.findChild(	self.cutPlnSep		)
	if indx == -1:
	    self.dynObjects.addChild(		self.cutPlnSep		)

        indx = self.dynObjects.findChild(	self.miscSep		)
	if indx == -1:
	    self.dynObjects.addChild(		self.miscSep		)

        indx = self.dynObjects.findChild(	self.volSelection	)
	if indx == -1:
	    self.dynObjects.addChild(		self.volSelection	)

        indx = self.dynObjects.findChild(	self.srfSelection	)
	if indx == -1:
	    self.dynObjects.addChild(		self.srfSelection	)

        indx = self.dynObjects.findChild(	self.linSelection	)
	if indx == -1:
	    self.dynObjects.addChild(		self.linSelection	)

        indx = self.dynObjects.findChild(	self.pntSelection	)
	if indx == -1:
	    self.dynObjects.addChild(		self.pntSelection	)

	#----- Misc. 04/09 H1 SH
        indx = self.dynObjects.findChild(	self.edgSelection	)
	if indx == -1:
	    self.dynObjects.addChild(		self.edgSelection	)
	    
        indx = self.dynObjects.findChild(	self.geomSep		)
	if indx == -1:
	    self.dynObjects.addChild(		self.geomSep		)

        indx = self.dynObjects.findChild(	self.loctSep		)
	if indx == -1:
	    self.dynObjects.addChild(		self.loctSep		)

        indx = self.dynObjects.findChild(	self.eignmodeSep	)
	if indx == -1:
	    self.dynObjects.addChild(		self.eignmodeSep	)

        indx = self.dynObjects.findChild(	self.jmagSep	        )
	if indx == -1:
	    self.dynObjects.addChild(		self.jmagSep	        )

        self.viewer.redraw(						)
        #----- Misc 4/08 : E9
        self.acuTform.pickableSrf   = False

#---------------------------------------------------------------------------
# color: set/get the actor color by their id
#---------------------------------------------------------------------------

    def color( self, id, red = None, green = None, blue = None ):
        '''
	    sets the color of the actor identified by its unique id
	    Arguments:
	        id		-  unique id of the actor
		red		-  red color value
		green		-  green color value
		blue		-  blue color value
	    Output: ( Only if red, green and blue are None )
	        [red,green,blue]
        '''
	if id not in self.actors:
	    raise acuSceneGraphError, "Actor Id out of bounds"
	retVal	 = self.actors[id].color(			)

	if red != None and green != None and blue != None:
	    self.actors[id].color(                red, green, blue 	)
	return retVal

#---------------------------------------------------------------------------
# display: set/get the actor display by their id
#---------------------------------------------------------------------------

    def display( self, id, style = None ):
        '''
	    sets the display of the actor identified by its unique id
	    Arguments:
	        id		-  unique id of the actor
		style		-  "outline","solid","none" or "wireframe"
	    Output: ( Only if style is None )
		style		-  "outline","solid","none" or "wireframe"

        '''

	if id not in self.actors:
	    raise acuSceneGraphError, "Actor Id out of bounds"

	curStyle	= self.actors[id].display( 			)

	if style == None:
	    return curStyle

	if curStyle != style:
	    self.actors[id].display(                style               )
	    self.redraw(						)

#---------------------------------------------------------------------------
# visibility: set/get the actor visibility by their id
#---------------------------------------------------------------------------

    def visibility( self, id, vis = None ):
        '''
	    sets the visibility of the actor identified by its unique id
	    Arguments:
	        id		-  unique id of the actor
		vis		-  True/False
	    Output: ( Only if vis is None )
		vis	        -  True/False
        '''
	if id not in self.actors:
	    raise acuSceneGraphError, "Actor Id out of bounds"

	curVis	= self.actors[id].visibility( 			        )

	if vis == None:
	    return curVis

	if vis:
            self.actors[id].visibilityOn( 			        )
        else:
            self.actors[id].visibilityOff( 			        )

#---------------------------------------------------------------------------
# highlight: highlight the actor by their id
#---------------------------------------------------------------------------

    def highlight( self, id ):
        '''
	    highlight the actor identified by its unique id
	    Arguments:
	        id		-  unique id of the actor
	    Output:
	        None
        '''

        if id not in self.actors:
	    raise acuSceneGraphError, "Actor Id out of bounds"

	#----- Misc. 6/07 F2 ; Adding "Volume Highlight" to preferences
##	self.actors[id].highlight(                                      )

        hlightType  = self.getHLighType(        self.actors[id]         )

        if hlightType:
            self.actors[id].highlight(          hlightType              )
        else:
            self.actors[id].highlight(                                  )

#---------------------------------------------------------------------------
# getHLighType: get the highlight type of actor
#---------------------------------------------------------------------------

    def getHLighType( self, actor ):
        '''
	    get the highlight type of actor
	    Arguments:
	        actor		-  the actor
	    Output:
	        None
        '''

        try:
            hlightType      = None
            winObj          = self.settingObj
            display         = actor.display(                            )

            if actor in self.srfActors.values():
                if actor.visibility():
                    hlightType= winObj.getHighlightSrfTypes(    display )
                else:
                    hlightType= winObj.getHighlightSrfTypes(    "None"  )

            elif actor in self.volActors.values():
                if actor.visibility():
                    hlightType= winObj.getHighlightVolTypes(    display )
                else:
                    hlightType= winObj.getHighlightVolTypes(    "None"  )

            #----- Misc. 04/09 H1 SH
            elif actor in self.edgActors.values():
                if actor.visibility():
                    hlightType= winObj.getHighlightEdgTypes(    display )
                else:
                    hlightType= winObj.getHighlightEdgTypes(    "None"  )

        except:
            return None

        return hlightType

#---------------------------------------------------------------------------
# unHighlight: unHighlight the actor by their id
#---------------------------------------------------------------------------

    def unHighlight( self, id ):
        '''
	    unHighlight the actor identified by its unique id
	    Arguments:
	        id		-  unique id of the actor
	    Output:
	        None
        '''

	if id not in self.actors:
		raise acuSceneGraphError, "Actor Id out of bounds"
	self.actors[id].unHighlight(                                    )

#---------------------------------------------------------------------------
# clear: clears the current scenegraph, call this before closing
#        the current database
#---------------------------------------------------------------------------

    def clear( self, remZoneActor = True ):
        '''
	    Deletes all the actors in the scenegraph.
	    
	    Arguments:
	        remZoneActor    - A flag to define whetare to remove
                                  zone mesh acor.
                                  #---- Misc. 04/09 J2 ; 08/27/09
	    Output:
	        None
        '''

	self.pntSelection.removeAllChildren(				)
	self.linSelection.removeAllChildren(				)
	self.srfSelection.removeAllChildren(				)
	self.volSelection.removeAllChildren(				)
	self.isoSrfSelection.removeAllChildren(				)
	self.isoLinSelection.removeAllChildren(				)
	#----- Misc. 04/09 H1 SH
	self.edgSelection.removeAllChildren(				)

        #----- Misc. 04/09 J2 SY
        if remZoneActor:	
            self.geomSep.removeAllChildren(				)
            self.geomActors	= {}
	
	self.miscSep.removeAllChildren(					)
	self.cutPlnSep.removeAllChildren(				)
        self.loctSep.removeAllChildren(					)
        self.eignmodeSep.removeAllChildren(				)
        self.jmagSep.removeAllChildren(				        )

	self.srfSelection.addChild(		self.clipPlane		)
	self.volSelection.addChild(		self.clipPlane		)

	self.vertexProperty	= None
	self.actors		= {}
	self.pntActors		= {}
	self.linActors		= {}
	self.srfActors		= {}
	self.volActors		= {}
	self.isoSrfActors       = {}
	self.isoLinActors       = {}
	#----- Misc. 04/09 H1 SH
	self.edgActors		= {}
	
##	self.geomActors		= {}  #---- Misc. 04/09 J2 SY
	self.loctActors         = {}
	self.cPlnActors		= {}
	self.eignmodeActors     = {}
	self.jmagActors         = {}
	self.nPntActors		= 0
	self.nLinActors		= 0
	self.nSrfActors		= 0
	self.nVolActors		= 0
	self.nIsoSrfActors      = 0
	self.nIsoLinActors      = 0
	#----- Misc. 04/09 H1 SH
	self.nEdgActors		= 0
	self.nGeomActors	= 0
	self.nCPlnActors	= 0
	self.nLoctActors        = 0
	self.nEignmodeActors    = 0
	self.nJmagActors        = 0

	self.globalCrdFlag	= False
	self.vertexProperty	= None

	self.crd                = []

#---------------------------------------------------------------------------
# setGlobalCrd: Function to set the vertexProperty object to be shared
#               between various actors. Use this for mesh data and not
#               for geometric data.
#---------------------------------------------------------------------------

    def setGlobalCrd( self, crd ):
        '''
	    With mesh, the crd data is shared by all the actors or mesh sets.
	    This function would initialize the global crd data to be used
	    by all mesh sets, so that crd is not copied multiple times.
	    Arguments:
	        crd	- a numarray of x,y,z coordinates, typically from acupu
	    Output:
	        None
        '''

        if crd != None:
	    if isinstance(crd, numarray.numarraycore.NumArray ):
		self.vertexProperty = SoVertexProperty()
		self.vertexProperty.vertex.setValues( 0, crd )
		self.globalCrdFlag	= True
		self.nNodes = crd.size()
		self.crd = numarray.array( crd )
		#print self.crd
	    else:
	        raise acuSceneGraphError, " Incorrect Type of crd "

#---------------------------------------------------------------------------
# setVerPro: Function to set the vertexProperty object.
#---------------------------------------------------------------------------

    def setVerPro( self, crd ):
        '''
	    With mesh, the crd data is shared by all the actors or mesh sets.
	    This function would initialize the global crd data to be used
	    by all mesh sets, so that crd is not copied multiple times.
	    Arguments:
	        crd	- a numarray of x,y,z coordinates, typically from acupu
	    Output:
	        None
        '''

        if crd != None:
	    if isinstance(crd, numarray.numarraycore.NumArray ):
		vertexProperty = SoVertexProperty(              )
		vertexProperty.vertex.setValues( 0, crd )
		return vertexProperty
	    else:
	        raise acuSceneGraphError, " Incorrect Type of crd "

#---------------------------------------------------------------------------
# addVolSet: Create an actor from  the volume data ( 3D elements )
#---------------------------------------------------------------------------

    def addVolSet(  self, crd, cnn,  topology,  item,
                    actorName   = None,         state       = None,
                    outlineLnClr= "Auto",       wirefrmLnClr= "Auto"
                 ):
        '''
	    creates a volume set representation of AcuSgActor object
	    Arguments:
	        crd	- a numarray of x,y,z coordinates
	        cnn	- a numarray of connectivity data
	        topology- "four_node_tet", "six_node_wedge" etc.
		item	- TreeItem object
		actorName- name of the actor
		state	- 'mesh' or 'geom'
		outlineLnClr	- mesh line color, default is 'Auto'
		wirefrmLnClr	- mesh wireframe color, default is 'Auto'

	    Output:
	        actor	- AcuSgActor object
        '''

        try:
	    name	= item.name
            if actorName:
                dataId  = str( actorName )#str(item.parent.name + actorName)
            else:
                dataId	= item.dataId
	    display     = item.display
	    vis         = item.visiblityFlg
	    trans       = item.transparencyFlg
	    transVal    = item.transVal
	    red	        = float( item.color.red() )   / 255
	    green	= float( item.color.green() ) / 255
	    blue	= float( item.color.blue() )  / 255
	    color	= [ red, green, blue ]

	    if state == 'mesh':
                if not self.globalCrdFlag:
                    self.setGlobalCrd(              crd                 )
                newActor	= AcuSgActor( self, crd, cnn, topology, \
						name, dataId, \
						self.vertexProperty, \
						display, color, vis, \
                                                trans,   transVal,
                                              outlineLnClr = outlineLnClr,
                                              wirefrmLnClr = wirefrmLnClr)

	    else:
                verPro          = self.setVerPro(   crd                 )
		newActor	= AcuSgActor( self, crd, cnn, topology, \
						name, dataId, verPro, \
						display, color, vis, \
                                                trans,   transVal,
                                              outlineLnClr = outlineLnClr,
                                              wirefrmLnClr = wirefrmLnClr)
	except  acuSceneGraphError, e:
	    print e

	newActor.pointSize(		2				)
	item.actor	                = newActor
        self.actors[dataId]		= newActor
	self.volActors[self.nVolActors]	= newActor
	self.nVolActors 		+= 1
	self.volSelection.addChild( newActor)
	return newActor

#---------------------------------------------------------------------------
# addSrfSet: Create an actor from  the surface data ( 2D elements )
#---------------------------------------------------------------------------

    def addSrfSet(  self,   crd,   cnn,   topology,  item,
                    actorName   = None,         state       = None,
                    outlineLnClr= "Auto",       wirefrmLnClr= "Auto"
                    
                 ):
        '''
	    creates a surface set representation of AcuSgActor object
	    Arguments:
	        crd	- a numarray of x,y,z coordinates
	        cnn	- a numarray of connectivity data
	        topology- "four_node_tet", "six_node_wedge" etc.
				item	- TreeItem object
		actorName- name of the actor
		state	- 'mesh' or 'geom'
		outlineLnClr	- mesh line color, default is 'Auto'
		wirefrmLnClr	- mesh wireframe color, default is 'Auto'

	    Output:
	        actor	- AcuSgActor object
        '''
        try:

	    name	= item.name
            if actorName:
                dataId  = str( actorName )#str(item.parent.name + actorName)
            else:
                dataId	= item.dataId
	    display     = item.display
	    vis         = item.visiblityFlg
	    trans       = item.transparencyFlg
	    transVal    = item.transVal
	    red		= float( item.color.red() )   / 255
	    green	= float( item.color.green() ) / 255
	    blue	= float( item.color.blue() )  / 255
	    color	= [ red, green, blue ]

	    if state == 'mesh':
                if not self.globalCrdFlag:
                    self.setGlobalCrd(              crd                 )
                newActor	= AcuSgActor( self, crd, cnn, topology, \
						name, dataId, \
						self.vertexProperty, \
						display, color, vis, \
                                                trans,   transVal,
                                              outlineLnClr = outlineLnClr,
                                              wirefrmLnClr = wirefrmLnClr)

	    else:
                verPro          = self.setVerPro(   crd                 )
		newActor	= AcuSgActor( self, crd, cnn, topology, \
						name, dataId, verPro, \
						display, color, vis, \
                                                trans,   transVal,
                                              outlineLnClr = outlineLnClr,
                                              wirefrmLnClr = wirefrmLnClr)

	except  acuSceneGraphError, e:
	    print e

	newActor.pointSize(		2				)
	item.actor	                = newActor
        self.actors[dataId]		= newActor
	self.srfActors[self.nSrfActors]	= newActor
	self.nSrfActors 		+= 1
	self.srfSelection.addChild( newActor)
	return newActor

#---------------------------------------------------------------------------
# addLinSet: Create an actor from the line data ( 1D elements )
#---------------------------------------------------------------------------

    def addLinSet( self, crd, cnn, topology, item,\
    			actorName = None, state = None ):
        '''
	    creates a line set representation of AcuSgActor object
	    Arguments:
	        crd	- a numarray of x,y,z coordinates
	        cnn	- a numarray of connectivity data
	        topology- "four_node_tet", "six_node_wedge" etc.
		item	- TreeItem object
		actorName- name of the actor
		state	- 'mesh' or 'geom'
	    Output:
	        actor	- AcuSgActor object
        '''
        try:

	    name	= item.name
            if actorName:
                dataId  = str( actorName )#str(item.parent.name + actorName)
            else:
                dataId	= item.dataId
	    display     = item.display
	    vis         = item.visiblityFlg
	    trans       = item.transparencyFlg
	    transVal    = item.transVal
	    red	        = float( item.color.red() )   / 255
	    green	= float( item.color.green() ) / 255
	    blue	= float( item.color.blue() )  / 255
	    color	= [ red, green, blue ]

	    if state == 'mesh':
                if not self.globalCrdFlag:
                    self.setGlobalCrd(              crd                 )
                newActor	= AcuSgActor( self, crd, cnn, topology, \
						name, dataId, \
						self.vertexProperty, \
						display, color, vis, \
                                                trans,   transVal       )

	    else:
                verPro          = self.setVerPro(   crd                 )
		newActor	= AcuSgActor( self, crd, cnn, topology, \
						name, dataId, verPro, \
						display, color, vis, \
                                                trans,   transVal       )
	except  acuSceneGraphError, e:
	    print e

	newActor.pointSize(		2				)
	item.actor	                = newActor
        self.actors[dataId]		= newActor
	self.linActors[self.nLinActors]	= newActor
	self.nLinActors 		+= 1
	self.linSelection.addChild( newActor)
	return newActor

#---------------------------------------------------------------------------
# addPntSet: Create an actor from the point/nbc data ( 0D elements )
#---------------------------------------------------------------------------

    def addPntSet( self, crd, cnn, topology, item,  \
			    actorName = None, state = None ):
        '''
	    creates a point set representation of AcuSgActor object
	    Arguments:
	        crd	- a numarray of x,y,z coordinates
	        cnn	- a numarray of connectivity data
	        topology- "four_node_tet", "six_node_wedge" etc.
		item	- TreeItem object
		actorName- name of the actor
		state	- 'mesh' or 'geom'
	    Output:
	        actor	- AcuSgActor object
        '''
        try:

	    name	= item.name
            if actorName:
                dataId  = str( actorName )#str(item.parent.name + actorName)
            else:
                dataId	= item.dataId
	    display     = item.display
	    vis         = item.visiblityFlg
	    trans       = item.transparencyFlg
	    transVal    = item.transVal
	    red	        = float( item.color.red() )   / 255
	    green	= float( item.color.green() ) / 255
	    blue	= float( item.color.blue() )  / 255
	    color	= [ red, green, blue ]

	    #The logic below is already implemented in acuSgActor
	    #nCnn	= len(cnn)
	    #if int(nCnn/2) == float(nCnn)/2:
	    #    nElms	= nCnn / 2
	    #    cnn.resize(		( nElms, 2 ) 			)

	    if state == 'mesh':
                if not self.globalCrdFlag:
                    self.setGlobalCrd(              crd                 )
                newActor	= AcuSgActor( self, crd, cnn, topology, \
						name, dataId, \
						self.vertexProperty, \
						display, color, vis, \
                                                trans,   transVal       )

	    else:
                verPro          = self.setVerPro(   crd                 )
		newActor	= AcuSgActor( self, crd, cnn, topology, \
						name, dataId, verPro, \
						display, color, vis, \
                                                trans,   transVal       )
		
	except  acuSceneGraphError, e:
	    print e

	newActor.pointSize(		2				)
	item.actor	                = newActor
        self.actors[dataId]		= newActor
	self.pntActors[self.nPntActors]	= newActor
	self.nPntActors 		+= 1
	self.pntSelection.addChild( newActor)
	return newActor

#----- Misc. 04/09 H1 SH
#---------------------------------------------------------------------------
# addEdgSet: Create an actor from the edge data ( 1D elements )
#---------------------------------------------------------------------------

    def addEdgSet( self, crd, cnn, topology, item,\
    			actorName = None, state = None ):
        '''
	    creates an edge set representation of AcuSgActor object
	    Arguments:
	        crd	- a numarray of x,y,z coordinates
	        cnn	- a numarray of connectivity data
	        topology- "four_node_tet", "six_node_wedge" etc.
		item	- TreeItem object
		actorName- name of the actor
		state	- 'mesh' or 'geom'
	    Output:
	        actor	- AcuSgActor object
        '''
        try:

	    name	= item.name
            if actorName:
                dataId  = str( actorName )
            else:
                dataId	= item.dataId
	    display     = item.display
	    vis         = item.visiblityFlg
	    trans       = item.transparencyFlg
	    transVal    = item.transVal
	    red	        = float( item.color.red() )   / 255
	    green	= float( item.color.green() ) / 255
	    blue	= float( item.color.blue() )  / 255
	    color	= [ red, green, blue ]

	    if state == 'mesh':
                if not self.globalCrdFlag:
                    self.setGlobalCrd(              crd                 )
                newActor	= AcuSgActor( self, crd, cnn, topology, \
						name, dataId, \
						self.vertexProperty, \
						display, color, vis, \
                                                trans,   transVal       )

	    else:
                verPro          = self.setVerPro(   crd                 )
		newActor	= AcuSgActor( self, crd, cnn, topology, \
						name, dataId, verPro, \
						display, color, vis, \
                                                trans,   transVal       )
	except  acuSceneGraphError, e:
	    print e

	newActor.pointSize(		2				)
	item.actor	                = newActor
        self.actors[dataId]		= newActor
	self.edgActors[self.nEdgActors]	= newActor
	self.nEdgActors 		+= 1
	self.edgSelection.addChild( newActor)
	return newActor
    
#---------------------------------------------------------------------------
# addCPlaneActor: Create an actor from  the surface data ( 2D elements )
#---------------------------------------------------------------------------

    def addCPlaneActor( self, crd, cnn, topology, actorName , color ):

        '''
	    creates a surface set representation of AcuSgActor object
	    Arguments:
	        crd	- a numarray of x,y,z coordinates
	        cnn	- a numarray of connectivity data
	        topology- "four_node_tet", "six_node_wedge" etc.
		display - "none","wireframe","mesh","outline" etc.["none"]
		color	- [ r, g, b ] values [ default None ]
		vis	- visibility of the volume set [ default = True ]
		actorName- Name of the actor
	    Output:
	        actor	- AcuSgActor object
        '''

        try:

	    #verPro      = self.setVerPro(   crd                 	)
	    verPro	= None
	    dataId	= actorName
	    name	= actorName
	    newActor	= AcuSgActor( self, crd, cnn, topology, \
					name, dataId, verPro, \
					"solid_wire", color, True, \
					False, 0.5, False		)

	    self.cPlnActors[self.nCPlnActors]	= newActor
	    self.nCPlnActors	+= 1
	    self.cutPlnSwt1.addChild(		newActor		)
	    return newActor
        except:
	    raise acuSceneGraphError, "error while adding cut plane data"

#---------------------------------------------------------------------------
# addIsoSrf: Create an actor from  the iso surface data ( 2D elements )
#---------------------------------------------------------------------------

    def addIsoSrf(  self, crd, cnn, topology, name , display,
                    color, vis, trans, transVal                 ):
        '''
	    creates a surface set representation of AcuSgActor object
	    Arguments:
	        crd	- A numarray of x,y,z coordinates
	        cnn	- A numarray of connectivity data
	        topology- "four_node_tet", "six_node_wedge" etc.
		name	- Name of the actor
		display - Display type of the actor
		color	- Color of the actor
		vis	- Visibility of the actor
		trans	- Tansparency state of the actor
		transVal- Tansparency value of the actor

	    Output:
	        actor	- AcuSgActor object
        '''
        try:

	    verPro	= None
	    dataId	= name
	    newActor	= AcuSgActor( self, crd, cnn, topology, \
					name, dataId, verPro, \
					display, color, vis, \
					trans, transVal, False		)

	    #self.actors[dataId]		        = newActor
	    self.isoSrfActors[self.nIsoSrfActors]	= newActor
	    self.nIsoSrfActors	+= 1
	    self.isoSrfSelection.addChild(	    newActor		)
	    return newActor
        except:
	    raise acuSceneGraphError, "error while adding cut plane data"

#---------------------------------------------------------------------------
# addIsoLine: Create an actor from  the iso line data ( 1D elements )
#---------------------------------------------------------------------------

    def addIsoLine(  self, crd, cnn, topology, name , display,
                    color, vis, trans, transVal                 ):
        '''
	    creates an iso line set representation of AcuSgActor object
	    Arguments:
	        crd	- A numarray of x,y,z coordinates
	        cnn	- A numarray of connectivity data
	        topology- Topology of iso-line actor
		name	- Name of the actor
		display - Display type of the actor
		color	- Color of the actor
		vis	- Visibility of the actor
		trans	- Tansparency state of the actor
		transVal- Tansparency value of the actor

	    Output:
	        actor	- AcuSgActor object
        '''
        try:

	    dataId	= name
	    newActor	= AcuSgActor( self, crd, cnn, topology,\
                                      name, dataId, self.vertexProperty,\
                                      display, color, vis,trans,\
                                      transVal, False		        )

	    newActor.pointSize(                     2                   )
	    #self.actors[dataId]		            = newActor
	    self.isoLinActors[self.nIsoLinActors]   = newActor
	    self.nIsoLinActors	+= 1
	    self.isoLinSelection.addChild(	    newActor		)
	    return newActor
        except:
	    raise acuSceneGraphError, "error while adding iso line data"
  
#---------------------------------------------------------------------------
# remAllCPlnActors:
#---------------------------------------------------------------------------

    def remAllCPlnActors( self ):

        for i in self.cPlnActors:
	    indx	= self.cutPlnSwt1.findChild(  self.cPlnActors[i])
	    if indx != -1:
	        self.cutPlnSwt1.removeChild( self.cPlnActors[i]	)
		self.nCPlnActors -= 1
        self.cPlnActors	= {}
	if self.nCPlnActors != 0:
	    raise acuSceneGraphError, "some cut plane actors are not removed"

#---------------------------------------------------------------------------
# remCPlnActor:
#---------------------------------------------------------------------------

    def remCPlnActor( self, cPlnActor ):
        '''
	    removes the cut plane actor from the scenegraph
	    Arguments:
	        cPlnActor - an object of type AcuSgActor
	    Output:
	        None
        '''

        try:

            for i in self.cPlnActors:
	        if cPlnActor == self.cPlnActors[i]:
	            indx	= self.cutPlnSwt1.findChild(  cPlnActor)
		    if indx != -1:
	                self.cutPlnSwt1.removeChild( self.cPlnActors[i])
		        del self.cPlnActors[i]
		    self.nCPlnActors -= 1
		    break

	except  acuSceneGraphError, e:
	    print e

#---------------------------------------------------------------------------
# remIsoActor: Remove iso surface actor from scene graph
#---------------------------------------------------------------------------

    def remIsoActor( self, isoActor ):
        '''
	    removes the iso surface actor from the scenegraph
	    Arguments:
	        isoActor - an object of type AcuSgActor
	    Output:
	        None
        '''

        try:
            for i in self.isoSrfActors:
	        if isoActor == self.isoSrfActors[i]:
	            indx	= self.isoSrfSelection.findChild( isoActor  )
		    if indx != -1:
	                self.isoSrfSelection.removeChild(self.isoSrfActors[i])
		        del self.isoSrfActors[i]
		    self.nIsoSrfActors -= 1
		    break

	except  acuSceneGraphError, e:
	    print e

#---------------------------------------------------------------------------
# remIsoLnActor: Remove iso line actor from scene graph
#---------------------------------------------------------------------------

    def remIsoLnActor( self, isoLinActor ):
        '''
	    removes the iso line actor from the scenegraph
	    Arguments:
	        isoLinActor - an object of type AcuSgActor
	    Output:
	        None
        '''

        try:
            for i in self.isoLinActors:
	        if isoLinActor == self.isoLinActors[i]:
	            indx	= self.isoLinSelection.findChild( isoLinActor)
		    if indx != -1:
	                self.isoLinSelection.removeChild(self.isoLinActors[i])
		        del self.isoLinActors[i]
		    self.nIsoLinActors -= 1
		    break

	except  acuSceneGraphError, e:
	    print e

#---------------------------------------------------------------------------
# remPntActor: Remove point actor from scene graph
#---------------------------------------------------------------------------

    def remPntActor( self, pntActor ):
        '''
	    removes the point actor from the scenegraph
	    Arguments:
	        pntActor - an object of type AcuSgActor
	    Output:
	        None
        '''

        try:
            for i in self.pntActors:
	        if pntActor == self.pntActors[i]:
	            indx	= self.pntSelection.findChild( pntActor  )
		    if indx != -1:
	                self.pntSelection.removeChild(self.pntActors[i])
		        del self.pntActors[i]
		    self.nPntActors -= 1
		    break

	except  acuSceneGraphError, e:
	    print e
	    
#---------------------------------------------------------------------------
# addGeomActor:
#---------------------------------------------------------------------------

    def addGeomActor( self,
    			type		= "cylinder",
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
			point		= None,
			pntList		= None,
			point1		= None,
			point2		= None,
			text		= None,
			pointSize	= 2,
                        lineWidth       = 2,
			fontSize	= None,
			arrowLength	= None,
			triSize		= None,
			tetSize		= None,
                        vis             = False,
                        trans           = False,
                        transVal        = 0.5,
                        points          = None  
                      
			):

        try:
	    geomActor	= AcuSgObject(
	    				parent		= self,
					type		= type,
					center		= center,
					normal		= normal,
                                        normalX         = normalX,
                                        normalY         = normalY,
                                        normalZ         = normalZ,
					radius		= radius,
					height		= height,
					width		= width,
					depth		= depth,
					xangle		= xangle,
					yangle		= yangle,
					zangle		= zangle,
					color		= color,
					point		= point,
					pntList		= pntList,
					point1		= point1,
					point2		= point2,
					text		= text,
					pointSize	= pointSize,
                                        lineWidth       = lineWidth,
					fontSize	= fontSize,
					triSize		= triSize,
					tetSize		= tetSize,
					arrowLength	= arrowLength,
                                        vis             = vis,
                                        trans           = trans,
                                        transVal        = transVal,
                                        points          = points
                                    )

            self.geomSep.addChild(		geomActor		)
	    self.geomActors[self.nGeomActors]	= geomActor
	    self.nGeomActors	+= 1
	    return geomActor

	except  acuSceneGraphError, e:
	    print e

#---------------------------------------------------------------------------
# remGeomActor:
#---------------------------------------------------------------------------

    def remGeomActor( self, geomActor ):

        try:

            for i in self.geomActors.keys():
	        if geomActor == self.geomActors[i]:
	            indx	= self.geomSep.findChild(    geomActor	)
		    if indx != -1:
	                self.geomSep.removeChild(	geomActor	)
	            else:
                        "The geom actor could not be removed form scene graph"
	            del self.geomActors[i]
##		    self.nGeomActors -= 1
		    break
	    else:
                acuSceneGraphError, "Geom Actor could not be removed"

	except  acuSceneGraphError, e:
	    print e

#---------------------------------------------------------------------------
# addTxtActor:
#---------------------------------------------------------------------------

    def addTxtActor( 	self,
    			value		= "ACUSIM",
			position	= [0.5,0.5],
			style		= "Times New Roman:bold",
			fontSize	= 12,
			color		= [1,0,0],
			horAlignment	= "CENTER",
			verAlignment	= "BOTTOM"
			):

        ''' add 2D text objects at a specified location '''

	txtActor	= SoSeparator(					)

	tLoc	= SoTranslation(					)
	txtActor.addChild(			tLoc			)

	txtClr	= SoBaseColor(						)
	txtActor.addChild(			txtClr			)

	r,g,b	= color[0], color[1], color[2]
	txtClr.rgb.setValue(			r,g,b			)

	txtFont	= SoFont(						)
	txtActor.addChild(			txtFont			)

	txtFont.name.setValue(			style			)
	txtFont.size.setValue(			fontSize		)

	txtObj	= SoText2(						)
	txtActor.addChild(			txtObj			)

	txtObj.string.setValue(			value			)

	if horAlignment == "LEFT":
	    txtObj.justification.setValue(	SoText2.LEFT		)
	elif horAlignment == "CENTER":
	    txtObj.justification.setValue(	SoText2.CENTER		)
	elif horAlignment == "RIGHT":
	    txtObj.justification.setValue(	SoText2.RIGHT		)
	else:
	    raise acuSceneGraphError, "Undefined horAlignment"

	self.txtSep.addChild(			txtActor		)
	self.txtActors[self.nTxtActors]		= txtActor
	self.txtLoc[self.nTxtActors]		= tLoc
	self.nTxtActors				+= 1
	self.setTxtActorLoc(		position, txtActor		)	
	return txtActor

#---------------------------------------------------------------------------
# setTxtActorLoc:
#---------------------------------------------------------------------------

    def setTxtActorLoc( self, position, txtActor ):

        sx, sy	=  position[0], position[1]

	w, h	= self.viewer.getGLSize().getValue(			)
	sx	= sx * w
	sy	= sy * h
	sx	= float( sx ) / float ( max( int(w-1), 1 ) )
	sy	= float( sy ) / float ( max( int(h-1), 1 ) )

	vv	= self.txtCam.getViewVolume( self.viewer.getGLAspectRatio())
	line	= SbLine(						)
	fD 	= self.txtCam.focalDistance.getValue(			)
	fPln	= vv.getPlane(			fD			)

	cPos	= SbVec2f(		sx, sy				)
	vv.projectPointToLine(		cPos, line			)
	cPnt	= SbVec3f(						)
	fPln.intersect(			line, cPnt			)

	for k, v in self.txtActors.items():
	    if v == txtActor:
	        key = k
		break

	x,y,z	= cPnt.getValue(					)
	self.txtLoc[key].translation.setValue(		x,y,z		)
	self.txtPos[key]	= cPos
	self.sizeChangedCb(		SbVec2s(w,h)			)	


#---------------------------------------------------------------------------
# remTxtActor:
#---------------------------------------------------------------------------

    def remTxtActor( self, txtActor ):

        try:

            for i in self.txtActors.keys():
	        if txtActor == self.txtActors[i]:
	            indx	= self.txtSep.findChild(    txtActor	)
		    if indx != -1:
	                self.txtSep.removeChild(	txtActor	)
	            del self.txtActors[i]
		    del self.txtPos[i]
		    del self.txtLoc[i]
		    self.nTxtActors -= 1

	except  acuSceneGraphError, e:
	    print e

#---------------------------------------------------------------------------
# addCmapActor:
#---------------------------------------------------------------------------
    def addCmapActor( 	self,
    			text        = "Temperature",
			textFont    = "Times-Roman",
			minVal	    = 0,
			maxVal	    = 5,
			nVals	    = 1,
                        textFontSize= 12,
			valFont     = "Times-Roman",
                        valFontSize = 12,
			xpos        = 0.05,
			ypos        = 0.05,
			xsize       = 20,
			ysize       = 100,
                        valXOffset  = 0.07,
                        valYOffset  = 0.05              ):

        ''' add 2D colormap legend at a specified location '''

	cmapActor = SoSeparator()
	
	imgLoc	= SoTranslation( )
	cmapActor.addChild(	imgLoc	)
	# Following translation moves the objects to point 0.0, 0.0 --- I got it from setImgActorLoc
	imgLoc.translation.setValue( -1.741, -1.0, -4.0 )
	
	cmap    = AcuSgCmapLegend(	        parent	    = self,
				                text        = text,
				                textFont    = textFont,
				                minVal	    = minVal,
				                maxVal	    = maxVal,
				                nVals	    = nVals,
                                                textFontSize= textFontSize,
				                valFont     = valFont,
                                                valFontSize = valFontSize,
				                xpos        = xpos,
				                ypos        = ypos,
				                xsize       = xsize,
				                ysize       = ysize,
                                                valXOffset  = valXOffset,
                                                valYOffset  = valYOffset    )

	cmapActor.addChild(             cmap                                )

	self.cmapSep.addChild( cmapActor )
	self.cmapActors[self.nCmapActors]	= cmapActor

	self.cmapPos[self.nCmapActors]	= SbVec2f( 0.0, 0.0 )
	w, h	= self.viewer.getGLSize().getValue(	)
	self.sizeChangedCb(	SbVec2s(w,h) )		
	self.nCmapActors	+= 1
	
	return cmap

#---------------------------------------------------------------------------
# remCmapActor:
#---------------------------------------------------------------------------

    def remCmapActor( self, cmapActor ):

        try:

            for i in range( self.nCmapActors ):
                if self.cmapActors[i].findChild(cmapActor) != -1:                
                    self.cmapSep.removeChild( self.cmapActors[i])
	        if cmapActor == self.cmapActors[i]:
	            indx	= self.cmapSep.findChild(  cmapActor	)
		    if indx != -1:
	                self.cmapSep.removeChild( cmapActor )
	            del self.cmapActors[i]
	            del self.cmapPos[i]
		    self.nCmapActors -= 1

	except  acuSceneGraphError, e:
	    print e
	
#---------------------------------------------------------------------------
# addImgActor:
#---------------------------------------------------------------------------

    def addImgActor( 	self,
    			filename	= None,
			image		= None,
			position	= [0.5,0.5],
			width		= -1,
			height		= -1,
			horAlignment	= "CENTER",
			verAlignment	= "BOTTOM"
			):

        ''' add 2D text objects at a specified location '''

	imgActor	= SoSeparator(					)

	imgLoc	= SoTranslation(					)
	imgActor.addChild(			imgLoc			)

	imgObj	= SoImage(						)
	imgActor.addChild(			imgObj			)

	if filename != None:
	    imgObj.filename.setValue(		filename		)
	elif image != None:

	    #### HACK for now. This way we can get the files from
	    #### acuIcon.getIcon('logo') and pass it directly to 
	    #### addImgActor( image=acuIcon.getIcon('logo')

            #----- Misc. 8/07 E4
            if isinstance( image, types.ListType):
                image   = qt.QPixmap(      image                           )

            if isinstance( image, qt.QPixmap):
	        image	= image.convertToImage(				)
		convert( 		image, imgObj			)
            elif isinstance( image, qt.QImage):
		convert( 		image, imgObj			)
            elif isinstance( image, SoImage):
	        imgObj	= image
            else:
	        filename	= "tmp.png"
	        image.save( 		filename, "PNG"			)
	        imgObj.filename.setValue(		filename	)
	else:
	    print "image actor was not assigned an image"

	imgObj.width.setValue(			width			)
	imgObj.height.setValue(			height			)

	if horAlignment == "RIGHT":
	    imgObj.horAlignment.setValue(	SoImage.RIGHT		)
	elif horAlignment == "CENTER":
	    imgObj.horAlignment.setValue(	SoImage.CENTER		)
	elif horAlignment == "LEFT":
	    imgObj.horAlignment.setValue(	SoImage.LEFT		)
	else:
	    raise acuSceneGraphError, "Undefined horAlignment"

	if verAlignment == "BOTTOM":
	    imgObj.vertAlignment.setValue(	SoImage.BOTTOM		)
	elif verAlignment == "TOP":
	    imgObj.vertAlignment.setValue(	SoImage.TOP		)
	elif verAlignment == "HALF":
	    imgObj.vertAlignment.setValue(	SoImage.HALF		)
	else:
	    raise acuSceneGraphError, "Undefined verAlignment"

	self.imgSep.addChild(			imgActor		)
	self.imgActors[self.nImgActors]		= imgActor
	self.imgLoc[self.nImgActors]		= imgLoc
	
	self.nImgActors				+= 1
	self.setImgActorLoc(		position, imgActor		)
	return imgActor

#---------------------------------------------------------------------------
# setImgActorLoc:
#---------------------------------------------------------------------------

    def setImgActorLoc( self, position, imgActor ):

        sx, sy	=  position[0], position[1]

	w, h	= self.viewer.getGLSize().getValue(			)
	sx	= sx * w
	sy	= sy * h
	sx	= float( sx ) / float ( max( int(w-1), 1 ) )
	sy	= float( sy ) / float ( max( int(h-1), 1 ) )

	vv	= self.imgCam.getViewVolume( self.viewer.getGLAspectRatio())
	line	= SbLine(						)
	fD 	= self.imgCam.focalDistance.getValue(			)
	fPln	= vv.getPlane(			fD			)

	cPos	= SbVec2f(		sx, sy				)
	vv.projectPointToLine(		cPos, line			)
	cPnt	= SbVec3f(						)
	fPln.intersect(			line, cPnt			)

	for k, v in self.imgActors.items():
	    if v == imgActor:
	        key = k
		break

	x,y,z	= cPnt.getValue(					)

	self.imgLoc[key].translation.setValue(		x,y,z		)
	self.imgPos[key]	= cPos
	self.sizeChangedCb(		SbVec2s(w,h)			)	

#---------------------------------------------------------------------------
# remImgActor:
#---------------------------------------------------------------------------

    def remImgActor( self, imgActor ):

        try:

            for i in range( self.nImgActors ):
	        if imgActor == self.imgActors[i]:
	            indx	= self.imgSep.findChild(    imgActor	)
		    if indx != -1:
	                self.imgSep.removeChild(	imgActor	)
	            del self.imgActors[i]
	            del self.imgLoc[i]
	            del self.imgPos[i]
		    self.nImgActors -= 1

	except  acuSceneGraphError, e:
	    print e


#---------------------------------------------------------------------------
# sizeChangedCb:
#---------------------------------------------------------------------------
    def sizeChangedCb( self , size ):


	w, h	= self.viewer.getGLSize().getValue(			)

        sAction1=  SoSearchAction(					)
	sAction1.setType(		SoTranslation.getClassTypeId()	)
	sAction1.LookFor	= 2
	sAction1.setInterest(		SoSearchAction.FIRST		)

	vv	= self.txtCam.getViewVolume(				)
	line	= SbLine(						)
	fD	= self.txtCam.focalDistance.getValue(			)
	fPln	= vv.getPlane(			fD			)

	for i in self.txtActors:
	    sAction1.apply(			self.txtActors[i]	)
	    nodePath	= sAction1.getPath(				)

	    if nodePath:
	        node	= nodePath.getTail(				)
		pos	= self.txtPos[i]
		sx,sy	= pos.getValue(					)
		sx	= sx * w
		sy	= sy * h
		sx	= float( sx ) / float ( max( int(w-1), 1 ) )
		sy	= float( sy ) / float ( max( int(h-1), 1 ) )
		pos	= SbVec2f(		sx,sy			)
		pt	= SbVec3f(					)
		vv.projectPointToLine(		pos, line		)
		fPln.intersect(			line, pt		)
		x,y,z	= pt.getValue(					)
		node.translation.setValue(	x,y,z			)

        sAction2=  SoSearchAction(					)
	sAction2.setType(		SoTranslation.getClassTypeId()	)
	sAction2.LookFor	= 2
	sAction2.setInterest(		SoSearchAction.FIRST		)

	vv	= self.imgCam.getViewVolume(				)
	line	= SbLine(						)
	fD	= self.imgCam.focalDistance.getValue(			)
	fPln	= vv.getPlane(			fD			)

	for i in self.imgActors:
	    sAction2.apply(			self.imgActors[i]	)
	    nodePath	= sAction2.getPath(				)

	    if nodePath:
	        node	= nodePath.getTail(				)
		pos	= self.imgPos[i]
		sx,sy	= pos.getValue(					)
		sx	= sx * w
		sy	= sy * h
		sx	= float( sx ) / float ( max( int(w-1), 1 ) )
		sy	= float( sy ) / float ( max( int(h-1), 1 ) )
		pos	= SbVec2f(		sx,sy			)
		pt	= SbVec3f(					)
		vv.projectPointToLine(		pos, line		)
		fPln.intersect(			line, pt		)
		x,y,z	= pt.getValue(					)
		node.translation.setValue(	x,y,z			)
    # Colormaps
	sAction3=  SoSearchAction(					)
	sAction3.setType(		SoTranslation.getClassTypeId()	)
	sAction3.LookFor	= 2
	sAction3.setInterest(		SoSearchAction.FIRST		)

	vv	= self.cmapCam.getViewVolume(				)
	line	= SbLine(						)
	fD	= self.cmapCam.focalDistance.getValue(			)
	fPln	= vv.getPlane(			fD			)

	for i in self.cmapActors:
	    sAction3.apply(			self.cmapActors[i]	)
	    nodePath	= sAction3.getPath(				)

	    if nodePath:
	        node	= nodePath.getTail(				)
		pos	= self.cmapPos[i]
		sx,sy	= pos.getValue(					)
		sx	= sx * w
		sy	= sy * h
		sx	= float( sx ) / float ( max( int(w-1), 1 ) )
		sy	= float( sy ) / float ( max( int(h-1), 1 ) )
		pos	= SbVec2f(		sx,sy			)
		pt	= SbVec3f(					)
		vv.projectPointToLine(		pos, line		)
		fPln.intersect(			line, pt		)
		x,y,z	= pt.getValue(					)
		node.translation.setValue(	x,y,z			)

            
#---------------------------------------------------------------------------
# getBoundingBox:
#---------------------------------------------------------------------------
    def getBoundingBox( self, path = None ):
        '''
	    computes the bounding box of the objects in the scenegraph
	    Arguments:
	        path	- bounding box of the specified node
		          if path == None, compute the bounding box
			  of the entire scene graph
    
	    Output:
	        None
        '''

        vp	= self.viewer.getViewportRegion(			)
	bboxAction	= SoGetBoundingBoxAction(	vp		)
	
	if path:
	    bboxAction.apply(			path			)
	else:
	    bboxAction.apply(			self.dynObjects		)
	bbox	= bboxAction.getBoundingBox(	).getBounds(		)
	
	return bbox  

#---------------------------------------------------------------------------
# addCutPlane:
#---------------------------------------------------------------------------
    def addCutPlane( self ):
        '''
	    add a cut plane to the scene graph
	    Arguments:
	        None	
	    Output:
	        None
        '''


	self.resetLassoTypes(						)

	self.cutPlnSwt1	= SoSwitch(					)
	self.cutPlnSep.addChild(		self.cutPlnSwt1		)

	self.cutPlnSwt2	= SoSwitch(					)
	self.cutPlnSep.addChild(		self.cutPlnSwt2		)

        self.cutPlane	= None
	self.cutPlane	= AcuSgCPlane( 		self			)
	self.cutPlnSwt2.addChild(	self.cutPlane.getActor()	)

	self.cutPlnSwt1.whichChild.setValue(	SO_SWITCH_NONE		)
	self.cutPlnSwt2.whichChild.setValue(	SO_SWITCH_ALL		)


	return self.cutPlane

#---------------------------------------------------------------------------
# remCutPlane:
#---------------------------------------------------------------------------

    def remCutPlane( self ):
        '''
	    remove the cut plane from the scene graph
	    Arguments:
	        None	
	    Output:
	        None
        '''

	self.remAllCPlnActors( 						)

        if self.cutPlane != None:
	    indx = self.cutPlnSwt2.findChild(  	self.cutPlane.getActor())
	    if indx != -1:
	        self.cutPlnSwt2.removeChild( self.cutPlane.getActor())
	        del self.cutPlane
	    self.cutPlane = None

	indx = self.cutPlnSep.findChild(  self.cutPlnSwt1		)
	if indx != -1:
	    self.cutPlnSep.removeChild( self.cutPlnSwt1			)

	indx = self.cutPlnSep.findChild(  self.cutPlnSwt2		)
	if indx != -1:
	    self.cutPlnSep.removeChild( self.cutPlnSwt2			)

	self.viewer.mode(		acuSgViewer.MODE_VIEWING	)

#---------------------------------------------------------------------------
# addLoctActor:
#---------------------------------------------------------------------------

    def addLoctActor( self,     crd,
                      cnn,      topology,
                      name,     dataId,
                      display,  color,
                      vis       = True):
        '''
	    Add a locate (element) actor to the scene graph.
	    
	    Arguments:
	        crd	- a numarray of x,y,z coordinates
	        cnn	- a numarray of connectivity data
	        topology- "four_node_tet", "six_node_wedge" etc.
		display - display type
		color	- [ r, g, b ] values 
		vis	- visibility of the actor [ default = True ]
	    Output:
	        actor	- AcuSgActor object
        '''

        try:
            loctActor   = AcuSgActor(       parent  = self,
                                            crd     = crd,
                                            cnn     = cnn,
                                            topology= topology,
                                            name    = name,
                                            dataId  = dataId,
                                            disp    = display,
                                            color   = color,
                                            vis     = vis               )

            self.loctSep.addChild(	            loctActor		)
	    self.loctActors[self.nLoctActors]	    = loctActor
	    self.nLoctActors	+= 1
	    return loctActor

	except  acuSceneGraphError, e:
	    print e

#---------------------------------------------------------------------------
# remLoctActor:
#---------------------------------------------------------------------------

    def remLoctActor( self, loctActor ):
        '''
	    Remove a locate (element) actor from the scene graph.
	    
	    Arguments:
	        loctActor   - a locate actor
	    Output:
                None
        '''

        try:
            for i in self.loctActors.keys():
	        if loctActor == self.loctActors[i]:
	            indx	= self.loctSep.findChild(loctActor	)
		    if indx != -1:
	                self.loctSep.removeChild(	loctActor	)
	                del self.loctActors[i]
	                #self.nLoctActors	-= 1
	            else:
                        "The locate actor could not be removed form scene graph"
		    break
	    else:
                acuSceneGraphError, "Locate Actor could not be removed"

	except  acuSceneGraphError, e:
	    print e

#---------------------------------------------------------------------------
# clip:
#---------------------------------------------------------------------------
    def clip( self, flag = None ):
        '''
	    set/get the clip flag 
	    Arguments:
	        flag	- True or False	
	    Output:
	        None
        '''

        if flag == None:
	    return self.clipFlg

	self.clipFlg = flag
	self.clipPlane.on.setValue(		flag			)

#---------------------------------------------------------------------------
# setClipPlane:
#---------------------------------------------------------------------------
    def setClipPlane( self, plane ):
        '''
	    set the plane field value of a clip plane 
	    Arguments:
	        plane	- SbPlane objecting representing the plane
	    Output:
	        None
        '''
        if isinstance( plane, SbPlane):
	    self.clipPlane.plane.setValue(	plane			)
	else:
	    raise acuSceneGraphError, "plane should be an SbPlane object"

#---------------------------------------------------------------------------
# render: Renders the current scenegraph in the viewer
#---------------------------------------------------------------------------

    def render( self ):
        '''
	    render the viewer
	    Arguments:
	    	None
	    Output:
	    	None
        '''
	self.viewer.render()

#---------------------------------------------------------------------------
# viewModel: 
#---------------------------------------------------------------------------

    def viewModel( self ):
        '''
	    viewModel
	    Arguments:
	    	None
	    Output:
	    	None
        '''
	cam	= self.viewer.getCamera(				)
	cam.viewAll( self.dynObjects, self.viewer.getViewportRegion()	)

#---------------------------------------------------------------------------
# showPickableVol: Keeps only the volume actors in the scenegraph
#---------------------------------------------------------------------------

    def showPickableVol( self ):
        '''
	    To show only the pickable surfaces in the graphical window
	    Arguments:
	    	None
	    Output:
	    	None
        '''

        indx = self.dynObjects.findChild(	self.volSelection	)
	if indx == -1:
	    self.dynObjects.addChild(		self.volSelection	)

        indx = self.dynObjects.findChild(	self.srfSelection	)
	if indx != -1:
	    self.dynObjects.removeChild(	self.srfSelection	)

        indx = self.dynObjects.findChild(	self.linSelection	)
	if indx != -1:
	    self.dynObjects.removeChild(	self.linSelection	)

        indx = self.dynObjects.findChild(	self.pntSelection	)
	if indx != -1:
	    self.dynObjects.removeChild(	self.pntSelection	)

	#----- Misc. 04/09 H1 SH
        indx = self.dynObjects.findChild(	self.edgSelection	)
	if indx != -1:
	    self.dynObjects.removeChild(	self.edgSelection	)
	    
        indx = self.dynObjects.findChild(	self.geomSep		)
	if indx != -1:
	    self.dynObjects.removeChild(	self.geomSep		)

	self.viewer.redraw(						)


#---------------------------------------------------------------------------
# showPickableSrf: Keeps only the surface actors in the scenegraph
#---------------------------------------------------------------------------

    def showPickableSrf( self ):
        '''
	    To show only the pickable surfaces in the graphical window
	    Arguments:
	    	None
	    Output:
	    	None
        '''

        indx = self.dynObjects.findChild(	self.volSelection	)
	if indx != -1:
	    self.dynObjects.removeChild(	self.volSelection	)

        indx = self.dynObjects.findChild(	self.srfSelection	)
	if indx == -1:
	    self.dynObjects.addChild(		self.srfSelection	)

        indx = self.dynObjects.findChild(	self.linSelection	)
	if indx != -1:
	    self.dynObjects.removeChild(	self.linSelection	)

        indx = self.dynObjects.findChild(	self.pntSelection	)
	if indx != -1:
	    self.dynObjects.removeChild(	self.pntSelection	)

	#----- Misc. 04/09 H1 SH
        indx = self.dynObjects.findChild(	self.edgSelection	)
	if indx != -1:
	    self.dynObjects.removeChild(	self.edgSelection	)
	    
        #indx = self.dynObjects.findChild(	self.geomSep		)
	#if indx != -1:
	#    self.dynObjects.removeChild(	self.geomSep		)

	self.viewer.redraw(						)

#---------------------------------------------------------------------------
# showPickableEdg: Keeps only the Edg actors in the scenegraph
#---------------------------------------------------------------------------

    def showPickableEdg( self ):
        '''
	    To show only the pickable edge in the graphical window
	    Arguments:
	    	None
	    Output:
	    	None
        '''

        indx = self.dynObjects.findChild(	self.volSelection	)
	if indx != -1:
	    self.dynObjects.removeChild(	self.volSelection	)

        indx = self.dynObjects.findChild(	self.srfSelection	)
	if indx != -1:
	    self.dynObjects.removeChild(	self.srfSelection	)

        indx = self.dynObjects.findChild(	self.linSelection	)
	if indx != -1:
	    self.dynObjects.removeChild(	self.linSelection	)

        indx = self.dynObjects.findChild(	self.pntSelection	)
	if indx != -1:
	    self.dynObjects.removeChild(	self.pntSelection	)

	#----- Misc. 04/09 H1 SH
        indx = self.dynObjects.findChild(	self.edgSelection	)
	if indx == -1:
	    self.dynObjects.addChild(	        self.edgSelection	)
	    
        #indx = self.dynObjects.findChild(	self.geomSep		)
	#if indx != -1:
	#    self.dynObjects.removeChild(	self.geomSep		)

	self.viewer.redraw(						)
	
#---------------------------------------------------------------------------
# getVolActor: Returns a volume actor by name
#---------------------------------------------------------------------------

    def getVolActor( self, name ):
        '''
	    Return the volume actor by name

	    Arguments:
	        name		- name of the actor
	    Output:
	        volActor	- AcuSgActor object representing a volume
        '''

        for i in range( self.nVolActors ):
	    if self.volActors[i].name == name:
	        return self.volActors[i]
	return None


#---------------------------------------------------------------------------
# getSrfActor: Returns a surface actor by name
#---------------------------------------------------------------------------

    def getSrfActor( self, name ):
        '''
	    Return the surface actor by name

	    Arguments:
	        name		- name of the actor
	    Output:
	        srfActor	- AcuSgActor object representing a surface
        '''

        for i in range( self.nSrfActors ):
	    if self.srfActors[i].name == name:
	        return self.srfActors[i]
	return None

#---------------------------------------------------------------------------
# visibleAllVolActors : Turn the visibility on for all the volume
#                       actors if all of them is off
#---------------------------------------------------------------------------

    def visibleAllVolActors( self ):
        '''
	    Check for make sure at least one of the volumes are visible.
            If none is visible, then turn the visibility on for all.

	    Arguments:
	        None
	    Output:
	        None
        '''
        
        visFlag        = False       
        for i in range( self.nVolActors ):
	    if self.volActors[i].visibility():
                visFlag = True
                break
        
        if not visFlag:
            self.visVolFlag = True
            for i in range( self.nVolActors ):
                self.volActors[i].visibilityOn( )
              
#---------------------------------------------------------------------------
# visibleAllSrfActors : Turn the visibility on for all the surface
#                       actors if all of them is off
#---------------------------------------------------------------------------

    def visibleAllSrfActors( self ):
        '''
	    Check for make sure at least one of the surfaces are visible.
            If none is visible, then turn the visibility on for all.

	    Arguments:
	        None
	    Output:
	        None
        '''
        
        visFlag        = False       
        for i in range( self.nSrfActors ):
	    if self.srfActors[i].visibility():
                visFlag = True
                break
        
        if not visFlag:
            self.visSrfFlag = True
            for i in range( self.nSrfActors ):
                self.srfActors[i].visibilityOn( )

#---------------------------------------------------------------------------
# visibleAllEdgActors : Turn the visibility on for all the edge
#                       actors if all of them is off
#---------------------------------------------------------------------------

    def visibleAllEdgActors( self ):
        '''
	    Check for make sure at least one of the edges are visible.
            If none is visible, then turn the visibility on for all.

	    Arguments:
	        None
	    Output:
	        None
        '''
        
        visFlag        = False       
        for i in range( self.nEdgActors ):
	    if self.edgActors[i].visibility():
                visFlag = True
                break
        
        if not visFlag:
            self.visEdgFlag = True
            for i in range( self.nEdgActors ):
                self.edgActors[i].visibilityOn( )

#---------------------------------------------------------------------------
# returnToLastVis : Turn the visibility off for all the surface or volume
#                   actors.
#---------------------------------------------------------------------------

    def returnToLastVis( self ):
        '''
            Turn the visibility off for all the surface or volume
            actors if its flag(visFlag) is True.

	    Arguments:
	        None
	    Output:
	        None
        '''
        
        if self.visVolFlag :
            for i in range( self.nVolActors ):
                self.volActors[i].visibilityOff( )

        if self.visSrfFlag:
            for i in range( self.nSrfActors ):
                self.srfActors[i].visibilityOff( )

        if self.visEdgFlag:
            for i in range( self.nEdgActors ):
                self.edgActors[i].visibilityOff( )

        self.visVolFlag = False      
        self.visSrfFlag = False
        self.visEdgFlag = False
            
        
#---------------------------------------------------------------------------
# getLinActor: Returns a line actor by name
#---------------------------------------------------------------------------

    def getLinActor( self, name ):
        '''
	    Return the line actor by name

	    Arguments:
	        name		- name of the actor
	    Output:
	        linActor	- AcuSgActor object representing a line
        '''

        for i in range( self.nLinActors ):
	    if self.linActors[i].name == name:
	        return self.linActors[i]
	return None

#---------------------------------------------------------------------------
# getPntActor: Returns a point actor by name
#---------------------------------------------------------------------------

    def getPntActor( self, name ):
        '''
	    Return the point actor by name

	    Arguments:
	        name		- name of the actor
	    Output:
	        pntActor	- AcuSgActor object representing a point
        '''

        for i in range( self.nPntActors ):
	    if self.pntActors[i].name == name:
	        return self.pntActors[i]
	return None

#----- Misc. 04/09 H1 SH
#---------------------------------------------------------------------------
# getEdgActor: Returns a edge actor by name
#---------------------------------------------------------------------------

    def getEdgActor( self, name ):
        '''
	    Return the edge actor by name

	    Arguments:
	        name		- name of the actor
	    Output:
	        edgActor	- AcuSgActor object representing an edge
        '''

        for i in range( self.nEdgActors ):
	    if self.edgActors[i].name == name:
	        return self.edgActors[i]
	return None
    
#---------------------------------------------------------------------------
# getExpFileTypes: Returns a file format types that the image can be saved
#---------------------------------------------------------------------------
    def getExpFileTypes( self ):
        '''
	    Return the file formats that are supported for exporting

	    Arguments:
	        None
	    Output:
	        formatList	- [ 'png', 'ps', 'iv', 'tiff', 'jpeg' ...]
        '''

	nTypes	= self.offRen.getNumWriteFiletypes( 			)

	imageFormat	= []

	#--- These two are always supported and not returned by fn. below
	
	imageFormat.append(			"iv"			)
	imageFormat.append(			"wrl"			)
	imageFormat.append(			"wrz"			)
	imageFormat.append(			"u3d"			)
	imageFormat.append(			"pdf"			)
	imageFormat.append(			"idtf"			)
	imageFormat.append(			"html"			)
	imageFormat.append(			"rgb"			)
	imageFormat.append(			"gif"			)

	for i in range( nTypes ):
	    extList, fName, descr = self.offRen.getWriteFiletypeInfo( i )
	    imageFormat.append(		extList.pop()			)

	imageFormat.sort(                                               )
	return imageFormat

#---------------------------------------------------------------------------
# _pruneModel: Removes selections and annotations node for save as iv, wrl options
#---------------------------------------------------------------------------

    def _pruneModel( self,  annotations,
                            curNode,
                            parent              = None,
                            removeInvisNodes    = False ):

        drawStyleInvisible = False

        for i in range( curNode.getNumChildren( ) ):

            node = curNode.getChild( i )

            #----- Convert selections to separators

            if isinstance( node, SoSelection ):
                sep = SoSeparator( )
                for j in range( node.getNumChildren( ) ):
                    sep.addChild( node.getChild( j ) )
                sep.setName( node.getName( ) )
                curNode.replaceChild( node, sep )
                node = sep

            #----- Remove invisible models

            if removeInvisNodes:
                if isinstance( node, SoDrawStyle ):
                    drawStyleInvisible = ( node.style.getValue() == SoDrawStyle.INVISIBLE )
                else:
                    curNode.removeChild( node )

            #----- Find annotations and continue recursive searching for group nodes

            if isinstance( node, SoAnnotation ):
                annotations.append( (node, curNode) )
                
            elif isinstance( node, SoGroup ) and node.getNumChildren( ) > 0:
                self._pruneModel( annotations, node, curNode )
                
#---------------------------------------------------------------------------
# saveAsIV
#---------------------------------------------------------------------------

    def saveAsIV( self,     fileName,
                            sceneGraph,
                            binaryFlag          = False,
                            removeInvisNodes    = False ):

        sceneGraph = sceneGraph.copy( )
        sceneGraph.removeChild( sceneGraph.getByName( "stc_objects" ) )
        
        annotations = []        
        self._pruneModel( annotations, sceneGraph, None, removeInvisNodes )
        for ( node, parent ) in annotations:
             parent.removeChild( node )

        writeAction = SoWriteAction( )
        writeAction.getOutput( ).setBinary( binaryFlag )                    
        writeAction.getOutput( ).openFile( fileName )
        writeAction.apply( sceneGraph )                    
        writeAction.getOutput( ).closeFile( )

#---------------------------------------------------------------------------
# saveAsVRML
#---------------------------------------------------------------------------

    def saveAsVRML( self,   fileName,
                            format,
                            sceneGraph,
                            binaryFlag          = False,
                            removeInvisNodes    = False ):

        sceneGraph = sceneGraph.copy( )
        sceneGraph.removeChild( sceneGraph.getByName( "stc_objects" ) )
        
        annotations = []        
        self._pruneModel( annotations, sceneGraph, None, removeInvisNodes )
        for ( node, parent ) in annotations:
             parent.removeChild( node )

        vrml2Action = SoToVRML2Action( )   
        vrml2Action.apply( sceneGraph )
        vrml2SceneGraph = vrml2Action.getVRML2SceneGraph( )
        
        writeAction = SoWriteAction( )
        writeAction.getOutput( ).setBinary( False )
        writeAction.getOutput( ).setHeaderString( '#VRML V2.0 utf8' )

        if format == 'wrl' and binaryFlag == False:                                
            writeAction.getOutput( ).openFile( fileName )            
            writeAction.apply( vrml2SceneGraph )                    
            writeAction.getOutput( ).closeFile( )

        else:        
            tmpFile = fileName + '.tmp'     
            writeAction.getOutput().openFile( tmpFile )                    
            writeAction.apply( vrml2SceneGraph )
            writeAction.getOutput().closeFile( )
                        
            fin = open( tmpFile, 'rb' )
            fout = gzip.open( fileName, 'wb' )
            fout.writelines( fin )
            fout.close( )                                        
            fin.close( )
                        
            os.remove( tmpFile )
            
#---------------------------------------------------------------------------
# saveFile:
#          The size of the image is currently hardcoded.
#          Could be an argument in future. [ see the code below. ]
#
#---------------------------------------------------------------------------

    def saveFile( self,     fileName,
                            format,
                            width       = None,
                            height      = None,
                            binaryFlag  = True ):

        '''
	    exports the graphic window in various file formats

	    Arguments:
	        fileName	-
	        format		- png, ps , iv , jpeg  etc.
		                  this list is obtained from getExpFileTypes()
	        binaryFlag	- For 'iv' format, this flat allows to
		                  save in binary/ascii format [ True ]
	    Output:
	        None
        '''

        binaryFlag = False # Test        
                
        if format == 'iv':
            self.saveAsIV( fileName, self.viewer.getSceneGraph( ), binaryFlag )
                
        elif format == 'wrl' or format == 'wrz':
            self.saveAsVRML( fileName, format, self.viewer.getSceneGraph( ), binaryFlag )

        elif format == 'idtf':
            acuConvertU3D.saveAsIdtf( self.viewer.getSceneGraph( ),
                                      None,
                                      fileName  )
            
        elif format == 'u3d':
            acuConvertU3D.saveAsU3d( self.viewer.getSceneGraph( ),
                                     None,
                                     None,
                                     fileName,
                                     True,
                                     0 )           

        elif format == 'pdf':
            acuConvertU3D.saveAsPdf( self.viewer.getSceneGraph( ),
                                     None,
                                     None,
                                     None,
                                     fileName,
                                     True,
                                     True,
                                     True,
                                     0,
                                     width,
                                     height,
                                     None,
                                     self.viewer.getBackgroundColor( ).getValue( ),
                                     self.display( self.actors.keys( )[-1] ),
                                     False )
            
        elif format == 'html':                
            acuConvertU3D.saveAsHtml( self.viewer.getSceneGraph( ),
                                      None,
                                      None,
                                      None,
                                      None,
                                      fileName,
                                      True,
                                      True,
                                      True,
                                      0,
                                      width,
                                      height,
                                      None,
                                      self.viewer.getBackgroundColor( ).getValue( ),
                                      self.display( self.actors.keys( )[-1] ),
                                      False ) 
          	
	else:
	    if self.offRen.isWriteSupported( SbName( format )	):

		vp		= self.viewer.getViewportRegion(	)
		dpi      	= 150

		if not ( width and height):
                    imgPixSz	= vp.getViewportSizePixels()
                    imgIn	= SbVec2f()
                    pixPerIn	= SoOffscreenRenderer.getScreenPixelsPerInch()
                    imgIn.setValue( imgPixSz[0]/pixPerIn, imgPixSz[1]/pixPerIn)
                    width       = imgIn[0] * dpi
                    height      = imgIn[1] * dpi
                    
                res        	= SbVec2s(				)
                res.setValue( 	                width,  height	        )

                vpr		= self.offRen.getViewportRegion(	)
                vpr.setWindowSize(		res		        )
                vpr.setPixelsPerInch(		dpi		        )

	        offSep	= SoSeparator(					)

		mainCam	= self.viewer.getCamera(			)
		offSep.addChild( 	mainCam 	                )
		
		rot	= mainCam.orientation.getValue(			)
		lookat	= SbVec3f(	0,0,-1				)
		rot.multVec(		lookat,lookat			)
		light	= SoDirectionalLight(				)
		light.direction.setValue(	lookat			)
		offSep.addChild( 		light 			)
	
		offSep.addChild( 	self.viewer.getSceneGraph() 	)

                #----- Start of Setting Background
		
		self.offRen.setBackgroundColor(
                    self.viewer.getBackgroundColor( )                   )

		if self.viewer.bgType != 'solid':                   

                    backgroundSep = SoSeparator(                        )
                    bgCam = SoOrthographicCamera(                       )
                    bgCam.viewportMapping.setValue(SoCamera.LEAVE_ALONE )
                    bgCam.farDistance.setValue(     2                   )
                    backgroundSep.addChild( bgCam                       )
                    backgroundSep.addChild( self.viewer.backgroundSep   )                    

                    offSep.addChild(            backgroundSep           )         
                    
                #----- End of Setting Background	 
                
		if not self.offRen.render( offSep ):
		    raise acuSceneGraphError, "cannot render the image"

                self.offRen.writeToFile( SbString( str(fileName) ), 
					 SbName(format )		)
	    else:
	        raise acuSceneGraphError, \
			"format <%s> is not supported" % format
	
#---------------------------------------------------------------------------
# _setOffscreenRenderer:
#---------------------------------------------------------------------------

    def _setOffscreenRenderer( self ):
        '''
	    Sets up the SoOffscreenRenderer object for exporting files

	    Arguments:
	        None
	    Output:
	        None
        '''

	vpr		= SbViewportRegion(				)
	self.offRen	= SoOffscreenRenderer( 		vpr 		)

#---------------------------------------------------------------------------
# setLineWidth:
#---------------------------------------------------------------------------

    def setLineWidth( self, width = None ):
        '''
	    sets the line width used in various actors

	    Arguments:
	        width	-  a valid width value
	    Output:
	        None
        '''

	if width != None:
	    ( lWd, hWd )	= self.linWidthLimits.getValue(		)
	    if width < lWd:
	        width	= lWd
	    
	    if width > hWd:
	        width	= hWd
	    for id in self.actors:
	        self.actors[id].lineWidth(		width		)

#---------------------------------------------------------------------------
# setShading:
#---------------------------------------------------------------------------

    def setShading( self, shading = None, phongCrAngle = math.pi/2.01 ):
        '''
	    sets the shading used in various actors

	    Arguments:
	        shading	-   'Flat', 'Gouraud', 'Phong' 
	    Output:
	        None
        '''

	materialBinding = SoMaterialBinding.PER_FACE
	creaseAngle = None
	grFlag = False
        shading = string.upper(                 shading                 )
	if shading != None:
	    if shading == 'FLAT':
	        creaseAngle = 0
	    
	    if shading == 'GOURAUD':
	        materialBinding = SoMaterialBinding.PER_VERTEX
	        creaseAngle = 0.2
	        grFlag = True
			
	    if shading == 'PHONG':
	        creaseAngle = phongCrAngle
			
	    for id in self.actors:			
		if type(self.actors[id]) == AcuSgActor:
		    self.actors[id].shadingModel( materialBinding, creaseAngle, grFlag)				       	
			
#---------------------------------------------------------------------------
# toggleBandedColor: 
#---------------------------------------------------------------------------

    def toggleBandedColor( self ):
        
        self.setCmap( cmap = "banded32" )
        
        for actor in self.actors.values( ):
            actor.display( style = "contour" )
			
#---------------------------------------------------------------------------
# setScalar: set the scalar vector
#---------------------------------------------------------------------------

    def setScalar( self,    scalar      = None,  name       = "",
                            sclrMinVal  = None,  sclrMaxVal = None ):
                   
        """
            Function to set the scalar vector.

	    Arguments:
                scalar      - Scaler vector value
                name        - Scaler name
                sclrMinVal  - Set scaler vector minimum value
                sclrMaxVal  - Set scaler vector maximum value                
                
	    Output: 
	        None
	"""        
        
        if scalar != None:
            if type( scalar ) != numarray.numarraycore.NumArray:
                scalar = numarray.array( scalar )
            
            if scalar.getrank( ) != 1 and scalar.shape[1] != 1:
                raise acuSceneGraphError, "Scalar shape must be nNodes * 1."

            self.scalarName = name
            self.scalar     = scalar

            self.tmpSclrMin = scalar.min( )
            self.tmpSclrMax = scalar.max( ) 

            if sclrMinVal != None:                
                self.setSclrMinVal( sclrMinVal )

            if sclrMaxVal != None:                
                self.setSclrMaxVal( sclrMaxVal )          
            
        else:
            raise acuSceneGraphError, "No scalar is specified."

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

        sclrMinVal = self.setSclrMinVal( sclrMinVal )
        sclrMaxVal = self.setSclrMaxVal( sclrMaxVal )

        #---- CFDCalc: Heat Sink Calc ; item 6 11/19/10; NP 11/24/10
        for actor in self.actors.values( ):
            actor.setSclrLimits( sclrMinVal, sclrMaxVal )

        for actor in self.isoSrfActors.values( ):
            actor.setSclrLimits( sclrMinVal, sclrMaxVal )
        #---- NP
        
        return ( sclrMinVal, sclrMaxVal )
			
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

        self.sclrMinVal = sclrMinVal     

        if self.sclrMinVal != None:
            return self.sclrMinVal
        else:
            return self.tmpSclrMin

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

        self.sclrMaxVal = sclrMaxVal

        if self.sclrMaxVal != None:
            return self.sclrMaxVal
        else:
            return self.tmpSclrMax

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

        if cmap != None:
            mapObj      = AcuCmap(                                      )
            self.cmap   = mapObj.getCmap( cmap                          )

        else:
             raise acuSceneGraphError, "No cmap specified."
            
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

        if vel != None:
            if type( vel ) != numarray.numarraycore.NumArray:
                vel = numarray.array( vel )
            
            if vel.getrank( ) != 2 or vel.shape[1] != 3:
                raise acuSceneGraphError, "Vel shape must be nNodes * 3."

            self.velName    = name
            self.vel        = vel

            if velScale == None:
                self.tmpVelScale = 1.0               
            else:
                self.setVelScale( velScale )

            if self.velScalarType == "magnitude":
                self.setVelScalar( velScalarType = "magnitude" )
                
        else:
            raise acuSceneGraphError, "No vel is specified."   

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

        if velScale != None:
            if velScale > 0:
                self.velScale = velScale
            else:
                raise acuSceneGraphError, "VelScale cannot be negative."

        if self.velScale != None:
            return self.velScale
        else:
            return self.tmpVelScale

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

        if velScalarType == "magnitude":
            if self.vel != None:
                self.velScalar = ( self.vel[:, 0] * self.vel[:, 0] + \
                                   self.vel[:, 1] * self.vel[:, 1] + \
                                   self.vel[:, 2] * self.vel[:, 2] ) \
                                   ** 0.5
            else:
                raise acuSceneGraphError, "No vel found for setting velScalar."

        elif velScalar != None:
            if type( velScalar ) != numarray.numarraycore.NumArray:
                velScalar = numarray.array( velScalar )
            
            if velScalar.getrank( ) != 1 and velScalar.shape[1] != 1:
                raise acuSceneGraphError, "velScalar shape must be nNodes * 1."

            self.velScalar  = velScalar                          
            
        else:
            raise acuSceneGraphError, "No velScalar is specified."

        self.velScalarType = velScalarType

        if velSclrMinVal == None:
            self.tmpVelSclrMin = self.velScalar.min( )               
        else:
            self.setVelSclrMinVal( velSclrMinVal )

        if velSclrMaxVal == None:
            self.tmpVelSclrMax = self.velScalar.max( )               
        else:
            self.setVelSclrMaxVal( velSclrMaxVal )
    
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

        velSclrMinVal = self.setVelSclrMinVal( velSclrMinVal )
        velSclrMaxVal = self.setVelSclrMaxVal( velSclrMaxVal )
        
        return ( velSclrMinVal, velSclrMaxVal )
			
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

        if velSclrMinVal != None:
            self.velSclrMinVal = velSclrMinVal

        if self.velSclrMinVal != None:
            return self.velSclrMinVal
        else:
            return self.tmpVelSclrMin

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

        if velSclrMaxVal != None:
            self.velSclrMaxVal = velSclrMaxVal

        if self.velSclrMaxVal != None:
            return self.velSclrMaxVal
        else:
            return self.tmpVelSclrMax

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

        if velWidth != None:
            if velWidth > 0:
                self.velWidth = velWidth
            else:
                raise acuSceneGraphError, "VelWidth cannot be negative."

        return self.velWidth

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

        if velArrowType != None:            
            if velArrowType in [ "none", "white_tip", "2d", "arrow", "white_tip_arrow", "pyramid" ]:
                self.velArrowType = velArrowType
            else:
                raise acuSceneGraphError, "Invalid velArrowType."

        return self.velArrowType   

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

        if velColorType != None:            
            if velColorType in [ "constant", "per_node" ]:
                self.velColorType = velColorType
            else:
                raise acuSceneGraphError, "Invalid velColorType."

        return self.velColorType                

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

        if velColor != None:
            self.velColor = numarray.array( velColor, shape = ( 1, 3 ) )             

        return self.velColor

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

        if velCmap != None:
            mapObj          = AcuCmap(                                  )
            self.velCmap    = mapObj.getCmap( velCmap                   )

        return self.velCmap

#---------------------------------------------------------------------------
# updateVelNormal: update velocity vector 2D arrows direction
#---------------------------------------------------------------------------

    def updateVelNormal( self, velNormal = None ):

        """
            Function to update velocity vector 2D arrows direction

             Arguments:
                velNormal   - The velocity vector 2D arrows direction
                
	    Output: 
	        None
	"""

        if velNormal != None:            
            self.velNormal = SbVec3f( velNormal )
        else:
            self.velNormal = SbVec3f( ( 0, 0, -1 ) )
            camOrt = self.viewer.getCamera( ).orientation.getValue( )
            camOrt.multVec( self.velNormal, self.velNormal )
            
        for actor in self.actors.values( ):
            if isinstance( actor, AcuSgActor ):
                actor.updateVelNormal( self.velNormal )
		
###---------------------------------------------------------------------------
### setHighlightTypes:
###---------------------------------------------------------------------------
##
	        #----- Misc. 6/07 F2
##    def setHighlightTypes( self, highlightTypes = None ):
##        '''
##	    sets the highlight type in various actors
##
##	    Arguments:
##	        highlightTypes	-  a list of highlight type
##	    Output:
##	        None
##        '''
##
##	if highlightTypes != None:
##
##	    for id in self.actors:
##                for value in highlightTypes:
##                    self.actors[id].highlightType(	display = value[0],
##                                                        type    = value[1]  )

#---------------------------------------------------------------------------
# setPointSize:
#---------------------------------------------------------------------------

    def setPointSize( self, size = None ):
        '''
	    sets the point size of the points used in various actors

	    Arguments:
	        size	-  a valid point size
	    Output:
	        None
        '''

	if size != None:
	    ( lSz, hSz )	= self.pntSizeLimits.getValue(		)
	    if size < lSz:
	        size = lSz

	    if size > hSz:
		size = hSz

	    for id in self.actors:
	        self.actors[id].pointSize(		size		)

#---------------------------------------------------------------------------
# addEigenmodeActor: Create an eigenmode actor
#---------------------------------------------------------------------------

    def addEigenmodeActor( self, crd, cnn,  topology,  display = "solid",
                           transparency = True,
                           transLevel   = 0.5,
                           actorName    = "eigenmode",
                           color        = [255, 0, 0] ):

        '''
	    creates an eigenmode actor
	    Arguments:
	        crd	    - a numarray of x,y,z coordinates
	        cnn	    - a numarray of connectivity data
	        topology    - "four_node_tet", "six_node_wedge" etc.
		display     - "none","wireframe","mesh","outline" etc.["none"]
                transparency- boolean, whether transparency is on or off
                transLevel  - transparency level
		actorName   - Name of the actor
		color	    - [ r, g, b ] values 
	    Output:
	        actor	    - AcuSgActor object
        '''

        try:
	    dataId	    = actorName
	    name	    = actorName
            eignmodeActor   = AcuSgActor(   parent  = self,
                                            crd     = crd,
                                            cnn     = cnn,
                                            topology= topology,
                                            name    = name,
                                            dataId  = dataId,
                                            disp    = display,
                                            color   = color,
                                            vis     = True,
                                            trans   = transparency,
                                            transVal= transLevel        )

            self.eignmodeSep.addChild(	            eignmodeActor	)
	    self.eignmodeActors[self.nEignmodeActors]= eignmodeActor
	    self.nEignmodeActors    += 1
	    return eignmodeActor
        except:
	    raise acuSceneGraphError, "error while adding eigenmode actor"

#---------------------------------------------------------------------------
# remEigenmodeActor:
#---------------------------------------------------------------------------

    def remEigenmodeActor( self, eigenmodeActor ):
        '''
	    Remove an Eigenmode actor from the scene graph.
	    
	    Arguments:
	        eigenmodeActor   - an Eigenmode actor
	    Output:
                None
        '''

        try:
            for i in self.eignmodeActors.keys():
	        if eigenmodeActor == self.eignmodeActors[i]:
	            indx	= self.eignmodeSep.findChild(eigenmodeActor)
		    if indx != -1:
	                self.eignmodeSep.removeChild(	eigenmodeActor	)
	                del self.eignmodeActors[i]
	                #self.nEignmodeActors	-= 1
	            else:
                        "The Eigenmode actor could not be removed form scene graph"
		    break
	    else:
                acuSceneGraphError, "Eigenmode Actor could not be removed"

	except  acuSceneGraphError, e:
	    print e

#---------------------------------------------------------------------------
# addJmagActor: Create an JMAG actor
#---------------------------------------------------------------------------

    def addJmagActor(   self, crd, cnn,  topology,  display = "solid",
                        transparency = True,
                        transLevel   = 0.5,
                        actorName    = "jmag",
                        color        = [255, 0, 0]
                    ):

        '''
	    creates an JMAG actor
	    Arguments:
	        crd	    - a numarray of x,y,z coordinates
	        cnn	    - a numarray of connectivity data
	        topology    - "four_node_tet", "six_node_wedge" etc.
		display     - "none","wireframe","mesh","outline" etc.["none"]
                transparency- boolean, whether transparency is on or off
                transLevel  - transparency level
		actorName   - Name of the actor
		color	    - [ r, g, b ] values 
	    Output:
	        actor	    - AcuSgActor object
        '''

        try:
	    dataId	    = actorName
	    name	    = actorName
            jmagActor       = AcuSgActor(   parent  = self,
                                            crd     = crd,
                                            cnn     = cnn,
                                            topology= topology,
                                            name    = name,
                                            dataId  = dataId,
                                            disp    = display,
                                            color   = color,
                                            vis     = True,
                                            trans   = transparency,
                                            transVal= transLevel        )

            self.jmagSep.addChild(	    jmagActor	                )
	    self.jmagActors[self.nJmagActors]   = jmagActor
	    self.nJmagActors += 1
	    return jmagActor
        except:
	    raise acuSceneGraphError, "error while adding JMAG actor"

#---------------------------------------------------------------------------
# remJmagActor:
#---------------------------------------------------------------------------

    def remJmagActor( self, jmagActor ):
        '''
	    Remove an JMAG actor from the scene graph.
	    
	    Arguments:
	        jmagActor   - an JMAG actor
	    Output:
                None
        '''

        try:
            for i in self.jmagActors.keys():
	        if jmagActor == self.jmagActors[i]:
	            indx	= self.jmagSep.findChild(   jmagActor   )
		    if indx != -1:
	                self.jmagSep.removeChild(	    jmagActor	)
	                del self.jmagActors[i]
	                #self.nJmagActors	-= 1
	            else:
                        "The JMAG actor could not be removed form scene graph"
		    break
	    else:
                acuSceneGraphError, "JMAG Actor could not be removed"

	except  acuSceneGraphError, e:
	    print e

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

        self.acuTform.setAllSettings(					)
        self.viewer.setAllSettings(                                     )

#---------------------------------------------------------------------------
# clearTransMtx
#---------------------------------------------------------------------------

    def clearTransMtx(self):

        for id in self.actors:			
	    if type( self.actors[id] ) == AcuSgActor:
		self.actors[id].clearTransMtx( )

#---------------------------------------------------------------------------
# explodeView
#---------------------------------------------------------------------------

    def explodeView( self, factor = None ):        
    
        if factor == None:
            return

        if factor == 0:
            self.explodedView = False
        else:
            self.explodedView = True

        #----- Center of Model

        xL  =  1e308
        xR  = -1e308
        yL  =  1e308
        yR  = -1e308
        zL  =  1e308
        zR  = -1e308        
        
        actors = self.actors.values( )
        actors.append( self )

        for actor in actors:
            axL = actor.crd[:, 0].min( )
            axR = actor.crd[:, 0].max( )
            ayL = actor.crd[:, 1].min( )
            ayR = actor.crd[:, 1].max( )
            azL = actor.crd[:, 2].min( )
            azR = actor.crd[:, 2].max( )

            if axL < xL:
                xL = axL
            if axR > xR:
                xR = axR
            if ayL < yL:
                yL = ayL
            if ayR > yR:
                yR = ayR
            if azL < zL:
                zL = azL
            if azR > zR:
                zR = azR

        cx  = 0.5 * ( xL + xR )
        cy  = 0.5 * ( yL + yR )
        cz  = 0.5 * ( zL + zR )

        X_C = numarray.array( ( cx, cy, cz ) )

        #----- Center of Actor and Translation

        for actor in self.actors.values( ):
            if actor.center != None:
                x_c = numarray.array( actor.center )

            else:               
                xL  = actor.crd[:, 0].min( )
                xR  = actor.crd[:, 0].max( )
                yL  = actor.crd[:, 1].min( )
                yR  = actor.crd[:, 1].max( )
                zL  = actor.crd[:, 2].min( )
                zR  = actor.crd[:, 2].max( )

                cx  = 0.5 * ( xL + xR )
                cy  = 0.5 * ( yL + yR )
                cz  = 0.5 * ( zL + zR )

                x_c = numarray.array( ( cx, cy, cz ) )

            actor.translate( factor * ( x_c - X_C ) ) 

#---------------------------------------------------------------------------
# _getActorProp:
#---------------------------------------------------------------------------

    def _getActorProp( self, actor ):

        if actor != None and actor != self.dynObjects \
           and not isinstance( actor, AcuSgActor ):
            raise acuSceneGraphError, "Invalid actor specified for clipping"

        if actor == None or actor == self.dynObjects:            
            actor = self.dynObjects
            container = self 
        else:
            container = actor
            
        findParent = SoSearchAction( )
	findParent.setNode( actor )
	findParent.apply( self.root )		
	parent = findParent.getPath( ).getNodeFromTail( 1 )	    

        return actor, container, parent

#---------------------------------------------------------------------------
# _findMatNodes: 
#---------------------------------------------------------------------------

    def _findMatNodes( self, materials, curNode ):

        for i in range( curNode.getNumChildren( ) ):
            node = curNode.getChild( i )

            if isinstance( node, SoMaterial ):
                materials.append( node )
				
	    elif isinstance( node, SoGroup ) and node.getNumChildren( ) > 0:
		self._findMatNodes( materials, node )	

#---------------------------------------------------------------------------
# _insertClipShape: 
#---------------------------------------------------------------------------

    def _insertClipShape( self, clipShape ):     

        actor, container, parent = self._getActorProp( clipShape.actor )

        if container.clipTranMat == None:
            container.clipTranMat = SoMaterial( )
            container.clipTranMat.setName( "ClipTransparentMat" )
            container.clipTranMat.transparency.setValue( 1.0 )

        if container.clipOpaqMat == None:			
            container.clipOpaqMat = SoMaterial( )
            container.clipOpaqMat.setName( "ClipOpaqueMat" )
            container.clipOpaqMat.transparency.setValue( 0.0 )

        #----- Always search for mat nodes, since the model may has been updated
            
        container.clipNestedMats = []
        self._findMatNodes( container.clipNestedMats, actor )
        for mat in container.clipNestedMats:
            mat.transparency.setIgnored( True )

        if container.clipShapeActorSep == None:
            container.clipShapeActorSep = SoSeparator( )
            container.clipShapeActorSep.setName( "ClipShapeActorSep" )
        if container.clipShapeActorSep.findChild( clipShape ) == -1:
            container.clipShapeActorSep.addChild( clipShape )

        if container.clipShapeActorList == None:
            container.clipShapeActorList = []
        if clipShape not in container.clipShapeActorList:
            container.clipShapeActorList.append( clipShape )

        actorIndex = parent.findChild( actor )       

        if parent.findChild( container.clipTranMat ) == -1:           
            parent.insertChild( container.clipTranMat, actorIndex )

        if parent.findChild( container.clipOpaqMat ) == -1:            
            parent.insertChild( container.clipOpaqMat, actorIndex + 2 )

        if parent.findChild( container.clipShapeActorSep ) == -1:           
            parent.insertChild( container.clipShapeActorSep, actorIndex + 3 )            

#---------------------------------------------------------------------------
# _delClipShape: 
#---------------------------------------------------------------------------

    def _delClipShape( self, clipShape ):

        actor, container, parent = self._getActorProp( clipShape.actor )

        if container.clipShapeActorSep != None and \
           container.clipShapeActorSep.findChild( clipShape ) != -1:
            container.clipShapeActorSep.removeChild( clipShape )

        if container.clipShapeActorList != None and \
           clipShape in container.clipShapeActorList:
            container.clipShapeActorList.remove( clipShape )

        #---- if no clip actor is found, revert the seceneGraph back to the previous state
            
        if container.clipShapeActorList == None or \
           len( container.clipShapeActorList ) == 0:        
            if container.clipTranMat != None and \
               parent.findChild( container.clipTranMat ) != -1 :
                parent.removeChild( container.clipTranMat )

            if container.clipOpaqMat != None and \
               parent.findChild( container.clipOpaqMat ) != -1 :
                parent.removeChild( container.clipOpaqMat )

            if container.clipShapeActorSep != None and \
               parent.findChild( container.clipShapeActorSep ) != -1 :
                parent.removeChild( container.clipShapeActorSep )
                
            if container.clipNestedMats != None:
                for mat in container.clipNestedMats:
                    mat.transparency.setIgnored( False )
                
#---------------------------------------------------------------------------
# _activeClipShape: 
#---------------------------------------------------------------------------

    def _activeClipShape( self, clipShape, activate ):

        if activate == True:
            self._insertClipShape( clipShape )
        else:
            self._delClipShape( clipShape ) 
        
#---------------------------------------------------------------------------
# addClipPlane
#---------------------------------------------------------------------------
    
    def addClipPlane( self, center,
                            direction,
                            side    = 'up',
                            actor   = None,
                            name    = None  ):

        actor, container, parent = self._getActorProp( actor )

        clipPlane = AcuSgClipShape( sceneGraph          = self,
                                    actor               = actor,
                                    clipShapeType       = 'plane',
                                    clipSide            = side,
                                    clipPlanePointList  = [ center, direction ],       
                                    name                = name )       

        return clipPlane

#---------------------------------------------------------------------------
# delClipPlane
#---------------------------------------------------------------------------
    
    def delClipPlane( self, clipPlane ):

        self._delClipShape( clipPlane ) 

#---------------------------------------------------------------------------
# addClipBox
#---------------------------------------------------------------------------

    def addClipBox( self,   xmin,
                            xmax,
			    ymin,
                            ymax,
                            zmin,
                            zmax,	
                            actor   = None,
                            name    = None  ):
	
        actor, container, parent = self._getActorProp( actor )

        clipBox = AcuSgClipShape( sceneGraph          = self,
                                  actor               = actor,
                                  clipShapeType       = 'box',                              
                                  clipBoxBoundList    = [ xmin, xmax, ymin, ymax, zmin, zmax ],
                                  name                = name )
        
        return clipBox

#---------------------------------------------------------------------------
# delClipBox
#---------------------------------------------------------------------------
	
    def delClipBox( self, clipBox ):

        self._delClipShape( clipBox )

#---------------------------------------------------------------------------
# setClipTrans:
#---------------------------------------------------------------------------
                
    def setClipTrans( self, transparent   = False,
                            transVal      = 0.5,
                            actor         = None  ):  

        actor, container, parent = self._getActorProp( actor )

        if transparent == True:
            transVal = 1.0

        if container.clipTranMat == None:
            container.clipTranMat = SoMaterial( )
            container.clipTranMat.setName( "ClipTransparentMat" )

        container.clipTranMat.transparency.setValue( transVal )

        if actor == self.dynObjects:

            for vol in self.volActors.values( ):
                if vol.clipTranMat != None:
                    vol.clipTranMat.transparency.setValue( transVal )

            for srf in self.srfActors.values( ):
                if srf.clipTranMat != None:
                    srf.clipTranMat.transparency.setValue( transVal )            

#---------------------------------------------------------------------------
# setClipMode:
#---------------------------------------------------------------------------

    def setClipMode( self,  mode    = 'max',
                            actor   = None  ):

        actor, container, parent = self._getActorProp( actor )

        if container.clipShapeActorList != None:
            for clipShape in container.clipShapeActorList:
                clipShape.setClipMode( mode )

        if actor == self.dynObjects:

            for vol in self.volActors.values( ):
                if vol.clipShapeActorList != None:
                    for clipShape in vol.clipShapeActorList:
                        clipShape.setClipMode( mode )

            for srf in self.srfActors.values( ):
                if srf.clipShapeActorList != None:
                    for clipShape in srf.clipShapeActorList:
                        clipShape.setClipMode( mode )    
		
#---------------------------------------------------------------------------
# Test:
#---------------------------------------------------------------------------

if __name__ == '__main__':
    print "run the test script"
