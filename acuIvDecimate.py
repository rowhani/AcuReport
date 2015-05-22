#===========================================================================
#
# Include files
#
#===========================================================================

import  sys
import  os

import  acudec

from    iv  import  *

#===========================================================================
#
# Errors
#
#===========================================================================

acuIvDecimate     = "ERROR from acuIvDecimate module"

#===========================================================================
#
# Global Variables
#
#===========================================================================

indexedFaceMap          = {}

#------------------------------------------------------------------------
# "_getMeshProperties" 
#------------------------------------------------------------------------

def _getMeshProperties( mesh ):

    '''
        Return the iv mesh properties: vertex, coordIndex, orderedRGBA
    '''

    vertexProperty  = SoVertexProperty( mesh.vertexProperty.getValue( ) )
    
    vertex          = vertexProperty.vertex.toNumarray( ).tolist( )
    coordIndex      = mesh.coordIndex.toNumarray( ).tolist( )
    orderedRGBA     = vertexProperty.orderedRGBA.toNumarray( ).tolist( )

    return ( vertex, coordIndex, orderedRGBA )

#------------------------------------------------------------------------
# "_setMeshProperties" 
#------------------------------------------------------------------------

def _setMeshProperties( mesh,
                        vertex,
                        coordIndex,                           
                        orderedRGBA ):

    '''
        Set the iv mesh properties: vertex, coordIndex, orderedRGBA
    '''
    
    vertexProperty = SoVertexProperty( )
    mesh.vertexProperty.setValue( vertexProperty )

    if vertex != None and len( vertex ) != 0:
        vertexProperty.vertex.setValues( 0, vertex )    

    if coordIndex != None and len( coordIndex ) != 0:
        mesh.coordIndex.setValues( 0, coordIndex )
        
    if orderedRGBA != None and len( orderedRGBA ) != 0:
        vertexProperty.orderedRGBA.setValues( 0, orderedRGBA )
 
    if len( vertexProperty.normal.toNumarray( ) ) != 0:
        vertexProperty.normal.setValues( 0, vertex )

#------------------------------------------------------------------------
# "_splitIndexList" 
#------------------------------------------------------------------------

def _splitIndexList( coordIndex ):

    '''
        Split the index list seperated by SO_END_FACE_INDEX
        into an array of ( nSrfs * var_size )
    '''
    
    splittedIndexList   = []
    
    srfIndices          = []    
    for index in coordIndex:
        if index != SO_END_FACE_INDEX:
            srfIndices.append( index ) 
        elif len( srfIndices ) != 0:
            splittedIndexList.append( srfIndices )
            srfIndices = []
            
    if index != SO_END_FACE_INDEX:
        splittedIndexList.append( srfIndices )

    return splittedIndexList

#------------------------------------------------------------------------
# "_mergeIndexList" 
#------------------------------------------------------------------------

def _mergeIndexList( indexList ):

    '''
        Merge the index list joind by SO_END_FACE_INDEX
        into a 1D array 
    '''    

    coordIndex  = []
    for srf in indexList:
        coordIndex.extend( srf )
        coordIndex.append( SO_END_FACE_INDEX )

    return coordIndex

#------------------------------------------------------------------------
# "_convertPackedColorListToRgb"  
#------------------------------------------------------------------------

def _convertPackedColorListToRgb( orderedRGBA ):

    '''
        Convert the packed (hex) color list to rgb color list
    '''

    if orderedRGBA == None or len( orderedRGBA ) == 0:
        return None

    rgbColorList = []
    
    for rgba in orderedRGBA:
        R = ( ( rgba & 0xff000000 ) >> 24 ) / 255.0
        G = ( ( rgba & 0x00ff0000 ) >> 16 ) / 255.0
        B = ( ( rgba & 0x0000ff00 ) >>  8 ) / 255.0
        A = ( ( rgba & 0x000000ff )       ) / 255.0

        rgbColorList.append( [R, G, B] ) 
               
    return rgbColorList

#------------------------------------------------------------------------
# "_convertRgbColorListToPacked"  
#------------------------------------------------------------------------

def _convertRgbColorListToPacked( rgbColorList ):

    '''
        Convert the rgb color list to packed (hex) color list 
    '''

    if rgbColorList == None or len( rgbColorList ) == 0:
        return None

    packedColorList = []
    
    for R, G, B in rgbColorList:
        packedColor = SbColor( R, G, B ).getPackedValue( )
        
        #packedColor = ( int( R * 255 ) << 24 ) + \
        #              ( int( G * 255 ) << 16 ) + \
        #              ( int( B * 255 ) <<  8 ) + \
        #              255

        packedColorList.append( packedColor ) 
               
    return packedColorList

#------------------------------------------------------------------------
# "_findAllDecimatableFaces" 
#------------------------------------------------------------------------

def _findAllDecimatableFaces( parent ):

    '''
        Look for all non-empty IndexedFaceSet meshes
    '''

    for i in range( parent.getNumChildren( ) ):
        node = parent.getChild( i )

        if isinstance( node, SoIndexedFaceSet ):
            if len( node.vertexProperty.getValue( ).vertex.toNumarray( ) ) != 0:
                if node not in indexedFaceMap.keys( ):
                    indexedFaceMap[node] = [parent, ]
                elif parent not in indexedFaceMap[node]:
                    indexedFaceMap[node].append( parent )

        elif isinstance( node, SoGroup ):
            _findAllDecimatableFaces( node )

#------------------------------------------------------------------------
# "_decimateIvMesh" 
#------------------------------------------------------------------------

def _decimateIvMesh(    mesh,
                        fct     = 1.0,
                        verbose = 0     ):

    '''
        Decimate an iv IndexedFaceSet mesh using acudec
    '''

    #----- Get vertex, coordIndex, orderedRGBA from iv mesh
    
    ( vertex, coordIndex, orderedRGBA ) = _getMeshProperties( mesh )

    crd         = vertex
    cnn         = _splitIndexList( coordIndex )
    clr         = _convertPackedColorListToRgb( orderedRGBA )

    #----- Decimate using acudec

    ( decCrd, decCnn, decClr ) = acudec.decimate( crd, cnn, clr, fct )

    keepNode    = ( len( decCnn ) != 0 )

    #----- Set vertex, coordIndex, orderedRGBA of the iv mesh

    vertex      = decCrd
    coordIndex  = _mergeIndexList( decCnn )
    orderedRGBA = _convertRgbColorListToPacked( decClr )

    _setMeshProperties( mesh, vertex, coordIndex, orderedRGBA )

    return keepNode  

#------------------------------------------------------------------------
# "decimateIvSceneGraph" : Decimate an iv scene graph completely
#------------------------------------------------------------------------

def decimateIvSceneGraph( sceneGraph,                         
                          fct         = 1.0,
                          verbose     = 0     ):

    '''
        Decimate an iv scene graph completely

	Arguments:
	    sceneGraphs	- The iv scene graph node
	    fct         - Decimation level [default=1.0 : no decimation]
	    verbose     - Verbosity level [default=0 : no progress displayed]	   
    
	Output:
	    The passed sceneGraph node
    '''

    if fct == None or fct >= 1.0:
        if verbose > 0:
            print "The iv scene graph is not decimated [fct=%s].\n" % str( fct )
        return sceneGraph

    if verbose > 0:
        print "Decimating the iv scene graph (or file)..."     

    #----- Find all decimatable faces

    global indexedFaceMap
    indexedFaceMap = {}
    
    _findAllDecimatableFaces( sceneGraph )

    #----- Decimate all the convertible faces

    for mesh in indexedFaceMap.keys( ):                   
        keepNode = _decimateIvMesh( mesh    = mesh,
                                    fct     = fct,
                                    verbose = verbose )
                
        if not keepNode:
            for parent in indexedFaceMap[mesh]:
                if parent.findChild( mesh ) != -1:
                    parent.removeChild( mesh )

    if verbose > 0:
        print "Decimating the iv scene graph (or file) done.\n"
        
    return sceneGraph

#------------------------------------------------------------------------
# "decimateIvFile" : Decimate an iv file completely and save the result
#------------------------------------------------------------------------

def decimateIvFile( inputIvFileName,
                    outputIvFileName    = None,
                    fct                 = 1.0,
                    verbose             = 0     ):

    '''
        Decimate an iv file completely and save the result

	Arguments:
	    inputIvFileName     - The input iv file name to be decimated
	    outputIvFileName    - The decimated output iv file name
	    fct                 - Decimation level [default=1.0 : no decimation]
	    verbose             - Verbosity level [default=0 : no progress displayed]	   
    
	Output:
	    The output iv file name
    '''

    if fct == None or fct >= 1.0:
        if verbose > 0:
            print "The iv file is not decimated [fct=%s].\n" % str( fct )
        return None

    #----- Load the scene graph

    SoInteraction.init( )
    
    inputIV = SoInput( )
    
    if not inputIV.openFile( inputIvFileName ):
        raise acuIvDecimateError, \
              "Cannot open file <%s>" % inputIvFileName
        sys.exit( 1 )
            
    sceneGraph = SoDB.readAll( inputIV )
    if not sceneGraph:
        print acuIvDecimateError, \
              "A problem occured while loading <%s>" % inputIvFileName
        sys.exit( 1 )           
            
    inputIV.closeFile( )

    #----- Start the decimation process

    decimateIvSceneGraph( sceneGraph = sceneGraph,                         
                          fct        = fct,
                          verbose    = verbose   )

    #----- Write the output iv file

    if outputIvFileName == None:
        outputIvFileName = os.path.splitext( inputIvFileName )[0] + "_decimated.iv"

    writeAction = SoWriteAction( )
    writeAction.getOutput( ).setBinary( False )
    writeAction.getOutput( ).openFile( outputIvFileName )
    writeAction.apply( sceneGraph )
    writeAction.getOutput( ).closeFile( )

    return outputIvFileName

#------------------------------------------------------------------------
# "Test" 
#------------------------------------------------------------------------

if __name__ == '__main__':

    decimateIvFile( inputIvFileName    = "HeatSink.iv",
                    fct                = 0.5,
                    verbose            = 3 )

    #-------------------------------------

    crd = ( ( 0.0000,  1.2142,  0.7453),
            ( 0.0000,  1.2142, -0.7453),
            (-1.2142,  0.7453,  0.0000),
            (-0.7453,  0.0000,  1.2142),
            ( 0.7453,  0.0000,  1.2142),
            ( 1.2142,  0.7453,  0.0000),
            ( 0.0000, -1.2142,  0.7453),
            (-1.2142, -0.7453,  0.0000),
            (-0.7453,  0.0000, -1.2142),
            ( 0.7453,  0.0000, -1.2142),
            ( 1.2142, -0.7453,  0.0000),
            ( 0.0000, -1.2142, -0.7453) )

    cnn = ( ( 1,  2,  3,  4,  5 ),
            ( 0,  1,  8,  7,  3 ),
            ( 0,  2,  7,  6,  4 ),
            ( 0,  3,  6, 10,  5 ),
            ( 0,  4, 10,  9,  1 ),
            ( 0,  5,  9,  8,  2 ),
            ( 9,  5,  4,  6, 11 ),
            ( 10, 4,  3,  7, 11 ),
            ( 6,  3,  2,  8, 11 ),
            ( 7,  2,  1,  9, 11 ),
            ( 8,  1,  5, 10, 11 ),
            ( 6,  7,  8,  9, 10 ) )

    clr = ( ( 1.0, 0.0, 0.0 ),
            ( 0.0, 0.0, 1.0 ),
            ( 0.0, 0.7, 0.7 ),
            ( 0.0, 1.0, 0.0 ),
            ( 0.7, 0.7, 0.0 ),
            ( 0.7, 0.0, 0.7 ),
            ( 0.0, 0.0, 1.0 ),
            ( 0.7, 0.0, 0.7 ),
            ( 0.7, 0.7, 0.0 ),
            ( 0.0, 1.0, 0.0 ),
            ( 0.0, 0.7, 0.7 ),
            ( 1.0, 0.0, 0.0 ) )

    fct = 0.5

    ( decCrd, decCnn, decClr ) = acudec.decimate( crd, cnn, clr, fct )

    print "acudec.decimate Demo:\n\n"

    print "crd"
    print crd
    print "\ndecCrd"
    print decCrd
    print "\n**********\n"
    
    print "cnn"
    print cnn
    print "\ndecCnn"
    print decCnn
    print "\n**********\n"
    
    print "clr"
    print clr
    print "\ndecClr"
    print decClr
    
