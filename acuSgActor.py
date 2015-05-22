#===========================================================================
#
# Include files
#
#===========================================================================

import  acupu
import  acuQt
import  numarray
import  types
import  random
import  math
import  string

from    numarray        import *
from    iv              import *
from    acuCmap         import AcuCmap

#===========================================================================
#
# Useful defines
#
#===========================================================================

TRUE    = 1
True    = 1
FALSE   = 0
False   = 0

drawStyleMap_o				= {}
drawStyleMap_o['none']			= SoDrawStyle.INVISIBLE
drawStyleMap_o['outline']		= SoDrawStyle.FILLED
drawStyleMap_o['wireframe']		= SoDrawStyle.INVISIBLE
drawStyleMap_o['mesh']			= SoDrawStyle.INVISIBLE
drawStyleMap_o['solid']			= SoDrawStyle.INVISIBLE
drawStyleMap_o['point']			= SoDrawStyle.INVISIBLE
drawStyleMap_o['points']		= SoDrawStyle.INVISIBLE
drawStyleMap_o['line']			= SoDrawStyle.INVISIBLE
drawStyleMap_o['solid_outline']		= SoDrawStyle.INVISIBLE
drawStyleMap_o['solid_wire']		= SoDrawStyle.INVISIBLE
drawStyleMap_o['contour']		= SoDrawStyle.INVISIBLE
drawStyleMap_o['velocity_vector']	= SoDrawStyle.INVISIBLE
drawStyleMap_o['line_point']		= SoDrawStyle.INVISIBLE
drawStyleMap_o[SoDrawStyle.INVISIBLE]	= 'none'
drawStyleMap_o[SoDrawStyle.LINES]	= 'none'
drawStyleMap_o[SoDrawStyle.FILLED]	= 'outline'
drawStyleMap_o[SoDrawStyle.POINTS]	= 'none'

drawStyleMap_so				= {}
drawStyleMap_so['none']			= SoDrawStyle.INVISIBLE
drawStyleMap_so['outline']		= SoDrawStyle.INVISIBLE
drawStyleMap_so['wireframe']		= SoDrawStyle.INVISIBLE
drawStyleMap_so['mesh']			= SoDrawStyle.INVISIBLE
drawStyleMap_so['solid']		= SoDrawStyle.INVISIBLE
drawStyleMap_so['point']		= SoDrawStyle.INVISIBLE
drawStyleMap_so['points']		= SoDrawStyle.INVISIBLE
drawStyleMap_so['line']			= SoDrawStyle.INVISIBLE
drawStyleMap_so['solid_outline']	= SoDrawStyle.FILLED
drawStyleMap_so['solid_wire']		= SoDrawStyle.INVISIBLE
drawStyleMap_so['contour']		= SoDrawStyle.INVISIBLE
drawStyleMap_so['velocity_vector']	= SoDrawStyle.INVISIBLE
drawStyleMap_so['line_point']		= SoDrawStyle.INVISIBLE
drawStyleMap_so[SoDrawStyle.INVISIBLE]	= 'none'
drawStyleMap_so[SoDrawStyle.LINES]	= 'none'
drawStyleMap_so[SoDrawStyle.FILLED]	= 'solid_outline'
drawStyleMap_so[SoDrawStyle.POINTS]	= 'none'

drawStyleMap_s				= {}
drawStyleMap_s['none']			= SoDrawStyle.INVISIBLE
drawStyleMap_s['outline']		= SoDrawStyle.INVISIBLE
drawStyleMap_s['wireframe']		= SoDrawStyle.LINES
drawStyleMap_s['mesh']			= SoDrawStyle.FILLED
drawStyleMap_s['solid']			= SoDrawStyle.FILLED
drawStyleMap_s['points']		= SoDrawStyle.POINTS
drawStyleMap_s['point']			= SoDrawStyle.POINTS
drawStyleMap_s['line']			= SoDrawStyle.LINES
drawStyleMap_s['solid_outline']		= SoDrawStyle.FILLED
drawStyleMap_s['solid_wire']		= SoDrawStyle.FILLED
drawStyleMap_s['contour']		= SoDrawStyle.INVISIBLE
drawStyleMap_s['velocity_vector']	= SoDrawStyle.INVISIBLE
drawStyleMap_s['line_point']		= SoDrawStyle.POINTS
drawStyleMap_s[SoDrawStyle.INVISIBLE]	= 'none'
drawStyleMap_s[SoDrawStyle.LINES]	= 'none'
drawStyleMap_s[SoDrawStyle.FILLED]	= 'solid'
drawStyleMap_s[SoDrawStyle.POINTS]	= 'points'

#------ Misc. 04/09 : J5 : SY
drawStyleMap_s1				= {}
drawStyleMap_s1['none']			= SoDrawStyle.INVISIBLE
drawStyleMap_s1['outline']		= SoDrawStyle.INVISIBLE
drawStyleMap_s1['wireframe']		= SoDrawStyle.INVISIBLE
drawStyleMap_s1['mesh']			= SoDrawStyle.INVISIBLE
drawStyleMap_s1['solid']		= SoDrawStyle.INVISIBLE
drawStyleMap_s1['points']		= SoDrawStyle.INVISIBLE
drawStyleMap_s1['point']		= SoDrawStyle.INVISIBLE
drawStyleMap_s1['line']			= SoDrawStyle.INVISIBLE
drawStyleMap_s1['solid_outline']	= SoDrawStyle.INVISIBLE
drawStyleMap_s1['solid_wire']		= SoDrawStyle.INVISIBLE
drawStyleMap_s1['contour']		= SoDrawStyle.INVISIBLE
drawStyleMap_s1['velocity_vector']	= SoDrawStyle.INVISIBLE
drawStyleMap_s1['line_point']		= SoDrawStyle.LINES
drawStyleMap_s1[SoDrawStyle.INVISIBLE]	= 'none'
drawStyleMap_s1[SoDrawStyle.LINES]	= 'none'
drawStyleMap_s1[SoDrawStyle.FILLED]	= 'solid'
drawStyleMap_s1[SoDrawStyle.POINTS]	= 'points'
#-----

drawStyleMap_w				= {}
drawStyleMap_w['none']			= SoDrawStyle.INVISIBLE
drawStyleMap_w['outline']		= SoDrawStyle.INVISIBLE
drawStyleMap_w['wireframe']		= SoDrawStyle.INVISIBLE
drawStyleMap_w['mesh']			= SoDrawStyle.LINES
drawStyleMap_w['solid']			= SoDrawStyle.INVISIBLE
drawStyleMap_w['points']		= SoDrawStyle.INVISIBLE
drawStyleMap_w['point']			= SoDrawStyle.INVISIBLE
drawStyleMap_w['line']			= SoDrawStyle.INVISIBLE
drawStyleMap_w['solid_outline']		= SoDrawStyle.INVISIBLE
drawStyleMap_w['solid_wire']		= SoDrawStyle.LINES
drawStyleMap_w['contour']		= SoDrawStyle.INVISIBLE
drawStyleMap_w['velocity_vector']	= SoDrawStyle.INVISIBLE
drawStyleMap_w['line_point']		= SoDrawStyle.LINES
drawStyleMap_w[SoDrawStyle.INVISIBLE]	= 'none'
drawStyleMap_w[SoDrawStyle.LINES]	= 'wireframe'
drawStyleMap_w[SoDrawStyle.FILLED]	= 'none'
drawStyleMap_w[SoDrawStyle.POINTS]	= 'none'

drawStyleMap_c				= {}
drawStyleMap_c['none']			= SoDrawStyle.INVISIBLE
drawStyleMap_c['outline']		= SoDrawStyle.INVISIBLE
drawStyleMap_c['wireframe']		= SoDrawStyle.INVISIBLE
drawStyleMap_c['mesh']			= SoDrawStyle.INVISIBLE
drawStyleMap_c['solid']			= SoDrawStyle.INVISIBLE
drawStyleMap_c['points']		= SoDrawStyle.INVISIBLE
drawStyleMap_c['point']			= SoDrawStyle.INVISIBLE
drawStyleMap_c['line']			= SoDrawStyle.INVISIBLE
drawStyleMap_c['solid_outline']		= SoDrawStyle.INVISIBLE
drawStyleMap_c['solid_wire']		= SoDrawStyle.INVISIBLE
drawStyleMap_c['contour']		= SoDrawStyle.FILLED
drawStyleMap_c['velocity_vector']	= SoDrawStyle.INVISIBLE
drawStyleMap_c['line_point']		= SoDrawStyle.INVISIBLE
drawStyleMap_c[SoDrawStyle.INVISIBLE]	= 'none'
drawStyleMap_c[SoDrawStyle.LINES]	= 'none'
drawStyleMap_c[SoDrawStyle.FILLED]	= 'contour'
drawStyleMap_c[SoDrawStyle.POINTS]	= 'none'

drawStyleMap_v				= {}
drawStyleMap_v['none']			= SoDrawStyle.INVISIBLE
drawStyleMap_v['outline']		= SoDrawStyle.INVISIBLE
drawStyleMap_v['wireframe']		= SoDrawStyle.INVISIBLE
drawStyleMap_v['mesh']			= SoDrawStyle.INVISIBLE
drawStyleMap_v['solid']			= SoDrawStyle.INVISIBLE
drawStyleMap_v['points']		= SoDrawStyle.INVISIBLE
drawStyleMap_v['point']			= SoDrawStyle.INVISIBLE
drawStyleMap_v['line']			= SoDrawStyle.INVISIBLE
drawStyleMap_v['solid_outline']		= SoDrawStyle.INVISIBLE
drawStyleMap_v['solid_wire']		= SoDrawStyle.INVISIBLE
drawStyleMap_v['contour']		= SoDrawStyle.INVISIBLE
drawStyleMap_v['velocity_vector']	= SoDrawStyle.FILLED
drawStyleMap_v['line_point']		= SoDrawStyle.INVISIBLE
drawStyleMap_v[SoDrawStyle.INVISIBLE]	= 'none'
drawStyleMap_v[SoDrawStyle.LINES]	= 'none'
drawStyleMap_v[SoDrawStyle.FILLED]	= 'velocity_vector'
drawStyleMap_v[SoDrawStyle.POINTS]	= 'none'

# o, s, w styles
drawStyleInvMap				= {}
__inv					= SoDrawStyle.INVISIBLE
__lin					= SoDrawStyle.LINES
__fil					= SoDrawStyle.FILLED
__pnt					= SoDrawStyle.POINTS
drawStyleInvMap[__inv, __inv, __inv]	= 'none'
drawStyleInvMap[__fil, __inv, __inv]	= 'outline'
drawStyleInvMap[__inv, __lin, __inv]	= 'wireframe'
drawStyleInvMap[__inv, __fil, __lin]	= 'mesh'
drawStyleInvMap[__inv, __pnt, __inv]	= 'point'
drawStyleInvMap[__inv, __fil, __inv]	= 'solid'
drawStyleInvMap[__inv, __fil, __lin]	= 'solid_wire'
drawStyleInvMap[__inv, __inv, __fil]	= 'contour'
drawStyleInvMap[__inv, __inv, __fil]	= 'velocity_vector'
drawStyleInvMap[__fil, __fil, __inv]	= 'solid_outline'

END_OF_INDEXED_SET = -1

SHP_VOLUME		= 3
SHP_SURFACE		= 2
SHP_EDGE		= 1
SHP_POINT		= 0

VIS_ELM_UNKNOWN		= 0
VIS_ELM_TET		= 1
VIS_ELM_PYRAMID		= 2
VIS_ELM_WEDGE		= 3
VIS_ELM_BRICK		= 4
VIS_ELM_TET10		= 5
VIS_SRF_TRI		= 6
VIS_SRF_QUAD		= 7
VIS_LINE		= 8
VIS_PNT			= 9

shapeTypeMap		        = {}
shapeTypeMap[VIS_ELM_UNKNOWN]	= -1
shapeTypeMap[VIS_ELM_TET]	= SHP_VOLUME
shapeTypeMap[VIS_ELM_PYRAMID]	= SHP_VOLUME
shapeTypeMap[VIS_ELM_WEDGE]	= SHP_VOLUME
shapeTypeMap[VIS_ELM_BRICK]	= SHP_VOLUME
shapeTypeMap[VIS_ELM_TET10]	= SHP_VOLUME
shapeTypeMap[VIS_SRF_TRI]	= SHP_SURFACE
shapeTypeMap[VIS_SRF_QUAD]	= SHP_SURFACE
shapeTypeMap[VIS_LINE]		= SHP_EDGE
shapeTypeMap[VIS_PNT]		= SHP_POINT

cnnTplMap				= {}

cnnTplMap['unknown']            	= VIS_ELM_UNKNOWN

cnnTplMap['point']          	  	= VIS_PNT
cnnTplMap['vertex']            		= VIS_PNT
cnnTplMap['1d']            		= VIS_PNT
cnnTplMap['1D']            		= VIS_PNT
cnnTplMap[0]            		= VIS_PNT

cnnTplMap['line']          	  	= VIS_LINE
cnnTplMap['edge']            		= VIS_LINE
cnnTplMap['2d']            		= VIS_LINE
cnnTplMap['2D']            		= VIS_LINE
cnnTplMap[1]            		= VIS_LINE

cnnTplMap['PRM_TPL_3TRI']       	= VIS_SRF_TRI
cnnTplMap['three_node_triangle']	= VIS_SRF_TRI
cnnTplMap['tri3']			= VIS_SRF_TRI
cnnTplMap['PRM_TPL_4TET_BND']		= VIS_SRF_TRI
cnnTplMap['PRM_TPL_5PYRAMID_BND_P']	= VIS_SRF_TRI
cnnTplMap['PRM_TPL_10TET_BND']		= VIS_SRF_TRI

cnnTplMap['PRM_TPL_4QUAD']      	= VIS_SRF_QUAD
cnnTplMap['four_node_quad']		= VIS_SRF_QUAD
cnnTplMap['quad4']			= VIS_SRF_QUAD
cnnTplMap['PRM_TPL_5PYRAMID_BND_Q']	= VIS_SRF_QUAD
cnnTplMap['PRM_TPL_6WEDGE_BND_Q']	= VIS_SRF_QUAD
cnnTplMap['PRM_TPL_8BRICK_BND']		= VIS_SRF_QUAD

cnnTplMap['PRM_TPL_4TET']		= VIS_ELM_TET
cnnTplMap['four_node_tet']      	= VIS_ELM_TET
cnnTplMap['tet4']			= VIS_ELM_TET

cnnTplMap['PRM_TPL_5PYRAMID']		= VIS_ELM_PYRAMID
cnnTplMap['five_node_pyramid']  	= VIS_ELM_PYRAMID
cnnTplMap['pyramid5']			= VIS_ELM_PYRAMID

cnnTplMap['PRM_TPL_6WEDGE']		= VIS_ELM_WEDGE
cnnTplMap['six_node_wedge']     	= VIS_ELM_WEDGE
cnnTplMap['wedge6']			= VIS_ELM_WEDGE

cnnTplMap['PRM_TPL_8BRICK']		= VIS_ELM_BRICK
cnnTplMap['eight_node_brick']     	= VIS_ELM_BRICK
cnnTplMap['hex8']			= VIS_ELM_BRICK

cnnTplMap['PRM_TPL_10TET']       	= VIS_ELM_TET10
cnnTplMap['ten_node_tet']       	= VIS_ELM_TET10
cnnTplMap['tet10']		       	= VIS_ELM_TET10

#===========================================================================
#
# Errors
#
#===========================================================================

acuSgActorError   = "ERROR from acuSgActor module"

#===========================================================================
#
# "AcuSgActor": Scene graph actor
#
#===========================================================================

class AcuSgActor( SoSeparator ):
    '''
	class AcuSgActor contains an SoSeparator() that holds a
	- SoFaceSet or SoLineSet or SoSomePointSet to store the shape
	- SoDrawStyle  for display types, wireframe, points, solid etc.
	- SoMaterial for specifying color attributes
	There will be on AcuSgActor object for each of the element sets,
	surface sets, nbc sets and pbc sets. For CAD there will be one
	for each of the REGIONS, FACES and EDGES in the model
    '''

    def __init__( self, parent, crd , cnn, topology, name, dataId,vProp = None,
    		 	disp = 'none', color = None, vis = False,
                        trans = False, transVal = 0.5, camFlag  = True,
                        outlineLnClr    = "Auto", wirefrmLnClr  = "Auto"
                ):
	'''
	    AcuSgActor is used to create SoIndexedFaceSet and SoIndexLineSet
	    objects for rendering volumes, surfaces, lines and points.

	    Arguments:
	        crd		- numarray of coords.(from acupu.readArray(..))
		cnn		- numarray of connectivity data
		topology	- "point","line","three_node_triangle" etc
		name		- name of the actor, element_set name etc.
		dataId		- unique id of the actor
		vProp		- SovertexProperty object [ default None ]
		disp		- display type [ default "solid" ]
		color		- [ red, green , blue ], default None
		vis		- visibility [ default False ]
		                  If display != none, vis is automatically
				  set to True.

		trans           - transparency [ default False ]
		transVal        - transparency value [0.0, 0.1, ... , 1.0]
	        outlineLinClr   - outline line color which are
                                  "Auto", "Black", "White" 

	        wirefrmLinClr   - wireframe line color which are
                                  "Auto", "Black", "White" 
		
	'''

	if crd == None or cnn == None or name == None:
	    raise acuSgActorError, "crd, cnn and name cannot be None"

	if topology not in cnnTplMap:
	    raise acuSgActorError, \
		    "Unknown topology <%s> " % topology

	SoSeparator.__init__(		self				)

	self.parent	        = parent
	self.vertProp	        = vProp
	self.crd	        = crd
	self.cnn	        = cnn
	self.name	        = name
	self.dataId	        = dataId
	self.area	        = None
	self.center	        = None
	self.normDir	        = None
	self.boundBox	        = None
        self.meshSet	        = None
        self.outlineSet	        = None
	self.camFlag	        = camFlag
	self.outlineLnClr       = outlineLnClr
	self.wirefrmLnClr       = wirefrmLnClr

	#----- Color Contour and Velocity Vector

	self.vertProp_c     = None     
        self.meshSet_c      = None
	self.updateContour  = True
        self.updateVel      = True
        self.firstVel       = True
        self.velDisplayed   = False
        self.colorIdx       = None

	self.nNodes         = self.crd.size()	
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

	#------- Create the appropriate meshSet for the cnn data

	self.cnnType		= cnnTplMap[ topology ]

	self.edgeAngle		= 80 # default value
	self.buildActorsFlag	= False
	self.extOutlineFlag	= False

	self.r,self.g,self.b	= 1.0, 1.0, 1.0
	self.hr,self.hg,self.hb	= 1.0, 1.0, 1.0
	self.hLightFlag		= False

        #----- Create proper iv name
	
	ivname = name.capitalize( )
	if ivname[0] != "_" and ivname[0] not in string.ascii_letters \
           or not ivname[0].isalpha():
            ivname = "_" + ivname

        for i in range( len( ivname ) ):
            s = ivname[i]
            if ord( s ) <= 0x20 or ord( s ) >= 0x7f \
               or s in ['"', "'", '+', '.', '\\', '/', '{', '}', ' ']:
                ivname = ivname[ : i] + "_" + ivname[i + 1 : ]       

	self.setName(                   ivname                          )
	self.name	= ivname
		
	self.pickFlag	= TRUE

        self.actor_o	= SoSeparator(					)
        self.actor_so	= SoSeparator(					)
        self.actor_s	= SoSeparator(					)
        #----- Misc. 04/09 : J5 : SY
        self.actor_s1	= SoSeparator(					)
        #-----
        self.actor_w	= SoSeparator(					)
        self.actor_c	= SoSeparator(					)
        self.actor_v	= SoSeparator(					)

	self.shapeHints	= SoShapeHints(					)
	self.shapeHints.vertexOrdering.setValue( SoShapeHints.CLOCKWISE)
	self.shapeHints.shapeType.setValue( SoShapeHints.UNKNOWN_SHAPE_TYPE)

	self.actor_o.addChild(		self.shapeHints			)
	self.actor_so.addChild(		self.shapeHints			)
	self.actor_s.addChild(		self.shapeHints			)
	#----- Misc. 04/09 : J5 : SY
	self.actor_s1.addChild(		self.shapeHints			)
	#-----
	self.actor_w.addChild(		self.shapeHints			)
        self.actor_c.addChild(		self.shapeHints			)
        self.actor_v.addChild(		self.shapeHints			)
        
	self.material	= SoMaterial(					)
	self.material_w	= SoMaterial(					)
	self.material_so= SoMaterial(					)	
	
	self.drawStyle_o= SoDrawStyle(					)
	self.drawStyle_so=SoDrawStyle(					)
	#----- Misc. 04/09 : J5 : SY
	self.drawStyle_s1= SoDrawStyle(					)
	#-----
	self.drawStyle_s= SoDrawStyle(					)
	self.drawStyle_w= SoDrawStyle(					)
	self.drawStyle_c= SoDrawStyle(					)
	self.drawStyle_v= SoDrawStyle(					)

        # related to velocity vector
	self.velLineDrawStyle = SoDrawStyle(				)
	self.velArrowDrawStyle = SoDrawStyle(				)

	self.actor_o.addChild(		self.material			)
	self.actor_s.addChild(		self.material			)
	#----- Misc. 04/09 : J5 : SY
	self.actor_s1.addChild(		self.material			)
	#-----
	self.actor_w.addChild(		self.material_w			)
	self.actor_so.addChild(		self.material_so		)

	self.actor_o.addChild(		self.drawStyle_o		)
	self.actor_so.addChild(		self.drawStyle_so		)
	self.actor_s.addChild(		self.drawStyle_s		)
	#----- Misc. 04/09 : J5 : SY
	self.actor_s1.addChild(		self.drawStyle_s1		)
	#-----
	self.actor_w.addChild(		self.drawStyle_w		)
	self.actor_c.addChild(		self.drawStyle_c		)
	self.actor_v.addChild(		self.drawStyle_v		)

	self.addChild(			self.actor_w			)
	self.poly	= SoPolygonOffset(				)
	self.addChild(			self.poly			)

	self.addChild(			self.actor_s			)
	#----- Misc. 04/09 : J5 : SY
	self.addChild(			self.actor_s1			)
	#-----
	self.addChild(			self.actor_o			)
	self.addChild(			self.actor_so			)
	self.addChild(			self.actor_c			)
	self.addChild(			self.actor_v			)
	
	self.vis		= vis
	self.style		= disp
	self.hLightStyle	= {}#"solid"
	self.trans              = trans
        self.transValue         = transVal

	if color != None:
	    self.r, self.g,self.b	= color[0], color[1], color[2]
	    self.color( 		self.r, self.g, self.b 		)

	self.linWidth	= self.drawStyle_s.lineWidth.getValue(		)
	self.pntSize	= self.drawStyle_s.pointSize.getValue(		)

	if self.vis:
	    self.create(						)
	    self.display(		self.style			)

	if self.trans:
            self.transparencyOn(                                        )       
        
        self.matrixTransform = SoTransform()
        self.insertChild(self.matrixTransform, 0)

        #----- Misc 11/09 B3-B6
	self.clipShapeActorList = None
        self.clipShapeActorSep  = None
        self.clipTranMat        = None
        self.clipOpaqMat        = None
        self.clipNestedMats     = None
 
#---------------------------------------------------------------------------
# create: builds the shape objects based on the crd, cnn data
#---------------------------------------------------------------------------

    def create( self ):
        '''
	    Function to build the actors from the mesh data. The
	    actors are not built at initialization of actor object,
	    rather at a later time.

	    Arguments:
	        extractEdges	- For outline display [default = True ]

	    Output:
	        None
        '''

	if self.buildActorsFlag:
	    return

	if shapeTypeMap[ self.cnnType ] == SHP_VOLUME:
	    nElms,nItems	= self.cnn.shape

	    if nElms == 0 or nItems == 0:
	        raise acuSgActorError,"zero elements in <%s> cnn"% name
	
	    #--- Now let us extract the surfaces of the volume

	    if self.cnnType == VIS_ELM_UNKNOWN or \
	    	self.cnnType == VIS_PNT or \
		self.cnnType == VIS_LINE or \
		self.cnnType == VIS_SRF_TRI or \
		self.cnnType == VIS_SRF_QUAD:
	        raise acuSgActorError, \
			"unknown element topology %s" % topology
	
	    self.tris	= numarray.arange(	    1, type = 'i'	)
	    self.nTris	= 0
	    self.quads	= numarray.arange(	    1, type = 'i'	)
	    self.nQuads	= 0

	    (self.tris, self.quads ) = acupu.getVolSrf( self.cnn )
	    if self.tris != None:
	        self.nTris	= len( self.tris )
	    if self.quads != None:
	        self.nQuads	= len( self.quads )

	    if self.nTris < 0 and self.nQuads < 0 :
	        raise acuSgActorError, \
			"Error extracting the volume surfaces"
	
	    if self.nTris > 0 or self.nQuads > 0:
	        cnnCopy	= numarray.zeros( self.nTris * 4 + self.nQuads * 5,
                                          type = 'i'                    )

		if self.nTris > 0:
		    self.tris.resize(	( self.nTris, 3 ) 		)
		    cnnCopyTris	= numarray.zeros(	(self.nTris, 4 ),
                                                        type = 'i'      )
		    for j in range( 3 ):
		        cnnCopyTris[:,j]	= self.tris[:,j]
		    cnnCopyTris[:,3]	= END_OF_INDEXED_SET
		    cnnCopyTris.ravel(					)
		    cnnCopy	= cnnCopyTris


		if self.nQuads > 0:
		    self.quads.resize(	( self.nQuads, 4 )		)
		    cnnCopyQuads = numarray.zeros(( self.nQuads, 5 ),
                                                  type = 'i'            )

		    for j in range( 4 ):
		        cnnCopyQuads[:,j]	= self.quads[:,j]
		    cnnCopyQuads[:,4]	= END_OF_INDEXED_SET
		    cnnCopyQuads.ravel(					)
		    cnnCopy	= cnnCopyQuads

		if self.nQuads > 0 and self.nTris > 0 :
		    cnnCopy	= numarray.concatenate( \
		    		( cnnCopyQuads, cnnCopyTris ) , 0	)

		self.meshSet	= SoIndexedFaceSet(			)
		self.meshSet_c	= SoIndexedFaceSet(			)
		
		#self.meshSet.setName(		self.name		)
		self.meshSet.coordIndex.setValues(	0, cnnCopy	)
		self.meshSet_c.coordIndex.setValues(	0, cnnCopy	)

		self.outlineSet	= SoIndexedLineSet(			)
		#self.outlineSet.setName(	self.name		)
		self.actor_o.addChild(		self.outlineSet		)
		self.actor_so.addChild(		self.outlineSet		)
		self.buildActorsFlag	= True


	if shapeTypeMap[ self.cnnType ] == SHP_SURFACE:
            
	    nElms,nItems	= self.cnn.shape

	    if nElms == 0 or nItems == 0:
	        raise acuSgActorError,"zero elements in <%s> cnn"% name

	    cnnCopy	= numarray.zeros( ( nElms, ( nItems + 1 ) ),
                                          type = 'i'                    )
	    for j in range( nItems ):
		cnnCopy[:,j]	= self.cnn[:,j]
	    cnnCopy[:,nItems]	= -1
	    cnnCopy.ravel(						)

	    self.meshSet	= SoIndexedFaceSet(			)
	    #self.meshSet.setName(		self.name		)
	    self.meshSet.coordIndex.setValues(	0, cnnCopy	)

	    self.meshSet_c	= SoIndexedFaceSet(			)
            self.meshSet_c.coordIndex.setValues(	0, cnnCopy	)
	    

	    area, center, normDir, dir1, dir2, bndBox = \
		    acupu.srfLayOut( self.crd, self.cnn )
	    self.area		= area
	    self.center		= center
	    self.normDir	= normDir
	    self.boundBox	= bndBox

	    self.outlineSet	= SoIndexedLineSet(			)

	    self.actor_o.addChild(		self.outlineSet		)
	    self.actor_so.addChild(		self.outlineSet		)
	    self.buildActorsFlag	= True

	if shapeTypeMap[ self.cnnType ] == SHP_EDGE:
	    nElms,nItems	= self.cnn.shape

	    if nElms == 0 or nItems == 0:
	        raise acuSgActorError,"zero elements in <%s> cnn"% self.name

	    cnnCopy	= numarray.zeros( ( nElms, ( nItems + 1 ) ),
                                          type = 'i'                    )
	    for j in range( nItems ):
		cnnCopy[:,j]	= self.cnn[:,j]
	    cnnCopy[:,nItems]	= -1
	    cnnCopy.ravel(						)

	    self.meshSet	= SoIndexedLineSet(			)
	    self.meshSet.coordIndex.setValues(	0, cnnCopy	)

	    self.area		= None
	    self.center		= None
	    self.normDir	= None
	    self.boundBox	= None
	    self.buildActorsFlag	= True

	if shapeTypeMap[ self.cnnType ] == SHP_POINT:
	    nNodes		= len(self.cnn)

	    if nNodes == 0:
	        raise acuSgActorError,"zero nodes in <%s> cnn"% self.name

	    if float(nNodes)/2 == nNodes/2:
	        nElms		= nNodes / 2
		nItems		= 2
	        self.cnn.resize(	( nElms,2 )			)
	    else:
	        nNodes		= nNodes + 1
	        nElms		= nNodes / 2
		nItems		= 2
	        self.cnn.resize(	( nNodes, )			)
	        self.cnn[nNodes-1]	= self.cnn[nNodes-3]
		self.cnn.resize(	( nElms, 2 )			)

	    cnnCopy	= numarray.zeros( ( nElms, ( nItems + 1 ) ),
                                          type = 'i'                    )
	    for j in range( nItems ):
		cnnCopy[:,j]	= self.cnn[:,j]
	    cnnCopy[:,nItems]	= -1
	    cnnCopy.ravel(						)

	    self.meshSet	= SoIndexedLineSet(			)
	    self.meshSet.coordIndex.setValues(	0, cnnCopy	)

	    self.area		= None
	    self.center		= None
	    self.normDir	= None
	    self.boundBox	= None
	    self.buildActorsFlag	= True


	if shapeTypeMap[ self.cnnType ] == SHP_SURFACE or \
	   shapeTypeMap[ self.cnnType ] == SHP_VOLUME  or \
	   shapeTypeMap[ self.cnnType ] == SHP_EDGE or \
	   shapeTypeMap[ self.cnnType ] == SHP_POINT:

	    if self.meshSet == None:
		raise acuSgActorError, "meshSet is none, error in crd"

	    if self.vertProp != None:
		if isinstance( self.vertProp, SoVertexProperty ):
		    self.meshSet.vertexProperty.setValue(  self.vertProp )
                    #----- Misc 06/10 B1
		    if self.outlineSet != None:
                        self.outlineSet.vertexProperty.setValue( self.vertProp )
		else:
		    raise acuSgActorError, \
		    	"vProp is not an SoVertexProperty"
	    else:
		if self.crd != None:
		    if isinstance( self.crd, numarray.numarraycore.NumArray ):
			self.vertProp	= SoVertexProperty(		)
			self.vertProp.vertex.setValues( 0, self.crd 	)
			self.meshSet.vertexProperty.setValue( self.vertProp )
			#----- Misc 06/10 B1
			if self.outlineSet != None:
                            self.outlineSet.vertexProperty.setValue( self.vertProp )
		    else:
			raise acuSgActorError,"Incorrect type of crd "
		else:
		    raise acuSgActorError, "crd is None "

	
	self.actor_s.addChild(		self.meshSet			)
	#----- Misc. 04/09 : J5 : SY
	self.actor_s1.addChild(		self.meshSet			)
	#-----

        #----- Color contour
	if shapeTypeMap[ self.cnnType ] == SHP_SURFACE or \
	   shapeTypeMap[ self.cnnType ] == SHP_VOLUME:
	
            self.vertProp_c = SoVertexProperty(		                )
            self.vertProp_c.vertex.setValues(   0,      self.crd 	)
            self.vertProp_c.materialBinding.setValue(
                                    SoMaterialBinding.PER_VERTEX_INDEXED)
            self.meshSet_c.vertexProperty.setValue(     self.vertProp_c )
            self.actor_c.addChild(		        self.meshSet_c  )

	    self.actor_w.addChild(		self.meshSet		)

##        if self.camFlag:
##	    #self.parent.viewer.viewAll(				)
##	    cam = self.parent.viewer.getCamera(				)
##	    cam.viewAll( self.parent.dynObjects, \
##	    		self.parent.viewer.getViewportRegion()		)
##	    #self.parent.acuTform.centerOfRotation(self.parent.dynObjects)
##	    self.parent.viewer.saveHomePosition(			)

#---------------------------------------------------------------------------
# edgeAngle: set/get the edge angle used for extracting mesh outlines
#---------------------------------------------------------------------------

    def edgeAngle( self, angle = None ):
        '''
	    Function to set the angle for extracting outline edges from
	    a surface mesh

	    Arguments:
	        angle		- value of the angle used to ext. edges

	    Output: ( return the angle value if angle == None )
	        angle		- value of the angle used to ext. edges
	
        '''
	retVal	= self.edgeAngle

	if angle != None:
	    self.edgeAngle	= angle

	return retVal

#---------------------------------------------------------------------------
# extractEdges: extracts the edges of the surface mesh for outline display
#---------------------------------------------------------------------------

    def extractEdges( self ):
        '''
	    Function to set the display type of the actor

	    Arguments:
	        style		- "outline", "solid", "wireframe", "none"

	    Output: ( only if style input is equal to None )
	        style		- "outline", "solid", "wireframe", "none"

        '''

	if self.extOutlineFlag:
	    return


	if shapeTypeMap[ self.cnnType ] == SHP_VOLUME:

	    #---- Extract the edges of the volume surfaces

	    edgeCnn	= numarray.arange( 		1, type = 'i'	)
	    triEdges	= numarray.arange(              1, type = 'i'   )
	    quadEdges 	= numarray.arange(              1, type = 'i'   )
	    nTriEdges	= 0
	    nQuadEdges	= 0

	    if self.nTris != 0 and self.tris != None:
		triEdges	=  acupu.getSrfEdge( self.crd, \
						self.edgeAngle, self.tris )
		if triEdges != None:
		    nTriEdges	= len( triEdges )
		if nTriEdges > 0:
		    triEdges.resize( ( nTriEdges, 2 ) 		)
		    triEdgesCopy	= numarray.zeros(( nTriEdges,3),
                                                         type = 'i'     )
		    for j in range( 2 ):
			triEdgesCopy[:,j]	= triEdges[:,j]
		    triEdgesCopy[:,2] = END_OF_INDEXED_SET
		    triEdgesCopy.ravel(				)
		    edgeCnn	= triEdgesCopy

	    if self.nQuads != 0 and self.quads != None:
		quadEdges	= acupu.getSrfEdge( self.crd, \
						self.edgeAngle, self.quads )
		if quadEdges != None:
		    nQuadEdges	= len( quadEdges )
		if nQuadEdges > 0:
		    quadEdges.resize(	(nQuadEdges,2)		)
		    quadEdgesCopy	= numarray.zeros((nQuadEdges,3),
                                                         type = 'i'     )
		    for j in range( 2 ):
			quadEdgesCopy[:,j]	= quadEdges[:,j]
		    quadEdgesCopy[:,2] = END_OF_INDEXED_SET
		    quadEdgesCopy.ravel(				)
		    edgeCnn	= quadEdgesCopy

	    if nQuadEdges > 0 and nTriEdges > 0 :
		edgeCnn	= numarray.concatenate( \
				( quadEdgesCopy, triEdgesCopy ) , 0	)

	    self.outlineSet.coordIndex.setValues(	0, edgeCnn	)
	    self.extOutlineFlag	= True


	elif shapeTypeMap[ self.cnnType ] == SHP_SURFACE:
	    # - Now let us extract the surface outline here
	    nEdges	= 0
	    edges 	= numarray.arange(      1, type = 'i'           )
	    if self.cnnType == VIS_SRF_TRI or self.cnnType == VIS_SRF_QUAD:
		edges  = acupu.getSrfEdge( self.crd, \
				self.edgeAngle,self.cnn 		)
		if edges != None:
		    nEdges = len( edges )
		if nEdges > 0:
		    edges.resize(	( nEdges, 2 )			)
		edgeCnn	= numarray.zeros(	(nEdges,3), type = 'i'	)
		for j in range( 2 ):
		    edgeCnn[:,j]	= edges[:,j]
		edgeCnn[:,2] = END_OF_INDEXED_SET
		edgeCnn.ravel(					)
		self.outlineSet.coordIndex.setValues( 0, edgeCnn	)
		self.extOutlineFlag	= True

	else:
	    raise acuSgActorError, \
	    		"Cannot extract edges for edges and lines"

	if self.vertProp != None:
	    if isinstance( self.vertProp, SoVertexProperty ):
		if shapeTypeMap[ self.cnnType ] == SHP_SURFACE or \
		   shapeTypeMap[ self.cnnType ] == SHP_VOLUME:
		    self.outlineSet.vertexProperty.setValue(self.vertProp)
	    else:
		raise acuSgActorError, \
		    "vertProp is not an SoVertexProperty"

#---------------------------------------------------------------------------
# sphericalHarmonics
#---------------------------------------------------------------------------
    def sphericalHarmonics(self, nu, nv, colorMap):

        # Coin generates a warning when nu and/or nv are even.
        assert(nu % 2 == 1)
        assert(nv % 2 == 1)

        i = arange(nu*nv)
        u = i % nu
        u %= nu
        u = 3.14*u/(nu-1)   # phi
        v = i / nu
        v %= nv
        v = 2*3.14*v/(nu-1) # theta   
        m = (4, 3, 2, 3, 6, 2, 6, 4)

        r = sin(m[0]*u)**m[1]+cos(m[2]*u)**m[3]+sin(m[4]*v)**m[5]+cos(m[6]*v)**m[7]
        xyzs = zeros((nu*nv, 3), Float)
        xyzs[:, 0] = r*sin(u)*cos(v)
        xyzs[:, 1] = r*sin(u)*sin(v)
        xyzs[:, 2] = r*cos(u)

        colors = colorMap.colors(v)

        return xyzs, colors
	
#---------------------------------------------------------------------------
# display: set/get the display style
#---------------------------------------------------------------------------

    def display( self, style = None ):
        
        """
	    Function to set the display type of the actor

	    Arguments:
	        style	- "outline", "solid", "wireframe", "contour", "velocity_vector", "none"

	    Output: 
	        The old display style
        """
        
	retVal	= self.style

        if style != None:            
	    if style not in drawStyleMap_o:
	        raise acuSgActorError, " undefined display type: %s " % style
                
	    if not self.buildActorsFlag:
		self.create(					        )

	    if ( style == "outline" or style == "solid_outline" ) \
               and not self.extOutlineFlag:
		self.extractEdges(					)

	    if style == "contour":
                self.recreateContour(                                   )

            if style == "velocity_vector":
                self.recreateVel(                                       )

            self.drawStyle_o.style.setValue(    drawStyleMap_o[style]   )
            self.drawStyle_s.style.setValue(    drawStyleMap_s[style]   )
            self.drawStyle_w.style.setValue(    drawStyleMap_w[style]   )
            self.drawStyle_s1.style.setValue(   drawStyleMap_s1[style]  )
            self.drawStyle_so.style.setValue(   drawStyleMap_so[style]  )
            self.drawStyle_c.style.setValue(    drawStyleMap_c[style]   )
            self.drawStyle_v.style.setValue(    drawStyleMap_v[style]   )            
                    
	    self.style	= style
	    
	    if self.hLightFlag:
                self.styleCopy	= style
	    
	return retVal

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
        
        if scalar != None:
            if type( scalar ) != numarray.numarraycore.NumArray:
                scalar = numarray.array( scalar )
            
            if scalar.getrank( ) != 1 and scalar.shape[1] != 1:
                raise acuSgActorError, "Scalar shape must be nNodes * 1."

            self.scalarName = name
            self.scalar     = scalar

            self.tmpSclrMin = scalar.min( )
            self.tmpSclrMax = scalar.max( )

            if sclrMinVal == None:  
                if self.parent.sclrMinVal != None and self.sclrMinVal == None:
                    self.setSclrMinVal( self.parent.sclrMinVal )                              
            else:
                self.setSclrMinVal( sclrMinVal )

            if sclrMaxVal == None:
                if self.parent.sclrMaxVal != None and self.sclrMaxVal == None:
                    self.setSclrMaxVal( self.parent.sclrMaxVal )               
            else:
                self.setSclrMaxVal( sclrMaxVal )

            self.updateContour = True

        elif self.parent.scalar != None:
            self.scalarName = name
            self.scalar     = self.parent.scalar

            self.sclrMinVal = self.parent.sclrMinVal
            self.tmpSclrMin = self.parent.tmpSclrMin
            self.sclrMaxVal = self.parent.sclrMaxVal
            self.tmpSclrMax = self.parent.tmpSclrMax

            self.updateContour = True
            
        else:
            raise acuSgActorError, "No scalar is specified."

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
        self.updateContour = True
   
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
        self.updateContour = True

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
            self.updateContour = True

        elif self.parent.cmap != None:
            self.cmap = self.parent.cmap
            self.updateContour = True

        else:
            self.parent.setCmap( )
            self.cmap = self.parent.cmap
            self.updateContour = True            
        
#---------------------------------------------------------------------------
# recreateContour: recreate the color contour display 
#---------------------------------------------------------------------------

    def recreateContour( self ):

        if self.updateContour == False:
            return
                
        if self.scalar == None:
            self.setScalar(                                             )

        if self.cmap == None:
            self.setCmap(                                               )

        if self.sclrMinVal != None:
            sclrMinVal = self.sclrMinVal
        else:
            sclrMinVal = self.tmpSclrMin

        if self.sclrMaxVal != None:
            sclrMaxVal = self.sclrMaxVal
        else:
            sclrMaxVal = self.tmpSclrMax

        diff = float( sclrMaxVal - sclrMinVal )
        if diff == 0:
            diff = 1.0
 
        fct	    = ( len( self.cmap ) - 1 ) / diff
        sclrIdx	    = fct * ( self.scalar - sclrMinVal ) + 0.5
        sclrIdx	    = numarray.clip( sclrIdx, 0, len( self.cmap ) - 1 )        

        R           = ( numarray.clip( self.cmap[:, 0], 0, 1 ) \
                        * 255 ).astype( 'i' )
        G           = ( numarray.clip( self.cmap[:, 1], 0, 1 ) \
                        * 255 ).astype( 'i' )
        B           = ( numarray.clip( self.cmap[:, 2], 0, 1 ) \
                        * 255 ).astype( 'i' )
        cmapRGBA    = ( R << 24 ) + ( G << 16 ) + ( B << 8 ) + 255       
        colorIdx    = cmapRGBA[sclrIdx]
        colorIdx.ravel( )

        self.vertProp_c.orderedRGBA.setValues( 0, colorIdx          )
        self.updateContour = False

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
                raise acuSgActorError, "Vel shape must be nNodes * 3."

            self.velName    = name
            self.vel        = vel

            if velScale == None:
                if self.parent.velScale == None:
                    self.tmpVelScale = 1.0
                elif self.velScale == None:
                    self.setVelScale( self.parent.velScale )                            
            else:
                self.setVelScale( velScale )

            if self.velScalarType == "magnitude":
                self.setVelScalar( velScalarType = "magnitude" )

            self.updateVel = True

        elif self.parent.vel != None:
            self.velName        = name
            self.vel            = self.parent.vel

            self.velScale       = self.parent.velScale
            self.tmpVelScale    = self.parent.tmpVelScale          

            self.updateVel = True
                
        else:
            raise acuSgActorError, "No vel is specified."

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
                self.updateVel = True
            else:
                raise acuSgActorError, "VelScale cannot be negative."

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
            elif self.parent.vel != None:
                self.velScalar = ( self.parent.vel[:, 0] * self.parent.vel[:, 0] + \
                                   self.parent.vel[:, 1] * self.parent.vel[:, 1] + \
                                   self.parent.vel[:, 2] * self.parent.vel[:, 2] ) \
                                   ** 0.5
            else:
                raise acuSgActorError, "No vel found for setting velScalar."

        elif velScalar != None:
            if type( velScalar ) != numarray.numarraycore.NumArray:
                velScalar = numarray.array( velScalar )
            
            if velScalar.getrank( ) != 1 and velScalar.shape[1] != 1:
                raise acuSgActorError, "velScalar shape must be nNodes * 1."

            self.velScalar  = velScalar

        elif self.parent.velScalar != None:
            self.velScalar  = self.parent.velScalar
            
        else:
            raise acuSgActorError, "No velScalar is specified."

        self.velScalarType = velScalarType

        if velSclrMinVal == None:
            if self.parent.velSclrMinVal == None:
                self.tmpVelSclrMin = self.velScalar.min( )
            elif self.velSclrMinVal == None:
                self.setVelSclrMinVal( self.parent.velSclrMinVal )                            
        else:
            self.setVelSclrMinVal( velSclrMinVal )

        if velSclrMaxVal == None:
            if self.parent.velSclrMaxVal == None:
                self.tmpVelSclrMax = self.velScalar.max( )
            elif self.velSclrMaxVal == None:
                self.setVelSclrMaxVal( self.parent.velSclrMaxVal )               
        else:
            self.setVelSclrMaxVal( velSclrMaxVal )

        self.updateVel = True

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
            self.velSclrMinVal  = velSclrMinVal
            self.updateVel      = True

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
            self.velSclrMaxVal  = velSclrMaxVal
            self.updateVel      = True

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
                self.velWidth   = velWidth
                self.updateVel  = True
            else:
                raise acuSgActorError, "VelWidth cannot be negative."

        elif self.parent.velWidth != None:
            self.velWidth   = self.parent.velWidth
            self.updateVel  = True

        else:
            sel.parent.setVelWidth( )
            self.velWidth   = self.parent.velWidth
            self.updateVel  = True

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
                self.velArrowType   = velArrowType
                self.updateVel      = True
            else:
                raise acuSgActorError, "Invalid velArrowType."

        elif self.parent.velArrowType != None:
            self.velArrowType   = self.parent.velArrowType
            self.updateVel      = True

        else:
            sel.parent.setVelArrowType( )
            self.velArrowType   = self.parent.velArrowType
            self.updateVel      = True

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
                self.velColorType   = velColorType
                self.updateVel      = True
            else:
                raise acuSgActorError, "Invalid velColorType."
        
        elif self.parent.velColorType != None:
            self.velColorType   = self.parent.velColorType
            self.updateVel      = True

        else:
            sel.parent.setVelColorType( )
            self.velColorType   = self.parent.velColorType
            self.updateVel      = True
            
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
            self.velColor   = numarray.array( velColor, shape = ( 1, 3 ) )
            self.updateVel  = True

        elif self.parent.velColor != None:
            self.velColor   = self.parent.velColor
            self.updateVel  = True

        else:
            sel.parent.setVelColor( )
            self.velColor   = self.parent.velColor
            self.updateVel  = True

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
            self.updateVel  = True

        elif self.parent.velCmap != None:
            self.velCmap    = self.parent.velCmap
            self.updateVel  = True

        else:
            sel.parent.setVelCmap( )
            self.velCmap    = self.parent.velCmap
            self.updateVel  = True

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
            camOrt = self.parent.viewer.getCamera( ).orientation.getValue( )
            camOrt.multVec( self.velNormal, self.velNormal )  
            
        if self.velArrowType != '2d':
            return
 
        crd2d = []
        cnn2d = []     
                
        for i in range( len( self.crd1 ) ):
            coord       = SbVec3f( self.crd0[i] )
            arFactor    = 0.3
            ar2d        = ( self.crd1[i] - self.crd0[i] ) * arFactor
            dirc        = SbVec3f( ar2d ).cross( self.velNormal ) * 0.5
            vec         = SbVec3f( self.crd1[i] - ar2d )                     
                   
            t0          = ( vec + dirc ).getValue( )
            t1          = ( vec - dirc ).getValue( )
                                   
            crd2d.append( t0 )
            crd2d.append( self.crd1[i] )
            crd2d.append( t1 )                                    
                    
            startInx    = i * 3
            cnn2d.append( startInx )
            cnn2d.append( startInx + 1 )
            cnn2d.append( startInx + 2 )
            cnn2d.append( SO_END_LINE_INDEX )                

        vel2dProp = SoVertexProperty( ) 
        vel2dProp.vertex.setValues( 0, crd2d )
        vel2dProp.orderedRGBA.setValues( 0, self.colorIdx )
                
        self.arrow2d.vertexProperty.setValue( vel2dProp )
        self.arrow2d.coordIndex.setValues(0, cnn2d )

#---------------------------------------------------------------------------
# recreateVel: recreate the velocity vector display 
#---------------------------------------------------------------------------

    def recreateVel( self ):

        if self.updateVel == False:
            if self.velArrowType == 'none':
                self.velLineDrawStyle.style.setValue( SoDrawStyle.FILLED )
            else:
                self.velArrowDrawStyle.style.setValue( SoDrawStyle.FILLED )
            return

        #----- Check for vel parameters
        
        if self.vel == None:
            self.setVel( )
       
        if self.velScalar == None:
            self.setVelScalar()
            
        if self.velWidth == None:
            self.setVelWidth( )

        if self.velArrowType == None:
            self.setVelArrowType( )
            
        if self.velColorType == None:            
            self.setVelColorType( )           
            
        if self.velColor == None:
            self.setVelColor( )         
            
        if self.velCmap == None:
            self.setVelCmap( )        
              
        self.drawStyle_v.lineWidth.setValue( self.velWidth )

        if self.firstVel:
            
            #----- Create inventor data structures
            
            self.velVertProp    = SoVertexProperty( )              
            self.velVertProp.materialBinding.setValue( SoMaterialBinding.PER_VERTEX_INDEXED )

            self.velLineGroup   = SoSeparator( )         
            self.velLineSet     = SoLineSet ()
            
            self.velLineSet.vertexProperty.setValue( self.velVertProp )
            self.velLineGroup.addChild( self.velLineDrawStyle )
            self.velLineGroup.addChild( self.velLineSet )

            self.velArrowGroup   = SoSeparator( )          
            self.velArrowSet     = SoSeparator( )

            self.velLineGroup.addChild( self.velArrowDrawStyle )
            self.velLineGroup.addChild( self.velArrowSet )
            
            self.actor_v.addChild( self.velLineGroup )
            self.actor_v.addChild( self.velArrowGroup )

            self.firstVel       = False           

        #----- Create velocity vector

        if self.velScale != None:
            velScale = self.velScale
        else:
            velScale = self.tmpVelScale
        
        nodes       = acupu.getCnnNodes( self.cnn )
        crd0        = self.crd[nodes]            
        crd1        = crd0 + velScale * self.vel[nodes]           

        if self.velArrowType == 'none':

            #----- Draw line set
            
            crdVel      = numarray.concatenate( ( crd0, crd1 ), axis = 1 ).copy( )            
            crdVel.setshape( 2 * len( nodes ), 3 )

            if self.velColorType == "constant":           
                cmap = self.velColor          
            else:
                cmap = self.velCmap  

            if self.velSclrMinVal != None:
                velSclrMinVal = self.velSclrMinVal
            else:
                velSclrMinVal = self.tmpVelSclrMin

            if self.velSclrMaxVal != None:
                velSclrMaxVal = self.velSclrMaxVal
            else:
                velSclrMaxVal = self.tmpVelSclrMax

            diff = float( velSclrMaxVal - velSclrMinVal )
            if diff == 0:
                diff = 1.0             
        
            fct	        = ( len( cmap ) - 1 ) / diff
            sclrIdx	= fct * ( self.velScalar - velSclrMinVal ) + 0.5
            sclrIdx	= numarray.clip( sclrIdx, 0, len( cmap ) - 1 )

            R           = ( numarray.clip( cmap[:, 0], 0, 1 ) \
                            * 255 ).astype( 'i' )
            G           = ( numarray.clip( cmap[:, 1], 0, 1 ) \
                            * 255 ).astype( 'i' )
            B           = ( numarray.clip( cmap[:, 2], 0, 1 ) \
                            * 255 ).astype( 'i' )
                   
            cmapRGBA    = ( R << 24 ) + ( G << 16 ) + ( B << 8 ) + 255 
            
            self.colorIdx = cmapRGBA[sclrIdx]
            self.colorIdx.ravel( )
              
            self.velVertProp.vertex.setValues( 0, crdVel )
            self.velVertProp.orderedRGBA.setValues( 0, self.colorIdx )

            self.velArrowDrawStyle.style.setValue( SoDrawStyle.INVISIBLE )
            self.velLineDrawStyle.style.setValue( SoDrawStyle.FILLED )
            
        else:
            
            #----- Draw arrow set
        
            self.velArrowSet.removeAllChildren( )
        
            arrowColor = SoMaterial( )
            color = self.velColor[0]        
            arrowColor.diffuseColor.setValue( color[0], color[1], color[2] )
            self.velArrowSet.addChild( arrowColor )
        
            lineRadius = self.velWidth / 100
    
            for i in range( len( crd0 ) ):   
                start   = crd0[i]
                end     = crd1[i]                       

                #--- Another way for defining angles and rotations 09/03/14
                '''
                r = math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2 + (start[2] - end[2]) ** 2)
                if r != 0:                
                    phi =  -math.asin(abs((start[2] - end[2])) / r)           
                    if math.cos(phi) != 0:
                        theta = -math.acos(abs((start[0] - end[0])) / (r * math.cos(phi)))         
                    else:
                        theta = -math.pi / 2
            
                zRot = SoRotationXYZ()
                zRot.axis.setValue("Z")
                zRot.angle.setValue(theta)

                yRot = SoRotationXYZ()
                yRot.axis.setValue("Y")
                yRot.angle.setValue(phi)
                '''

                #--- Convert cartesian coordinates to spherical coordinates
                
                x = end[0] - start[0]
                y = end[1] - start[1]
                z = end[2] - start[2]

                rXY = math.sqrt( x ** 2 + y ** 2 )
                r = math.sqrt( x ** 2 + y ** 2 + z ** 2 )

                if x != 0:
                    theta = math.atan( y / x )
                else:
                    theta = math.pi / 2
            
                if z != 0:
                    phi = math.atan( rXY / z )         
                else:
                    phi = math.pi / 2
            
                if r != 0:                    

                    #-- Add arrow orientation
                    
                    arrowSet = SoSeparator( )              

                    trans = SoTranslation( )
                    trans.translation.setValue( SbVec3f( start[0], start[1], start[2] ) )

                    yRot = SoRotation( )
                    yRot.rotation.setValue( SbVec3f( 0, 1, 0 ), phi )
        
                    zRot = SoRotation()
                    zRot.rotation.setValue( SbVec3f( 0, 0, 1 ), theta )

                    pos = SoTranslation( )
                    pos.translation.setValue( SbVec3f( 0, r / 2, 0 ) )
        
                    arrowSet.addChild( trans )                
                    arrowSet.addChild( yRot )
                    arrowSet.addChild( zRot )
                    arrowSet.addChild( pos )
                    
                    arrow = SoSeparator( )            

                    #-- Add arrow line
                    
                    arrowLine = SoCylinder( )
                    arrowLine.radius.setValue( lineRadius )
                    arrowLine.height.setValue( r )
            
                    arrow.addChild( arrowLine ) 
        
                    trans = SoTranslation( )
     
                    trans.translation.setValue( SbVec3f( 0, r / 2, 0 ) )

                    arrow.addChild( trans )

                    #-- Add arrow tip
                    
                    if self.velArrowType == "white_tip" and \
                        not ( color[0] == 1 and color[1] == 1 and color[2] == 1 ):
                        tipColor = SoMaterial( )
                        tipColor.diffuseColor.setValue( 1, 1, 1 )
                        arrow.addChild (arrowColor )
            
                    arrowTip = SoCone( )
                    arrowTip.bottomRadius.setValue( lineRadius * 2 )
                    arrowTip.height.setValue( 0.05 )
            
                    arrow.addChild( arrowTip )

                    arrowSet.addChild( arrow )   

                    self.velArrowSet.addChild( arrowSet )

            self.velArrowDrawStyle.style.setValue( SoDrawStyle.FILLED )
            self.velLineDrawStyle.style.setValue( SoDrawStyle.INVISIBLE )

        self.updateVel = True        
        
#---------------------------------------------------------------------------
# velDisplay: set the velocity vector 
#---------------------------------------------------------------------------

    def velDisplay( self, display = True ):

        self.velDisplayed = display
        
        if display == False:
            self.drawStyle_v.style.setValue( SoDrawStyle.INVISIBLE )
            self.velArrowDrawStyle.style.setValue( SoDrawStyle.INVISIBLE )
            self.velLineDrawStyle.style.setValue( SoDrawStyle.INVISIBLE )
            return
        
        else:          
            self.drawStyle_v.style.setValue( SoDrawStyle.FILLED )
            self.recreateVel( )       
            
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

	retVal	= self.trans

        if trans != None:
	    self.trans	= trans
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
		raise acuSgActorError, \
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
# "setTransparency" : Set Transparency of actor.
#---------------------------------------------------------------------------

    def setTransparency( self, status = 'on' ):
        ''' Set Transparency of actor.'''

        if status != 'on':
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

#---------------------------------------------------------------------------
# color: set/get the color of the actor
#---------------------------------------------------------------------------

    def color( self, r = None, g = None, b = None ):
        '''
	    Function to set the color of the actor

	    Arguments:
	        r,g,b		- red, blue, green values
	        
	    Output: ( only if r,g,b input is equal to None )
	        [ r, g, b ]	- red, blue, green values

	    Example:
	        actorColor	= acuSgActorError.color()
		acuSgActorError.color( red, green, blue )
	'''

	retVal	= ( self.r, self.g, self.b )


        if r != None and g != None and b != None:
	    self.r, self.g, self.b	= r, g, b
	    if not self.hLightFlag:
                self.material.diffuseColor.setValue(    r, g, b 	)

                #----- Misc. 1/08 J1 3/26/08
                self.setOutlineLnClr(                   r, g, b         )
                self.setWirefrmLnClr(                   r, g, b         )

	return retVal

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
	retVal	= self.vis

        if vis != None:
	    self.vis	= vis
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
# "setVisibility" : Set Visibility of actor.
#---------------------------------------------------------------------------

    def setVisibility( self, status = 'on' ):
        ''' Set Visibility of actor.'''

        if status != 'on':
            self.visibilityOff(                                         )
        else:
            self.visibilityOn(                                          )

#---------------------------------------------------------------------------
# "visibilityOff" : Set visibility of actor.
#---------------------------------------------------------------------------

    def visibilityOff( self ):
        ''' Set actor invisible.'''

	if self.findChild(	self.actor_w 	) != -1:
	    self.removeChild(		self.actor_w			)

        #----- Misc. 04/09 : J5 : SY
	if self.findChild(	self.actor_s1 	) != -1:
	    self.removeChild(		self.actor_s1			)
	#-----

	if self.findChild(	self.actor_s 	) != -1:
	    self.removeChild(		self.actor_s			)

	if self.findChild(	self.actor_o 	) != -1:
	    self.removeChild(		self.actor_o			)

	if self.findChild(	self.actor_so 	) != -1:
	    self.removeChild(		self.actor_so			)
	    
	if self.findChild(	self.actor_c 	) != -1:
	    self.removeChild(		self.actor_c			)

	if self.findChild(	self.actor_v 	) != -1:
	    self.removeChild(		self.actor_v			)

        self.visibility(                    False                       )

#---------------------------------------------------------------------------
# "visibilityOn" : Set visibility of actor.
#---------------------------------------------------------------------------

    def visibilityOn( self ):
        ''' Set actor visible.'''

        self.visibility(                    True                        )
	if self.findChild(	self.actor_w 	) == -1:
	    self.addChild(		self.actor_w			)

	if self.findChild(	self.actor_s 	) == -1:
	    self.addChild(		self.actor_s			)

        #----- Misc. 04/09 : J5 : SY
	if self.findChild(	self.actor_s1 	) == -1:
	    self.addChild(		self.actor_s1			)
	#-----

	if self.findChild(	self.actor_o 	) == -1:
	    self.addChild(		self.actor_o			)

	if self.findChild(	self.actor_so 	) == -1:
	    self.addChild(		self.actor_so			)

	if self.findChild(	self.actor_c 	) == -1:
	    self.addChild(		self.actor_c			)

	if self.findChild(	self.actor_v 	) == -1:
	    self.addChild(		self.actor_v			)

	if self.hLightFlag:
            self.display(               self.styleCopy                  )
        else:
            self.display(               self.style                      )

###---------------------------------------------------------------------------
### highlightType: set/get the highlight type of the display style
###---------------------------------------------------------------------------
##      #----- Misc. 6/07 F2
##    def highlightType( self, display, type = None ):
##        '''
##	    Function to set the highlight type of the actor.
##	    
##	    Arguments:
##                display         - display type of an actor
##	        type		- highlight type
##
##	    Output: ( Only if type equal to None )
##	        type		- highlight type
##	'''
##
##        if type != None:
##            self.hLightStyle[ display ] = type
##
##        else:
##            if self.hLightStyle.has_key( display ):
##                return self.hLightStyle[ display ]
##
##            #----- should be added to Preferences
##            if display == "line_point" or display == "line":
##                return "line"

#---------------------------------------------------------------------------
# highlight: highlight the actor
#---------------------------------------------------------------------------

    def highlight( self, hLight = None ):
        '''
	    Function to highlight the actor

	    Arguments:
	        None

	    Output:
	        None
	'''

        if not self.hLightFlag:
	    r,g,b	= self.hr, self.hg, self.hb
	    self.material.diffuseColor.setValue( 	r, g, b		)
	    
            #----- Misc. 1/08 J1 3/26/08
            if self.outlineLnClr == "Auto":
                self.setOutlineLnClr(                   r, g, b         )
                self.setWirefrmLnClr(                   r, g, b         )

	    self.styleCopy		= self.style

            #------ Misc. 6/07 F2 & G4

	    if not self.visibility():
                self._hLightVis(                                        )
                
	    if hLight:
                type        = hLight

	    elif not self.visibility():
		if shapeTypeMap[ self.cnnType ] == SHP_POINT:
		    type    = "point"
		else:
		    type    = "wireframe"
		
            elif self.style == "line_point" or self.style == "line":
                type        = "line"
            elif self.style == "point":
                type        = "point"
                
            #----- adding for "Add To" mode
            else:
                type        = self.parent.getHLighType(     self        )
                if not type:
                    acuSgActorError, "Invalid highlight type %s" %self.style
	    
	    self.display( 		type                            )
	    self.hLightFlag		= True

#---------------------------------------------------------------------------
# unHighlight: highlight the actor
#---------------------------------------------------------------------------

    def unHighlight( self ):
        '''
	    Function to unhighlight the actor

	    Arguments:
	        None

	    Output:
	        None
	'''
        if self.hLightFlag:
	    r,g,b	= self.r, self.g, self.b
	    self.material.diffuseColor.setValue( 	r, g, b		)
	    
            #----- Misc. 1/08 J1 3/26/08
	    self.setOutlineLnClr(                       r, g, b         )
            self.setWirefrmLnClr(                       r, g, b         )

	    self.display(		self.styleCopy			)
	    self.hLightFlag	= False

            if not self.visibility():
		self._unHLightInvis(                                    )

#---------------------------------------------------------------------------
# highLightColor: sets the highlight color.
#     [ By default this is set to white. what if the background color is
#       white. This functions allows to change the highlight color      ]
#---------------------------------------------------------------------------

    def highlightColor( self, hr = None, hg = None, hb = None ):
        '''
	    Function to set the highlight color,
	    default is white but could be changed for a light background

	    Arguments:
	        hr, hg,hb	- r,g,b values

	    Output: ( Only if hr,hg,hb are equal to None )
	        hr, hg,hb	- r,g,b values
	'''
        if hr != None and hg != None and hb != None:
	    self.hr,self.hg,self.hb = hr, hg, hb
	else:
	    return [self.hr,self.hg,self.hb]


#---------------------------------------------------------------------------
# lineWidth: set/get the linewidth of the display style,
#            when style = "outline" or "solid_outline"
#---------------------------------------------------------------------------

    def lineWidth( self, width = None ):
        '''
	    Function to set the line width of the actor,

	    Arguments:
	        width		- line width value

	    Output: ( Only if width equal to None )
	        width		- line width value
	'''
	retVal	= self.linWidth

	if width != None:
	    self.drawStyle_s.lineWidth.setValue( width )
	    self.drawStyle_w.lineWidth.setValue( width )
	    self.drawStyle_o.lineWidth.setValue( width )
	    self.drawStyle_so.lineWidth.setValue(width )
	    self.drawStyle_c.lineWidth.setValue( width )
	    self.drawStyle_v.lineWidth.setValue( width )
	    self.linWidth	= width

	return retVal

#---------------------------------------------------------------------------
# pointSize: set/get the pointSize of the display style,
#            when style = "point""
#---------------------------------------------------------------------------

    def pointSize( self, size = None ):
        '''
	    Function to set the point size of the actor when the display
	    type is "point",

	    Arguments:
	        size		- point size

	    Output: ( Only if size equal to None )
	        size		- point size
	'''

	retVal	= self.pntSize

        if size != None:
	    self.drawStyle_s.pointSize.setValue( size )
	    self.drawStyle_w.pointSize.setValue( size )
	    self.drawStyle_o.pointSize.setValue( size )
	    self.drawStyle_so.pointSize.setValue(size )
	    self.drawStyle_c.pointSize.setValue( size )
	    self.drawStyle_v.pointSize.setValue( size )
	    self.pntSize	= size

	return retVal

#---------------------------------------------------------------------------
# Shading: set/get the shadingModel of the display style,
#---------------------------------------------------------------------------

    def shadingModel( self, materialBinding = None, creaseAngle = 0.5, grFlag = False ):
        '''
	    Function to set the shading model of the actor,

	    Arguments:
	        light		 - light model
                materialBinding  - PER_FACE or PER_VERTEX
		creaseAngle      - 
		grFlag           - Gouraud shading flag
	    Output: 
	        None
	'''

        if materialBinding != None:
            self.shapeHints.creaseAngle.setValue(creaseAngle)
            self.vertProp.materialBinding.setValue( materialBinding )
            self.parent.grLight.on.setValue(grFlag)                          
                
#---------------------------------------------------------------------------
# destroy:  destructor for the actor
#---------------------------------------------------------------------------

    def destroy( self ):
        '''
	    Function to destroy the actor object.

	    Arguments:
	        None
	    Output:
	        None
	'''
        self.drawStyle_o	= None
        self.drawStyle_s	= None
        #----- Misc. 04/09 : J5 : SY
        self.drawStyle_s1	= None
        #-----
        self.drawStyle_w	= None
        self.drawStyle_so	= None
        self.drawStyle_c	= None
        self.drawStyle_v	= None

        self.material	= None
        self.material_w	= None
        self.material_so= None

        self.meshSet	= None
        self.outlineSet	= None
        self.area	= None
        self.center	= None
        self.normDir	= None
        self.boundBox	= None
	self.crd	= None
	self.cnn	= None
	self.vertProp	= None

	self.actor_o	= None
	self.actor_s	= None
	self.actor_w	= None
	self.actor_so	= None
	self.actor_c	= None
	self.actor_v	= None

        self.meshSet	        = None
        self.meshSet_c          = None
        self.outlineSet	        = None
        self.area	        = None
        self.center	        = None
        self.normDir	        = None
        self.boundBox	        = None
	self.crd	        = None
	self.cnn	        = None
	self.vertProp	        = None

	self.actor_o	        = None
	self.actor_s	        = None
	#----- Misc. 04/09 : J5 : SY
	self.actor_s1	        = None
	#-----
	self.actor_w	        = None
	self.actor_so	        = None
	self.actor_c	        = None

	self.removeAllChildren(					        )

#---------------------------------------------------------------------------
# _hLightVis:  Visible the actor in invisible mode and hLight
#---------------------------------------------------------------------------

    def _hLightVis( self ):
        '''
	    Visible the actor in invisible mode and hLight.

	    Arguments:
	        None
	    Output:
	        None
	'''

	if self.findChild(	self.actor_w 	) == -1:
	    self.addChild(		self.actor_w			)

	if self.findChild(	self.actor_s 	) == -1:
	    self.addChild(		self.actor_s			)

        #----- Misc. 04/09 : J5 : SY
	if self.findChild(	self.actor_s1 	) == -1:
	    self.addChild(		self.actor_s1			)
	#-----

	if self.findChild(	self.actor_o 	) == -1:
	    self.addChild(		self.actor_o			)

	if self.findChild(	self.actor_so 	) == -1:
	    self.addChild(		self.actor_so			)

	if self.findChild(	self.actor_c 	) == -1:
	    self.addChild(		self.actor_c			)

	if self.findChild(	self.actor_v 	) == -1:
	    self.addChild(		self.actor_v	                )

#---------------------------------------------------------------------------
# _unHLightInvis:  Invisible the actor in invisible mode and unhLight
#---------------------------------------------------------------------------

    def _unHLightInvis( self ):
        '''
	    Invisible the actor in invisible mode and unHLight.
	    The actor that was visibled in invisible and hlight mode.

	    Arguments:
	        None
	    Output:
	        None
	'''

	if self.findChild(	self.actor_w 	) != -1:
	    self.removeChild(		self.actor_w			)

	if self.findChild(	self.actor_s 	) != -1:
	    self.removeChild(		self.actor_s			)

        #----- Misc. 04/09 : J5 : SY
        if self.findChild(	self.actor_s1 	) != -1:
	    self.removeChild(		self.actor_s1			)
	#-----

	if self.findChild(	self.actor_o 	) != -1:
	    self.removeChild(		self.actor_o			)

	if self.findChild(	self.actor_so 	) != -1:
	    self.removeChild(		self.actor_so			)

	if self.findChild(	self.actor_c 	) != -1:
	    self.removeChild(		self.actor_c			)

	if self.findChild(	self.actor_v 	) != -1:
	    self.removeChild(		self.actor_v			)


#---------------------------------------------------------------------------
# crd:  Visible the actor in invisible mode and hLight
#---------------------------------------------------------------------------

    def resetCrd( self, crd = None ):
        '''
	     Reset the coordinatest value of an actor .

	    Arguments:
	        crd     - The new coordinate value
	    Output: ( Only if crd equal to None )
	        crd     - The coordinate value
	'''
        
        if crd != None:
	    if not isinstance(crd, numarray.numarraycore.NumArray ):
                try:
                    crd     = numarray.array(                   crd     )
                except:
                    raise acuSgActorError, " Incorrect Type of crd."

	    self.vertProp.vertex.setValues(         0,          crd     )

	    #----- Misc 06/10 B1
	    if self.vertProp_c != None:
                self.vertProp_c.vertex.setValues(   0,          crd     )

#---------------------------------------------------------------------------
# outlineLinClr: set/get the outline line color value
#---------------------------------------------------------------------------

    def outlineLinClr( self, clr = None ):
        '''
	    Function to set/get the Outline line color value

	    Arguments:
	        clr		- Outline line color which are
                                  "Auto", "Black", "White" 

	    Output: ( only if clr input is equal to None )
	'''

	retVal  = self.outlineLnClr

	if clr != None:
	    self.outlineLnClr   = clr

	return retVal

#---------------------------------------------------------------------------
# wirefrmLinClr: set/get the wireframe line color of the actor
#---------------------------------------------------------------------------

    def wirefrmLinClr( self, clr = None ):
        '''
	    Function to set/get the Wireframe line color value

	    Arguments:
	        clr		- Wireframe line color which are
                                  "Auto", "Black", "White" 

	    Output: ( only if clr input is equal to None )
	'''


	retVal  = self.wirefrmLnClr

	if clr != None:
	    self.wirefrmLnClr   = clr

	return retVal

#---------------------------------------------------------------------------
# setOutlineLnClr: set the outline line color of the actor
#---------------------------------------------------------------------------

    def setOutlineLnClr( self, rc, bc, gc ):
        '''
	    Function to set the Outline line color of the actor

	    Arguments:
                rc,gc,bc    - red, blue, green color values

	    Output:
                None
	'''

        if self.outlineLnClr == "Auto":
            r, g, b = acuQt.setOpsClr(  rc * 255, gc * 255, bc * 255    )
            r       = r / 255.0
            g       = g / 255.0
            b       = b / 255.0
                    
        elif self.outlineLnClr == "Black":
            r       = 0
            g       = 0
            b       = 0
        elif self.outlineLnClr == "White":
            r       = 1
            g       = 1
            b       = 1
        else:
            raise acuSgActorError, \
                  "Undefined Outline line color: %s " %self.outlineLnClr

        self.material_so.diffuseColor.setValue(         r,  g,  b       )

#---------------------------------------------------------------------------
# setOutlineLnClr: set the outline line color of the actor
#---------------------------------------------------------------------------

    def setWirefrmLnClr( self, rc, bc, gc ):
        '''
	    Function to set the Wireframe line color of the actor

	    Arguments:
                rc,gc,bc    - red, blue, green color values

	    Output:
                None
	'''

        if self.wirefrmLnClr == "Auto":
            r, g, b = acuQt.setOpsClr(  rc * 255, gc * 255, bc * 255    )
            r       = r / 255.0
            g       = g / 255.0
            b       = b / 255.0
                    
        elif self.wirefrmLnClr == "Black":
            r       = 0
            g       = 0
            b       = 0
        elif self.wirefrmLnClr == "White":
            r       = 1
            g       = 1
            b       = 1
        else:
            raise acuSgActorError, \
                  "Undefined Wireframe line color: %s " %self.wirefrmLnClr

        self.material_w.diffuseColor.setValue(          r,  g,  b       )

#---------------------------------------------------------------------------
# bndBox: Returns the bounding box of an object
#---------------------------------------------------------------------------

    def bndBox( self ):
        '''
	    Returns the bounding box of an object

	    Arguments:
                None    

	    Output:
                None
	'''

        bndBox  = acupu.srfLayOut(          self.crd, self.cnn      )[5]
        
        return bndBox
    
#---------------------------------------------------------------------------
# transMtx
#---------------------------------------------------------------------------

    def transMtx( self, transMtx = None ):
        
        if transMtx == None:
            return self.matrixTransform
        
        else:
            self.removeChild( self.matrixTransform )
            self.matrixTransform = transMtx
            self.insertChild( self.matrixTransform, 0 )

#---------------------------------------------------------------------------
# clearTransMtx
#---------------------------------------------------------------------------

    def clearTransMtx( self ):

        self.transMtx( SoTransform( ) )    

#---------------------------------------------------------------------------
# translate
#---------------------------------------------------------------------------

    def translate( self, trans = ( 0.0, 0.0, 0.0 ) ):
        
        self.matrixTransform.translation.setValue( SbVec3f( trans ) ) 

#---------------------------------------------------------------------------
# rotate
#---------------------------------------------------------------------------

    def rotate( self,   center  = ( 0.0, 0.0, 0.0 ),
                        axis    = ( 0.0, 0.0, 1.0 ),
                        angle   = 0.0                 ):
        
        self.matrixTransform.center.setValue( SbVec3f( center ) )        
	self.matrixTransform.rotation.setValue( SbRotation( SbVec3f( axis ), angle ) )	       

#---------------------------------------------------------------------------
# scale
#---------------------------------------------------------------------------

    def scale( self, scale = ( 1.0, 1.0, 1.0 ) ):

        self.matrixTransform.scaleFactor.setValue( scale )  

#===========================================================================
#
# Test
#
#===========================================================================

if __name__ == '__main__':
    print "Test Code"

