#===========================================================================
#
# In this class, we have these visualization mode :
#   "Normal",
#   "pick"( for surface and volume and edge),
#   "surface single pick", ,    "Single point pick",
#   "cut plane",    "zoom",     "lasso pick",
#   "rubber pick",  "center",   "Show Surface",
#   "Fit Surface"
#
# Their mouse button combinations and definitions :
#
# "Normal" :
#   Left Mouse                  -> Rotation (+ Ctrl or Shift do the same)
#   Middle mouse                -> Move     (+ Ctrl or Shift do the same)
#   Right mouse                 -> Zoom     (+ Ctrl or Shift do the same)
#   Wheel mouse                 -> Zoom
#   Alt + Left Mouse            -> Highlight selected surface      
#   Alt + Ctrl  + Any Mouse     -> Show popup menu of the selected item
#
# "Pick"( "surface pick", "volume pick", "edge pick" ) :
#   Left Mouse                  -> Select and Unselect
#   Middle Mouse                -> Apply the selection
#   Right Mouse                 -> Cancel the selection
#   Ctrl    + Any Mouse         -> Transform model
#   Shift                       -> Change visualization mode to  rubber band pick
#   Shift   + Ctrl              -> Change visualization mode to lasso pick
#
# "rubber band" :
#   Left Mouse                  -> Draw rubber band
#
# "Lasso pick" :
#   Left Mouse                  -> Draw Lasso Lines
#
# "Surface single pick" :
#   Left Mouse                  -> Select and Unselect
#   Ctrl    + Any Mouse         -> Transform model
#
# "Single point pick" :
#   Left Mouse                  -> Select a point
#   Ctrl    + Any Mouse         -> Transform model
#
# "Cut plane" :
#   Ctrl    + Any Mouse         -> Transform model
#   Any Mouse(or Alt+Any Mouse) -> Transform the cut plane
#
# "Zoom" :
#   Left Mouse                  -> Zoom
#
# "Center" :
#   Left Mouse                  -> Define the location of Center
#
# "Show Surface" and "Fit Surface" :
#   Left Mouse                  -> Define the location
#   Ctrl    + Any Mouse         -> Transform model
#
#===========================================================================

#===========================================================================
#
# Include files
#
#===========================================================================

import	os
import	sys
import  acuQt
import  acuUtil

import	math
import  string
import	numarray
import  types

import	random
import	acuSgViewer
import	acuSgActor

from	iv	    import	*

#===========================================================================
#
# Acusim logo
#
#===========================================================================

_logo = [
"210 41 4 1",
"  c #141313",
". c #ed193d",
"X c #ed7589",
"O c None",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOX.............OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOXX.....X................OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOX......XXOOX.................XXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO O  OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO  O OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOXXXOOOOOOOX........XOOOX............X..........OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOOOOOOOOO       OOOOOOOOOOO          OOOO     OOOOOO     OOOOOO        OOOOOO     OOOOOO      OOOOOO      OOOOOOOOOOOOX.XOOOOOOOOOX......XOOOOX.........XOOOOOOOXX......OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOOOOOOOO        OOOOOOOOO             OOO     OOOOOO     OOOOO           OOOO     OOOOOO      OOOOO       OOOOOOOOOOO..XOOOOOOOOOOOOX....OOOO.........XOOOOOOOOOOOO......OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOOOOOOOO        OOOOOOOO              OOO     OOOOOO     OOOO           OOOOO     OOOOO       OOOOO       OOOOOOOOOO..OOOOOOOOOOOOOOO...XOOO.........OOOOOOOOOOOOOOO......OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOOOOOOO         OOOOOOO              OOO      OOOOOO     OOOO           OOOOO     OOOOO        OOOO       OOOOOOOOO..XOOOOOOOOOOOOOOOO................XOOOOOOOOOOOOOO......OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOOOOOOO         OOOOOOO       OOOOO  OOO     OOOOOOO     OOO     OOOOO OOOOO      OOOOO        OOO        OOOOOOOOO..OOOOOOOOOOOOOOOOOX.................XOOOOOOOOOOOOO.....OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOOOOOO     O     OOOOO      OOOOOOOO OOO     OOOOOOO     OOO      OOOOOOOOOO     OOOOO         OOO        OOOOOOOO..XOOOOOOOOOOOOOOOOOO...................OOOOOOOOOOOO.....XOOOOOOOOOOOOOOOOOOOOOOOOOOXX....OOOO",
"OOOOOOOO     O     OOOOO     OOOOOOOOOOOOO     OOOOOO     OOOO      OOOOOOOOOO     OOOOO         OO         OOOOOOOO..OOOOOOOOOOOOOOOOOOOO...................XOOOOOOOOOOO....OOOOOOOOOOOOOOOOOOOOOOOOO.........XOO",
"OOOOOOO     OO     OOOOO     OOOOOOOOOOOOO     OOOOOO     OOOOO       OOOOOOOO     OOOOO         OO         OOOOOOOX..OOOOOOOOOOOOOOOOOOOX.....................OOOOOOOOOO....OOOOOOOOOOOOOOOOOOOOOOO............OO",
"OOOOOOO     OO     OOOO      OOOOOOOOOOOOO     OOOOOO     OOOOO         OOOOOO     OOOOO    O    O          OOOOOOOX.XOOOOOOOOOOOOOOOOOOOO......................OOOOOOOOOX..XOOOOOOOOOOOOOOOOOOOOOX.............XO",
"OOOOOO     OOO     OOOO     OOOOOOOOOOOOOO     OOOOOO     OOOOOO         OOOOO     OOOO     O         OO    OOOOOOOX.XOOOOOOOOOOOOOOOOOOOO.........X.X...........OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOX......XXOX....XO",
"OOOOOO     OOOO     OOO      OOOOOOOOOOOO     OOOOOOO     OOOOOOOO        OOO     OOOOO     O         OO    OOOOOOOX.XOOOOOOOOOOOOOOOOOOOO......XOOOOOOX..........OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO....XOOOOOOX....O",
"OOOOO               OOOO     OOOOOOOOOOOO     OOOOOO      OOOOOOOOO       OOO     OOOOO     OO        OO    OOOOOOOX..OOOOOOOOOOOOOOOOOOOO....XOOOOX...............XOOOOOOOOOOOOOOOOOOOOOOOOOOOO....OOOOOOOOO...XO",
"OOOOO               OOO      OOOOOOOOOOOO     OOOOOO     OOOOOOOOOOOO     OOO     OOOO     OOO       OO     OOOOOOOO..OOOOOOOOOOOOOOOOOOOX...XOOOO...XOOOOOOX.......XOOOOOOOOOOOOOOOOOOOOOOOOOOO...OOOOOOOOOO....O",
"OOOO                OOOO     OOOOOOOOOOOO      OOOOO     OOOO  OOOOOO     OOO     OOOO     OOO       OOO    OOOOOOOOX.XOOOOOOOOOOOOOOOOOO...XOOOO..OOOOOOOOOOOX......XOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO...XO",
"OOOO                 OOO       OOOOO OOOO      OOOO      OOOO    OOO      OOO     OOOO     OOO      OOOO    OOOOOOOOO..OOOOOOOOOOOOOOOOOX...OOOO..OOOOOOOOOOOOOOX.....XOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOX...OO",
"OOO      OO O O      OOOO             OOO               OOOO              OOO     OOO     OOOO      OOO     OOOOOOOOOX.XOOOOOOOOOOOOOOOO...XOOOX.XOOOOOOOOOOOOOOOO.....XOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOX...OO",
"OOO     OOOOOOOO     OOOO            OOOOO              OOOO             OOO      OOO     OOOOO    OOOOO    OOOOOOOOOO..OOOOOOOOOOOOOOO....XOOX..OOOOOOOOOOOOOOOOOO.....XOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO...XOO",
"OO      OOOOOOOO     OOOOO           OOOOOO            OOOOOO           OOOO     OOOO     OOOOO    OOOOO    OOOOOOOOOOO..XOOOOOOOOOOOO......X...OOOOOOOOOOOOOOOOOOOOX....XOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO...OOO",
"OO     OOOOOOOOO     OOOOOOO         OOOOOOO          OOOOOOOO         OOOOO     OOO      OOOOO   OOOOOO    OOOOOOOOOOOOX..OOOOOOOOOO..........OOOOOOOOOOOOOOOOOOOOOOX....XOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOX..XOOO",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO  O OOOOOOOOOOOO    OOOOOOOOOOOOO O  OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOXXOOOOOOOOOOOXOXXOOOOOOOOOOOOOOOOOOOOOOOOOOO.....OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOX...OOOO",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOX....XOOOOOOOOOOOOOOOOOOOOOOOOOOOO...OOOOO",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO....XOOOOOOOOOOOOOOOOOOOOOOOOOO...XOOOOO",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO.....OOOOOOOOOOOOOOOOOOOOOOOO...XOOOOOO",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOX....XOOOOOOOOOOOOOOOOOOOOX...XOOOOOOO",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO.....XOOOOOOOOOOOOOOOOOX...OOOOOOOOO",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO......OOOOOOOOOOOOOX...XOOOOOOOOOO",
"OOO   OOOOOOOOOOOOOOOOOOO    OOOOOOOOOOOOOOOOOOO    OOOOOOOOOOOOOOO      OOOOOOOOOOOOOOO OOOOOOO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO   OOOOOOOOOOOOOOOOOO    OOOOOOOOOOOOOOOOOX.....XXOOOOOOX....XOOOOOOOOOOOO",
"OO OO OOOOOOOOOOOOOOOOOO  OO  OOOOOOOOOOOOOOOOO  OOOOOOOOOOOOOOOOOOOO  OOOOOOOOOOOOOOOOO OOO OOO OOOOOOOOOOOOOOOOOO  OOOOOOOOOOOOOOOOOOO O  OOOOOOOOOOOOOOOOO OOOOOOOOOOOOOOOOOOOOOOOX............OOOOOOOOOOOOOOOO",
"OO OOOOOOOOOOOOOOOOOOOO OOOOO  OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO OOOOOOOOOOOOOOOOOO  OO  OO OOOOOOOOOOOOOOOOOO  OOOOOOOOOOOOOOOOOOO OO OOOOOOOOOOOOOOOOO OOOOOOOOOOOOOOOOOOOOOOOOOOOXXXXXXOOOOOOOOOOOOOOOOOOO",
"OOO  OOOOOOOOOOOOOOOOOO OOOOOO OOOOOOOOOOOOOOOO     OOOOOOOOOOOOOOOOO  OOOOOOOOOOOOOOOOOO O   O  OOOOOOOOOOOOOOOOO OO OOOOOOOOOOOOOOOOO  O OOOOOOOOOOOOOOOOOO    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOO  OOOOOOOOOOOOOOOOO OOOOOO OOOOOOOOOOOOOOOO  OOOOOOOOOOOOOOOOOOOO OOOOOOOOOOOOOOOOOOO   OO  OOOOOOOOOOOOOOOOOO OO OOOOOOOOOOOOOOOOOO   OOOOOOOOOOOOOOOOO  OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOOO  OOOOOOOOOOOOOOOO OOOOO  OOOOOOOOOOOOOOOO  OOOOOOOOOOOOOOOOOOOO OOOOOOOOOOOOOOOOOOOO  OO  OOOOOOOOOOOOOOOOOO     OOOOOOOOOOOOOOOOO O OOOOOOOOOOOOOOOOOO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OO OO OOOOOOOOOOOOOOOOOO  OO  OOOOOOOOOOOOOOOOO  OOOOOOOOOOOOOOOOOOOO  OOOOOOOOOOOOOOOOOOO OOO OOOOOOOOOOOOOOOOOO OOOO OOOOOOOOOOOOOOOO  OO OOOOOOOOOOOOOOOOO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OO    OOOOOOOOOOOOOOOOOOO    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO OOOO  OOOOOOOOOOOOOOOO OO OOOOOOOOOOOOOOOOO    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
]

#===========================================================================
#
# Useful definitions
#
#===========================================================================

TRUE  = 1
True  = 1
FALSE = 0
False = 0

#===========================================================================
#
# Errors
#
#===========================================================================

acuSgTformError   = "ERROR from acuSgTform module"

#===========================================================================
#
# "AcuSgTform":  Scene graph transformation
#
#===========================================================================

class AcuSgTform:

    '''
        All the transformation functions, keyboard and mouse call back
	functions are implemented in this class for Coin/SoQt graphical
	window.
    '''

    def __init__(self, 	parent, settingObj	= None		):
        '''
	    Arguments:
	        parent		- parent object
	        settingObj	- settings object
	    Output:
	        None
        '''

	self.srfPickFlag= FALSE
	self.srfSinglePickFlag=FALSE
	self.volPickFlag= FALSE
        #----- Misc. 04/09 H1 SH
	self.edgPickFlag= FALSE
        self.cutPlnFlag	= FALSE
	self.lassoPickMode= SoExtSelection.ALL_SHAPES
	self.lassoPickPlcy= SoExtSelection.FULL
	self.cPlane	= None
        self.index	= -1
        self.asg	= parent
	self.viewer	= self.asg.viewer

	self.settingObj	= settingObj

        self.logoDsp    = acuQt.getSettingInt( 'mainBack/logo',     1   )
	
	acusimHome	= os.environ["ACUSIM_HOME"]
	acusimMach	= os.environ["ACUSIM_MACHINE"]
	acusimVer	= os.environ["ACUSIM_VERSION"]
	self.acuLogoFile	= \
	os.path.join( acusimHome,acusimMach,acusimVer,"script","acusimLogo.png")

        if self.logoDsp:

	    if os.path.exists( self.acuLogoFile ):
                self.logoAct= self.asg.addImgActor(
                                        filename    = self.acuLogoFile,
                                        position    = [0.01,0.93],
                                        width       = -1,
                                        height      = -1,
                                        horAlignment= "LEFT",
                                        verAlignment= "TOP"		)
	    else:
                self.logoAct= self.asg.addImgActor(
                                        filename    = None,
                                        image	    = _logo,
                                        position    = [0.01,0.93],
                                        width       = -1,
                                        height      = -1,
                                        horAlignment= "LEFT",
                                        verAlignment= "TOP"		)

	self.line		= SbLine()

	self.x1, self.y1	= 0.0, 0.0
	self.x2, self.y2	= 0.0, 0.0
	self.mode		= "none"
	self.transMat		= {}

	self.actorList		= []
	self.unPickableActors	= []
	self.pickedPnt		= None
	self.singlePickPntCallback = None

        #----- Misc 4/08 : E9
        self.win                = self.asg.settingObj
	self.pickableSrf        = False
	self.lstVal             = None

	#----- Misc 05/09 : G1
	self.globalCenter       = None
	self.pickingStarted     = False
	self.pointGeomActor     = None

#---------------------------------------------------------------------------
# zoomPlot: zoom the selected area of the graphical window
#---------------------------------------------------------------------------

    def zoomPlot( self ):
        '''
	    Function to zoom the selected area obtained by drawing a
	    rectangle in the graphical window
	    Arguments:
	        None

	    Output:
	        None
        '''
        #----- Misc 4/08 : E9
        # Get the last value
        self.recalstVal     = self.getUndoSettVals(                     )

	self.resetMode(							)
        self.mode = "zoom"
	self.viewer.render(						)
	self.asg.pntSelection.lassoType.setValue( SoExtSelection.RECTANGLE)
	self.asg.linSelection.lassoType.setValue( SoExtSelection.RECTANGLE)
	self.asg.srfSelection.lassoType.setValue( SoExtSelection.RECTANGLE)
	self.asg.volSelection.lassoType.setValue( SoExtSelection.RECTANGLE)
	#----- Misc. 04/09 H1 SH
	self.asg.edgSelection.lassoType.setValue( SoExtSelection.RECTANGLE)

	self.viewer.render(						)
	self.viewer.mode(		acuSgViewer.MODE_PICKING	)
	self.viewer.actualRedraw(					)

#---------------------------------------------------------------------------
# rubberZoom: rubber band zooming
#---------------------------------------------------------------------------

    def rubberZoom( self ):
        ''' rubber band zooming '''

	x = ( self.x1 + self.x2 ) / 2.0
	y = ( self.y1 + self.y2 ) / 2.0
	loc = [ x, y ]
	
	self.translateCamera( loc )
	rbWidth		= abs( self.x2 - self.x1 )
	rbHeight	= abs( self.y2 - self.y1 )
	sF		=  max( rbWidth, rbHeight )
	if sF == 0: return
	camera = self.viewer.getCamera()
	camHt		= camera.height.getValue() * sF
	camera.height.setValue( 		camHt 			)
	self.viewer.redraw(						)

#---------------------------------------------------------------------------
# eventCallback: callback applied on SoEventCallback node
#---------------------------------------------------------------------------

    def eventCallback( self, userData, eventCB ):
        '''
	    Callback function for SoEventCallback object

	    Argument:
	        userData	- callback data
	        eventCB		- SoEventCallback object
	    Output:
	        None
        '''
        event		= eventCB.getEvent(				)
	shiftDown	= event.wasShiftDown(				)
	ctrlDown	= event.wasCtrlDown(				)
	altDown		= event.wasAltDown(				)

	if( SoMouseButtonEvent.isButtonPressEvent( event, \
			SoMouseButtonEvent.BUTTON1	)):

	    if self.srfPickFlag or self.volPickFlag or self.edgPickFlag:
	        if shiftDown and ctrlDown:
		    self.mode	= 'lassoPick'
	        elif shiftDown:
		    self.mode	= 'rbPick'
		else:
		    self.mode	= 'pick'

	    elif self.srfSinglePickFlag:
                self.mode   = 'pick'
	    elif altDown and not ctrlDown: ### while not in AddTo Mode
		self.mode   = 'hLight'
		self.asg.volSelection.lassoType.setValue( SoSelection.SINGLE)
		self.asg.srfSelection.lassoType.setValue( SoSelection.SINGLE)
		self.asg.linSelection.lassoType.setValue( SoSelection.SINGLE)
		self.asg.pntSelection.lassoType.setValue( SoSelection.SINGLE)
                #----- Misc. 04/09 H1 SH
		self.asg.edgSelection.lassoType.setValue( SoSelection.SINGLE)

            #----- Misc 12/09 : B4
            elif ctrlDown and not shiftDown and altDown and \
                 self.mode in ['none', 'menu' , 'hLight' ]:
                self.mode = 'menu'
            #-----

	    x, y	= event.getPosition().getValue()
	    self.viewer.saveLog(	event.getPosition()	)
	    vpr		= self.viewer.getViewportRegion()
	    sx, sy	= vpr.getViewportSizePixels().getValue()
	    self.x1	= float( x ) / sx
	    self.y1	= float( y ) / sy

	if( SoMouseButtonEvent.isButtonReleaseEvent( event, \
			SoMouseButtonEvent.BUTTON1	)):
	    x, y	= event.getPosition().getValue()
	    self.viewer.saveLog(	event.getPosition()	)
	    vpr		= self.viewer.getViewportRegion()
	    sx, sy	= vpr.getViewportSizePixels().getValue()
	    self.x2	= float( x ) / sx
	    self.y2	= float( y ) / sy

	    if ( self.srfPickFlag or self.volPickFlag or self.edgPickFlag) \
	    	and self.mode == 'rbPick' and not shiftDown and \
		not ctrlDown:

	        self.mode	= 'pick'
##		self.asg.redraw(					)

	    if self.mode == "zoom":
	        self.rubberZoom(					)
		self.mode	= "none"
		self.viewer.mode(	acuSgViewer.MODE_VIEWING	)

                #----- Misc 4/08 : E9
                # Get the new value
                newVal      = self.getUndoSettVals( mode = 'new'        )
                if self.win:
                    tag     = self.win.undoStn.UNDO_TAG_ZOOM
                    self.win.addSettingMarker(  tag,
                                                par     = 'transform',
                                                lastVal = self.recalstVal,
                                                newVal  = newVal,
                                                func    = self.refreshUndoSett)
        

	    if self.mode == "center":
		loc = [ self.x2, self.y2 ]
		self.translateCamera( loc )
		self.viewer.redraw()
		self.mode = "none"
		self.viewer.mode(	acuSgViewer.MODE_VIEWING	)
		self.viewer.setMouseBinding("CTRL", self.ctrlBinding	)
		self.viewer.setMouseBinding("SHIFT", self.shiftBinding	)
		self.viewer.setMouseBinding("SHIFT_CTRL", self.shCtrlBinding)
		self.asg.addStaticCameras(				)

                #----- Misc 4/08 : E9
                # Get the new value
                newVal  = self.getUndoSettVals( mode = 'new'            )

                if self.win:
                    tag = self.win.undoStn.UNDO_TAG_CENTER
                    self.win.addSettingMarker(  tag,
                                                par     = 'transform',
                                                lastVal = self.recalstVal,
                                                newVal  = newVal,
                                                func    = self.refreshUndoSett)

	    if self.mode == "pntPickFD":
	        self.mode = "none"
		self.pickedPnt = None
		self.viewer.mode(	acuSgViewer.MODE_VIEWING	)
		loc = [ self.x2, self.y2 ]
		#self.viewer.setMouseBinding( "CTRL", self.ctrlBinding	)
		#self.viewer.setMouseBinding( "SHIFT", self.shiftBinding	)
		#self.viewer.setMouseBinding( "SHIFT_CTRL", self.shCtrlBinding)

		camera	= self.viewer.getCamera(			)
		viewVol	= camera.getViewVolume(self.viewer.getGLAspectRatio())
		fd      = camera.focalDistance.getValue(		)
		panPlane= viewVol.getPlane( 		fd 		)
		pt	= SbVec2f( self.x2, self.y2 )
		viewVol.projectPointToLine( pt , self.line 		)
		curPlanePt	= SbVec3f(				)
		panPlane.intersect( self.line, curPlanePt 		)
		cx,cy,cz= curPlanePt.getValue(				)

		point	= self.asg.addGeomActor(    type    = "point",
						    point   = [cx,cy,cz],
						    pointSize= 10,
						    vis	= True,
						    color =[1,0,0]	 )

	    if self.mode == "pntPick":
	        
                #self.mode = "none"
		#self.viewer.mode(	acuSgViewer.MODE_VIEWING	)
		#self.viewer.setMouseBinding( "CTRL", self.ctrlBinding	)
		#self.viewer.setMouseBinding( "SHIFT", self.shiftBinding	)
		#self.viewer.setMouseBinding( "SHIFT_CTRL", self.shCtrlBinding)
	        self.mode = "none"
		self.pickedPnt = None
		self.viewer.mode(	acuSgViewer.MODE_VIEWING	)
		vpr	= self.viewer.getViewportRegion(		)
		rpa	= SoRayPickAction(		vpr		)

		camera	= self.viewer.getCamera(			)
		viewVol	= camera.getViewVolume(self.viewer.getGLAspectRatio())
		fd      = camera.focalDistance.getValue(		)
		nd      = camera.nearDistance.getValue(			)
		pt	= SbVec2f( self.x2, self.y2 )

		viewVol.projectPointToLine( pt , self.line 		)

		fdPlane= viewVol.getPlane( 		fd 		)
		fdPlanePt= SbVec3f(					)
		fdPlane.intersect( 	self.line, fdPlanePt 		)

		ndPlane= viewVol.getPlane( 		nd 		)
		ndPlanePt= SbVec3f(					)
		ndPlane.intersect( 	self.line, ndPlanePt 		)

		
                ndx,ndy,ndz =  ndPlanePt.getValue()
		fdx,fdy,fdz =  fdPlanePt.getValue()
		ax,ay,az    = fdx-ndx,fdy-ndy,fdz-ndz
		mag         = math.sqrt( ax*ax + ay*ay + az*az )
		ax,ay,az    = ax/mag, ay/mag, az/mag
		axisVec     = SbVec3f( ax,ay,az )

		rpa.setRay( 		ndPlanePt, axisVec 		)
		rpa.apply( 		self.asg.dynObjects 		)
		#rpa.apply( 		self.asg.root 			)
		
                pickedPoint = rpa.getPickedPoint(			)

		if pickedPoint:
		    (px,py,pz) =  pickedPoint.getPoint().getValue()
		    self.pickedPnt = (px,py,pz)
		    point = self.asg.addGeomActor(    type    = "point",
						    point   = [px,py,pz],
						    pointSize= 10,
						    vis	= True,
						    color =[1,0,0]	 )
		    if self.singlePickPntCallback:
		        self.singlePickPntCallback( self.pickedPnt,point)

        if self.srfPickFlag or self.srfSinglePickFlag:
	    if self.mode == 'pick':
		self.asg.srfSelection.lassoType.setValue( \
				SoExtSelection.NOLASSO			)
		self.asg.srfSelection.policy.setValue( \
				SoSelection.SINGLE			)

	    if self.mode == 'rbPick':

		self.asg.srfSelection.lassoType.setValue( \
				SoExtSelection.RECTANGLE		)
		self.asg.srfSelection.lassoPolicy.setValue(\
				self.lassoPickPlcy			)
		self.asg.srfSelection.lassoMode.setValue(\
				self.lassoPickMode			)

	    if self.mode == 'lassoPick':
		self.asg.srfSelection.lassoType.setValue( \
				SoExtSelection.LASSO			)
		self.asg.srfSelection.lassoPolicy.setValue(\
				self.lassoPickPlcy			)
		self.asg.srfSelection.lassoMode.setValue(\
				self.lassoPickMode			)

	    self.asg.srfSelection.deselectAll(				)

        if self.volPickFlag:

	    if self.mode == 'pick':
		self.asg.volSelection.lassoType.setValue( \
				SoExtSelection.NOLASSO			)
		self.asg.volSelection.policy.setValue( \
				SoSelection.SINGLE			)

	    if self.mode == 'rbPick':

		self.asg.volSelection.lassoType.setValue( \
				SoExtSelection.RECTANGLE		)
		self.asg.volSelection.lassoPolicy.setValue(\
				self.lassoPickPlcy			)
		self.asg.volSelection.lassoMode.setValue(\
				self.lassoPickMode			)

	    if self.mode == 'lassoPick':
		self.asg.volSelection.lassoType.setValue( \
				SoExtSelection.LASSO			)
		self.asg.volSelection.lassoPolicy.setValue(\
				self.lassoPickPlcy			)
		self.asg.volSelection.lassoMode.setValue(\
				self.lassoPickMode			)

	    self.asg.volSelection.deselectAll(				)

        #----- Misc. 04/09 H1 SH
	if self.edgPickFlag:

	    if self.mode == 'pick':
		self.asg.edgSelection.lassoType.setValue( \
				SoExtSelection.NOLASSO			)
		self.asg.edgSelection.policy.setValue( \
				SoSelection.SINGLE			)

	    if self.mode == 'rbPick':

		self.asg.edgSelection.lassoType.setValue( \
				SoExtSelection.RECTANGLE		)
		self.asg.edgSelection.lassoPolicy.setValue(\
				self.lassoPickPlcy			)
		self.asg.edgSelection.lassoMode.setValue(\
				self.lassoPickMode			)

	    if self.mode == 'lassoPick':
		self.asg.edgSelection.lassoType.setValue( \
				SoExtSelection.LASSO			)
		self.asg.edgSelection.lassoPolicy.setValue(\
				self.lassoPickPlcy			)
		self.asg.edgSelection.lassoMode.setValue(\
				self.lassoPickMode			)

	    self.asg.edgSelection.deselectAll(				)

    #--------------------------------------------------------------------
    # The middle button clicking is equivalent to pressing the "Done"
    # button and right click is "Cancel" . Misc. 6/07 G11
    #---------------------------------------------------------------------
        
	if( SoMouseButtonEvent.isButtonPressEvent( event, \
			SoMouseButtonEvent.BUTTON3	)):

            #----- Misc 12/09 : B4
            if ctrlDown and not shiftDown and altDown and \
               self.mode in ['none', 'menu' , 'hLight' ]:
                self.mode   = 'menu'
            #-----
            else:
                mainWin	        = self.asg.settingObj
                if mainWin and mainWin.addToMode:
                    mainWin.addToDlg.doAddTo(                           )

	if( SoMouseButtonEvent.isButtonPressEvent( event, \
			SoMouseButtonEvent.BUTTON2	)):

            #----- Misc 12/09 : B4
            if ctrlDown and not shiftDown and altDown and \
               self.mode in ['none', 'menu' , 'hLight' ]:
                self.mode   = 'menu'
            #-----
            else:
                mainWin	        = self.asg.settingObj
                if mainWin and mainWin.addToMode:
                    mainWin.addToDlg.cancelAddTo(                       )

        #----- Misc 12/09 : B4
        if self.mode == 'menu':
            pickedPoint     = eventCB.getPickedPoint(                   )
            if pickedPoint:
                path        = pickedPoint.getPath(                      )
                self.volSrfPopUp(            None,          path        )


#----- Misc 12/09 : B4
#---------------------------------------------------------------------------
# volSrfPopUp:
#---------------------------------------------------------------------------

    def volSrfPopUp( self, obj, selectionPath ):
	    
        if self.mode != "menu": return

        actor       = None
        N           = selectionPath.getLength(                          )
        selFlag     = None
        for i in range( N ):
            node    = selectionPath.getNodeFromTail(            i       )
            if node.getClassTypeId() == \
		    SoIndexedFaceSet.getClassTypeId():
                for j in range( N-i ):
                    parNode = selectionPath.getNodeFromTail(    i+j     )
                    if isinstance( parNode, acuSgActor.AcuSgActor):
                        if self.asg.srfSelection.findChild(parNode)!= -1:
                            selFlag = 'srf'
                            actor   = parNode.dataId
                            break
                        elif self.asg.volSelection.findChild(parNode)!= -1:
                            selFlag = 'vol'
                            actor   = parNode.dataId

        self.mode   = "none"
        if selFlag  == 'srf':
            self.asg.srfSelection.deselectAll(			        )
        elif selFlag == 'vol':
            self.asg.volSelection.deselectAll(			        )
        self.viewer.mode(	            acuSgViewer.MODE_VIEWING    )
                
        if actor:
            mainWin = self.asg.settingObj
            mainWin.popupActor(             actor                       )

#---------------------------------------------------------------------------
# toggleHLightSrf: toggle into the surface highlighting mode
#---------------------------------------------------------------------------

    def toggleHLightSrf( self ):
        '''
	    start/stop highlighting surface entities that are part of the
	    selected face

	    Argument:
	        None
	    Output:
	        None
        '''

	if self.mode == 'hLight':
	    self.mode = 'none'
	    self.asg.srfSelection.deselectAll(				)
            self.asg.returnToLastVis(                                   )
	    self.asg.redraw(						)
	    self.asg.srfSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	    self.viewer.mode(		acuSgViewer.MODE_VIEWING	)
	else:
	    self.mode = 'hLight'
	    self.asg.visibleAllSrfActors(                               )
	    self.asg.showPickableSrf(					)
	    self.asg.srfSelection.lassoType.setValue( SoSelection.SINGLE)
	    self.viewer.mode(		acuSgViewer.MODE_PICKING	)

#---------------------------------------------------------------------------
# toggleHLightVol: toggle into the volume highlighting mode
#---------------------------------------------------------------------------

    def toggleHLightVol( self ):
        '''
	    start highlighting volume entities that are part of the
	    selected region

	    Argument:
	        None
	    Output:
	        None
        '''
	if self.mode == 'hLight':
	    self.mode = 'none'
	    self.asg.volSelection.deselectAll(				)
            self.asg.returnToLastVis(                                   )
	    self.asg.redraw(						)
	    self.asg.volSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	    self.viewer.mode(		acuSgViewer.MODE_VIEWING	)
	else:
	    self.mode = 'hLight'
	    self.asg.visibleAllVolActors(                               )
	    self.asg.showPickableVol(					)
	    self.asg.volSelection.lassoType.setValue( SoSelection.SINGLE)
	    self.viewer.mode(		acuSgViewer.MODE_PICKING	)

#---------------------------------------------------------------------------
# startPickSrf: go into the selection mode and pick surfaces
#---------------------------------------------------------------------------

    def startPickSrf( self, curActorList = None ):
        '''
	    start picking surface entities that are not part of
	    curActorList

	    Argument:
	        curActorList	- List of actors not to be selected
	    Output:
	        None
        '''

        self.actorList = []
	self.srfPickFlag = TRUE
	self.asg.remStaticObjects(					)
	#----- Misc. 4/08 D4
	self.asg.visibleAllSrfActors(                                   )
	#----- End of D4
	self.asg.showPickableSrf(					)
	self.viewer.mode(		acuSgViewer.MODE_PICKING	)
	self.viewer.actualRedraw(					)

	if curActorList != None:
	    try:
	        for actor in curActorList:
		    self.unPickableActors.append(	actor		)
	    except:
	        raise acuSgTformError,"curActorList is not a List"

#---------------------------------------------------------------------------
# setSinglePickMode:
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# singlePickPnt:
#---------------------------------------------------------------------------
    def singlePickPnt( self, callbackObj = None ):
        '''
	    start single picking surface entities.
	    Argument:
	        pt1Obj	=> QTextArea 
	        pt2Obj	=> QTextArea 
	        pt3Obj	=> QTextArea 
	    Output:
	        None
        '''
        self.mode = "pntPick"
	self.asg.pntSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	self.asg.linSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	self.asg.srfSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	self.asg.volSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	#----- Misc. 04/09 H1 SH
	self.asg.edgSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	
	self.viewer.mode( 	acuSgViewer.MODE_PICKING 		)
	self.asg.remStaticObjects(					) 
	self.pickedPnt = None
	self.singlePickPntCallback = callbackObj

	#return (0, 0, 0) # WHAT

#---------------------------------------------------------------------------
# getSinglePickPnt:
#---------------------------------------------------------------------------

    def getSinglePickPnt( self ):
        '''
	    get single picking surface entities.
	    Argument:
	        None
	    Output:
	        return (x,y,z) location of picked point
        '''
	if self.pickedPnt:
	    ( px,py,pz) = self.pickedPnt[0],self.pickedPnt[1],self.pickedPnt[2]
	    self.pickedPnt = None

	    return (px,py,pz)
        else:
	    return None

#---------------------------------------------------------------------------
# singlePickSrf:
#---------------------------------------------------------------------------

    def singlePickSrf( self ):
        '''
	    start single picking surface entities.
	    Argument:
	        None
	    Output:
	        None
        '''

        self.actorList          = []
	self.srfSinglePickFlag  = TRUE
	#----- Misc. 4/08 D4
	self.asg.visibleAllSrfActors(                                   )
	#----- End of D4
	self.asg.showPickableSrf(					)
	self.viewer.mode(		acuSgViewer.MODE_PICKING	)
	self.asg.remStaticObjects(					)
	self.viewer.actualRedraw(					)

#---------------------------------------------------------------------------
# startPickVol: go into the selection mode and pick volumes
#---------------------------------------------------------------------------

    def startPickVol( self, curActorList = None ):
        '''
	    start picking volume entities that are not part of
	    curActorList

	    Argument:
	        curActorList	- List of actors not to be selected
	    Output:
	        None	
        '''

        self.actorList = []

	self.volPickFlag = TRUE
	self.asg.remStaticObjects(					)
	#----- Misc. 4/08 D4
	self.asg.visibleAllVolActors(                                   )
	#----- End of D4
	self.asg.showPickableVol(					)
	self.viewer.mode(		acuSgViewer.MODE_PICKING	)
	self.viewer.actualRedraw(					)

	if curActorList != None:
	    try:
	        for actor in curActorList:
		    self.unPickableActors.append(	actor		)
	    except:
	        raise acuSgTformError,"curActorList is not a List"

#----- Misc. 04/09 H1 SH
#---------------------------------------------------------------------------
# startPickEdg: go into the selection mode and pick edges
#---------------------------------------------------------------------------

    def startPickEdg( self, curActorList = None ):
        '''
	    start picking edge entities that are not part of
	    curActorList

	    Argument:
	        curActorList	- List of actors not to be selected
	    Output:
	        None	
        '''

        self.actorList = []

	self.edgPickFlag = TRUE
	self.asg.remStaticObjects(					)
	#----- Misc. 4/08 D4
	self.asg.visibleAllEdgActors(                                   )
	#----- End of D4
	self.asg.showPickableEdg(					)
	self.viewer.mode(		acuSgViewer.MODE_PICKING	)
	self.viewer.actualRedraw(					)

	if curActorList != None:
	    try:
	        for actor in curActorList:
		    self.unPickableActors.append(	actor		)
	    except:
	        raise acuSgTformError,"curActorList is not a List"

#---------------------------------------------------------------------------
# endPick:
#---------------------------------------------------------------------------

    def endPick( self ):
        '''
	    End picking surface or volume entities

	    Argument:
	        None	
	    Output:
	        newActorList	- List of actors that are selected

        '''

        #----- Misc. 4/08 D4
        self.asg.returnToLastVis(                                       )
        #----- End of D4
	self.asg.addStaticCameras(					)
	self.asg.addStaticObjects(					)
	self.unPickableActors	= []

	if self.volPickFlag:
	    self.volPickFlag	= FALSE
	    self.asg.volSelection.deselectAll(				)
	    self.viewer.mode(		acuSgViewer.MODE_VIEWING	)
	    self.asg.resetSelection(    'volume'                        )
	    self.asg.redraw(						)
	    self.mode	= "none"
	    self.asg.volSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	    for id in self.actorList:
	        self.asg.unHighlight(			id		)
	    return self.actorList

	elif self.srfPickFlag:
	    self.srfPickFlag	= FALSE
	    self.asg.srfSelection.deselectAll(				)
	    self.viewer.mode(		acuSgViewer.MODE_VIEWING	)
	    self.asg.resetSelection(    'surface'                       )
	    self.asg.redraw(						)
	    self.mode	= "none"
	    self.asg.srfSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	    for id in self.actorList:
	        self.asg.unHighlight(			id		)
	    return self.actorList

        #----- Misc. 04/09 H1 SH
	elif self.edgPickFlag:
	    self.edgPickFlag	= FALSE
	    self.asg.edgSelection.deselectAll(				)
	    self.viewer.mode(		acuSgViewer.MODE_VIEWING	)
	    self.asg.resetSelection(    'edge'                          )
	    self.asg.redraw(						)
	    self.mode	= "none"
	    self.asg.edgSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	    for id in self.actorList:
	        self.asg.unHighlight(			id		)
	    return self.actorList

        elif self.srfSinglePickFlag:
            self.srfSinglePickFlag=FALSE
	    self.asg.srfSelection.deselectAll(				)
	    self.viewer.mode(		acuSgViewer.MODE_VIEWING	)
	    self.asg.redraw(						)
	    self.mode	= "none"
	    if len( self.actorList ) != 1:  return
	    pickActorId = self.actorList[0]
	    self.asg.unHighlight(			pickActorId	)
	    for srfActor in self.asg.srfActors.values():
                if srfActor.dataId == pickActorId:
                    #----- Mesh Extraction problem; we need geom Set not
                    # model name, also when we have new DB it does not work
                    # 11/29/2007; Misc. 8/07 H1
                    return srfActor.dataId #srfActor.name
            
	else:
	    print "neither volume or surface selection modes are on"
	
#---------------------------------------------------------------------------
# pntSelCallback: callback applied on SoExtSelection/SoSelection node
#---------------------------------------------------------------------------

    def pntSelCallback( self, obj, selectionPath ):
        '''
	    Callback function for SoExtSelection object

	    Argument:
	        obj		- callback data
	        selectionPath	- selectionPath could be used to traverse
		                  selected actors
	    Output:
	        None
        '''
	if self.mode == "zoom":
	    self.asg.pntSelection.lassoType.setValue( \
				SoExtSelection.NOLASSO			)

#---------------------------------------------------------------------------
# linSelCallback: callback applied on SoExtSelection/SoSelection node
#---------------------------------------------------------------------------

    def linSelCallback( self, obj, selectionPath ):
        '''
	    Callback function for SoExtSelection object

	    Argument:
	        obj		- callback data
	        selectionPath	- selectionPath could be used to traverse
		                  selected actors
	    Output:
	        None
        '''
	if self.mode == "zoom":
	    self.asg.linSelection.lassoType.setValue( \
				SoExtSelection.NOLASSO			)

#----- Misc. 04/09 H1 SH
#---------------------------------------------------------------------------
# edgSelCallback: callback applied on SoExtSelection/SoSelection node
#---------------------------------------------------------------------------

    def edgSelCallback( self, obj, selectionPath ):
        '''
	    Callback function for SoExtSelection object

	    Argument:
	        obj		- callback data
	        selectionPath	- selectionPath could be used to traverse
		                  selected actors
	    Output:
	        None
        '''

        if self.mode == "rbPick" or self.mode == "lassoPick":
	    N =  selectionPath.getLength()
	    for i in range( N ):
		node	= selectionPath.getNodeFromTail(i)
		try:
		    if node.getClassTypeId() == \
		    		SoIndexedFaceSet.getClassTypeId():
			for j in range( N-i ):
			    parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
				if parNode.dataId not in self.actorList:
				    self.actorList.append( parNode.dataId)
				    parNode.highlight(			)

		    if node.getClassTypeId() == \
		    		SoIndexedLineSet.getClassTypeId():
			for j in range( N-i ):
			    parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
##			        if parNode.extOutlineFlag:
				    if parNode.dataId not in self.actorList:
					self.actorList.append( parNode.dataId)
					parNode.highlight(		)
		except:
		    pass
        if self.mode == "pick":
	    N =  selectionPath.getLength()
	    for i in range( N ):
		node	= selectionPath.getNodeFromTail(i)
		try:
		    if node.getClassTypeId() == \
		    		SoIndexedFaceSet.getClassTypeId():
			for j in range( N-i ):
			    parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
				if parNode.dataId not in self.actorList:
				    self.actorList.append( parNode.dataId)
				    parNode.highlight(			)
				else:
				    self.actorList.remove( parNode.dataId)
				    parNode.unHighlight(		)

		    if node.getClassTypeId() == \
		    		SoIndexedLineSet.getClassTypeId():
			for j in range( N-i ):
			    parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
##			        if parNode.extOutlineFlag:
				    if parNode.dataId not in self.actorList:
					self.actorList.append( parNode.dataId)
					parNode.highlight(		)
				    else:
					self.actorList.remove( parNode.dataId)
					parNode.unHighlight(		)
		except:
		    pass

        if self.mode == "hLight":
            try:
	        N =  selectionPath.getLength()
	        for i in range( N ):
		    node	= selectionPath.getNodeFromTail(i)
	            if node.getClassTypeId() == \
		    		SoIndexedFaceSet.getClassTypeId():
		        for j in range( N-i ):
		            parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
			        mainWin	        = self.asg.settingObj
				mainWin.hLightEdgActorGroup(parNode.dataId)
		    if node.getClassTypeId() == \
		    		SoIndexedLineSet.getClassTypeId():
		        for j in range( N-i ):
		            parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
##			        if parNode.extOutlineFlag:
			            mainWin	= self.asg.settingObj
				    mainWin.hLightEdgActorGroup(parNode.dataId)
	    except:
	        pass

	    self.asg.edgSelection.deselectAll(			)
	    
	if self.mode == "zoom":
	    self.asg.edgSelection.lassoType.setValue( \
				SoExtSelection.NOLASSO			)

#---------------------------------------------------------------------------
# srfSelCallback: callback applied on SoExtSelection/SoSelection node
#---------------------------------------------------------------------------

    def srfSelCallback( self, obj, selectionPath ):
        '''
	    Callback function for SoExtSelection object

	    Argument:
	        obj		- callback data
	        selectionPath	- selectionPath could be used to traverse
		                  selected actors
	    Output:
	        None
        '''

        if self.mode == "rbPick" or self.mode == "lassoPick":
	    N =  selectionPath.getLength()
	    for i in range( N ):
		node	= selectionPath.getNodeFromTail(i)
		try:
		    if node.getClassTypeId() == \
		    		SoIndexedFaceSet.getClassTypeId():
			for j in range( N-i ):
			    parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
				if parNode.dataId not in self.actorList and \
				   parNode.dataId not in self.unPickableActors:
				    self.actorList.append( parNode.dataId)
				    parNode.highlight(			)

		    if node.getClassTypeId() == \
		    		SoIndexedLineSet.getClassTypeId():
			for j in range( N-i ):
			    parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
			        if parNode.extOutlineFlag:
				    if parNode.dataId not in self.actorList and \
				       parNode.dataId not in self.unPickableActors:
					self.actorList.append( parNode.dataId)
					parNode.highlight(		)
		except:
		    pass

        if self.mode == "pick":
	    N =  selectionPath.getLength()
	    for i in range( N ):
		node	= selectionPath.getNodeFromTail(i)
		try:
		    if node.getClassTypeId() == \
		    		SoIndexedFaceSet.getClassTypeId():
			for j in range( N-i ):
			    parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
			        if parNode not in self.unPickableActors:
				    if parNode.dataId not in self.actorList:

                                        #------ Single pick actor
                                        if self.srfSinglePickFlag and \
                                           len( self.actorList ) > 0: return
                                        
					self.actorList.append( parNode.dataId)
					parNode.highlight(		)

				    else:
					self.actorList.remove( parNode.dataId)
					parNode.unHighlight(		)
		    if node.getClassTypeId() == \
		    		SoIndexedLineSet.getClassTypeId():
			for j in range( N-i ):
			    parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
			        if parNode.extOutlineFlag:
				    if parNode not in self.unPickableActors:
					if parNode.dataId not in self.actorList:

                                            #------ Single pick actor
                                            if self.srfSinglePickFlag and \
                                               len( self.actorList ) > 0: return
                                            
					    self.actorList.append( parNode.dataId)
					    parNode.highlight(		)
					else:
					    self.actorList.remove( parNode.dataId)
					    parNode.unHighlight(	)
		except:
		    pass

	if self.mode == "showSurf" or self.mode == "fitSurf" or \
		self.mode == "centerOfRotation":
            addMarker = False
	    try:
	        N =  selectionPath.getLength()
	        for i in range( N ):
		    node	= selectionPath.getNodeFromTail(i)
	            if node.getClassTypeId() == \
		    		SoIndexedFaceSet.getClassTypeId():
		        for j in range( N-i ):
		            parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
			        if self.mode == "fitSurf":
				    self.showSelSurface(parNode,True	)
				    #----- Misc 4/08 : E9
				    if self.win:
                                        tag=self.win.undoStn.UNDO_TAG_FIT_SUR
                                        addMarker = True

                                    
				elif self.mode == "showSurf":
				    self.showSelSurface(parNode		)
				    #----- Misc 4/08 : E9
				    if self.win:
                                        tag=self.win.undoStn.UNDO_TAG_SHOW_SUR
                                        addMarker = True

				else:
				    self.centerOfRotation(parNode	)
		    if node.getClassTypeId() == \
		    		SoIndexedLineSet.getClassTypeId():
		        for j in range( N-i ):
		            parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
			        if parNode.extOutlineFlag:
			            if self.mode == "fitSurf":
				        self.showSelSurface(parNode,True)
                                        #----- Misc 4/08 : E9
				        if self.win:
                                            tag=self.win.undoStn.UNDO_TAG_FIT_SUR
                                            addMarker = True
                                        
				    elif self.mode == "showSurf":
				        self.showSelSurface(parNode	)
                                        #----- Misc 4/08 : E9
				        if self.win:
                                            tag=self.win.undoStn.UNDO_TAG_SHOW_SUR
                                            addMarker = True

				    else:
				        self.centerOfRotation(parNode	)
	    except:
	        pass

	    self.asg.srfSelection.deselectAll(			        )
	    self.viewer.mode(	acuSgViewer.MODE_VIEWING		)
	    self.mode = "none"
	    self.asg.redraw(						)
            if addMarker:
                #----- Misc 4/08 : E9
                self.pickableSrf = False
		# Get the new value
                newVal = self.getUndoSettVals(  mode = 'new'            )
                if self.win:
                    self.win.addSettingMarker(  tag,
                                                par     = 'transform',
                                                lastVal = self.recalstVal,
                                                newVal  = newVal,
                                                func    = self.refreshUndoSett)

	if self.mode == "hLight":
	    try:
	        N =  selectionPath.getLength()
	        for i in range( N ):
		    node	= selectionPath.getNodeFromTail(i)
	            if node.getClassTypeId() == \
		    		SoIndexedFaceSet.getClassTypeId():
		        for j in range( N-i ):
		            parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
			        mainWin	        = self.asg.settingObj
			        if mainWin:
                                    mainWin.hLightSrfActorGroup(parNode.dataId)
		    if node.getClassTypeId() == \
		    		SoIndexedLineSet.getClassTypeId():
		        for j in range( N-i ):
		            parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
			        if parNode.extOutlineFlag:
			            mainWin	= self.asg.settingObj
			            if mainWin:
                                        mainWin.hLightSrfActorGroup(parNode.dataId)
	    except:
	        pass

	    self.asg.srfSelection.deselectAll(			)

	if self.mode == "zoom":
	    self.asg.srfSelection.lassoType.setValue( \
				SoExtSelection.NOLASSO			)

#---------------------------------------------------------------------------
# volSelCallback:
#---------------------------------------------------------------------------

    def volSelCallback( self, obj, selectionPath ):
        '''
	    Callback function for SoExtSelection object

	    Argument:
	        obj		- callback data
	        selectionPath	- selectionPath could be used to traverse
		                  selected actors
	    Output:
	        None
        '''

        if self.mode == "rbPick" or self.mode == "lassoPick":
	    N =  selectionPath.getLength()
	    for i in range( N ):
		node	= selectionPath.getNodeFromTail(i)
		try:
		    if node.getClassTypeId() == \
		    		SoIndexedFaceSet.getClassTypeId():
			for j in range( N-i ):
			    parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
				if parNode.dataId not in self.actorList:
				    self.actorList.append( parNode.dataId)
				    parNode.highlight(			)

		    if node.getClassTypeId() == \
		    		SoIndexedLineSet.getClassTypeId():
			for j in range( N-i ):
			    parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
			        if parNode.extOutlineFlag:
				    if parNode.dataId not in self.actorList:
					self.actorList.append( parNode.dataId)
					parNode.highlight(		)
		except:
		    pass
        if self.mode == "pick":
	    N =  selectionPath.getLength()
	    for i in range( N ):
		node	= selectionPath.getNodeFromTail(i)
		try:
		    if node.getClassTypeId() == \
		    		SoIndexedFaceSet.getClassTypeId():
			for j in range( N-i ):
			    parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
				if parNode.dataId not in self.actorList:
				    self.actorList.append( parNode.dataId)
				    parNode.highlight(			)
				else:
				    self.actorList.remove( parNode.dataId)
				    parNode.unHighlight(		)

		    if node.getClassTypeId() == \
		    		SoIndexedLineSet.getClassTypeId():
			for j in range( N-i ):
			    parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
			        if parNode.extOutlineFlag:
				    if parNode.dataId not in self.actorList:
					self.actorList.append( parNode.dataId)
					parNode.highlight(		)
				    else:
					self.actorList.remove( parNode.dataId)
					parNode.unHighlight(		)
		except:
		    pass

        if self.mode == "hLight":
            try:
	        N =  selectionPath.getLength()
	        for i in range( N ):
		    node	= selectionPath.getNodeFromTail(i)
	            if node.getClassTypeId() == \
		    		SoIndexedFaceSet.getClassTypeId():
		        for j in range( N-i ):
		            parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
			        mainWin	        = self.asg.settingObj
			        if mainWin:
                                    mainWin.hLightVolActorGroup(parNode.dataId)
		    if node.getClassTypeId() == \
		    		SoIndexedLineSet.getClassTypeId():
		        for j in range( N-i ):
		            parNode = selectionPath.getNodeFromTail(i+j)
			    if isinstance( parNode, acuSgActor.AcuSgActor):
			        if parNode.extOutlineFlag:
			            mainWin	= self.asg.settingObj
			            if mainWin:
                                        mainWin.hLightVolActorGroup(parNode.dataId)
	    except:
	        pass

	    self.asg.volSelection.deselectAll(			)


	if self.mode == "zoom":
	    self.asg.volSelection.lassoType.setValue( \
				SoExtSelection.NOLASSO			)

#---------------------------------------------------------------------------
# home: sets the camera to it's home position
#---------------------------------------------------------------------------

    def home( self ):
        '''
	    sets the camera to home position
	    Arguments:
	        None
	    Output:
	        None
        '''
        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )

        self.viewer.resetToHomePosition()
        self.changeRotationCenter(self.globalCenter)

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(         mode = 'new'        )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_HOME
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )
        
#---------------------------------------------------------------------------
# fit: sets the camera to fit all the actors in the scenegraph
#---------------------------------------------------------------------------

    def fit( self ):
        '''
	    sets the camera to fit all the actors in the scenegraph
	    Arguments:
	        None
	    Output:
	        None
        '''
        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )

        self.asg.viewModel(					        )

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(     mode = 'new'            )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_FIT
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )

#---------------------------------------------------------------------------
# alignAxis: align the camera to closest principal axis
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
# snap: compute and align the camera to closest principal axis
#---------------------------------------------------------------------------

    def snap( self , zsnap = False,
              #----- Misc 4/08 : E9
              addMarker = True          ):
        '''
	    snaps the camera to to the closest principal axes
	    Arguments:
	        zsnap	 - if True snaps only in the z-plane ( default=False)
	    Output:
	        None
        '''

	camera	= self.viewer.getCamera()
	pos	= camera.position.getValue()
	fDist	= camera.focalDistance.getValue()
	rot	= camera.orientation.getValue()

        #----- Misc 4/08 : E9
        if addMarker:
            # Get the last value
            lstVal      = self.getUndoSettVals(                         )
	upvec		= SbVec3f( 0, 1, 0 )
	lookat		= SbVec3f( 0, 0,-1 )

	rot.multVec( upvec , upvec  )
	rot.multVec( lookat, lookat )

	ux,uy,uz	= upvec.getValue()
	dx,dy,dz	= lookat.getValue()
	px,py,pz	= pos.getValue()

	fx		= px + dx * fDist
	fy		= py + dy * fDist
	fz		= pz + dz * fDist

	ax, ay, az	= px - fx, py - fy, pz - fz
	aa		= math.sqrt( ax*ax + ay*ay + az*az )
	ax, ay, az	= self.alignAxis( ax, ay, az )

	px, py, pz	= fx + aa*ax, fy + aa*ay, fz + aa*az
	t		= ax * ux + ay * uy + az * uz
	ux, uy, uz	= ux - t * ax, uy - t * ay, uz - t * az

	if zsnap:
	    t		= math.sqrt( ux*ux + uy*uy + uz*uz )
	    ux,uy,uz	= ux / t, uy / t, uz / t
	else:
	    ux,uy,uz	= self.alignAxis( ux, uy, uz )
	
	focalPoint	= SbVec3f( fx, fy, fz )
	upVec		= SbVec3f( ux, uy, uz )

	camera.position.setValue( 	SbVec3f(px,py,pz) 		)
	camera.pointAt( 		focalPoint, upVec 		)
	self.viewer.redraw(						)

        #----- Misc 4/08 : E9
        if addMarker :
            # Get the new value
            newVal      = self.getUndoSettVals(     mode = 'new'        )

            if self.win:
                tag         = self.win.undoStn.UNDO_TAG_SNAP
                self.win.addSettingMarker(  tag,
                                            par     = 'transform',
                                            lastVal = lstVal,
                                            newVal  = newVal,
                                            func    = self.refreshUndoSett)

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
        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )

        self.snap(  True, addMarker = False )

        # Get the new value
        newVal      = self.getUndoSettVals(         mode = 'new'        )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_SNAPZ
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )

        #----- End of Misc 4/08 : E9

#---------------------------------------------------------------------------
# showSurface: set the mode to picking to allow picking the surface
#              to be projected normal to the screen
#---------------------------------------------------------------------------


    def showSurface( self ):
        '''
	    positions the camera in such a way that the normal to the
	    screen is parallel to the normal to the mesh set.
	    Arguments:
	        None
	    Output:
	        None
        '''
	if self.mode == 'rbPick' or self.mode == 'pick' or \
	   self.mode == 'lassoPick':
	   return

        #----- Misc 4/08 : E9
        # Get the last value
        self.recalstVal  = self.getUndoSettVals(                         )
        self.pickableSrf = True

        self.mode = "showSurf"
	self.asg.pntSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	self.asg.linSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	self.asg.srfSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	self.asg.volSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	#----- Misc. 04/09 H1 SH
	self.asg.edgSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	
	self.asg.showPickableSrf(					)
	self.viewer.mode( 	acuSgViewer.MODE_PICKING 		)
	self.asg.remStaticObjects(					)
	self.viewer.actualRedraw(					)
	
#---------------------------------------------------------------------------
# showSelSurface: project the selected surface normal to the screen
#---------------------------------------------------------------------------

    def showSelSurface( self, actor, fitFlag = False ):
        '''
	    show the selected surface. Used by  showSurface function

	    Arguments:
	        srfName		- name of the surface actor
	        fitFlag		- To fit the surface in the window( False )
	    Output:
	        None
        '''

	if actor != None:
	    camera	= self.viewer.getCamera(			)

	    fd		= camera.focalDistance.getValue(		)
	    pos		= camera.position.getValue(			)
	    rot		= camera.orientation.getValue(			)

	    lookat	= SbVec3f( 		0, 0, -1 		)
	    rot.multVec( 			lookat, lookat 		)

	    upvec	= SbVec3f( 		0, 1, 0 		)
	    rot.multVec( 			upvec, upvec 		)

	    ux,uy,uz	= upvec.getValue(				)
	    px,py,pz	= pos.getValue(					)
	    dx,dy,dz	= lookat.getValue(				)

	    fx,fy,fz	= px - fd*dx, py - fd*dy, pz - fd*dz

	    if actor.normDir == None:
	        nx, ny, nz = 1, 0, 0
		print "No Normal"
	    else:
		nx,ny,nz	= actor.normDir

	    px,py,pz	= fx - fd * nx , fy - fd * ny , fz - fd * nz
	    camera.position.setValue( 		SbVec3f( px,py,pz ) 	)
	    camera.pointAt( SbVec3f( fx,fy,fz ),SbVec3f(ux,uy,uz) 	)

	    if fitFlag == True:
		cx, cy, cz	= actor.center
		ctr		= SbVec3f( 		cx, cy, cz 	)
		viewVol	= camera.getViewVolume( \
					self.viewer.getGLAspectRatio() 	)

		viewVol.projectToScreen(  	ctr, ctr		)
		lx, ly, lz	= ctr.getValue()
		loc		= [ lx, ly ]
		self.translateCamera( 		loc 			)
		vpr	= self.viewer.getViewportRegion(		)
		camera.viewAll(			actor,vpr,0.3		)

	    self.viewer.redraw(						)
	self.asg.addStaticObjects(					)

#---------------------------------------------------------------------------
# fit: fits the selected surface in the window
#---------------------------------------------------------------------------

    def fitSurface( self ):
        '''
	    fit the selected surface.

	    Arguments:
	        None
	    Output:
	        None
	'''
	if self.mode == 'rbPick' or self.mode == 'pick' or \
	   self.mode == 'lassoPick':
	   return
        #----- Misc 4/08 : E9
        # Get the last value
        self.recalstVal  = self.getUndoSettVals(                     )
        self.pickableSrf = True

        self.mode = "fitSurf"
	self.asg.pntSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	self.asg.linSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	self.asg.srfSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	self.asg.volSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	#----- Misc. 04/09 H1 SH
        self.asg.edgSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	
	self.asg.showPickableSrf(					)

	self.viewer.mode( 	acuSgViewer.MODE_PICKING 		)
	self.asg.remStaticObjects(					)
	self.viewer.actualRedraw(					)

#---------------------------------------------------------------------------
# expFunc1:
#---------------------------------------------------------------------------
    def expFunc1( self ):
        self.expFuncLasso(					)

#---------------------------------------------------------------------------
# expFunc2DActors:  Usage for adding 2D text actors
#---------------------------------------------------------------------------

    def expFunc2DActors( self ):
        self.asg.addTxtActor(		"ACUSIM 0.1 0.5", [0.0,0.5]	)
        self.asg.addTxtActor(		"ACUSIM 0.5 0.5", [0.5,0.5]	)
        self.asg.addTxtActor(		"ACUSIM 0.9 0.5", [1.0,0.5]	)

        self.asg.addTxtActor(		"ACUSIM 0.5 0.1", [0.5,0.0]	)
        self.asg.addTxtActor(		"ACUSIM 0.5 0.3", [0.5,0.3]	)
        self.asg.addTxtActor(		"ACUSIM 0.5 0.9", [0.5,1.0]	)
    

#---------------------------------------------------------------------------
# expFuncLasso: Usage for setting lasso mode 
#---------------------------------------------------------------------------
    def expFuncLasso( self ):
        if self.lassoPickMode != SoExtSelection.ALL_SHAPES:
	    self.lassoPickMode= SoExtSelection.ALL_SHAPES
        else:
	    self.lassoPickMode= SoExtSelection.VISIBLE_SHAPES
 

#---------------------------------------------------------------------------
# expFuncCutPlane:  experimental function for drawing cut planes
#---------------------------------------------------------------------------
    def expFuncCutPlane( self ):
        if not self.cutPlnFlag:
	    self.startCutPlane()
        else:
	    self.endCutPlane()

#---------------------------------------------------------------------------
# startCutPlane:  
#---------------------------------------------------------------------------
    def startCutPlane( self ):
	self.viewer.mode(		acuSgViewer.MODE_PICKING	)
	self.asg.remStaticObjects(					)
	self.viewer.actualRedraw(					)
        self.cutPlnFlag	= TRUE
	self.viewer.actualRedraw(					)
	self.cPlane = self.asg.addCutPlane(				)

#---------------------------------------------------------------------------
# endCutPlane:  
#---------------------------------------------------------------------------
    def endCutPlane( self ):
	self.viewer.mode(		acuSgViewer.MODE_VIEWING	)
        self.cutPlnFlag	= FALSE
	self.cutPlane	= None
	self.asg.remCutPlane(						)
	self.asg.addStaticObjects(					)

#---------------------------------------------------------------------------
# expFunc1SrfPick:  experimental function for surface picking
#---------------------------------------------------------------------------

    def expFunc1SrfPick( self ):
        '''
	    Function for surface picking
	'''
	##### Unhighlight all the surfaces before calling this code block

	if self.srfPickFlag:
	    myList = self.endPick(					)
	    for id in myList:
	        if id not in self.asg.actors:
		    raise acuSgTformError,"Unknown actor <%d> " % id
		mainWin	= self.asg.settingObj
		if mainWin:
                    admSets	= mainWin.adminSets
                    if id in admSets.srfMeshModel:
                        print "DataId of the actor <%s>  : " % id
                        print "Surface Group name  <%s>  : " % admSets.srfMeshModel[id]
                    if id in admSets.srfGeomModel:
                        print "DataId of the actor <%s>  : " % id
                        print "Surface Group Name  <%s>  : " % admSets.srfGeomModel[id]
	else:
	    self.startPickSrf(						)

#---------------------------------------------------------------------------
# expFunc2:  experimental function for volume picking
#---------------------------------------------------------------------------

    def expFunc2( self ):
        '''
	    Function for volume picking
	'''

	##### Unhighlight all the volumes before calling this code block
	if self.volPickFlag:
	    myList = self.endPick(					)
	    for id in myList:
	        if id not in self.asg.actors:
		    raise acuSgTformError, "Unknown actor <%d> " % id
		mainWin	= self.asg.settingObj
		if mainWin:
                    admSets	= mainWin.adminSets
                    if id in admSets.volMeshModel:
                        print "DataId of the actor <%s>  : " % id
                        print "Surface Group name  <%s>  : " % admSets.volMeshModel[id]
                    if id in admSets.volGeomModel:
                        print "DataId of the actor <%s>  : " % id
                        print "Surface Group Name  <%s>  : " % admSets.volGeomModel[id]
	else:
	    	self.startPickVol(					)

#---------------------------------------------------------------------------
# center: makes the selected point to be the center of the window
#         the point is captured by previous mouse click
#---------------------------------------------------------------------------

    def center( self ):
        '''
	    To make the location provided to be the center of the screen.
	    This location is obtained by mouse click

	    Arguments:
	        None
	    Output:
	        None
        '''
        #----- Misc 4/08 : E9
        # Get the last value
        self.recalstVal = self.getUndoSettVals(                     )
	self.resetMode(							)
        self.mode = "center"
	self.asg.pntSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	self.asg.linSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	self.asg.srfSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	self.asg.volSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	#----- Misc. 04/09 H1 SH
	self.asg.edgSelection.lassoType.setValue( SoExtSelection.NOLASSO)
	
	self.viewer.mode( 	acuSgViewer.MODE_PICKING 		)
	self.ctrlBinding	= self.viewer.getMouseBinding(	"CTRL"	)
	self.shiftBinding	= self.viewer.getMouseBinding(	"SHIFT"	)
	self.shCtrlBinding	= self.viewer.getMouseBinding("SHIFT_CTRL")
	self.viewer.setMouseBinding( "CTRL", "NONE")
	self.viewer.setMouseBinding( "SHIFT", "NONE")
	self.viewer.setMouseBinding( "SHIFT_CTRL", "NONE")
	self.asg.remStaticCameras(					)
	self.viewer.actualRedraw(					)

#---------------------------------------------------------------------------
# centerOfRotation:
#---------------------------------------------------------------------------

    def centerOfRotation( self, value = None  ):
        ''' set the center of rotation 
	    Arguments:
	        value = node or path of the scenegraph. 
		        if None (default) dynObjects of sceneGraph is assumed
	    Output:
	        None
	
	'''
	vp 	= self.viewer.getViewportRegion(			)
	bbox = SoGetBoundingBoxAction(			vp		)

	if value == None:
	    bbox.apply(				self.asg.dynObjects	)
	    xL,yL,zL,xR,yR,zR	= bbox.getBoundingBox().getBounds(	)
	    cx	= 0.5 * ( xL + xR )
	    cy	= 0.5 * ( yL + yR )
	    cz	= 0.5 * ( zL + zR )
	    self.viewer.setFocalPoint(		[cx,cy,cz]		)

	elif isinstance( value, acuSgActor.AcuSgActor):
	    bbox.apply(				value			)
	    xL,yL,zL,xR,yR,zR	= bbox.getBoundingBox().getBounds(	)
	    cx	= 0.5 * ( xL + xR )
	    cy	= 0.5 * ( yL + yR )
	    cz	= 0.5 * ( zL + zR )
	    self.viewer.setFocalPoint(		[cx,cy,cz]		)

	elif type(value) == types.ListType or type(value) == types.TupleType:
	    if len(value) == 2:
		vv	= camera.getViewVolume( \
					self.viewer.getGLAspectRatio() 	)
		line	= SbLine(					)
		fD	= camera.focalDistance.getValue(		)
		pln	= vv.getPlane(		fD			)
		pos	= SbVec2f(	value[0], value[1]		)
		vv.projectPointToLine(		pos, line		)

		pt	= SbVec3f(					)
		pln.intersect(			line, pt		)
		cx,cy,cz= pt.getValue(					)
		self.viewer.setFocalPoint(	[cx,cy,cz]		)

	    elif len(value) == 3:
	        self.viewer.setFocalPoint(		value		)
	else:
	    print "undefined argument type to centerOfRotation"

   

#---------------------------------------------------------------------------
# setLassoPickPolicy:
#---------------------------------------------------------------------------

    def setLassoPickPolicy( self, policy ):

        ''' set lasso pick policy 
	    Argument:
	        policy	 - "FULL", "PART", "FULL_BBOX", "PART_BBOX"
	    Output:
	        None
        '''

	if policy == "FULL":
	    self.lassoPickPlcy	= SoExtSelection.FULL
	elif policy == "FULL_BBOX":
	    self.lassoPickPlcy	= SoExtSelection.FULL_BBOX
	elif policy == "PART":
	    self.lassoPickPlcy	= SoExtSelection.PART
	elif policy == "PART_BBOX":
	    self.lassoPickPlcy	= SoExtSelection.PART_BBOX
        else:
	    print "undefined policy in setLassoPickPolicy"

        if self.srfPickFlag and \
		( self.mode == 'rbPick' or self.mode == 'lassoPick'):
	    self.asg.srfSelection.lassoPolicy.setValue(self.lassoPickPlcy)

        if self.volPickFlag and \
		( self.mode == 'rbPick' or self.mode == 'lassoPick'):
	    self.asg.volSelection.lassoPolicy.setValue(self.lassoPickPlcy)

        #----- Misc. 04/09 H1 SH
	if self.edgPickFlag and \
		( self.mode == 'rbPick' or self.mode == 'lassoPick'):
	    self.asg.edgSelection.lassoPolicy.setValue(self.lassoPickPlcy)

#---------------------------------------------------------------------------
# setLassoPickMode:
#---------------------------------------------------------------------------

    def setLassoPickMode( self, lmode ):

        ''' set lasso pick mode 
	    Argument:
	        lmode	 - "ALL_SHAPES", "VISIBLE_SHAPES"
	    Output:
	        None
        '''

	if lmode == "ALL_SHAPES":
	    self.lassoPickMode	= SoExtSelection.ALL_SHAPES
	elif lmode == "VISIBLE_SHAPES":
	    self.lassoPickMode	= SoExtSelection.VISIBLE_SHAPES
        else:
	    print "undefined lasso mode in setLassoPickMode"

        if self.srfPickFlag and \
		( self.mode == 'rbPick' or self.mode == 'lassoPick'):
	    self.asg.srfSelection.lassoMode.setValue( self.lassoPickMode)

        if self.volPickFlag and \
		( self.mode == 'rbPick' or self.mode == 'lassoPick'):
	    self.asg.volSelection.lassoMode.setValue( self.lassoPickMode)

        #----- Misc. 04/09 H1 SH
	if self.edgPickFlag and \
		( self.mode == 'rbPick' or self.mode == 'lassoPick'):
	    self.asg.edgSelection.lassoMode.setValue( self.lassoPickMode)

#---------------------------------------------------------------------------
# translateCamera: translates the camera to the spefied location
#---------------------------------------------------------------------------

    def translateCamera( self, loc = None ):
        '''
	    To translate the camera to the provided location in screen
	    coordinates

	    Arguments:
	        loc	- x,y values of the screen location
	    Output:
	        None
        '''

	camera	= self.viewer.getCamera(				)
	viewVol	= camera.getViewVolume( \
	    self.viewer.getGLAspectRatio() 				)

	fd          	= camera.focalDistance.getValue(		)
	panPlane	= viewVol.getPlane( 		fd 		)

	tox,toy	= loc[0],loc[1]
	viewVol.projectPointToLine( 	SbVec2f(tox,toy), self.line 	)

	curPlanePt	= SbVec3f(					)
	panPlane.intersect( 		self.line, curPlanePt 		)
	cx,cy,cz	= curPlanePt.getValue(				)


	viewVol.projectPointToLine( 	SbVec2f(0.5,0.5), self.line 	)
	oldPlanePt	= SbVec3f(					)
	panPlane.intersect( 		self.line, oldPlanePt 		)
	ox,oy,oz	= oldPlanePt.getValue(				)

	px,py,pz	= camera.position.getValue(			)
	px,py,pz	= px + (cx-ox), py + (cy-oy),pz + (cz-oz)

	camera.position.setValue( 	SbVec3f( px,py,pz ) 		)

#---------------------------------------------------------------------------
# toggleAxis: function to toggle the axis
#---------------------------------------------------------------------------

    def toggleAxis( self ):
        '''
	    toggles the axis display in the graphical window
	    Arguments:
	        None
	    Output:
	        None
        '''

	if self.viewer.isFeedbackVisible():
	    self.viewer.setFeedbackVisibility( 		False 		)
	else:
	    self.viewer.setFeedbackVisibility( 		True 		)
	self.viewer.redraw(						)

#---------------------------------------------------------------------------
# rotatePX45:  Rotate the camera by 45 degrees in plus X
#---------------------------------------------------------------------------


    def rotatePX45( self ):
        '''
	    Rotate the camera in +X ( not screen X ) by 45 degrees
	    Arguments:
	        None
	    Output:
	        None
        '''

        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )
        
	self.resetMode(							)

	camera = self.viewer.getCamera(					)
	angle	= math.pi/4
	rot	= SbRotation( 		SbVec3f( 1,0,0 ), angle 	)
	pos	= camera.position.getValue(				)
	curVal = camera.orientation.getValue( 				)

	mtx	= SbMatrix(						)
	mtx.setRotate( 			rot 				)
	mtx.multVecMatrix( 		pos, pos 			)

	camera.position.setValue( 	pos 				)
	camera.orientation.setValue( 	curVal *  rot 			)

	self.asg.viewModel(						)

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(         mode = 'new'        )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_ROTATE_X_P
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )
        
#---------------------------------------------------------------------------
# rotateMX45:  Rotate the camera by 45 degrees in minus X
#---------------------------------------------------------------------------

    def rotateMX45( self ):
        '''
	    Rotate the camera in -X ( not screen X ) by 45 degrees
	    Arguments:
	        None
	    Output:
	        None
        '''

        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )
        
	self.resetMode(							)
	camera 	= self.viewer.getCamera(				)
	angle	= math.pi/4
	rot	= SbRotation( 		SbVec3f( -1,0,0 ), angle 	)
	pos	= camera.position.getValue(				)
	curVal	= camera.orientation.getValue( 				)

	mtx	= SbMatrix(						)
	mtx.setRotate( rot 						)
	mtx.multVecMatrix( 		pos, pos 			)

	camera.position.setValue( 	pos 				)
	camera.orientation.setValue( 	curVal *  rot 			)

	self.asg.viewModel(						)

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(         mode = 'new'        )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_ROTATE_X_M
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )
        
#---------------------------------------------------------------------------
# rotatePY45:  Rotate the camera by 45 degrees in plus Y
#---------------------------------------------------------------------------

    def rotatePY45( self ):
        '''
	    Rotate the camera in +Y ( not screen Y ) by 45 degrees
	    Arguments:
	        None
	    Output:
	        None
        '''

        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )
        
	self.resetMode(							)
	camera	= self.viewer.getCamera(				)
	angle	= math.pi/4
	rot	= SbRotation( 		SbVec3f( 0,1,0 ), angle 	)
	pos	= camera.position.getValue(				)
	curVal	= camera.orientation.getValue( 				)

	mtx	= SbMatrix(						)
	mtx.setRotate( 			rot 				)
	mtx.multVecMatrix( 		pos, pos 			)

	camera.position.setValue( 	pos 				)
	camera.orientation.setValue( 	curVal *  rot 			)

	self.asg.viewModel(						)

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(         mode = 'new'        )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_ROTATE_Y_P
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )
        
#---------------------------------------------------------------------------
# rotateMY45:  Rotate the camera by 45 degrees in minus Y
#---------------------------------------------------------------------------

    def rotateMY45( self ):
        '''
	    Rotate the camera in -Y ( not screen Y ) by 45 degrees
	    Arguments:
	        None
	    Output:
	        None
        '''

        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )
        
	self.resetMode(							)
	camera	= self.viewer.getCamera(				)
	angle	= math.pi/4
	rot	= SbRotation( 		SbVec3f( 0,-1,0 ), angle 	)
	pos	= camera.position.getValue(				)
	curVal	= camera.orientation.getValue( 				)

	mtx	= SbMatrix(						)
	mtx.setRotate( 			rot 				)
	mtx.multVecMatrix( 		pos, pos 			)

	camera.position.setValue( 	pos 				)
	camera.orientation.setValue( 	curVal *  rot 			)

	self.asg.viewModel(						)

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(             mode = 'new'    )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_ROTATE_Y_M
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )
        
#---------------------------------------------------------------------------
# rotatePZ45:  Rotate the camera by 45 degrees in pluz Z
#---------------------------------------------------------------------------

    def rotatePZ45( self ):
        '''
	    Rotate the camera in +Z ( not screen Z ) by 45 degrees
	    Arguments:
	        None
	    Output:
	        None
        '''

        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )
        
	self.resetMode(							)
	camera	= self.viewer.getCamera(				)
	angle	= math.pi/4
	rot	= SbRotation( 		SbVec3f( 0,0,1 ), angle 	)
	pos	= camera.position.getValue(				)
	curVal	= camera.orientation.getValue( 				)

	mtx	= SbMatrix(						)
	mtx.setRotate( 				rot 			)
	mtx.multVecMatrix( 			pos, pos 		)

	camera.position.setValue( 		pos 			)
	camera.orientation.setValue( 		curVal *  rot 		)

	self.asg.viewModel(						)

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(     mode = 'new'            )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_ROTATE_Z_P
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )
        
#---------------------------------------------------------------------------
# rotateMZ45:  Rotate the camera by 45 degrees in minus Z
#---------------------------------------------------------------------------

    def rotateMZ45( self ):
        '''
	    Rotate the camera in -Z ( not screen Z ) by 45 degrees
	    Arguments:
	        None
	    Output:
	        None
        '''

        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )
        
	self.resetMode(							)
	camera	= self.viewer.getCamera(				)
	angle	= math.pi/4
	rot	= SbRotation( 		SbVec3f( 0,0,-1 ), angle 	)
	pos	= camera.position.getValue(				)
	curVal	= camera.orientation.getValue( 				)

	mtx	= SbMatrix(						)
	mtx.setRotate( 			rot 				)
	mtx.multVecMatrix( 		pos, pos 			)

	camera.position.setValue( 	pos 				)
	camera.orientation.setValue( 	curVal *  rot 			)

	self.asg.viewModel(						)

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(         mode = 'new'        )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_ROTATE_Z_M
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )

#---------------------------------------------------------------------------
# rotate:  Rotate the camera by arbitrary degrees in arbitrary direction
#---------------------------------------------------------------------------

    def rotate( self, dir, angle ):
        '''
	    Rotate the camera by arbitrary degrees in arbitrary direction
	    Arguments:
	        dir     - A direction ( 'x+', '+x', 'xplus',
                                        'y+', '+y', 'yplus',
                                        'z+', '+z', 'zplus',
                                        'x-', '-x', 'xminus',
                                        'y-', '-y', 'yminus',
                                        'z-', '-z', 'zminus'    )
                            It is in case insensitive manor

                angle   - Degree of rotation
                
	    Output:
	        None
        '''

        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )
        
	self.resetMode(							)

        if dir and angle:
            direction   = string.lower( dir                             )
        else:
            raise acuSgTformError, "Direction or angle value "\
                                    "in rotate is undefined"

	if direction in [ 'x+', '+x', 'xplus'   ]:
            vector  = SbVec3f(          1,0,0                           )
            if self.win:
                tag     = self.win.undoStn.UNDO_TAG_ROTATE_X_P

        elif direction in [ 'x-', '-x', 'xminus']:
            vector  = SbVec3f(          -1,0,0                          )
            if self.win:
                tag     = self.win.undoStn.UNDO_TAG_ROTATE_X_M

        elif direction in [ 'y+', '+y', 'yplus' ]:
            vector  = SbVec3f(          0,1,0                           )
            if self.win:
                tag     = self.win.undoStn.UNDO_TAG_ROTATE_Y_P

        elif direction in [ 'y-', '-y', 'yminus']:
            vector  = SbVec3f(          0,-1,0                          )
            if self.win:
                tag     = self.win.undoStn.UNDO_TAG_ROTATE_Y_M

        elif direction in [ 'z+', '+z', 'zplus' ]:
            vector  = SbVec3f(          0,0,1                           )
            if self.win:
                tag     = self.win.undoStn.UNDO_TAG_ROTATE_Z_P

        elif direction in [ 'z-', '-z', 'zminus']:
            vector  = SbVec3f(          0,0,-1                          )
            if self.win:
                tag     = self.win.undoStn.UNDO_TAG_ROTATE_Z_M

        else:
            raise acuSgTformError, "Direction '(%s)' value "\
                      "in rotate is undefined or incorrect." %dir

        camera      = self.viewer.getCamera(				)
	angle	    = math.pi/(         180/angle                       )
        
	rot	    = SbRotation( 	vector, angle 	                )
	pos	    = camera.position.getValue(				)
	curVal      = camera.orientation.getValue( 			)

	mtx	= SbMatrix(						)
	mtx.setRotate( 			rot 				)
	mtx.multVecMatrix( 		pos, pos 			)

	camera.position.setValue( 	pos 				)
	camera.orientation.setValue( 	curVal *  rot 			)

	self.asg.viewModel(						)

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(         mode = 'new'        )

        if self.win:
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )
        
#---------------------------------------------------------------------------
# resetMode:
#---------------------------------------------------------------------------

    def resetMode( self ):
        '''
	    reset mode from zoom or center to none
        '''

        if  ( self.mode == 'zoom' or self.mode == 'center' or \
	    self.mode == 'showSurf' or self.mode == 'fitSurf' ) \
	    and (self.mode != 'pick' and self.mode != 'rbPick' and \
	    self.mode != 'lassoPick' ):
	    self.mode = 'none'
	    self.viewer.mode(	acuSgViewer.MODE_VIEWING	)
	    self.asg.resetLassoTypes(				)
	    self.asg.addStaticCameras(				)
	    self.asg.addStaticObjects(				)

#---------------------------------------------------------------------------
# setXp:  sets the camera to look up in X direction
#---------------------------------------------------------------------------

    def setXp( self ):
        '''
	    Sets the camera to look up in X direction
	    Arguments:
	        None
	    Output:
	        None
        '''

        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )

	self.resetMode(							)
	camera	= self.viewer.getCamera(				)

	target	= SbVec3f( 			1,0,0 			)
	upvec	= SbVec3f( 			0,1,0 			)
	pos	= SbVec3f( 			-1,0,0 			)

	camera.position.setValue( 		pos 			)
	camera.pointAt( 			target, upvec 		)

	self.asg.viewModel(					        )

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(     mode = 'new'            )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_VIEW_X_P
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )
	
#---------------------------------------------------------------------------
# setXm:  sets the camera to look down in X direction
#---------------------------------------------------------------------------

    def setXm( self ):
        '''
	    Sets the camera to look down in X direction
	    Arguments:
	        None
	    Output:
	        None
        '''

        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )
        
	self.resetMode(							)
	camera	= self.viewer.getCamera(				)

	target	= SbVec3f( 			-1,0,0 			)
	upvec	= SbVec3f(  			0,1,0 			)
	pos	= SbVec3f(  			1,0,0 			)

	camera.position.setValue( 		pos 			)
	camera.pointAt( 			target, upvec 		)

	self.asg.viewModel(					        )

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(     mode = 'new'            )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_VIEW_X_M
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )

#---------------------------------------------------------------------------
# setYp:  sets the camera to look up in Y direction
#---------------------------------------------------------------------------

    def setYp( self ):
        '''
	    Sets the camera to look up in Y direction
	    Arguments:
	        None
	    Output:
	        None
        '''

        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )
        
	self.resetMode(							)
	camera	= self.viewer.getCamera(				)

	target	= SbVec3f(  			0, 1,0 			)
	upvec	= SbVec3f(  			0, 0,1 			)
	pos	= SbVec3f(  			0,-1,0 			)

	camera.position.setValue( 		pos 			)
	camera.pointAt( 			target, upvec 		)

	self.asg.viewModel(					        )

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(     mode = 'new'            )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_VIEW_Y_P
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )

#---------------------------------------------------------------------------
# setYm:  sets the camera to look down in Y direction
#---------------------------------------------------------------------------

    def setYm( self ):
        '''
	    Sets the camera to look down in Y direction
	    Arguments:
	        None
	    Output:
	        None
        '''

        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )
        
	self.resetMode(							)
	camera	= self.viewer.getCamera(				)
	target	= SbVec3f(  			0,-1,0 			)
	upvec	= SbVec3f(  			0, 0,1 			)
	pos	= SbVec3f(  			0, 1,0 			)

	camera.position.setValue( 		pos 			)
	camera.pointAt( 			target, upvec 		)

	self.asg.viewModel(					        )

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(     mode = 'new'            )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_VIEW_Y_M
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )
        
#---------------------------------------------------------------------------
# setZp:  sets the camera to look up in Z direction
#---------------------------------------------------------------------------

    def setZp( self ):
        '''
	    Sets the camera to look up in Z direction
	    Arguments:
	        None
	    Output:
	        None
        '''

        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )
        
	self.resetMode(							)
	camera	= self.viewer.getCamera(				)
	target	= SbVec3f(  			0, 0, 1 		)
	upvec	= SbVec3f(  			1, 0, 0 		)
	pos	= SbVec3f(  			0, 0,-1 		)

	camera.position.setValue( 		pos 			)
	camera.pointAt( 			target, upvec 		)

	self.asg.viewModel(					        )

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(     mode = 'new'            )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_VIEW_Z_P
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )
        
#---------------------------------------------------------------------------
# setZm:  sets the camera to look down in Z direction
#---------------------------------------------------------------------------

    def setZm( self ):
        '''
	    Sets the camera to look down in Z direction
	    Arguments:
	        None
	    Output:
	        None
        '''

        #----- Misc 4/08 : E9
        # Get the last value
        lstVal      = self.getUndoSettVals(                             )
        
	self.resetMode(							)
	camera	= self.viewer.getCamera(				)
	target	= SbVec3f(  			0, 0,-1 		)
	upvec	= SbVec3f(  			1, 0, 0 		)
	pos	= SbVec3f(  			0, 0, 1 		)

	camera.position.setValue( 		pos 			)
	camera.pointAt( 			target, upvec 		)

	self.asg.viewModel(					        )

        #----- Misc 4/08 : E9
        # Get the new value
        newVal      = self.getUndoSettVals(     mode = 'new'            )

        if self.win:
            tag         = self.win.undoStn.UNDO_TAG_VIEW_Z_M
            self.win.addSettingMarker(  tag,
                                        par     = 'transform',
                                        lastVal = lstVal,
                                        newVal  = newVal,
                                        func    = self.refreshUndoSett  )
        
#---------------------------------------------------------------------------
# recall:  recall the camera position stored by id
#---------------------------------------------------------------------------

    def recall( self, id ):
        '''
	    recall the camera settings from a dictionary with the key
	    provided to the function in the form of an id
	    Arguments:
	        id		- key of the stored position
	    Output:
	        None
        '''

	if self.transMat.has_key(id):
	    camera	= self.viewer.getCamera(			)
	    storedCam	= self.transMat[id]
	    camera.copyContents( 	storedCam, FALSE		)
	
#---------------------------------------------------------------------------
# store:  store the camera position by id
#---------------------------------------------------------------------------

    def store( self, id ):
        '''
	    stores the camera settings in a dictionary with the key
	    provided to the function in the form of an id
	    Arguments:
	        id		- key of the stored position
	    Output:
	        None
        '''
	camera		= self.viewer.getCamera()
	storedCam	= SoOrthographicCamera()
	storedCam.copyContents(			camera, FALSE		)
	self.transMat[id]	= storedCam

#---------------------------------------------------------------------------
# toggleLogo: function to toggle the logo
#---------------------------------------------------------------------------

    def toggleLogo( self, addMark = True ):
        '''
	    toggles the logo display in the graphical window
	    Arguments:
	        None
	    Output:
	        None
        '''
        #----- Misc 4/08 : E2
        if addMark and self.win:
            tag = self.win.undoStn.UNDO_TAG_TGL_LOGO
            self.win.addSettingMarker(  tag,
                                        func = self.toggleLogo          )
        #----- End of Misc 4/08 : E2

        if not self.logoDsp:

	    if os.path.exists( self.acuLogoFile ):
                self.logoAct= self.asg.addImgActor(
                                        filename    = self.acuLogoFile,
                                        position    = [0.01,0.98],
                                        width       = -1,
                                        height      = -1,
                                        horAlignment= "LEFT",
                                        verAlignment= "TOP"		)
	    else:
                self.logoAct= self.asg.addImgActor(
                                        filename    = None,
                                        image	    = _logo,
                                        position    = [0.01,0.98],
                                        width       = -1,
                                        height      = -1,
                                        horAlignment= "LEFT",
                                        verAlignment= "TOP"		)
            self.logoDsp    = 1
	else:
            self.asg.remImgActor(           self.logoAct                )
            self.logoDsp    = 0
        self.viewer.redraw(						)

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
	
	acuQt.setSetting(         'mainBack/logo',    self.logoDsp	)


#----- Misc 4/08 : E9
#---------------------------------------------------------------------------
# getUndoSettVals: 
#---------------------------------------------------------------------------

    def getUndoSettVals( self,mode = 'last' ):
        '''
	    Get the values need for undo/redo refreshing 
	    Arguments:
	        mode    -   "last" to get the last vals or
                            "new" to get the new vals 
	    Output:
	        None
        '''
	
        getVals = False
        vals    = self.lstVal
        if mode == 'last':
            if not self.lstVal:
                getVals = True
            elif( self.viewer.getCameraPosition(),
                    self.viewer.getCameraOrientation(),
                    self.viewer.getCameraHeight() )     != self.lstVal[0:3]:
                getVals = True
                
        else:
            getVals = True

        if getVals:
            vals =( self.viewer.getCameraPosition(),
                    self.viewer.getCameraOrientation(),
                    self.viewer.getCameraHeight(),
                    self.asg.pntSelection.lassoType.getValue(),
                    self.asg.linSelection.lassoType.getValue(),
                    self.asg.srfSelection.lassoType.getValue(),
                    self.asg.volSelection.lassoType.getValue(),
                    #----- Misc. 04/09 H1 SH
                    self.asg.edgSelection.lassoType.getValue(),
                    self.viewer.modeFlag,
                    self.mode,
                    self.viewer.getMouseBinding("CTRL"),
                    self.viewer.getMouseBinding("SHIFT"),
                    self.viewer.getMouseBinding("SHIFT_CTRL"),
                    self.pickableSrf                                    )

            self.lstVal    = vals

        return vals

#---------------------------------------------------------------------------
# refreshUndoSett:
#---------------------------------------------------------------------------

    def refreshUndoSett( self, values ):
        ''' refresh the value of camera,lassoType,mode,...'''

        pos, orint, height                                  = values[0:3]
        pntSelect, linSelect, srfSelec, volSelect, edgSelect= values[3:8]
        viewerMode, mode                                    = values[8:10]
	self.ctrlBinding,self.shiftBinding,self.shCtrlBinding=values[10:13]
	self.pickableSrf                                    = values[13]
	
        self.viewer.setCameraPosition(              pos                 )
        self.viewer.setCameraOrientation(           orint               )
        self.viewer.setCameraHeight(                height              )

	self.asg.pntSelection.lassoType.setValue(   pntSelect           )
	self.asg.linSelection.lassoType.setValue(   linSelect           )
	self.asg.srfSelection.lassoType.setValue(   srfSelec            )
	self.asg.volSelection.lassoType.setValue(   volSelect           )
	#----- Misc. 04/09 H1 SH
	self.asg.edgSelection.lassoType.setValue(   edgSelect           )

        self.viewer.mode(                           viewerMode          )
        self.mode   = mode

	self.viewer.setMouseBinding( "CTRL",        self.ctrlBinding    )
	self.viewer.setMouseBinding( "SHIFT",       self.shiftBinding   )
	self.viewer.setMouseBinding( "SHIFT_CTRL",  self.shCtrlBinding  )

        if self.pickableSrf:
            self.asg.showPickableSrf(                                   )
        else:
            self.asg.redraw(                                            )
        
#----- End of Misc 4/08 : E9
            

#---------------------------------------------------------------------------
# getCenterOfActor
#---------------------------------------------------------------------------

    def getCenterOfActor( self, actor = None ):

        #----- If no actor is specified, then all dynamic actors are considered
        
        if actor == None:
            actor = self.asg.dynObjects

        if isinstance( actor, acuSgActor.AcuSgActor ) and actor.center != None:
            return actor.center

        else:            
            vp 	    = self.viewer.getViewportRegion( )
            bbox    = SoGetBoundingBoxAction( vp )                       
            bbox.apply( actor )
            
            xL,yL,zL,xR,yR,zR   = bbox.getBoundingBox( ).getBounds( )
            
            cx	= 0.5 * ( xL + xR )
            cy	= 0.5 * ( yL + yR )
            cz	= 0.5 * ( zL + zR )

            if isinstance( actor, acuSgActor.AcuSgActor ):
                actor.center = (cx, cy, cz)

            return (cx, cy, cz)

#---------------------------------------------------------------------------
# changeRotationCenter
#---------------------------------------------------------------------------

    def changeRotationCenter( self, center ):
       
        if center == None:
            center = self.centerOfModelRotation( apply = False )

        self.globalCenter = center
        center = SbVec3f( center )

        #----- Change camera orientation
        
        camera = self.viewer.getCamera( )
        camera.pointAt( center )

        #----- Change camera focal distance (center)

        cameraPosition = camera.position.getValue( )
        newFocalDistance = ( center - cameraPosition ).length( )        
        camera.focalDistance.setValue( newFocalDistance )
        
#---------------------------------------------------------------------------
# globalRotation
#---------------------------------------------------------------------------

    def globalRotation( self ):

        globalCenter = ( 0, 0, 0 )
        self.changeRotationCenter( globalCenter )

        return globalCenter
       
#---------------------------------------------------------------------------
# centerOfModelRotation
#---------------------------------------------------------------------------

    def centerOfModelRotation( self, actor = None, apply = True ):

        centerOfActor = self.getCenterOfActor( actor )

        if apply:
            self.changeRotationCenter( centerOfActor )

        return centerOfActor
    
#---------------------------------------------------------------------------
# centerOfVisibleRotation
#---------------------------------------------------------------------------

    def centerOfVisibleRotation( self ):

        #----- Visible actors are dynamic objects

        centerOfVisibileActors = self.centerOfModelRotation( self.asg.dynObjects )

        return  centerOfVisibileActors

#---------------------------------------------------------------------------
# centerOfSurfaceRotation
#---------------------------------------------------------------------------

    def centerOfSurfaceRotation( self ):

        if not self.pickingStarted:
            self.singlePickSrf( )
            self.pickingStarted = True

        else:
            selectedSrf = self.endPick( )
            self.pickingStarted = False
            
            if selectedSrf != None:
                srf = self.asg.actors[ selectedSrf ]
                centerOfSurface = self.centerOfModelRotation( srf )

                return centerOfSurface
            
            else:
                return None

#---------------------------------------------------------------------------
# centerOfVolumeRotation
#---------------------------------------------------------------------------

    def centerOfVolumeRotation( self ):

        if not self.pickingStarted:
            self.startPickVol( )
            self.pickingStarted = True

        else:
            selectedVol = self.endPick( )
            self.pickingStarted = False
            
            if selectedVol != None and selectedVol != []:
                vol = self.asg.actors[ selectedVol[0] ]
                centerOfVolume = self.centerOfModelRotation( vol )

                return centerOfVolume
            
            else:
                return None

#---------------------------------------------------------------------------
# centerOfScreenRotation
#---------------------------------------------------------------------------

    def centerOfScreenRotation( self ):

        vpr	= self.viewer.getViewportRegion( )            
	rpa	= SoRayPickAction( vpr )  
	
	camera          = self.viewer.getCamera( )
	farDistance     = camera.focalDistance.getValue( )
	nearDistance    = camera.nearDistance.getValue( )

	centerOfScreen  = SbVec3f( self.getCenterOfActor( self.asg.dynObjects ) )
	cameraPosition  = camera.position.getValue( )
        cameraDirection = centerOfScreen - cameraPosition
        cameraDirection.normalize( )
        
	rpa.setRay( cameraPosition, cameraDirection, nearDistance, farDistance )
	rpa.apply( self.asg.dynObjects )

	pickedPoint = rpa.getPickedPoint( )	

	if pickedPoint != None:
            projectedCenterOfScreen = pickedPoint.getPoint( ).getValue( )
            self.changeRotationCenter( projectedCenterOfScreen )

            return projectedCenterOfScreen

        else:
            return None

#---------------------------------------------------------------------------
# pickCenterRotation
#---------------------------------------------------------------------------

    def pickCenterRotation( self ):

        if not self.pickingStarted:
            self.singlePickPnt( )
            self.pickingStarted = True

        else:
            self.asg.returnToLastVis( )
            self.asg.addStaticCameras( )
            self.asg.addStaticObjects( )
            self.viewer.mode( acuSgViewer.MODE_VIEWING )
            self.asg.remGeomActor( self.pointGeomActor )            
            self.pointGeomActor = None
            self.pickingStarted = False
                
            pickedCenter = self.getSinglePickPnt( )

            if pickedCenter != None:
                self.changeRotationCenter( pickedCenter )
              
            return pickedCenter

#---------------------------------------------------------------------------
# enterCenterRotation
#---------------------------------------------------------------------------

    def enterCenterRotation( self, center ):

        if center != None:
            self.changeRotationCenter( center )

        return center       
        
#---------------------------------------------------------------------------
# rotationCenter
#---------------------------------------------------------------------------
        
    def rotationCenter( self, type, center = None ):

        '''
            Arguments:

                        type    - "global", "model", "visible", "surface",
                                  "volume", "screen", "pick", "value"

            Output:
                        center
        '''              

        if   type == "global":
            center = self.globalRotation( )

        elif type == "model":
            center = self.centerOfModelRotation( apply = True )

        elif type == "visible":
            center = self.centerOfVisibleRotation( )        

	elif type == "surface":
            center = self.centerOfSurfaceRotation( )

        elif type == "volume":
            center = self.centerOfVolumeRotation( )            

        elif type == "screen":
            center = self.centerOfScreenRotation( )    

        elif type == "pick":
            center = self.pickCenterRotation( ) 

        elif type == "value":
            center = self.enterCenterRotation( center )
       
        return center
