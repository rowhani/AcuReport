#---------------------------------------------------------------------------
# Get the modules
#---------------------------------------------------------------------------

import  math
import  types
import  string
import  numarray

import  acuUtil

#---------------------------------------------------------------------------
# Define Constants
#---------------------------------------------------------------------------

False   = 0
FALSE	= 0
false	= 0

True    = 1
TRUE	= 1
true	= 1

#===========================================================================
#
# Errors
#
#===========================================================================

class HeatSinkError( Exception ):
    def __init__( self, value ):
        self.value = "ERROR from HeatSink.py module: %s" % value
    def __str__( self ):
        return repr( self.value )

#===========================================================================
# Set Pin Fin heat sink "Draft angle" value; min and max
#===========================================================================

def setPfAngleCnd():

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'

    sinkHeight  = GetArray( path = node,        par = 'heat_sink_size',
                            unit = "m"                                  )[2]
    baseHeight  = GetReal(  path = node,        par = 'heat_sink_base_height',
                            unit = "m"                                  )
    height      = sinkHeight - baseHeight

    pfPinDiam   = GetReal(  path = node,        par = 'pf_pin_diameter',
                            unit = "m"                                  )

    angRad      = math.atan( ( pfPinDiam / ( 2  * height ) )            )
    angle       = math.degrees(                 angRad                  )

    return "par>=0 and par<%s" %str( angle )

#---------------------------------------------------------------------------
# calFinNumSidGap : Calculate heat sink fin-x/y numbers and side-x/y gaps
#---------------------------------------------------------------------------

def calFinNumSidGap(  sinkSize,  wid,   gap ):

    eps         = 1.e-8
    finNum      = int( ( sinkSize + gap ) / ( wid + gap ) + eps )
    sidGap      = sinkSize - finNum * wid - ( finNum - 1) * gap
    if abs(sidGap) < eps: sidGap = 0

    if finNum < 1 or sidGap < 0:
        raise HeatSinkError, "The model dimensions are invalid."

    return finNum, sidGap

#===========================================================================
# Calculate cross cut resolve parameters
#===========================================================================

def calCrossCutResolve():

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'

    resolve     = GetEnum(  path = node,        par = 'resolve'	        )
    sinkSize    = GetArray( path = node,        par = 'heat_sink_size',
                            unit = "m"                                  )
    sinkLength  = sinkSize[0]
    sinkWidth   = sinkSize[1]
    
    if resolve == "number_of_fins":
        finXWidth   = GetReal(  path = node,    par = 'fin_x_width',
                                unit = "m"                              )
        finXGap     = GetReal(  path = node,    par = 'fin_x_gap',
                                unit = "m"                              )
        finYWidth   = GetReal(  path = node,    par = 'fin_y_width',
                                unit = "m"                              )
        finYGap     = GetReal(  path = node,    par = 'fin_y_gap',
                                unit = "m"                              )
        eps         = 1.e-8
        
        numXFins    = int((sinkLength + finXGap)/(finXWidth + finXGap)+ eps)
        sideXGap    = (sinkLength - numXFins * finXWidth - (numXFins - 1) * finXGap) / 2

        numYFins    = int((sinkWidth + finYGap)/(finYWidth + finYGap)+ eps)
        sideYGap    = (sinkWidth - numYFins * finYWidth - (numYFins - 1) * finYGap) / 2

        if numXFins < 1 or sideXGap < 0 or numYFins < 1 or sideYGap < 0:
            raise HeatSinkError, 'The dimensions are invalid.'
        
        PutInt(	            node,	        "fin_x_num",
                            numXFins,           clobber = True          )

        PutReal(	    node,	        "side_x_gap",
                            sideXGap,           unit = "m",
                            clobber = True                              )

        PutInt(	            node,	        "fin_y_num",
                            numYFins,            clobber = True          )

        PutReal(	    node,	        "side_y_gap",
                            sideYGap,            unit = "m",
                            clobber = True                              )
        
    elif resolve == "fin_width":
        finXGap     = GetReal(  path = node,    par = 'fin_x_gap',
                                unit = "m"                              )

        finYGap     = GetReal(  path = node,    par = 'fin_y_gap',
                                unit = "m"                              )
        
        numXFins    = GetInt(   path = node,    par = 'fin_x_num'       )
        
        sideXGap    = GetReal(  path = node,    par = 'side_x_gap',
                                unit = "m"                              )

        numYFins    = GetInt(   path = node,    par = 'fin_y_num'       )
        
        sideYGap    = GetReal(  path = node,    par = 'side_y_gap',
                                unit = "m"                              )

        finXWidth= (sinkLength - 2 * sideXGap - (numXFins-1) * finXGap) / numXFins

        finYWidth= (sinkWidth - 2 * sideYGap - (numYFins-1) * finYGap) / numYFins
        
        if finXWidth < 0 or finYWidth < 0:
            raise HeatSinkError, 'The dimensions are invalid.'

        PutReal(	    node,	        "fin_x_width",   finXWidth,
                            unit = "m",        clobber = True          )

        PutReal(	    node,	        "fin_y_width",   finYWidth,
                            unit = "m",        clobber = True          )

    else:
        finXWidth= GetReal( path = node,        par = 'fin_x_width',
                            unit = "m"                                  )

        finYWidth= GetReal( path = node,        par = 'fin_y_width',
                            unit = "m"                                  )
        
        numXFins    = GetInt(   path = node,    par = 'fin_x_num'       )
        
        sideXGap    = GetReal(  path = node,    par = 'side_x_gap',
                                unit = "m"                              )

        numYFins    = GetInt(   path = node,    par = 'fin_y_num'       )
        
        sideYGap    = GetReal(  path = node,    par = 'side_y_gap',
                                unit = "m"                              )

        finXGap     = (sinkLength - 2 * sideXGap - numXFins * finXWidth) / (numXFins-1)
        finYGap     = (sinkWidth - 2 * sideYGap - numYFins * finYWidth) / (numYFins-1)
        
        if finXGap < 0 or finYGap < 0:
            raise HeatSinkError, 'The dimensions are invalid.'

        PutReal(	    node,	        "fin_x_gap",     finXGap,
                            unit = "m",        clobber = True           )

        PutReal(	    node,	        "fin_y_gap",     finYGap,
                            unit = "m",        clobber = True           )

    return finXWidth, finXGap, numXFins, sideXGap, finYWidth, finYGap, numYFins, sideYGap

#===========================================================================
# Calculate extrusion resolve parameters
#===========================================================================

def calExtrusionResolve():

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'

    resolve     = GetEnum(  path = node,        par = 'ex_resolve'	)
    sinkWidth   = GetArray( path = node,        par = 'heat_sink_size',
                            unit = "m"                                  )[1]
    
    if resolve == "number_of_fins":
        finWidth= GetReal(  path = node,        par = 'ex_fin_y_width',
                            unit = "m"                                  )
        finGap  = GetReal(  path = node,        par = 'ex_fin_y_gap',
                            unit = "m"                                  )
        eps     = 1.e-8
        
        numFins = int( (sinkWidth + finGap) / (finWidth + finGap) + eps ) 
        sideGap = (sinkWidth - numFins * finWidth - (numFins - 1) * finGap) / 2

        if numFins <= 0 or sideGap < 0:
            raise HeatSinkError, 'The dimensions are invalid.'
        
        PutInt(	            node,	        "ex_fin_y_num",
                            numFins,            clobber = True          )

        PutReal(	    node,	        "ex_side_y_gap",
                            sideGap,            unit = "m",
                            clobber = True                              )
        
    elif resolve == "fin_width":
        finGap  = GetReal(  path = node,        par = 'ex_fin_y_gap',
                            unit = "m"                                  )
        numFins = GetInt(   path = node,        par = 'ex_fin_y_num'    )
        sideGap = GetReal(  path = node,        par = 'ex_side_y_gap',
                            unit = "m"                                  )

        finWidth= (sinkWidth - 2 * sideGap - (numFins-1) * finGap) / numFins
        if finWidth < 0:
            raise HeatSinkError, 'The dimensions are invalid.'

        PutReal(	    node,	        "ex_fin_y_width",   finWidth,
                            unit = "m",        clobber = True           )

    else:
        finWidth= GetReal(  path = node,        par = 'ex_fin_y_width',
                            unit = "m"                                  )
        numFins = GetInt(   path = node,        par = 'ex_fin_y_num'    )
        sideGap = GetReal(  path = node,        par = 'ex_side_y_gap',
                            unit = "m"                                  )

        finGap  = (sinkWidth - 2 * sideGap - numFins * finWidth) / (numFins-1)
        
        if finGap < 0:
            raise HeatSinkError, 'The dimensions are invalid.'

        PutReal(	    node,	        "ex_fin_y_gap",     finGap,
                            unit = "m",        clobber = True           )

    return finWidth, finGap, numFins, sideGap

#===========================================================================
# Calculate Diamond cut heat sink fin numbers
#===========================================================================

def calDiamCutFinNum():

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'
    sinkSize    = GetArray( path = node,        par = 'heat_sink_size',
                            unit = "m"                                  )
    dcFinWidth  = GetReal(  path = node,        par = 'dc_fin_width',
                            unit = "m"                                  )
    dcFinGap    = GetReal(  path = node,        par = 'dc_fin_gap',
                            unit = "m"                                  )

    wid         = dcFinWidth    * math.cos(             math.radians(45))
    gap         = dcFinGap      * math.cos(             math.radians(45))
    GAP         = (2 * dcFinGap + dcFinWidth)* math.cos(math.radians(45))
    
    numX, sideX = calFinNumSidGap(   sinkSize[0],       wid,    GAP     )
    numY, sideY = calFinNumSidGap(   sinkSize[1],       wid,    GAP     )

    finNum      = 0
    x1          = (sinkSize[0] - sideX )/ 2
    y1          = (sinkSize[1] - sideY )/ 2
    x0          = -x1
    y0          = -y1
    LX          = wid + gap
    LY          = LX
    Y0          = y0 - 2 * LY
    for m in xrange( numY ):
        Y0      += 2 * LY
        Y1      = Y0 + LY
        X0      = x0 - LX
        for n in xrange( numX ):
            X0  += LX
            finNum += 1
            
            X0  += LX
            if X0 > x1 or Y1 >y1: continue
            finNum += 1

    PutInt(	            node,	        "dc_fin_num",
                            finNum,             clobber = True          )

    return dcFinWidth, finNum

#===========================================================================
# Calculate heat sink weight
#===========================================================================

def calHeatSinkWeight( xSize, nx, ySize, ny ):

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'

    sinkSize    = GetArray( path = node,    par = 'heat_sink_size',
                            unit = "m"                                  )
    baseHightSize=GetReal(  path = node,    par = 'heat_sink_base_height',
                            unit = "m"                                  )
    zSize       = sinkSize[2] - baseHightSize

    sinkVol     = nx * ny * xSize * ySize * zSize
    baseVol     = sinkSize[0] * sinkSize[1] * baseHightSize
    totVol      = sinkVol + baseVol

    material    = GetRef(   path = node,    par = "sink_material_model" )
    nodeMat	= ROOT + RS + 'MATERIAL_MODEL' + RS + material
    nodeDens	= nodeMat + RS + 'DENSITY_MODEL'
    density     = GetReal(  path = nodeDens,par = "density",
                            unit = "kg/m3"                              )

    weight      = totVol * density
    PutReal(	            node,	        "heat_sink_weight",
                            weight,             unit = "kg",
                            clobber = True                              )

    return weight

#===========================================================================
# Calculate Pin fin heat sink fin numbers and weight
#===========================================================================

def calPinFinNumWeight():

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'
    sinkSize    = GetArray( path = node,        par = 'heat_sink_size',
                            unit = "m"                                  )
    arngmnt     = GetEnum(  path = node,        par = 'pf_arrangement'  )
    pfPinDiameter=GetReal(  path = node,        par = "pf_pin_diameter",
                            unit = "m"                                  )
    pfFinGap    = GetReal(  path = node,        par = "pf_fin_gap",
                            unit = "m"                                  )
    angle       = GetReal(  path = node,        par = "pf_angle",
                            unit = "rad"                                )
    if angle == 0: angle = math.radians(        1.e-8                   )
    finNum      = 0

    if arngmnt == "staggered":
        diam    = pfPinDiameter * math.cos(     math.radians( 45 )      )
        gap     = pfFinGap      * math.cos(     math.radians( 45 )      )
        GAP     =( 2*pfFinGap + pfPinDiameter)* math.cos( math.radians(45))
        
        numX, sideX = calFinNumSidGap(   sinkSize[0],    diam,   GAP    )
        numY, sideY = calFinNumSidGap(   sinkSize[1],    diam,   GAP    )

        x1      = (sinkSize[0]  - sideX) / 2
        y1      = (sinkSize[1]  - sideY) / 2
        x0      = -x1
        y0      = -y1
        x0      += diam / 2
        y0      += diam / 2
        LX      = diam + gap
        LY      = LX
        Y0      = y0 - 2 * LY
        for m in xrange( numY ):
            Y0  += 2 * LY
            Y1  = Y0 + LY
            X0  = x0 - LX
            for n in xrange( numX ):
                X0  += LX
                finNum += 1

                X0  += LX
                if X0 > x1 or Y1 >y1: continue
                finNum += 1
    else:
        numX, sideX = calFinNumSidGap(          sinkSize[0],
                                                pfPinDiameter,  pfFinGap)
        numY, sideY = calFinNumSidGap(          sinkSize[1],
                                                pfPinDiameter,  pfFinGap)
        finNum      = numX * numY

    #---------------------------------------------------------------------
    # Calculate heat sink weight
    #---------------------------------------------------------------------

    baseHightSize=GetReal(  path = node,    par = 'heat_sink_base_height',
                            unit = "m"                                  )
    h           = sinkSize[2]   - baseHightSize
    r           = pfPinDiameter - 2 * ( h   *   math.tan( angle )       )
    
    conVol      = math.pi/12*h*(pfPinDiameter**2+r**2+ r * pfPinDiameter)
    sinkVol     = finNum * conVol
    baseVol     = sinkSize[0] * sinkSize[1] * baseHightSize
    totVol      = sinkVol + baseVol

    material    = GetRef(   path = node,    par = "sink_material_model" )
    nodeMat	= ROOT + RS + 'MATERIAL_MODEL' + RS + material
    nodeDens	= nodeMat + RS + 'DENSITY_MODEL'
    density     = GetReal(  path = nodeDens,par = "density",
                            unit = "kg/m3"                              )

    weight      = totVol * density

    PutInt(	            node,	        "pf_fin_num",
                            finNum,             clobber = True          )

    PutReal(	            node,	        "heat_sink_weight",
                            weight,             unit = "kg",
                            clobber = True                              )

    return finNum, weight 

#===========================================================================
# Open the Heat Sink panel and tabs
#===========================================================================

def usrOpenHeatSink( item, args ):

    node = ROOT + RS + 'User' + RS + 'HEAT_SINK'

    MenuTab(tabs	= ( ( 'CAD',	        'cad'		),
			    ( 'Mesh',	        'mesh'		),
			    ( 'Problem',	'problem'	),
                            ( 'Process',	'process'	),
                            ),
	    node	= node,
	    par	        = 'tab',
	    redraw	= True,
	    default	= 'cad'
	    )

    tab	= GetTab(	path = node,		par = 'tab'	        )

    if tab == 'cad':
	usrOpenHeatSinkCAD(	    item,	args			)
    elif tab == 'mesh':
	usrOpenHeatSinkMesh(	    item,	args			)
    elif tab == 'problem':
	usrOpenHeatSinkProblem(     item,	args			)
    elif tab == 'process':
	usrOpenHeatSinkProcess(     item,	args			)
	
#===========================================================================
# Open a CAD - For designing, importing and grouping the CAD
#===========================================================================

def usrOpenHeatSinkCAD( item, args ):

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'
    URL         = "heat_sink.htm"

    #---------------------------------------------------------------------
    # Define related menus
    #---------------------------------------------------------------------

    MenuArray(  name    = 'Tunnel size',
                tooltip = 'Tunnel size',
                whatsthis='Tunnel size',
                node    = node,
                par     = 'tunnel_size',
                unitCat = 'length',
                aryType	= 'vector:size',
                cols    = (3,3),
                rows    = (1,1)						)

    MenuArray(  name    = 'Board size',
                tooltip = 'Board size',
                whatsthis='Board size',
                node    = node,
                par     = 'board_size',
                unitCat = 'length',
                aryType	= 'vector:size',
                cols    = (3,3),
                rows    = (1,1)						)

    MenuArray(  name    = 'Chip size',
                tooltip = 'Chip size',
                whatsthis='Chip size',
                node    = node,
                par     = 'chip_size',
                unitCat = 'length',
                aryType	= 'vector:size',
                cols    = (3,3),
                rows    = (1,1)						)

    MenuEnum(	name	= 'Heat sink type',
		tooltip	= 'Heat sink type',
		whatsthis='Heat sink type',
		helpURL	= URL + '#Heat_sink_type',
		node	= node,
		par	= 'heat_sink_type',
                enum    = ( ('None',        'none'          ),
                            ('Cross Cut',   'cross cut'     ),
                            ('Extrusion',   'extrusion'     ),
                            ('Diamond Cut', 'diamond cut'   ),
                            ('Pin Fin',     'pin fin'       ),
                          ),
		redraw	= True						)

    #---------------------------------------------------------------------
    # Set Menus for different Heat Sink types
    #---------------------------------------------------------------------

    sinkType	= GetEnum(   path = node,    par = 'heat_sink_type'	)
    heatSinkWeight = None

    if sinkType != "none":

        MenuArray(name  = 'Heat sink size',
                tooltip = 'Heat Sink Size',
                whatsthis='Heat sink size',
                node    = node,
                par     = 'heat_sink_size',
                unitCat = 'length',
                aryType	= 'vector:size',
                cols    = (3,3),
                rows    = (1,1),
                redraw  = True                                          )

        MenuReal(name	= 'Heat sink base height',
		tooltip	= 'Heat sink base height',
		whatsthis='Heat sink base height',
		helpURL	= URL + '#Heatsinkbaseheight',
		node	= node,
		par	= 'heat_sink_base_height',
                unitCat = 'length',
                cond    = 'par > 0',
                redraw  = True                                          )

        sinkSize        = GetArray( path = node,     par = 'heat_sink_size',
                                    unit = "m"                          )
    if sinkType == "cross cut":

        MenuEnum(name	= 'Resolve',
                tooltip	= 'Resolve type',
                whatsthis='Resolve type',
                helpURL	= URL + '#Resolve_type',
                node	= node,
                par	= 'resolve',
                enum    = ( ('Number of fins',  'number_of_fins'),
                            ('Fin width',       'fin_width'     ),
                            ('Fin gap',         'fin_gap'       ),
                          ),
                redraw	= True					        )

        ( finXWidth, finXGap, numXFins, sideXGap,
          finYWidth, finYGap, numYFins, sideYGap ) = calCrossCutResolve()
        
        resolve         = GetEnum(  path = node,    par = 'resolve'	)
        heatSinkWeight  = calHeatSinkWeight(        finXWidth,  numXFins,
                                                    finYWidth,  numYFins)

        if resolve == "number_of_fins":

            MenuReal(name= 'Fin x-width',
                tooltip	= 'Fin x-width',
                whatsthis='Fin x-width',
                helpURL	= URL + '#Fin x-width',
                node	= node,
                par	= 'fin_x_width',
                unitCat = 'length',
                cond    = 'par > 0',
                redraw	= True                                          )

            MenuReal(name= 'Fin x-gap',
                tooltip	= 'Fin x-gap',
                whatsthis='Fin x-gap',
                helpURL	= URL + '#Fin x-gap',
                node	= node,
                par	= 'fin_x_gap',
                unitCat = 'length',
                redraw	= True,
                cond    = 'par > 0'					)

            MenuInfo(name= 'Number of x-fins',
		tooltip	= 'Number of x-fins',
		whatsthis='Number of x-fins',
		helpURL	= URL + '#Number of x-fins',
                value   = numXFins                                    	)
            
            MenuInfo(name= 'Side x-gap',
		tooltip	= 'Side x-gap',
		whatsthis='Side x-gap',
		helpURL	= URL + '#Side x-gap',
                value   = '%.6g m' % sideXGap                           )

            MenuReal(name= 'Fin y-width',
                tooltip	= 'Fin y-width',
                whatsthis='Fin y-width',
                helpURL	= URL + '#Fin y-width',
                node	= node,
                par	= 'fin_y_width',
                unitCat = 'length',
                redraw	= True,
                cond    = 'par > 0'					)

            MenuReal(name= 'Fin y-gap',
                tooltip	= 'Fin y-gap',
                whatsthis='Fin y-gap',
                helpURL	= URL + '#Fin y-gap',
                node	= node,
                par	= 'fin_y_gap',
                unitCat = 'length',
                redraw	= True,
                cond    = 'par > 0',					)

            MenuInfo(name= 'Number of y-fins',
		tooltip	= 'Number of y-fins',
		whatsthis='Number of y-fins',
		helpURL	= URL + '#Number of y-fins',
                value   = numYFins                                    	)
            
            MenuInfo(name= 'Side y-gap',
		tooltip	= 'Side y-gap',
		whatsthis='Side y-gap',
		helpURL	= URL + '#Side y-gap',
                value   = '%.6g m' % sideYGap                           )
            
        elif resolve == "fin_width":

            MenuInfo(name= 'Fin x-width',
		tooltip	= 'Fin x-width',
		whatsthis='Fin x-width',
		helpURL	= URL + '#Fin x-width',
                value   = '%.6g m' % finXWidth                          )

            MenuReal(name= 'Fin x-gap',
                tooltip	= 'Fin x-gap',
                whatsthis='Fin x-gap',
                helpURL	= URL + '#Fin x-gap',
                node	= node,
                par	= 'fin_x_gap',
                unitCat = 'length',
                redraw	= True,
                cond    = 'par > 0'					)

            MenuInt(name= 'Number of x-fins',
		tooltip	= 'Number of x-fins',
		whatsthis='Number of x-fins',
		helpURL	= URL + '# x-fins',
		node	= node,
                cond    ='par > 0',
		par	= 'fin_x_num',
                redraw  = True                                          )            

            MenuReal(name= 'Side x-gap',
                tooltip	= 'Side x-gap',
                whatsthis='Side x-gap',
                helpURL	= URL + '#Side x-gap',
                node	= node,
                par	= 'side_x_gap',
                unitCat = 'length',
                cond    = 'par >= 0',
                redraw	= True                                          )
            
            MenuInfo(name= 'Fin y-width',
		tooltip	= 'Fin y-width',
		whatsthis='Fin y-width',
		helpURL	= URL + '#Fin y-width',
                value   = '%.6g m' % finYWidth                          )

            MenuReal(name= 'Fin y-gap',
                tooltip	= 'Fin y-gap',
                whatsthis='Fin y-gap',
                helpURL	= URL + '#Fin y-gap',
                node	= node,
                par	= 'fin_y_gap',
                unitCat = 'length',
                redraw	= True,
                cond    = 'par > 0'					)

            MenuInt(name= 'Number of y-fins',
		tooltip	= 'Number of y-fins',
		whatsthis='Number of y-fins',
		helpURL	= URL + '# y-fins',
		node	= node,
                cond    ='par > 0',
		par	= 'fin_y_num',
                redraw  = True                                          )            

            MenuReal(name= 'Side y-gap',
                tooltip	= 'Side y-gap',
                whatsthis='Side y-gap',
                helpURL	= URL + '#Side y-gap',
                node	= node,
                par	= 'side_y_gap',
                unitCat = 'length',
                cond    = 'par >= 0',
                redraw	= True                                          )
        else:

            MenuReal(name= 'Fin x-width',
                tooltip	= 'Fin x-width',
                whatsthis='Fin x-width',
                helpURL	= URL + '#Fin x-width',
                node	= node,
                par	= 'fin_x_width',
                unitCat = 'length',
                cond    = 'par > 0',
                redraw	= True                                          )

            MenuInfo(name= 'Fin x-gap',
		tooltip	= 'Fin x-gap',
		whatsthis='Fin x-gap',
		helpURL	= URL + '#Fin x-gap',
                value   = '%.6g m' % finXGap                          	)
            
            MenuInt(name= 'Number of x-fins',
		tooltip	= 'Number of x-fins',
		whatsthis='Number of x-fins',
		helpURL	= URL + '# x-fins',
		node	= node,
                cond    ='par > 0',
		par	= 'fin_x_num',
                redraw  = True                                          )            

            MenuReal(name= 'Side x-gap',
                tooltip	= 'Side x-gap',
                whatsthis='Side x-gap',
                helpURL	= URL + '#Side x-gap',
                node	= node,
                par	= 'side_x_gap',
                unitCat = 'length',
                cond    = 'par >= 0',
                redraw	= True                                          )

            MenuReal(name= 'Fin y-width',
                tooltip	= 'Fin y-width',
                whatsthis='Fin y-width',
                helpURL	= URL + '#Fin y-width',
                node	= node,
                par	= 'fin_y_width',
                unitCat = 'length',
                redraw	= True,
                cond    = 'par > 0'					)

            MenuInfo(name= 'Fin y-gap',
		tooltip	= 'Fin y-gap',
		whatsthis='Fin y-gap',
		helpURL	= URL + '#Fin y-gap',
                value   = '%.6g m' % finYGap                          	)

            MenuInt(name= 'Number of y-fins',
		tooltip	= 'Number of y-fins',
		whatsthis='Number of y-fins',
		helpURL	= URL + '# y-fins',
		node	= node,
                cond    ='par > 0',
		par	= 'fin_y_num',
                redraw  = True                                          )            

            MenuReal(name= 'Side y-gap',
                tooltip	= 'Side y-gap',
                whatsthis='Side y-gap',
                helpURL	= URL + '#Side y-gap',
                node	= node,
                par	= 'side_y_gap',
                unitCat = 'length',
                cond    = 'par >= 0',
                redraw	= True                                          )

    elif sinkType == "extrusion":

        MenuEnum(name	= 'Resolve',
                tooltip	= 'Resolve type',
                whatsthis='Resolve type',
                helpURL	= URL + '#Resolve_type',
                node	= node,
                par	= 'ex_resolve',
                enum    = ( ('Number of fins',  'number_of_fins'),
                            ('Fin width',       'fin_width'     ),
                            ('Fin gap',         'fin_gap'       ),
                          ),
                redraw	= True					        )

        finWidth, finGap, numFins, sideGap  = calExtrusionResolve(      )
        exResolve   = GetEnum(  path = node,        par = 'ex_resolve'	)

        heatSinkWeight= calHeatSinkWeight(  sinkSize[0],    1,
                                            finWidth,       numFins     )
        
        if exResolve == "number_of_fins":

            MenuReal(name= 'Fin y-width',
                tooltip	= 'Fin y-width',
                whatsthis='Fin y-width',
                helpURL	= URL + '#Fin y-width',
                node	= node,
                par	= 'ex_fin_y_width',
                unitCat = 'length',
                cond    = 'par > 0',
                redraw	= True                                          )

            MenuReal(name= 'Fin y-gap',
                tooltip	= 'Fin y-gap',
                whatsthis='Fin y-gap',
                helpURL	= URL + '#Fin y-gap',
                node	= node,
                par	= 'ex_fin_y_gap',
                unitCat = 'length',
                cond    = 'par > 0',
                redraw	= True                                          )

            MenuInfo(name= 'Number of y-fins',
		tooltip	= 'Number of y-fins',
		whatsthis='Number of y-fins',
		helpURL	= URL + '#Number of y-fins',
                value   = numFins                                    	)
            
            MenuInfo(name= 'Side y-gap',
		tooltip	= 'Side y-gap',
		whatsthis='Side y-gap',
		helpURL	= URL + '#Side y-gap',
                value   = '%.6g m' % sideGap                          	)
            
        elif exResolve == "fin_width":

            MenuInfo(name= 'Fin y-width',
		tooltip	= 'Fin y-width',
		whatsthis='Fin y-width',
		helpURL	= URL + '#Fin y-width',
                value   = '%.6g m' % finWidth                          	)

            MenuReal(name= 'Fin y-gap',
                tooltip	= 'Fin y-gap',
                whatsthis='Fin y-gap',
                helpURL	= URL + '#Fin y-gap',
                node	= node,
                par	= 'ex_fin_y_gap',
                unitCat = 'length',
                cond    = 'par > 0',
                redraw	= True                                          )

            MenuInt(name= 'Number of y-fins',
		tooltip	= 'Number of y-fins',
		whatsthis='Number of y-fins',
		helpURL	= URL + '# y-fins',
		node	= node,
                cond    ='par > 0',
		par	= 'ex_fin_y_num',
                redraw  = True                                          )            

            MenuReal(name= 'Side y-gap',
                tooltip	= 'Side y-gap',
                whatsthis='Side y-gap',
                helpURL	= URL + '#Side y-gap',
                node	= node,
                par	= 'ex_side_y_gap',
                unitCat = 'length',
                cond    = 'par >= 0',
                redraw	= True                                          )

        else:

            MenuReal(name= 'Fin y-width',
                tooltip	= 'Fin y-width',
                whatsthis='Fin y-width',
                helpURL	= URL + '#Fin y-width',
                node	= node,
                par	= 'ex_fin_y_width',
                unitCat = 'length',
                cond    = 'par > 0',
                redraw	= True                                          )

            MenuInfo(name= 'Fin y-gap',
		tooltip	= 'Fin y-gap',
		whatsthis='Fin y-gap',
		helpURL	= URL + '#Fin y-gap',
                value   = '%.6g m' % finGap                          	)
            
            MenuInt(name= 'Number of y-fins',
		tooltip	= 'Number of y-fins',
		whatsthis='Number of y-fins',
		helpURL	= URL + '# y-fins',
		node	= node,
                cond    ='par > 0',
		par	= 'ex_fin_y_num',
                redraw  = True                                          )            

            MenuReal(name= 'Side y-gap',
                tooltip	= 'Side y-gap',
                whatsthis='Side y-gap',
                helpURL	= URL + '#Side y-gap',
                node	= node,
                par	= 'ex_side_y_gap',
                unitCat = 'length',
                cond    = 'par >= 0',
                redraw	= True                                          )

    elif sinkType == "diamond cut":
        
        wid, finNum     = calDiamCutFinNum(                             )
        heatSinkWeight  = calHeatSinkWeight(        2 * wid,    finNum,
                                                    wid,        1       )

        MenuReal(name	= 'Fin width',
		tooltip	= 'Fin width',
		whatsthis='Fin width',
		helpURL	= URL + '#Fin width',
		node	= node,
		par	= 'dc_fin_width',
                unitCat = 'length',
                cond    = 'par > 0',
                redraw	= True                                          )

        MenuReal(name	= 'Fin gap',
		tooltip	= 'Fin gap',
		whatsthis='Fin gap',
		helpURL	= URL + '#Fin gap',
		node	= node,
		par	= 'dc_fin_gap',
                unitCat = 'length',
                redraw	= True,
                cond    = 'par > 0'					)

        MenuInfo(name   = 'Number of fins',
		tooltip	= 'Number of fins',
		whatsthis='Number of fins',
		helpURL	= URL + '#Number of fins',
                value   = finNum                                    	)

    elif sinkType == "pin fin":

        finNum, heatSinkWeight  = calPinFinNumWeight(                   )

        MenuEnum(name	= 'Arrangement',
                tooltip	= 'Arrangement type',
                whatsthis='Arrangement type',
                helpURL	= URL + '#Arrangement_type',
                node	= node,
                redraw  = True,
                par	= 'pf_arrangement',
                enum    = ( ('In-line',     'inLine'),
                            ('Staggered',   'staggered'       ),
                          ),
                 )

        MenuReal(name	= 'Pin diameter',
		tooltip	= 'Pin diameter',
		whatsthis='Pin diameter',
		helpURL	= URL + '#PinDiameter',
		node	= node,
		par	= 'pf_pin_diameter',
                unitCat = 'length',
                cond    = 'par > 0',
                redraw  = True                                          ) 

        MenuReal(name	= 'Fin gap',
		tooltip	= 'Fin gap',
		whatsthis='Fin gap',
		helpURL	= URL + '#Fin gap',
		node	= node,
		par	= 'pf_fin_gap',
                unitCat = 'length',
                redraw  = True,
                cond    = 'par > 0'					)

        pfAngleCnd      = setPfAngleCnd(                                )
        MenuReal(name	= 'Draft angle',
		tooltip	= 'Draft angle',
		whatsthis='Draft angle',
		helpURL	= URL + '#Draft angle',
		node	= node,
		par	= 'pf_angle',
                unitCat = 'angle',
                redraw  = True,
                cond    = pfAngleCnd					)

        MenuInfo(name   = 'Number of fins',
		tooltip	= 'Number of fins',
		whatsthis='Number of fins',
		helpURL	= URL + '#Number of fins',
                value   = finNum                                    	)

    #---------------------------------------------------------------------
    # Heat sink weight
    #---------------------------------------------------------------------

    if heatSinkWeight != None:
        MenuInfo(name   = 'Heat sink weight',
		tooltip	= 'Heat sink weight',
		whatsthis='Heat sink weight',
		helpURL	= URL + '#HeatSinkWeight',
                value   = '%.6g Kg' % heatSinkWeight                   	)
    
    #---------------------------------------------------------------------
    # Execute the generate CAD function
    #---------------------------------------------------------------------

    MenuFunc(	name	= 'Generate CAD',
		tooltip	= 'Generate CAD',
		whatsthis='Click this the button to automatically \n'
			  'Generate CAD',
		helpURL	= URL + '#func',
		node	= node,
		par	= 'funcGenCad',
		func	= usrBuildHeatSinkCad				)

    #---------------------------------------------------------------------
    # Create Images
    #---------------------------------------------------------------------

    MenuFunc(	name	= 'Generate images',
		tooltip	= 'Generate images',
		whatsthis='Click this the button to automatically \n'
			  'Generate images from created CAD',
		helpURL	= URL + '#func',
		node	= node,
		par	= 'funcGenImages',
		func	= usrBuildHeatSinkImages			)

#===========================================================================
# generateCADFunc - Call the HeatSinkCAD.heatSinkModel to generate the CAD.
#===========================================================================

def usrBuildHeatSinkCad( 	dialog  = False,	tail    = False,
				args    = None,		sendState= None,
				win     = None,		name    = None,
				fileName= None
                        ):

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'
    sinkType    = None

    if not dialog and sendState:
        sendState(                              'started'               )

    if type( args ) == types.DictType:
        if args.has_key('fileName'):
            fileName            = args['fileName']
                
        if args.has_key('htSinkType'):
            sinkType            = args['htSinkType']
        
    
    sinkBaseDims= None
    sinkDims    = None
    ccXFinWidth = None
    ccXFinGap   = None
    ccYFinWidth = None
    ccYFinGap   = None
    exYFinWidth = None
    exYFinGap   = None
    dcFinWidth  = None
    dcFinGap    = None
    pfPinDiameter= None
    pfFinGap    = None
    pfArngmnt   = "inLine"
    pfFinAngle  = 0.0

    #---------------------------------------------------------------------
    # Get the usr data from data base and checking them
    #---------------------------------------------------------------------

    tunlSize    = GetArray(     path = node,    par = 'tunnel_size',
                                unit = "m"                             )
    boardSize   = GetArray(     path = node,    par = 'board_size',
                                unit = "m"                             )
    chipSize    = GetArray(     path = node,    par = 'chip_size',
                                unit = "m"                             )

    # Hack to work around array editor squirriliness
    if len(boardSize.shape)==2:
        boardSize  = boardSize[0,:]
    if len(tunlSize.shape)==2:
        tunlSize  = tunlSize[0,:]
    if len(chipSize.shape)==2:
        chipSize  = chipSize[0,:]

    for i in xrange( 3 ):
        if boardSize[i] > tunlSize[i]:
            raise HeatSinkError, "The Board dimensions are invalid. " \
                  "They could not be more than Tunnel dimensions."

    for i in xrange( 2 ):
        if chipSize[i] > boardSize[i]:
            raise HeatSinkError, "The Chip length and width dimensions "\
                  "are invalid. They could not be more than Board dimensions."

    if not sinkType:
        sinkType    = GetEnum(  path = node,    par = 'heat_sink_type'	)
    sinkType        = sinkType.lower(                                   )

    if sinkType != "none":
        sinkSize    = GetArray( path = node,    par = 'heat_sink_size',
                                unit = "m"                             )
        sinkHightSize=GetReal(  path = node,
                                par  = 'heat_sink_base_height',
                                unit = "m"                             )

        for i in xrange( 2 ):
            if sinkSize[i] > boardSize[i]:
                raise HeatSinkError, "The Heat Sink length and width dimensions "\
                      "are invalid. They could not be more than Board dimensions."

        partsHeight =  boardSize[2] /2 + chipSize[2] + sinkSize[2]
        if partsHeight > tunlSize[2] / 2:
            raise HeatSinkError, "The model height dimensions are invalid."

        #----- Calculate sinkBaseDims
        sinkBaseDims= (         sinkSize[0],    sinkSize[1],
                                sinkHightSize                           )

        sinkDims    = (         sinkSize[0],    sinkSize[1],
                                sinkSize[2] - sinkHightSize             )

    if sinkType == "cross cut":
        ccXFinWidth = GetReal(  path = node,    par = 'fin_x_width',
                                unit = "m"                             )
        ccXFinGap   = GetReal(  path = node,    par = 'fin_x_gap',
                                unit = "m"                             )
        ccYFinWidth = GetReal(  path = node,    par = 'fin_y_width',
                                unit = "m"                             )
        ccYFinGap   = GetReal(  path = node,    par = 'fin_y_gap',
                                unit = "m"                             )

    elif sinkType == "extrusion":
        exYFinWidth = GetReal(  path = node,    par = 'ex_fin_y_width',
                                unit = "m"                             )
        exYFinGap   = GetReal(  path = node,    par = 'ex_fin_y_gap',
                                unit = "m"                             )

    elif sinkType == "diamond cut":
        dcFinWidth  = GetReal(  path = node,    par = 'dc_fin_width',
                                unit = "m"                             )
        dcFinGap    = GetReal(  path = node,    par = 'dc_fin_gap',
                                unit = "m"                             )

    elif sinkType == "pin fin":
        pfArngmnt   = GetEnum(  path = node,    par = 'pf_arrangement')
        pfPinDiameter= GetReal( path = node,    par = 'pf_pin_diameter',
                                unit = "m"                              )
        pfFinGap    = GetReal(  path = node,    par = 'pf_fin_gap',
                                unit = "m"                              )
        pfFinAngle  = GetReal(  path = node,    par = 'pf_angle',
                                unit = "rad"                            )

        h           = sinkSize[2]   - sinkHightSize
        radius      = pfPinDiameter - 2 * ( h   *  math.tan(pfFinAngle) )
        if radius <= 0:
            raise HeatSinkError, "The draft angle value is not valid."

    #---------------------------------------------------------------------
    # Generating the CAD
    #---------------------------------------------------------------------

    if not fileName:
        prefix  = string.replace(   sinkType,   " ",        ""          )
        suffix  = ".x_t"
        indx    = acuUtil.getMaxFileInd(        prefix,     suffix      )
        if indx == -1: indx = 1
        else:   indx += 1
        fileName= prefix + str(indx) + suffix

    print "Generating CAD, under file: ", fileName

    ExecExtFunc(                    _funcName   = "HeatSinkCAD.heatSinkModel",
                                    _imports    = "HeatSinkCAD",
                                    fileName    = fileName,
                                    tunnelDims  = tunlSize,
                                    boardDims   = boardSize,
                                    chipDims    = chipSize,
                                    sinkBaseDims= sinkBaseDims,
                                    sinkDims    = sinkDims,
                                    ccXFinWidth = ccXFinWidth,
                                    ccXFinGap   = ccXFinGap,
                                    ccYFinWidth = ccYFinWidth,
                                    ccYFinGap   = ccYFinGap,
                                    exYFinWidth = exYFinWidth,
                                    exYFinGap   = exYFinGap,
                                    dcFinWidth  = dcFinWidth,
                                    dcFinGap    = dcFinGap,
                                    pfPinDiameter=pfPinDiameter,
                                    pfFinGap    = pfFinGap,
                                    pfArngmnt   = pfArngmnt,
                                    pfFinAngle  = pfFinAngle,
                                    sinkType    = sinkType
                )
    
    #---------------------------------------------------------------------
    # Importing the CAD in automatically
    #---------------------------------------------------------------------

    ToolImportGeom(                 args        = {'fileName':fileName},
                                    dialog      = False                 )

    #---------------------------------------------------------------------
    # Group the Volumes and Surfaces
    #---------------------------------------------------------------------

    print "Grouping the Volumes and Surfaces"
    usrGroupHeatSinkVolumes(						)
    usrGroupHeatSinkSurfaces(						)

    #---------------------------------------------------------------------
    # Remove empty model and redraw data tree to show the grouping result
    #---------------------------------------------------------------------

    geomChild   = GetChildren(                  modelSrf                )
    for child in geomChild:
        if IsSrfEmpty( child ):
	    PurgeSrf(                           child                   )

    geomChild   = GetChildren(                  modelVol                )
    for child in geomChild:
        if IsVolEmpty( child ):
	    PurgeVol(                           child                   )

    TreeRedraw(                                                         )

    #---------------------------------------------------------------------
    # Reset the display
    #---------------------------------------------------------------------

    usrSetHeatSinkDisplays(						)

    if not dialog and sendState:
        sendState(                              'finished'              )

#===========================================================================
# groupVolModel -  Group the volumes based on the part name.
#===========================================================================

def usrGroupHeatSinkVolumes():

    GroupGeom(  groupType = "PART_NAME",        entityType = "VOLUME"   )

#===========================================================================
# groupSrfModel - Group the Surfaces
#===========================================================================

def usrGroupHeatSinkSurfaces():

    tol		    = 1.0e-4

    #--------------------------------------------------------------------
    # Get the CAD model bndBox
    #--------------------------------------------------------------------

    nodeDB	    = ROOT + RS + 'main' + RS + 'CAD_DATA'
    xMin            = GetReal(      nodeDB,     'xMin',         0       )
    yMin            = GetReal(      nodeDB,     'yMin',         0       )
    zMin            = GetReal(      nodeDB,     'zMin',         0       )
    xMax            = GetReal(      nodeDB,     'xMax',         0       )
    yMax            = GetReal(      nodeDB,     'yMax',         0       )
    zMax            = GetReal(      nodeDB,     'zMax',         0       )

    xSize           = xMax - xMin
    xMin            += tol * xSize
    xMax            -= tol * xSize

    ySize           = yMax - yMin
    yMin            += tol * ySize
    yMax            -= tol * ySize

    zSize           = zMax - zMin
    zMin            += tol * zSize
    zMax            -= tol * zSize

    sibFaceMap      = GetDic(       nodeDB,     'sibFaceMap',   {}	)

    #--------------------------------------------------------------------
    # Get the CAD model surfaces data and group them
    #--------------------------------------------------------------------

    geomChild       = GetChildren(              geomSrf                 )
    geomChildPath   = geomSrf + RS

    pNameDic        = {}
    inflowModel     = []
    outflowModel    = []
    side1Model      = []
    side2Model      = []
    bottomModel     = []
    topModel        = []
    wallModel       = []
    boardChipModel  = []
    boardModel      = []
    chipModel       = []
    heatSinkChipModel=[]
    heatSinkModel   = []
    
    for child in geomChild:
        childAttr   = string.split(	        child,          ":"	)
	regSet	    = childAttr[2]

	if regSet in pNameDic:
            pName   = pNameDic[ regSet ]
        else:
            pName   = GetRegPartName(	        regSet			)
            pNameDic[ regSet ]  = pName
	
        if pName == "tunnel":

            #-------------------------------------------------------------
            # Group the surfaces with parent volume "Tunnel"
            #-------------------------------------------------------------

            ctr     = GetArray( geomChildPath + child,  'center'        )

            if ctr[0] <= xMin:
                inflowModel.append(             child                   )
                
            elif ctr[0] >= xMax:
                outflowModel.append(            child                   )

            elif ctr[1] <= yMin:
                side1Model.append(              child                   )

            elif ctr[1] >= yMax:
                side2Model.append(              child                   )

            elif ctr[2] <= zMin:
                bottomModel.append(             child                   )

            elif ctr[2] >= zMax:
                topModel.append(                child                   )

            else:
                wallModel.append(               child                   )

        elif pName == "board":

            #-------------------------------------------------------------
            # Group the surfaces with parent volume "Board"
            #-------------------------------------------------------------

            sibPartName     = None
            if sibFaceMap[ child ] != child:
                sibSet      = sibFaceMap[ child ]
                sibAttr	    = string.split(	sibSet,	":"		)
                sibRegSet   = sibAttr[2]

                if sibRegSet in pNameDic:
                    sibPartName = pNameDic[ sibRegSet ]
                else:
                    sibPartName = GetRegPartName(       sibRegSet	)
                    pNameDic[ sibRegSet ] = sibPartName

            if sibPartName == "chip":
                boardChipModel.append(          child                   )
                
            else:
                boardModel.append(              child                   )

        elif pName == "chip":
            chipModel.append(                   child                   )


        elif pName == "heat sink":

            #-------------------------------------------------------------
            # Group the surfaces with parent volume "Heat Sink"
            #-------------------------------------------------------------

            sibPartName     = None
            if sibFaceMap[ child ] != child:
                sibSet      = sibFaceMap[ child ]
                sibAttr	    = string.split(	sibSet,	":"		)
                sibRegSet   = sibAttr[2]

                if sibRegSet in pNameDic:
                    sibPartName = pNameDic[ sibRegSet ]
                else:
                    sibPartName = GetRegPartName(       sibRegSet	)
                    pNameDic[ sibRegSet ] = sibPartName

            if sibPartName == "chip":
                heatSinkChipModel.append(       child                   )

            else:
                heatSinkModel.append(           child                   )

        else:
            raise HeatSinkError, "The parent volume %s is not valid."%pName

    MoveGeomSrf(                        geom    = inflowModel,
                                        model   = "inflow",
                                        new     = True	                )

    MoveGeomSrf(                        geom    = outflowModel,
                                        model   = "outflow",
                                        new     = True                  )

    MoveGeomSrf(                        geom    = side1Model,
                                        model   = "side 1",
                                        new     = True                  )

    MoveGeomSrf(                        geom    = side2Model,
                                        model   = "side 2",
                                        new     = True                  )

    MoveGeomSrf(                        geom    = bottomModel,
                                        model   = "bottom",
                                        new     = True                  )

    MoveGeomSrf(                        geom    = topModel,
                                        model   = "top",
                                        new     = True                  )

    MoveGeomSrf(                        geom    = wallModel,
                                        model   = "wall",
                                        new     = True                  )

    MoveGeomSrf(                        geom    = boardChipModel,
                                        model   = "board/chip",
                                        new     = True                  )

    MoveGeomSrf(                        geom    = boardModel,
                                        model   = "board",
                                        new     = True                  )

    MoveGeomSrf(                        geom    = chipModel,
                                        model   = "chip",
                                        new     = True                  )

    MoveGeomSrf(                        geom    = heatSinkChipModel,
                                        model   = "heat sink/chip",
                                        new     = True                  )

    MoveGeomSrf(                        geom    = heatSinkModel,
                                        model   = "heat sink",
                                        new     = True                  )

#===========================================================================
# Set the display type
#===========================================================================

def usrSetHeatSinkDisplays():

    #---------------------------------------------------------------------
    # Set the Display of all volumes to off
    #---------------------------------------------------------------------

    volChild    = GetChildren(                  modelVol                )
    for child in volChild:
        VolDisplay(     model   = child,        display = False         )

    #---------------------------------------------------------------------
    # Set the Display of surfaces
    #---------------------------------------------------------------------

    SrfDisplay(         model   = "inflow",     display_type = "outline",
                        color   = [0, 0, 1.0]                           )
    SrfDisplay(         model   = "outflow",    display_type = "outline",
                        color   = [0, 0, 1.0]                           )
    SrfDisplay(         model   = "side 1",     display_type = "outline",
                        color   = [0, 0, 1.0]                           )
    SrfDisplay(         model   = "side 2",     display_type = "outline",
                        color   = [0, 0, 1.0]                           )
    SrfDisplay(         model   = "bottom",     display_type = "outline",
                        color   = [0, 0, 1.0]                           )
    SrfDisplay(         model   = "top",        display_type = "outline",
                        color   = [0, 0, 1.0]                           )
    SrfDisplay(         model   = "wall",       display_type = "outline",
                        color   = [0, 0, 1.0],  display      = False    )

    SrfDisplay(         model   = "board/chip", display_type = "solid",
                        color   = [0.5, 0.25, 0.0]                      )
    SrfDisplay(         model   = "board",      display_type = "solid",
                        color   = [0.5, 0.25, 0.0]                      )

    SrfDisplay(         model   = "chip",       display_type = "solid",
                        color   = [0.5, 0.5, 0.5]                       )

    SrfDisplay(         model   = "heat sink/chip",
                        display_type = "solid",
                        color   = [1.0, 0.5, 0.0]                       )
    SrfDisplay(         model   = "heat sink",  display_type = "solid",
                        color   = [1.0, 0.5, 0.0]                       )

#===========================================================================
# usrBuildHeatSinkImages -  Save the created CAD image
#===========================================================================

def usrBuildHeatSinkImages( 	dialog  = False,	tail    = False,
				args    = None,		sendState= None,
				win     = None,		name    = None,
				fileName= None
                        ):

    if not dialog and sendState:
        sendState(                              'started'               )

    StoreCamera(                                'heatSinkImg'           )

    SetFootNote(                                text = ""               )

    #---------------------------------------------------------------------
    # Reset the display
    #---------------------------------------------------------------------

    usrSetHeatSinkDisplays(						)

    #---------------------------------------------------------------------
    # Create four images front.png, top.png, side.png, isometric.png
    #---------------------------------------------------------------------

    VisFit(                                                             )

    print "Create image file: Images/front.png"
    VisAlignDir(        "+X"                                            )
    VisRotate(          "+X",                   90                      )
    VisZoom(                                    -0.88                   )
    SaveImage(          fileName= "front.png",  dirName     = "Images"  )

    print "Create image file: Images/top.png"
    VisAlignDir(        "-Z"                                            )
    VisRotate(          "-Z",                   90                      )
    VisZoom(                                    -0.5                    )
    SaveImage(          fileName= "top.png",    dirName     = "Images"  )

    print "Create image file: Images/side.png"
    VisAlignDir(        "+Y"                                            )
    VisZoom(                                    -0.5                    )
    SaveImage(          fileName= "side.png",   dirName     = "Images"  )

    print "Create image file: Images/isometric.png"
    VisRotate(          "+Y",                   45                      )
    VisRotate(          "-Z",                   45                      )
    VisRotate(          "-X",                   45                      )
    VisZoom(                                    -0.2                    )
    SaveImage(          fileName= "isometric.png",
                        dirName = "Images"                              )

    ResetFootNote(                                                      )
    RecallCamera(                               'heatSinkImg'           )

    if not dialog and sendState:
        sendState(                              'finished'              )
    
#===========================================================================
# Set the default displays
#===========================================================================

def usrOpenHeatSinkMesh( item, args ):

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'
    URL         = "heat_sink.htm"

    MenuEnum(	name	= 'Mesh density',
		tooltip	= 'Mesh density',
		whatsthis='Mesh density',
		helpURL	= URL + '#mesh_density',
		node	= node,
		par	= 'mesh_density',
                enum    = ( ('Coarse',        'coarse'     ),
                            ('Medium',        'medium'     ),
                            ('Fine',          'fine'       ),
                          )						)

    MenuFunc(	name	= 'Generate mesh',
		tooltip	= 'Generate mesh',
		whatsthis='Click this the button to automatically \n'
			  'Generate the mesh',
		helpURL	= URL + '#func',
		node	= node,
		par	= 'funcGenMesh',
		func	= usrBuildHeatSinkMesh                          )

#===========================================================================
# usrBuildHeatSinkMesh -  Set mesh sizes and generate mesh.
#===========================================================================

def usrBuildHeatSinkMesh( 	dialog  = False,	tail    = False,
				args    = None,		sendState= None,
				win     = None,		name    = None,
				fileName= None
                        ):

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'
    URL         = "heat_sink.htm"

    #---------------------------------------------------------------------
    # Get the mesh factor
    #---------------------------------------------------------------------

    meshDensity = GetEnum( node, "mesh_density", default = "coarse" )

    if meshDensity == 'coarse':
        meshFct	= 1
    elif meshDensity == 'medium':
        meshFct	= 0.7
    elif meshDensity == 'fine':
        meshFct	= 0.5

    #---------------------------------------------------------------------
    # Setup meshing parameters
    #---------------------------------------------------------------------

    sinkSize    = GetArray( path = node,        par = 'heat_sink_size',
                            unit = "m"                                  )
    heatSinkLength	= sinkSize[0] 

    sinkMeshSize	= meshFct * heatSinkLength / 16
    globalMeshSize	= 8 * sinkMeshSize
    roiUpDist		= heatSinkLength
    roiDownDist		= 10 * heatSinkLength
    wallMeshSize	= 4 * sinkMeshSize
    wallHeight0		= meshFct * 3.e-4
    curvAngle		= meshFct ** 1.5 * 20
    curvFct		= 0.1

    #---------------------------------------------------------------------
    # Set the global attributes
    #---------------------------------------------------------------------

    cmdSetGlobalMeshAttributes(		clobber		= True,
					MeshSizeType	= 'absolute_value',
					AbsMeshSize	= globalMeshSize )

    #---------------------------------------------------------------------
    # Turn off all surface/volume mesh attributes
    #---------------------------------------------------------------------

    geomChild   = GetChildren(		modelVol                	)
    for child in geomChild:
        cmdSetVolumeMeshAttributes(	name    = child,
					active  = False			)

    geomChild   = GetChildren(		modelSrf                	)
    for child in geomChild:
        cmdSetSurfaceMeshAttributes(	name    = child,
					active  = False			)

    #---------------------------------------------------------------------
    # Remove the chip
    #---------------------------------------------------------------------

    cmdSetVolumeMeshAttributes(		name		= 'chip',
					active		= True,
					MeshSizeType	= 'no_mesh'	)

    #---------------------------------------------------------------------
    # Set the "heat sink" surface
    #---------------------------------------------------------------------

    cmdSetSurfaceMeshAttributes(	name		= 'heat sink',
					active		= True,
					AbsMeshSize	= sinkMeshSize,
					CurvatureRefinementFlag = True,
					CurvatureAngle	= curvAngle,
					CurvatureMeshSizeFactor = curvFct,
					RegionOfInfluenceFlag = True,
					InfluenceType	= "DIRECTIONAL",
					InfluenceSizeFactor = 4.,
					InfluenceDirection = ((1,0,0),),
					UpstreamInfluenceDistance = roiUpDist,
					DownstreamInfluenceDistance = roiDownDist,
					InfluenceStartAngle = 15.	)


    #---------------------------------------------------------------------
    # Set the "wall" surface
    #---------------------------------------------------------------------

    cmdSetSurfaceMeshAttributes(	name            = 'wall',
					active          = True,
					AbsMeshSize	= wallMeshSize,
					BoundaryLayerFlag = True,
					BoundaryLayerSpec = 'type_2',
					FirstLayerHeight  = wallHeight0,
					NumberOfLayers    = 3,
					BoundaryLayerPropagateFlag = False )

    usrStartMeshProcess( args )

#===========================================================================
# usrStartMeshProcess - 
#===========================================================================
 
def usrStartMeshProcess( args ):

    nodeDB      = ROOT + RS + 'main'
    geomFlag    = GetBool(      nodeDB, 'geom_flag', False              )
    if not geomFlag:
        print "No geometry is loaded in the database, can't generate mesh"
        return
    meshArgs                        = {}
    meshArgs['Export ams file']     = True
    meshArgs['Launch AcuMeshSim']   = True
    meshArgs['Reduced mesh flag']   = True
    meshArgs['Mesh type']           = 'ACUMESH_VOL_MESH'

    ToolGenMesh(        dialog      = False,    tail	= False,
                        args        = meshArgs, modal	= True,
                        sendState   = None                              )

    ToolImportMesh(     dialog      = False,    sendState= None         )

#===========================================================================
# Open problem panel
#===========================================================================

def usrOpenHeatSinkProblem( item, args ):

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'
    URL         = "heat_sink.htm"

    advancedFeat=   GetBool(  path  = node, par = 'advanced_features')

    MenuBool(   name	= 'Advanced features',
                tooltip	= 'Display advanced features',
		whatsthis='Display advanced features',
		helpURL	= URL + '#advanced_features',
		node	= node,
		par	= 'advanced_features',
		redraw	= True,
		default	= False						)

    MenuReal(name	= 'Package Theta JC',
             tooltip	= 'Package Theta JC',
             whatsthis  ='Theta JC for chip',
             node	= node,
             par	= 'theta_jc',
             unitCat    = 'unitless',
             cond       = 'par > 0',
             )
    
    MenuReal(name	= 'Package Theta JB',
             tooltip	= 'Package Theta JB',
             whatsthis  ='Theta JC for board',
             node	= node,
             par	= 'theta_jb',
             unitCat    = 'unitless',
             cond       = 'par > 0',
             )    

    MenuRef(name    = 'Fluid material model',
            tooltip = 'Name of the fluid material model.',
            whatsthis='Material model for the working fluid.',
            node    = node,
            par     = 'fluid_material_model',
            ref     = ( ROOT + RS + 'MATERIAL_MODEL',
                        'type',
                        'par1 == "fluid"' 
                        )
            )

#FS    MenuRef(name    = 'Board material model',
#FS	    tooltip = 'Name of the board material model.',
#FS	    whatsthis='Material model for the board.',
#FS	    node    = node,
#FS	    par     = 'board_material_model',
#FS	    ref     = ( ROOT + RS + 'MATERIAL_MODEL',
#FS			'type',
#FS			'par1 == "solid"' 
#FS			)
#FS	    )

    MenuRef(name    = 'Heat sink material model',
            tooltip = 'Name of the heat sink material model.',
            whatsthis='Material model for the heat sink.',
            node    = node,
            par     = 'sink_material_model',
            ref     = ( ROOT + RS + 'MATERIAL_MODEL',
                        'type',
                        'par1 == "solid"' 
                        )
            )

    if advancedFeat:
        MenuReal(	name	= 'Copper conductivity',
                 	tooltip	= 'Thermal conductivity copper',
                 	whatsthis = 'Thermal conductivity copper',
                 	node	= node,
                 	par	= 'k_cu',
                 	unitCat	= 'conductivity',
                 	cond	= 'par > 0',
		 	redraw	= True,
                 	)

        MenuReal(	name	= 'Dielectric conductivity',
                 	tooltip	= 'Thermal Conductivity of dielectric',
                 	whatsthis = 'Thermal Conductivity of dielectric material',
                 	node	= node,
                 	par	= 'k_die',
                 	unitCat = 'conductivity',
                 	cond    = 'par > 0',
		 	redraw  = True,
                 	)

        MenuReal(	name	= 'Thickness of 1 oz Copper',
                 	tooltip	= 'Thickness of 1 oz/ft^2 Copper sheet',
			whatsthis = 'Thickness of 1 oz/ft^2 Copper sheet',
			node	= node,
			par	= 't_1oz_cu',
			unitCat = 'length',
			cond    = 'par > 0',
			redraw  = True,
			)

    MenuArray(	name	= 'Board layer parameters',
		tooltip	= 'Array of:  copper thickness ounces, Percent Copper',
		whatsthis = 'Physical thickness and percentage Copper',
		node	= node,
		aryInfo   = ('multi_column', '(1+;2)', '(d,2)' ),
		unitCat   = None,
#FS		colHead   = 'Copper Thickness:Copper Coverage',
		colHead   = 'Thickness [Ounces of Copper]:Percent Copper Coverage',
		aryType   = 'multi_column',                    
		cols      = (2,2),
		rows      = (1, 1000000 ),
		par       = 'board_layer_par',
		redraw    = True,
		)

    cond	= usrGetBoardConductivity(				)

    MenuInfo(  name     = 'Board in-plane conductivity',
	       tooltip	 = 'in-plane conductivity',
	       whatsthis ='in-plane conductivity',
	       helpURL	 = URL + '#in-plane cond',
	       value   = '%g W/m-k' % cond[0]
	       )

    MenuInfo(  name    = 'Board normal conductivity',
	       tooltip	= 'normal conductivity',
	       whatsthis='normal conductivity',
	       helpURL	= URL + '#normal cond',
	       value   = '%g W/m-k' % cond[2]
	       )


    MenuArray(  name    = 'Solution cases',
                tooltip = 'Solution cases: Air Speed, Air Temp, Power',
                whatsthis='Solution cases: Air Speed (m/s), Air Temp (K), Power(W)',
                node    = node,
                aryInfo = ('multi_column', '(1+;3)', '(d,3)' ),
                unitCat = 'velocity:temperature:heat_rate',
                colHead = 'Air Speed:Temperature:Chip Power',
                aryType = 'multi_column',                    
                cols    = (3,3),
                rows    = ( 1, 1000000 ),
                par     = 'solution_cases',
                redraw  = True,
                )

    MenuFunc(	name	= 'Generate input file',
		tooltip	= 'Generate input file',
		whatsthis='Click this the button to automatically \n'
			  'set the problem parameters and write input',
		helpURL	= URL + '#func',
		node	= node,
		par	= 'funcGenInput',
		func	= usrBuildHeatSinkInput
                )
    
#===========================================================================
# usrBuildHeatSinkInput -  Set the B.C.s, materials, and solver settings
#===========================================================================

def usrBuildHeatSinkInput( 	dialog = False,		tail = False,
				args = None,		sendState = None,
				win = None,		name = None,
				fileName = None				):

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'
    URL         = "heat_sink.htm"

    nodeDB      = ROOT + RS + 'main'
    geomFlag    = GetBool(      nodeDB, 'geom_flag', False              )
    if not geomFlag:
        print "No geometry is loaded in the database, can't compute heat flux"
        return
    meshFlag    = GetBool(      nodeDB, 'mesh_flag', False              )
    if not meshFlag:
        print "No mesh is loaded in the database, can't write input file"
        return

    #---------------------------------------------------------------------
    # Global settings
    #---------------------------------------------------------------------
    
    cmdSetProblemDescription(       title        =  'Heat Sink Model',
                                    sub_title    =  'Steady RANS simulation',
                                    temperature  =  'advective_diffusive',
                                    turbulence   =  'spalart_allmaras'
                                    )

    #---------------------------------------------------------------------
    # Build the board conductivity
    #---------------------------------------------------------------------
    
    cond	= usrGetBoardConductivity( )

    cmdSetConductivityModel(	name            = 'Board',
				type            = 'constant_anisotropic', 
				anisotropic_conductivity= cond,
				clobber         = True
                                )

    #---------------------------------------------------------------------
    # Element sets
    #---------------------------------------------------------------------
    
    tmp = GetRef( node,'fluid_material_model' )    
    cmdSetElementSets(              name          = 'tunnel',
                                    medium        = 'fluid',
                                    material_model= tmp
                                    ) 
#FS    tmp = GetRef( node,'board_material_model' )
    cmdSetElementSets(              name          = 'board',
                                    medium        = 'solid',
                                    material_model= 'Board'
                                    )
    tmp = GetRef( node,'sink_material_model' )
    cmdSetElementSets(              name          = 'heat sink',
                                    medium        = 'solid',
                                    material_model= tmp
                                    )     
    cmdSetElementSets(              name          = 'chip',
                                    active        = False
                                    )   

    #---------------------------------------------------------------------
    # Multiplier functions
    #---------------------------------------------------------------------
    
    solnArray = GetArray( node,'solution_cases',default=( 5, 300, 50 ) )

    if len(solnArray.shape)==1:
        tmp       = numarray.zeros( (1,3),'d' )
        tmp[0,:]  = solnArray
        solnArray = tmp
    
    nCases,tmp= solnArray.shape
    sortedIndices = numarray.argsort(solnArray[:,0])
    inletVel  = solnArray[sortedIndices,0]
    inletTemp = solnArray[sortedIndices,1]
    chipPower = solnArray[sortedIndices,2]

    data      = numarray.ones( (nCases,2) ,'d')
    data[:,0] = numarray.reshape(numarray.arange( nCases ) + 1,(nCases,1))[:,0]*data[:,0]

    data[:,1] = inletVel
    cmdSetMultiplierFunction(       name          = 'Velocity Multiplier',
                                    type          = 'piecewise_linear',
                                    curve_fit_values = (data),
                                    curve_fit_variable = 'time_step',
                                    )
    data[:,1] = inletTemp
    cmdSetMultiplierFunction(       name          = 'Temperature Multiplier',
                                    type          = 'piecewise_linear',
                                    curve_fit_values = (data),
                                    curve_fit_variable = 'time_step',
                                    )    
    data[:,1] = chipPower
    cmdSetMultiplierFunction(       name          = 'Heat Flux Multiplier',
                                    type          = 'piecewise_linear',
                                    curve_fit_values = (data),
                                    curve_fit_variable = 'time_step',
                                    )
    
    theta_jc	= GetReal(		node,		"theta_jc"	)
    theta_jb	= GetReal(		node,		"theta_jb"	)

    cmdSetMultiplierFunction(       name          = 'Heat_QC',
                                    type          = 'user_function',
				    user_function = 'usrHeatQc',
				    user_values   = ( theta_jc, theta_jb ),
				    evaluation    = 'once_per_solution_update',
				    filter        = 'mic',
				    dependencies  = ('Heat Flux Multiplier')
                                    )
    
    cmdSetMultiplierFunction(       name          = 'Heat_QB',
                                    type          = 'user_function',
				    user_function = 'usrHeatQb',
				    evaluation    = 'once_per_solution_update',
				    filter        = 'mic',
				    dependencies  = ('Heat Flux Multiplier',
				    		     'Heat_QC')
                                    )
    
    #---------------------------------------------------------------------
    # Boundary conditions
    #---------------------------------------------------------------------
    
    nodeSrf = modelSrf+RS+"board/chip"
    geomSets = GetList( nodeSrf, 'geomSets', [] )
    bcArea = 0
    for geomSet in geomSets:
        (nSrfs,area,ctr,nrm,dir1,dir2,bBox) = MnuInfoSrf(geom = geomSet)
        bcArea = bcArea+area
    if bcArea == 0:
        print "Zero area in board/chip group"
        return
        
    nodeSrf = modelSrf+RS+"heat sink/chip"
    geomSets = GetList( nodeSrf, 'geomSets', [] )
    hcArea = 0
    for geomSet in geomSets:
        (nSrfs,area,ctr,nrm,dir1,dir2,bBox) = MnuInfoSrf(geom = geomSet)
        hcArea = hcArea+area
    if hcArea == 0:
        print "Zero area in heat sink/chip group"
        return

    geomChild   = GetChildren(                  modelSrf                )
    for child in geomChild:
        cmdSetSimpleBoundaryCondition(    name        = child,
                                          active      = True,
                                          type        = 'wall'
                                          )
        cmdSetSurfaceOutput(              name        = child,
                                          active      = True,
                                          )
    
    srfName = 'board/chip'
    cmdSetSimpleBoundaryCondition(  name                          = srfName,
                                    type                          = 'wall',
                                    heat_flux                     = 0.5/bcArea,
                                    heat_flux_multiplier_function = 'Heat_QB'
                                    )
    nodeCbc = modelSrf + RS + srfName + RS + 'SIMPLE_BOUNDARY_CONDITION'
    PutBool( path=nodeCbc, par = 'advanced_features', value=True)
    
    srfName = 'heat sink/chip'
    cmdSetSimpleBoundaryCondition(  name                          = srfName,
                                    type                          = 'wall',
                                    heat_flux                     = 0.5/hcArea,
                                    heat_flux_multiplier_function = 'Heat_QC'
                                    )
    nodeCbc = modelSrf + RS + srfName + RS + 'SIMPLE_BOUNDARY_CONDITION'
    PutBool( path=nodeCbc, par = 'advanced_features', value=True)    

    srfName = 'inflow'
    cmdSetSimpleBoundaryCondition(  name          = srfName,
                                    type          = 'inflow',
                                    inflow_type   = 'average_velocity',
                                    average_velocity = 1.0,
                                    average_velocity_multiplier_function = 'Velocity Multiplier',
                                    temperature   = 1.0,
                                    temperature_multiplier_function = 'Temperature Multiplier'
                                    )
    nodeCbc = modelSrf + RS + srfName + RS + 'SIMPLE_BOUNDARY_CONDITION'
    PutBool( path=nodeCbc, par = 'advanced_features', value=True)

    cmdSetSimpleBoundaryCondition(  name          = 'outflow',
                                    type          = 'outflow',
                                    )

    for surface in ('side 1','side 2','top','bottom'):
        cmdSetSimpleBoundaryCondition(  name          = surface,
                                        type          = 'slip',
                                        )          

    #---------------------------------------------------------------------
    # Nodal data
    #---------------------------------------------------------------------
    
    cmdSetNodalInitialCondition(    x_velocity                    = inletVel[0],
                                    eddy_viscosity                = .0001,
                                    temperature                   = inletTemp[0],
                                  )
    cmdSetNodalOutput(              output_frequency              = 1,
                                    )
    cmdSetRestartOutput(            output_frequency              = 1,
                                    )    

    #---------------------------------------------------------------------
    # Solution strategy
    #---------------------------------------------------------------------
    
    cmdSetAutoSolutionStrategy(     max_time_steps                = nCases,
                                    relaxation_factor             = 0.25
                                    )
    
    cmdSetStagger(                  name                          = 'control',
				    min_stagger_iterations	  = 2,
				    max_stagger_iterations	  = 40,
				    convergence_tolerance	  = 1.e-3,
                                    staggers                      = 
					('flow','turbulence'),
                                    protect_parameters            = True
                                    )

    cmdSetStagger(                  name                          = 'temperature',
                                    equation                      = 'temperature',
				    min_stagger_iterations	  = 2,
				    max_stagger_iterations	  = 40,
                                    linear_solver_tolerance       = .001,
                                    convergence_tolerance         = .001,
                                    num_krylov_vectors            = 40,
                                    max_linear_solver_iterations  = 10000,
                                    protect_parameters            = True
                                    )

    cmdSetTimeSequence(             min_time_steps                = nCases,
                                    max_time_steps                = nCases,
                                    stagger_convergence_tolerance = 1.0e-3,
                                    min_stagger_iterations        = 1,
                                    max_stagger_iterations        = 1,
                                    stagger_lhs_update_frequency  = 1,
                                    staggers                      = 
					('control','temperature'),
                                    protect_parameters            = True
                                    )

    #---------------------------------------------------------------------
    # Start the input file specification
    #---------------------------------------------------------------------
    
    usrStartInpFileProcess( args )

#===========================================================================
# usrGetBoardConductivity - 
#===========================================================================

def usrGetBoardConductivity( ):
    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'
    URL         = "heat_sink.htm"

    k_cu        = GetReal(      node,     'k_cu'                	)
    k_die       = GetReal(      node,     'k_die'               	)
    t_1oz_cu    = GetReal(      node,     't_1oz_cu',	unit = "m"	)

    boardSize   = GetArray(     path = node,    par = 'board_size',
                                unit = "m"                             )
    if len(boardSize.shape)==2:
        boardSize  = boardSize[0,:]

    t_pcb	= boardSize[2]

    layerArray = GetArray( node,'board_layer_par',default=( 0.01, 99.0 ) )

    if len(layerArray.shape)==1:
	layerArray.shape = (1,2)
    
    nLayers	= layerArray.shape[0]
    t_cu 	= layerArray[:,0]
    C_cu  	= layerArray[:,1]

    k_sum	= 0
    t_mat	= 0
    for i in range( nLayers ):
	if t_cu[i] > 0 and C_cu[i] > 0:
	    k_sum	= k_sum \
			+ (t_cu[i] * t_1oz_cu * C_cu[i] * k_cu)/(100 * t_pcb)
	    t_mat	= t_mat + t_cu[i] * t_1oz_cu

    if t_mat > t_pcb:
        raise HeatSinkError, \
	    "Total board layers <%g> greater than board height <%g>" % \
	    ( t_mat, t_pcb )

    t_die	= (t_pcb - t_mat) / nLayers

    k_xx	=  k_sum + (nLayers-1) * t_die * k_die / t_pcb
    k_zz	=  k_die

    cond = [ k_xx, k_xx, k_zz, 0, 0, 0 ]
    
    return( cond )

#===========================================================================
# usrStartInpFileProcess - 
#===========================================================================
 
def usrStartInpFileProcess( args ):

    ToolGenInput(   dialog      = False,        args = args,
                    sendState   = None                                  )

#===========================================================================
# Open HeatSink Process : process automation
#===========================================================================

def usrOpenHeatSinkProcess( item, args ):

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'
    URL         = "heat_sink.htm"

    #---------------------------------------------------------------------
    # Define related menus
    #---------------------------------------------------------------------

    MenuStr(	name	= 'Problem name',
		tooltip	= 'Name of the problem',
		whatsthis='Specify a name for the job\n'
			'This has no impact on the run',
		helpURL	= URL + '#name',
		node	= node,
		par	= 'problem',
		default	= 'HeatSink'				        )

    MenuEnum(	name	= 'Heat sink type',
		tooltip	= 'Heat sink type',
		whatsthis='Heat sink type',
		helpURL	= URL + '#Heat_sink_type',
		node	= node,
		par	= 'heat_sink_type',
                enum    = ( ('None',        'none'          ),
                            ('Cross Cut',   'cross cut'     ),
                            ('Extrusion',   'extrusion'     ),
                            ('Diamond Cut', 'diamond cut'   ),
                            ('Pin Fin',     'pin fin'       ),
                          )                                             )

    MenuFile(	name	= 'CAD file name',
		tooltip	= 'Name of the CAD file',
		whatsthis='Name of the CAD file',
		helpURL	= URL + 'CAD.htm',
		node	= node,
		par	= 'CADFile',
		default	= 'htSink.x_t'				        )

    MenuBool(	name	= 'Generate CAD',
		tooltip	= 'Generate and import the CAD',
		whatsthis='Process the following\n'
			  '1. Start Heat Sink\n'
			  '2. Generate the CAD\n'
			  '3. Import into AcuConsole',
		helpURL	= URL + '#gnrt_cad',
		node	= node,
		par	= 'gnrtCad',
		default	= True						)

    MenuBool(	name	= 'Save images',
		tooltip	= 'Save images',
		whatsthis='Save images',
		helpURL	= URL + '#SaveImages',
		node	= node,
		par	= 'saveImgs',
		default	= True						)

    MenuBool(	name	= 'Generate mesh',
		tooltip	= 'Generate and import the Mesh',
		whatsthis='Process the following\n'
			  '1. Set the mesh parameters\n'
			  '2. Generate the mesh\n'
			  '3. Import into AcuConsole',
		helpURL	= URL + '#gnrt_mesh',
		node	= node,
		par	= 'gnrtMesh',
		default	= True						)

    MenuBool(	name	= 'Import mesh',
		tooltip	= 'Import Mesh',
		whatsthis='Import Mesh',
		helpURL	= URL + '#ImportMesh',
		node	= node,
		par	= 'importMesh',
		default	= True						)

    MenuBool(	name	= 'Generate input',
		tooltip	= 'Set problem parameters and generate input',
		whatsthis='Process the following\n'
			  '1. Set the input parameters\n'
			  '2. Build AcuSolve input file\n',
		helpURL	= URL + '#gnrt_input',
		node	= node,
		par	= 'gnrtInput',
		default	= True						)

    MenuBool(	name	= 'Launch AcuSolve',
		tooltip	= 'Launch AcuSolve',
		whatsthis='Launch AcuSolve',
		helpURL	= URL + '#LaunchAcuSolve',
		node	= node,
		par	= 'launchAcuSolve',
		default	= True						)   

    MenuBool(	name	= 'Run AcuProbe',
		tooltip	= 'Run AcuProbe',
		whatsthis='Run AcuProbe',
		helpURL	= URL + '#RunAcuProbe',
		node	= node,
		par	= 'runAcuProbe',
		default	= True						)
    
    MenuFunc(	name	= 'Start process',
		tooltip	= 'Start Process',
		whatsthis='Click this button to execute processes',
		helpURL	= URL + '#func',
		node	= node,
		par	= 'funcStartProcess',
		func	= usrStartHeatSinkProcess,
		redraw	= True,
		args	= ( item )					)

#===========================================================================
# usrStartHeatSinkProcess - Apply user specifications to start process
#===========================================================================

def usrStartHeatSinkProcess( args = None ):

    node        = ROOT + RS + 'User' + RS + 'HEAT_SINK'
    procList    = []
    
    problem     = GetStr(                   node,           'problem'   )
    cadFile     = GetFile(                  node,           'CADFile'   )
    htSinkType  = GetEnum(                  node,
                                            'heat_sink_type'            )
    gntCadFile  = {}
    gntCadFile['fileName']                  = cadFile
    gntCadFile['htSinkType']                = htSinkType

    meshArgs    = {}
    meshArgs['Export ams file']             = True
    meshArgs['Launch AcuMeshSim']           = True
    meshArgs['Reduced mesh flag']           = True
    meshArgs['Mesh type']                   = 'ACUMESH_VOL_MESH'

    solveArgs   = {}
    solveArgs['Generate AcuSolve input files']  = True
    solveArgs['Launch AcuSolve']            = True
    solveArgs['Run on remote host']         = False
    solveArgs['Restart']                    = False

    procInfo    = (#( ProcessName,          dialog,         tail,
                   # func,                  args,           
                   # parName,               depProc,        depState,
                   # fileName,              name
        
                    ('Generate CAD',        False,          False,
                     usrBuildHeatSinkCad,   { 'fileName'    : cadFile },
                     'gnrtCad',             None,           None,
                     None,                  None                        ),

                    ('Save Images',         False,          False,
                     usrBuildHeatSinkImages,None,
                     'saveImgs',            None,           None,
                     None,                  None                        ),

                    ('Generate Mesh',       False,          False,
                     ToolGenMesh,           meshArgs,
                     'gnrtMesh',            'Generate CAD', 'finished',
                     None,                  None                        ),

                    ('Import Mesh',         False,          False,
                     ToolImportMesh,        None,
                     'importMesh',          'Generate Mesh','finished',
                     None,                  None                        ),

                    ('Generate Input',      False,          False,
                     ToolGenInput,          None,
                     'gnrtInput',           'Import Mesh',  'finished',
                     problem + '.inp',      None                        ),

                    ('Launch AcuSolve',     False,          False,
                     ToolLaunchAcuSolve,    solveArgs,
                     'launchAcuSolve',      'Import Mesh',  'finished',
                     None,                  None                        ),

                    ('Run AcuProbe',        False,          False,
                     ToolRunAcuProbe,       None,
                     'runAcuProbe',         'Launch AcuSolve','started',
                     None,                  None                        ),
                )

    for process in procInfo:
        menuVal = GetBool(  node,           process[5]                  )

        if menuVal:
            prc = ProcDef(  procName        = process[0],
                            dialog          = process[1],
                            tail            = process[2],
                            func            = process[3],
                            name            = process[9],
                            fileName        = process[8],
                            args            = process[4],
                            depProc         = process[6],
                            depState        = process[7]                )

            procList.append(                prc                         )

    ProcStart(              problem         = problem,
                            dir             = ".",
                            procs           = procList                  )

#===========================================================================
# usrBatch - User batch function
#===========================================================================
 
def usrBatch(	importPars	= False,	
		buildCad	= False,
		buildImages	= False,	
		buildMesh	= False,
		buildInput	= False,
                exit            = True
            ):

    if importPars:
        node    = ROOT + RS + 'User' + RS + 'HEAT_SINK'
        print 'Reading "%s" par parameters and store into data base ...' %importPars
        
	ReadPars(   fileName    = importPars,       node    = node,
                    parMap      = parMap,           clobber = True      )

    if buildCad:
	usrBuildHeatSinkCad(                                            )

    if buildImages:
	usrBuildHeatSinkImages(                                         )

    if buildMesh:
	usrBuildHeatSinkMesh(                                           )

    if buildInput:
	usrBuildHeatSinkInput(                                          )

    if exit:
        CloseDb(                                                        )
        Exit(                                                           )

#===========================================================================
# Set the parent entry
#===========================================================================

CAE	= TreeItem(	parent	= root,
			name	= 'Automation',	
			tooltip	= 'CAE Automation',
			whatsthis = 'This contains AcuSolve '
                                    'user custom panel',
			helpURL	= 'main.htm#example',
			sort	= FALSE,
			popup	= ()
                    )

#===========================================================================
# Set the tree entry
#===========================================================================

item	= TreeItem(	parent	= CAE,	
			name	= 'Heat Sink',	
			tooltip	= 'Define the problem',
			whatsthis = 'Open a panel to define the problem\n'
				    'and equations to be solved\n',
			helpURL	= 'main.htm#problem description',
			sort	= FALSE,
			popup	=  (( 'Open', usrOpenHeatSink ),),
			click2	= 'Open',
		    )

#===========================================================================
# Initialize some material models
#===========================================================================

nodeMatModel    = ROOT + RS + 'MATERIAL_MODEL'

#---------------------------------------------------------------------------
# Board
#---------------------------------------------------------------------------

cmdSetDensityModel(         name            = 'Board',
			    type            = 'constant',
			    density         = 8920,
			    clobber         = False
		)
cmdSetSpecificHeatModel(    name            = 'Board',
			    type            = 'constant',
			    specific_heat   = 385,
			    latent_heat_type= 'none',
			    clobber         = False
		)
cmdSetConductivityModel(    name            = 'Board',
			    type            = 'constant', 
			    conductivity    = 400,
			    turbulent_prandtl_number= 0.91,
			    clobber         = False
		)
cmdSetMaterialModel(        name            = 'Board',
			    medium          = 'solid',
			    clobber         = False
		)
nodeMat     = nodeMatModel + RS + 'Board'
PutTab(     nodeMat,        'tab',          'density',	False	)
PutTab(     nodeMat,        'tab_diffusivity','1',          False	)

#---------------------------------------------------------------------------
# 'Copper'
#---------------------------------------------------------------------------

cmdSetDensityModel(         name            = 'Copper',
			    type            = 'constant',
			    density         = 8920,
			    clobber         = False
		)
cmdSetSpecificHeatModel(    name            = 'Copper',
			    type            = 'constant',
			    specific_heat   = 385,
			    latent_heat_type= 'none',
			    clobber         = False
		)
cmdSetConductivityModel(    name            = 'Copper',
			    type            = 'constant', 
			    conductivity    = 400,
			    turbulent_prandtl_number= 0.91,
			    clobber         = False
		)
cmdSetMaterialModel(        name            = 'Copper',
			    medium          = 'solid',
			    clobber         = False
		)
nodeMat     = nodeMatModel + RS + 'Copper'
PutTab(     nodeMat,        'tab',          'density',	False	)
PutTab(     nodeMat,        'tab_diffusivity','1',          False	)

#---------------------------------------------------------------------------
# 'Air @ sea level'
#---------------------------------------------------------------------------

cmdSetDensityModel(         name            = 'Air @ sea level',
			    type            = 'constant',
			    density         = 1.225,
			    clobber         = False
		)
cmdSetSpecificHeatModel(    name            = 'Air @ sea level',
			    type            = 'constant',
			    specific_heat   = 1005,
			    latent_heat_type= 'none',
			    clobber         = False
		)
cmdSetViscosityModel(       name            = 'Air @ sea level',
			    type            = 'constant',
			    viscosity       = 1.781e-5,
			    clobber         = False
		)
cmdSetConductivityModel(    name            = 'Air @ sea level',
			    type            = 'constant',
			    conductivity    = 0.02521,
			    clobber         = False
		)
cmdSetMaterialModel(        name            = 'Air @ sea level',
			    medium          = 'fluid',
			    clobber         = False
		)
nodeMat     = nodeMatModel + RS + 'Air @ sea level'
PutTab(     nodeMat,        'tab',          'density',	False	)
PutTab(     nodeMat,        'tab_diffusivity','1',          False	)

#---------------------------------------------------------------------------
# 'Air @ 5,000 ft'
#---------------------------------------------------------------------------

cmdSetDensityModel(         name            = 'Air @ 5,000 ft',
			    type            = 'constant',
			    density         = 1.055,
			    clobber         = False
		)
cmdSetSpecificHeatModel(    name            = 'Air @ 5,000 ft',
			    type            = 'constant',
			    specific_heat   = 1009,
			    latent_heat_type= 'none',
			    clobber         = False
		)
cmdSetViscosityModel(       name            = 'Air @ 5,000 ft',
			    type            = 'constant',
			    viscosity       = 1.741e-5,
			    clobber         = False
		)
cmdSetConductivityModel(    name            = 'Air @ 5,000 ft',
			    type            = 'constant',
			    conductivity    = 0.029,
			    clobber         = False
		)
cmdSetMaterialModel(        name            = 'Air @ 5,000 ft',
			    medium          = 'fluid',
			    clobber         = False
		)
nodeMat     = nodeMatModel + RS + 'Air @ 5,000 ft'
PutTab(     nodeMat,        'tab',          'density',	False	)
PutTab(     nodeMat,        'tab_diffusivity','1',          False	)

#---------------------------------------------------------------------------
# Air @ 10,000 ft
#---------------------------------------------------------------------------

cmdSetDensityModel(         name            = 'Air @ 10,000 ft',
			    type            = 'constant',
			    density         = 0.905,
			    clobber         = False
		)
cmdSetSpecificHeatModel(    name            = 'Air @ 10,000 ft',
			    type            = 'constant',
			    specific_heat   = 1012,
			    latent_heat_type= 'none',
			    clobber         = False
		)
cmdSetViscosityModel(       name            = 'Air @ 10,000 ft',
			    type            = 'constant',
			    viscosity       = 1.692e-5,
			    clobber         = False
		)
cmdSetConductivityModel(    name            = 'Air @ 10,000 ft',
			    type            = 'constant',
			    conductivity    = 0.032,
			    clobber         = False
		)
cmdSetMaterialModel(        name            = 'Air @ 10,000 ft',
			    medium          = 'fluid',
			    clobber         = False
		)
nodeMat     = nodeMatModel + RS + 'Air @ 10,000 ft'
PutTab(     nodeMat,        'tab',          'density',	False	)
PutTab(     nodeMat,        'tab_diffusivity','1',          False	)

#===========================================================================
# Initialize
#===========================================================================

node = ROOT + RS + 'User' + RS + 'HEAT_SINK'

PutArray(	node,	"tunnel_size",		( 304,  152,    152 ),
		unit = "mm",                 	clobber = False         )
PutArray(	node,	"board_size",           ( 76.2, 115.4,  1.6 ),
		unit = "mm",                 	clobber = False         )
PutArray(	node,	"chip_size",            ( 12,   12,     1 ),
		unit = "mm",                 	clobber = False         )
PutArray(	node,	"heat_sink_size",       ( 25.4, 25.4,   10 ),
		unit = "mm",                 	clobber = False         )
PutReal(	node,	"heat_sink_base_height",2,
		unit = "mm",                 	clobber = False         )

PutEnum(	node,	"heat_sink_type",	"cross cut",
						clobber = False		)

#----- Cross Cut variables
PutEnum(	node,	"resolve",	        "number_of_fins",
						clobber = False		)
PutReal(	node,	"fin_x_width",          1,
		unit = "mm",                 	clobber = False         )
PutReal(	node,	"fin_x_gap",            1.5,
		unit = "mm",                 	clobber = False         )
PutReal(	node,	"fin_y_width",          1,
		unit = "mm",                 	clobber = False         )
PutReal(	node,	"fin_y_gap",            1.5,
		unit = "mm",                 	clobber = False         )

calCrossCutResolve(                                                     )

#----- Extrusion variables

PutEnum(	node,	"ex_resolve",	        "number_of_fins",
						clobber = False		)
PutReal(	node,	"ex_fin_y_width",       1,
		unit = "mm",                 	clobber = False         )
PutReal(	node,	"ex_fin_y_gap",         1.5,
		unit = "mm",                 	clobber = False         )

calExtrusionResolve(                                                    )

#----- Diamond Cut variables

PutReal(	node,	"dc_fin_width",         1.5,
		unit = "mm",                 	clobber = False         )
PutReal(	node,	"dc_fin_gap",           1.5,
		unit = "mm",                 	clobber = False         )
PutInt(	        node,	"dc_fin_num",           61,
                                                clobber = False         )

#----- Pin Fin variables

PutEnum(	node,	"pf_arrangement",	"inLine",
						clobber = False		)
PutReal(	node,	"pf_pin_diameter",      1.5,
		unit = "mm",                 	clobber = False         )
PutReal(	node,	"pf_fin_gap",           1.5,
		unit = "mm",                 	clobber = False         )
PutReal(	node,	"pf_angle",             0,
		unit = "deg",                   clobber = False         )
PutInt(	        node,	"pf_fin_num",           64,
                                                clobber = False         )

#----- Default mesh

PutEnum(	node,	"mesh_density",		"coarse",
						clobber = False		)

PutRef(	        node,	"fluid_material_model", "Air",
                                                clobber = False         )

PutRef(	        node,	"board_material_model", "Aluminum",
                                                clobber = False         )

PutRef(	        node,	"sink_material_model",  "Copper",
                                                clobber = False         )

PutReal(	node,	"theta_jc",             3,
                                                clobber = False         )

PutReal(	node,	"theta_jb",             1,
                                                clobber = False         )
#----- Default mesh

PutBool(	node,	"advanced_features",		False           )

#----- Default Board Parameters

PutReal(	node,	"k_cu",                 380,
                                                clobber = False         )

PutReal(	node,	"k_die",                0.2,
                                                clobber = False         )

PutReal(	node,	"t_1oz_cu",             0.0014,
                unit = "inch",			clobber = False         )

PutArray(	node,	"board_layer_par",     (0.0014,99.0),
                                                clobber = False         )

#----- Solution cases

PutArray(	node,	"solution_cases",	( 5, 300, 50 ),
                                                clobber = False         )

#===========================================================================
# Initialize
#===========================================================================

parMap  = (
    (   'array[0]',     'tunnel_length',        'tunnel_size'       ),
    (   'array[1]',     'tunnel_width',         'tunnel_size'       ),
    (   'array[2]',     'tunnel_height',        'tunnel_size'       ),
    (   'array[0]',     'board_length',         'board_size'        ),
    (   'array[1]',     'board_width',          'board_size'        ),
    (   'array[2]',     'board_height',         'board_size'        ),
    (   'array[0]',     'chip_length',          'chip_size'         ),
    (   'array[1]',     'chip_width',           'chip_size'         ),
    (   'array[2]',     'chip_height',          'chip_size'         ),
    (   'array[0]',     'sink_length',          'heat_sink_size'    ),
    (   'array[1]',     'sink_width',           'heat_sink_size'    ),
    (   'array[2]',     'sink_height',          'heat_sink_size'    ),
    (   'real',         'base_height',          'heat_sink_base_height'),
    (   'enum',         'sink_type',            'heat_sink_type'    ),
    (   'real',         'cc_x_fin_width',       'fin_x_width'       ),
    (   'real',         'cc_x_fin_gap',         'fin_x_gap'         ),
    (   'real',         'cc_y_fin_width',       'fin_y_width'       ),
    (   'real',         'cc_y_fin_gap',         'fin_y_gap'         ),
    (   'ref',          'base_material',        'board_material_model'),
    (   'ref',          'sink_material',        'sink_material_model'),
    (   'real',         'chip_theta_jc',        'theta_jc'          ),
    (   'real',         'chip_theta_jb',        'theta_jb'          ),
    (   'real',         'k_cu',                 'k_cu'              ),
    (   'real',         'k_die',            	'k_die'             ),
    (   'real',         't_1oz_cu',             't_1oz_cu'          ),
    (   'array[\\1,0]', 't_Cu__indx_(\d+)',	'board_layer_par'   ),         
    (	'array[\\1,1]',	'C_Cu__indx_(\d+)',	'board_layer_par'   ),
    (   'ref',          'fluid_material',       'fluid_material_model'),
    (   'array[\\1,0]', 'air_speed__indx_(\d+)','solution_cases'    ),         
    (	'array[\\1,1]',	'air_temperature__indx_(\d+)','solution_cases'),
    (	'array[\\1,2]',	'chip_power__indx_(\d+)','solution_cases'   ),
    (	'bool',		'turbulence',           'turbulence'        ),
)
