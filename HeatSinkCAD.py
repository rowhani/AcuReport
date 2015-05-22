#---------------------------------------------------------------------------
# Get the modules
#---------------------------------------------------------------------------

import  os
import  sys

from    math        	import *
from    gone.gone_model	import *

#---------------------------------------------------------------------------
# Define Constants.
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

HeatSinkCADError    = "ERROR from HeatSinkCAD Module"

#---------------------------------------------------------------------------
# heatSinkModel : Create a heat sink model
#---------------------------------------------------------------------------

def heatSinkModel(  fileName,       tunnelDims,     boardDims,
                    chipDims,
                    sinkBaseDims    = None,   #--- Heat Sink G2 ; NP ; 05/09/10 for type = None
                    sinkDims        = None,   #---                   "
                    ccXFinWidth     = None,
                    ccXFinGap       = None,
                    ccYFinWidth     = None,
                    ccYFinGap       = None,
                    exYFinWidth     = None,
                    exYFinGap       = None,                    
                    dcFinWidth      = None,
                    dcFinGap        = None,
                    pfPinDiameter   = None,
                    sinkType        = 'cross cut'
                ):
    

    
    """ Create a heat sink model.

        Argument:
            
            fileName    - Generated file name must have extension .x_t or .x_b.                                
            tunnelDims  - List of "tunnel" dimensions.
            boardDims   - List of "board" dimensions
            chipDims    - List of "chip" dimensions.
            sinkBaseDims- List of "heat sink base section" dimensions.
            sinkDims    - List of "heat sink top section" dimensions.
            ccXFinWidth - The width of each "fin" on X axis for "Cross Cut" type.
            ccXFinGap  - The gap between the "fins" on X axis for "Cross Cut" type. 
            ccYFinWidth - The width of each "fin" on Y axis for "Cross Cut" type.
            ccYFinGap   - The gap between the "fins" on Y axis for "Cross Cut" type.
            exYFinWidth - The width of each "fin" on Y axis for "Extrusion" type.
            exYFinGap   - The gap between the "fins" on Y axis for "Extrusion" type.            
            dcFinWidth  - The width of each "fin" for "Diamond Cut" type.
            dcFinGap    - The gap between the "fins" for "Diamond Cut" type.
            pfPinDiameter-The diameter of the " pins" for "Pin Fin" type.
            sinkType    - Heat sink type can be "None","Cross Cut","Extrusion","Diamond Cut" or "Pin Fin"..
            
        Output:
            
            A heat sink model file with x_t or x_b extension.
    """
        
    model1          = pk.PK_ENTITY_null
    model2          = pk.PK_ENTITY_null
    model3          = pk.PK_ENTITY_null
    model4          = pk.PK_ENTITY_null

    GO_init(                                                            )

    #--------------------------------------------------------------------
    # Check file name extension
    #--------------------------------------------------------------------
        
    absPath	    = os.path.abspath(	                str( fileName )	)
    baseName        = os.path.basename(		        absPath		)
    fileInfo        = os.path.splitext(		        baseName	)
    fileExt	    = fileInfo[1]
	
    if fileExt not in [ ".x_t", ".x_b" ]:
        raise HeatSinkCADError, "unknown file format to write"

    if sinkType == "none": sinkType = None
    if sinkType:
        sinkType        = sinkType.lower(                               )
        
    #--------------------------------------------------------------------
    # Set the model parts
    #--------------------------------------------------------------------

    while True:

        #----------------------------------------------------------------
        # Error checking
        #----------------------------------------------------------------

        for i in xrange( 3 ):
            if boardDims[i] > tunnelDims[i]:
                raise HeatSinkCADError, "The Board dimensions are invalid. " \
                    "They could not be more than Tunnel dimensions."

        for i in xrange( 2 ):
            if chipDims[i] > boardDims[i]:
                raise HeatSinkCADError, "The Chip length and width dimensions "\
                  "are invalid. They could not be more than Board dimensions."
            
        if sinkType:
            for i in xrange( 2 ) :           
                if sinkDims[i] > boardDims[i]:
                    raise HeatSinkCADError, "The Heat Sink length and width dimensions "\
                      "are invalid. They could not be more than Board dimensions."
        
            partsHeight =  boardDims[2] /2 + chipDims[2] + sinkDims[2]
        
            if partsHeight > tunnelDims[2] / 2:
                raise HeatSinkCADError, "The model height dimensions are invalid."
        
        #----------------------------------------------------------------
        # Set the Tunnel model
        #----------------------------------------------------------------
        x0          = -tunnelDims[0] / 2
        y0          = -tunnelDims[1] / 2
        z0          = -tunnelDims[2] / 2
        x1          = tunnelDims[0]  / 2
        y1          = tunnelDims[1]  / 2
        z1          = tunnelDims[2]  / 2
                
	(rc, tunnel)= GO_BODY_create_box_distances(     x0, x1, y0,
                                                        y1, z0, z1      )   
                                                         
		
	if tunnel   == pk.PK_ENTITY_null:
            raise HeatSinkCADError, "There is not an entity for tunnel."
                
	model1      = tunnel

        #----------------------------------------------------------------
        # Set the Board model
        #----------------------------------------------------------------

	x0          = -boardDims[0]  / 2
        y0          = -boardDims[1]  / 2
        z0          = -boardDims[2]  / 2
        x1          = boardDims[0]   / 2
        y1          = boardDims[1]   / 2
        z1          = boardDims[2]   / 2
                
        (rc, board)= GO_BODY_create_box_distances(      x0, x1, y0,
                                                        y1, z0, z1      )   
                                                              
                
	if board    == pk.PK_ENTITY_null:
            raise HeatSinkCADError,"There is not an entity for board."
                              
	model2      = board

        #----------------------------------------------------------------
        # Set the Chip model
        #----------------------------------------------------------------

	x0          = -chipDims[0]  / 2
        y0          = -chipDims[1]  / 2
        z0          = z1
        x1          = chipDims[0]   / 2
        y1          = chipDims[1]   / 2
        z1          = z0 + chipDims[2]
                
        ( rc, chip )= GO_BODY_create_box_distances(     x0, x1, y0,   
                                                        y1, z0, z1      )

	if chip     == pk.PK_ENTITY_null:                   
            raise HeatSinkCADError,"There is not an entity for chip."
                              
        model3      = chip
        
        if sinkType:
        #----------------------------------------------------------------
        # Set the HeatSink base model
        #----------------------------------------------------------------
		
            x0      = -sinkBaseDims[0] / 2
            y0      = -sinkBaseDims[1] / 2
            z0      = z1
            x1      = sinkBaseDims[0]  / 2
            y1      = sinkBaseDims[1]  / 2
            z1      = z0 + sinkBaseDims[2]

                
            (rc,baseSink)= GO_BODY_create_box_distances(x0, x1, y0,   
                                                        y1, z0, z1      )

            if baseSink == pk.PK_ENTITY_null:                    
                raise HeatSinkCADError, \
                            "There is not an entity for heat sink base."
        
            model4  = baseSink

            if sinkType in ['cross cut','extrusion'] :
            
                if sinkType == 'extrusion': 
                    ccYFinGap   = exYFinGap
                    ccYFinWidth = exYFinWidth

                setCrossExtFins(sinkDims,   ccXFinGap,  ccXFinWidth,
                                ccYFinGap,  ccYFinWidth,model4,
                                z1                                      ) 
            
            if sinkType == 'diamond cut':
                setDiamFin(     sinkDims,   dcFinWidth, dcFinGap,
                                model4,     z1                          )
            
            if sinkType =='pin fin':            
                setPinFin(      sinkDims,   pfPinDiameter,
                                model4,     z1                          )
                                     		
        #---------------------------------------------------------------
        # Create part names
        #---------------------------------------------------------------             
	rc          = GO_PART_set_name(     model1,     "tunnel"        )
	rc          = GO_PART_set_name(     model2,     "board"         )
	rc          = GO_PART_set_name(     model3,     "chip"          )

	if sinkType:
            rc      = GO_PART_set_name(     model4,     "heat sink"     )
		
        break

    #--------------------------------------------------------------------
    # Writes the model on a file
    #--------------------------------------------------------------------
    if sinkType: 
        if model1 != pk.PK_ENTITY_null and model2 != pk.PK_ENTITY_null and \
           model3 != pk.PK_ENTITY_null and model4 != pk.PK_ENTITY_null:
                
            if fileExt == ".x_t" :
                rc  = GO_PART_write_text(  [model1,model2,
                                            model3,model4],
                                            fileName                    )
            elif fileExt == ".x_b" :
                rc  = GO_PART_write_binary([model1,model2,
                                            model3,model4],
                                            fileName                    )
    else:
        if model1 != pk.PK_ENTITY_null and model2 != pk.PK_ENTITY_null and \
           model3 != pk.PK_ENTITY_null:

            if fileExt == ".x_t" :
                rc  = GO_PART_write_text(  [model1,model2,
                                            model3],
                                            fileName                    )
            elif fileExt == ".x_b" :
                rc  = GO_PART_write_binary([model1,model2,
                                            model3],
                                            fileName                    )
        
    #--------------------------------------------------------------------
    # Deletes the entities
    #--------------------------------------------------------------------

    GO_ENTITY_delete_all(						)

    #--------------------------------------------------------------------
    # Close the session
    #--------------------------------------------------------------------
    

#------------------------------------------------------------------------
# setCrossExtFins : Set fins for 'Cross Cut' and 'Extrusion' heat sinks.
#------------------------------------------------------------------------

def setCrossExtFins(sinkDims,     ccXFinGap,       ccXFinWidth,       
                    ccYFinGap,    ccYFinWidth,     model,
                    z
                    ):
    
    """  Set fins for 'Cross Cut' and 'Extrusion' heat sinks.

        Argument:
            sinkDims    - List of "heat sink top section" dimensions.
            ccXFinGap   - The gap between the "fins" on X axis for "Cross Cut" type. 
            ccYFinWidth - The width of each "fin" on Y axis for "Cross Cut" type.
            ccYFinGap   - The gap between the "fins" on Y axis for "Cross Cut" type.
            ccYFinWidth - The width of each "fin" on Y axis for "Extrusion" type.
            model       - The model which blades would be attached that.
            z           - The "z" dimension for setting the blads.
            
            
        Output:
            None
       
    """
    
    #--------------------------------------------------------------------
    # Set the HeatSink model
    #--------------------------------------------------------------------

    fct = 1. + 1.e-8
    if ccXFinGap and ccXFinWidth :
        finNumX = int((sinkDims[0] + fct*ccXFinGap) / (ccXFinGap + ccXFinWidth))
        sideGapX= sinkDims[0] - finNumX * ccXFinWidth - (finNumX-1)* ccXFinGap
        if finNumX <= 1 :
            raise HeatSinkCADError, "The model dimensions are invalid."
    else:
        finNumX  = 1
        sideGapX = 0 

    finNumY = int((sinkDims[1] + fct*ccYFinGap) / (ccYFinGap + ccYFinWidth))
    sideGapY= sinkDims[1] - finNumY * ccYFinWidth - (finNumY-1)* ccYFinGap
    
    if finNumY <= 1:
        raise HeatSinkCADError, "The model dimensions are invalid."
    
    x0      = -(sinkDims[0] - sideGapX )  / 2
    y0      = -(sinkDims[1] - sideGapY )  / 2
    z0      = z
    x1      = (sinkDims[0] - sideGapX )   / 2
    y1      = (sinkDims[1] - sideGapY )   / 2
    z1      = z0 + sinkDims[2]
                                                             
    (rc,heatSink)= GO_BODY_create_box_distances(    x0, x1, y0,
                                                    y1, z0, z1          )   
               
    if heatSink == pk.PK_ENTITY_null:
        raise HeatSinkCADError,"There is not an entity for heat sink."
                              
		
    (rc, model)= GO_BODY_unite(                     model,
                                                    heatSink            )
	    
    if model   == pk.PK_ENTITY_null:                    
        raise HeatSinkCADError, "There is not an entity."

    #-------------------------------------------------------------------
    # Set the XFins
    #-------------------------------------------------------------------
            
    for XBld in range(1,finNumX ):
        (rc,XBlade) = GO_BODY_create_box_distances(
                            x0 + XBld * ccXFinWidth + \
                            (XBld-1) * ccXFinGap,
                            x0 + XBld * ccXFinWidth + \
                            (XBld-1) * ccXFinGap + ccXFinGap,
                            y0, y1,
                            z0, z1                                      )
		
        if XBlade == pk.PK_ENTITY_null:
            raise HeatSinkCADError,"There is not an entity for X blade."
                            
        (rc,model)  = GO_BODY_subtract(             model,
                                                    XBlade              )
        if model == pk.PK_ENTITY_null:
            raise HeatSinkCADError, "There is not an entity."

    #-------------------------------------------------------------------
    # Set the YFins
    #-------------------------------------------------------------------
                            
    for YBld in range(1,finNumY):
        (rc,YBlade) = GO_BODY_create_box_distances(
                            x0, x1,
                            y0 + YBld * ccYFinWidth + \
                            (YBld-1) * ccYFinGap,
                            y0 + YBld * ccYFinWidth + \
                            (YBld-1) * ccYFinGap + ccYFinGap,
                            z0, z1                                      )


        if YBlade == pk.PK_ENTITY_null:
            raise HeatSinkCADError,"There is not an entity for Y blade."
                                      
                        
        (rc,model)  = GO_BODY_subtract(             model,
                                                    YBlade              )
        if model == pk.PK_ENTITY_null:
            raise HeatSinkCADError,"There is not an entity."

#---------------------------------------------------------------------------
# setDiamFin : Set fins for 'Diamond Cut' heat sink.
#---------------------------------------------------------------------------

def setDiamFin(sinkDims,            dcFinWidth,     dcFinGap,
               model,               z
               ):
    
    """  Set fins for for 'Diamond Cut' heat sink.

        Argument:
            sinkDims    - List of "heat sink top section" dimensions.
            dcFinWidth  - The width of each "fin" for "Diamond Cut" type.
            dcFinGap    - The gap between the "fins" for "Diamond Cut" type.
            model       - The model which blades would be attached that.
            z           - The "z" dimension for setting the blads.
                        
        Output:
            None
       
    """          

    widDim      = dcFinWidth   / cos(   radians(45)   )
    gapDim      = dcFinGap     / cos(   radians(45)   )
    
    fct = 1. + 1.e-8
    if sinkDims[0] == sinkDims[1]:
        finNumX = int((sinkDims[0] + fct*gapDim) / ( gapDim + widDim ))
        sideGapX= sinkDims[0] - finNumX * widDim - (finNumX - 1) * gapDim
        finNumY = finNumX
        sideGapY= sideGapX       
        finNum  = 2 * finNumX 
        
    else:
        finNumX = int((sinkDims[0] + fct*gapDim) / ( gapDim + widDim ))
        finNumY = int((sinkDims[1] + fct*gapDim) / ( gapDim + widDim ))
        sideGapX= sinkDims[0] - finNumX * widDim - (finNumX - 1) * gapDim
        sideGapY= sinkDims[0] - finNumY * widDim - (finNumY - 1) * gapDim
        finNum  = finNumX + finNumY

    if finNumX <= 1 or finNumY <= 1:
        raise HeatSinkCADError, "The model dimensions are invalid."

    x0          = -(sinkDims[0] - sideGapX) / 2
    y0          = -(sinkDims[1] - sideGapY) / 2
    z0          = z
    x1          = (sinkDims[0]  - sideGapX) / 2
    y1          = (sinkDims[1]  - sideGapY) / 2
    z1          = z0 + sinkDims[2]

    x0          += (dcFinWidth / 2)
    x1          += (dcFinWidth / 2)
    y0          += (dcFinWidth / 2)
    y1          += (dcFinWidth / 2)

    for finN in range(0,finNumX):
        (rc,fin)= GO_BODY_create_box_cross_section(
                    (x0 + (finN * gapDim) + (finN * widDim), y0, z1),
                    (x1, y1 - (finN * gapDim) - (finN * widDim) ,z1),                                                                                    
                     dcFinWidth ,
                     sinkDims[2]                                        )
    
        if fin == pk.PK_ENTITY_null:            
            raise HeatSinkCADError,"There is not an entity for fin."
                                      
                        
        (rc,model)= GO_BODY_unite(                  model,
                                                    fin                 )
        if model == pk.PK_ENTITY_null:
            raise HeatSinkCADError,"There is not an entity."
        
                    
    for finN in range(0,finNumY):
        
        (rc,fin)= GO_BODY_create_box_cross_section(
                    (x0 ,y0 + (finN * gapDim) + (finN * widDim), z1),
                    (x1 - (finN * gapDim) - (finN * widDim), y1 ,z1),                                                                                    
                     dcFinWidth ,
                     sinkDims[2]                                        )
    
    
        if fin == pk.PK_ENTITY_null:            
            raise HeatSinkCADError,"There is not an entity for fin."
                                      
                        
        (rc,model)= GO_BODY_unite(                  model,
                                                    fin                 )
        if model == pk.PK_ENTITY_null:
            raise HeatSinkCADError,"There is not an entity."
        
    for finN in range(0,finNum):
        
        (rc,fin)= GO_BODY_create_box_cross_section(
                    (x0 + (finN + 2)* widDim + finN * gapDim, y0, z1),
                    (x0, y0 + (finN + 2)*widDim + finN * gapDim , z1),                                                                                    
                     dcFinGap ,
                     sinkDims[2]                                        )
        
        if fin == pk.PK_ENTITY_null:            
            raise HeatSinkCADError,"There is not an entity for fin."
                                      
                        
        (rc,model)= GO_BODY_subtract(               model,
                                                    fin                 )
        if model == pk.PK_ENTITY_null:
            raise HeatSinkCADError,"There is not an entity."

#---------------------------------------------------------------------------
# setPinFin : Set fins for 'Pin Fin' heat sink.
#---------------------------------------------------------------------------

def setPinFin(sinkDims,            pfPinDiameter,
               model,              z
               ):
    
    """  Set fins for for 'Diamond Cut' heat sink.

        Argument:
            sinkDims    - List of "heat sink top section" dimensions.
            pfPinDiameter- Diameter of each "pins".
            model       - The model which blades would be attached that.
            z           - The "z" dimension for setting the blads.
                        
        Output:
            None
       
    """

    fct = 1. + 1.e-8
    valX        = int((sinkDims[0] + fct*pfPinDiameter ) / (2*pfPinDiameter))   
    finNumX     = 2 * valX + 1
    sideGapX    = sinkDims[0] - finNumX * pfPinDiameter

    valY        = int((sinkDims[1] + fct*pfPinDiameter ) / (2*pfPinDiameter))   
    finNumY     = 2 * valY + 1
    sideGapY    = sinkDims[1] - finNumY * pfPinDiameter

    if finNumX <= 1 or finNumY <= 1:
        raise HeatSinkCADError, "The model dimensions are invalid."
    
    pfPinR      = pfPinDiameter/ 2
    x0          = -(sinkDims[0] - sideGapX) / 2
    y0          = -(sinkDims[1] - sideGapY) / 2
    z0          = z
    x1          = (sinkDims[0]  - sideGapX) / 2
    y1          = (sinkDims[1]  - sideGapY) / 2
    z1          = z0 + sinkDims[2]

    x0          += pfPinR
    y0          += pfPinR
    
    for finNY in range(0,finNumY,2):
        
        for finNX in range(0,finNumX,2):
            (rc,fin)= GO_BODY_create_cylinder(
                    (x0 + (finNX * pfPinDiameter),
                     y0 + (finNY * pfPinDiameter), z0),
                    (x0 + (finNX * pfPinDiameter),
                     y0 + (finNY * pfPinDiameter), z1),
                     pfPinR                                             )
    
            if fin == pk.PK_ENTITY_null:            
                raise HeatSinkCADError,"There is not an entity for fin."
                        
            (rc,model)= GO_BODY_unite(              model,
                                                    fin                 )
            if model == pk.PK_ENTITY_null:
                raise HeatSinkCADError,"There is not an entity."
       
#========================================================================
#
# Test
#
#========================================================================

if __name__ == '__main__':

#------------------------------------------------------------------------
# An example for generating a 'Cross cut' heat Sink.
#------------------------------------------------------------------------  
    test1                       = True
    
    if test1 :
        heatSinkModel(      
            fileName            = 'crossCut.x_t' ,      
            tunnelDims          = ( 1., 1., 1.          ),
            boardDims           = ( 0.5, 0.5, 0.02      ),
            chipDims            = ( 0.2, 0.2, 0.008     ),
            sinkType            = "cross cut",                 
            sinkBaseDims        = ( 0.4, 0.4, 0.01      ),
            sinkDims            = ( 0.37, 0.37, 0.06    ),
            ccXFinWidth         = 0.02 ,
            ccXFinGap           = 0.03 ,
            ccYFinWidth         = 0.02,
            ccYFinGap           = 0.03 )

#------------------------------------------------------------------------
# An example for generating a 'Extrusion' heat Sink.
#------------------------------------------------------------------------  
    test2                       = True
    
    if test2 :
        heatSinkModel(      
            fileName            = 'extrusion.x_t' ,         
            tunnelDims          = ( 1., 1., 1.          ),
            boardDims           = ( 0.5, 0.5, 0.02      ),
            chipDims            = ( 0.2, 0.2, 0.008     ),
            sinkType            = 'extrusion',          
            sinkBaseDims        = ( 0.4, 0.4, 0.01      ),
            sinkDims            = ( 0.37, 0.37, 0.06    ),
            exYFinWidth         = 0.01,
            exYFinGap           = 0.02            
                                                                        )
        heatSinkModel(      
            fileName            = 'extrusion_2.x_t' ,         
            tunnelDims          = ( 1., 1., 1.          ),
            boardDims           = ( 0.5, 0.5, 0.02      ),
            chipDims            = ( 0.2, 0.2, 0.008     ),
            sinkType            = 'extrusion',          
            sinkBaseDims        = ( 0.4, 0.4, 0.01      ),
            sinkDims            = ( 0.4, 0.4, 0.06    ),
            exYFinWidth         = 0.01,
            exYFinGap           = 0.02            
                                                                        )
#------------------------------------------------------------------------
# An example for generating a 'Diamond Cut' heat Sink.
#------------------------------------------------------------------------  
    test3                       = True
    
    if test3 :
        heatSinkModel(      
            fileName            = 'diamond.x_t' ,         
            tunnelDims          = ( 1., 1., 1.          ),
            boardDims           = ( 0.5, 0.5, 0.02      ),
            chipDims            = ( 0.2, 0.2, 0.008     ),
            sinkType            = 'diamond cut',          
            sinkBaseDims        = ( 0.4, 0.4, 0.01      ),
            sinkDims            = ( 0.37, 0.37, 0.03    ), 
            dcFinWidth          = 0.01,
            dcFinGap            = 0.02                                  )

        heatSinkModel(      
            fileName            = 'diamond_2.x_t' ,         
            tunnelDims          = ( 1., 1., 1.          ),
            boardDims           = ( 0.5, 0.5, 0.02      ),
            chipDims            = ( 0.2, 0.2, 0.008     ),
            sinkType            = 'diamond cut',          
            sinkBaseDims        = ( 0.4, 0.4, 0.01      ),
            sinkDims            = ( 0.4, 0.4, 0.03    ), 
            dcFinWidth          = 0.01,
            dcFinGap            = 0.02                                  )

        heatSinkModel(      
            fileName            = 'diamond_3.x_t' ,         
            tunnelDims          = ( 1., 1., 1.          ),
            boardDims           = ( 0.5, 0.5, 0.02      ),
            chipDims            = ( 0.2, 0.2, 0.008     ),
            sinkType            = 'diamond cut',          
            sinkBaseDims        = ( 0.0254, 0.0254, 0.01      ),
            sinkDims            = ( 0.0254, 0.0254, 0.01    ), 
            dcFinWidth          = 0.002,
            dcFinGap            = 0.002                                  )

#------------------------------------------------------------------------
# An example for generating a 'Pin Fin' heat Sink.
#------------------------------------------------------------------------  
    test4                       = True
    
    if test4 :
        heatSinkModel(      
            fileName            = 'pinFin.x_t' ,         
            tunnelDims          = ( 1., 1., 1.          ),
            boardDims           = ( 0.5, 0.5, 0.02      ),
            chipDims            = ( 0.2, 0.2, 0.008     ),
            sinkType            = 'pin fin',          
            sinkBaseDims        = ( 0.4, 0.4, 0.01      ),
            sinkDims            = ( 0.37, 0.37, 0.06    ),
            pfPinDiameter       = 0.012                                  )
    
        heatSinkModel(      
            fileName            = 'pinFin_2.x_t' ,         
            tunnelDims          = ( 1., 1., 1.          ),
            boardDims           = ( 0.5, 0.5, 0.02      ),
            chipDims            = ( 0.2, 0.2, 0.008     ),
            sinkType            = 'pin fin',          
            sinkBaseDims        = ( 0.4, 0.4, 0.01      ),
            sinkDims            = ( 0.4, 0.4, 0.06    ),
            pfPinDiameter       = 0.012                                  )
    
