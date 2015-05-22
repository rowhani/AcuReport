#===========================================================================
#
# Include files
#
#===========================================================================

import  sys
import  os
import  math
import  numarray
import  acuIvDecimate

from    iv              import  *
from    acuIdtfShapes   import  *
from    acuIdtfNodes    import  *

#===========================================================================
#
# Errors
#
#===========================================================================

acuConvertIdtfError   = "ERROR from acuConvertIdtf module"

#========================================================================
#
# Global Variables
#
#========================================================================

SupportedNodes = [      "<class 'iv.SoSpotLight'>",
                        "<class 'iv.SoPointLight'>",
                        "<class 'iv.SoDirectionalLight'>",
                        "<class 'iv.SoOrthographicCamera'>",
                        "<class 'iv.SoPerspectiveCamera'>",
                        "<class 'iv.SoGroup'>",
                        "<class 'iv.SoSeparator'>",                     
                        "<class 'iv.SoMaterial'>",
                        "<class 'iv.SoIndexedFaceSet'>",
                        "<class 'iv.SoIndexedLineSet'>",                        
                        "<class 'iv.SoTranslation'>",
                        "<class 'iv.SoRotation'>",
                        "<class 'iv.SoScale'>",
                        "<class 'iv.SoTransform'>",
                        "<class 'iv.SoMatrixTransform'>",    
                        "<class 'iv.SoSphere'>",
                        "<class 'iv.SoCone'>",
                        "<class 'iv.SoCube'>",
                        "<class 'iv.SoCylinder'>",
                        "<class 'iv.SoCoordinate3'>"       ]

#========================================================================
#
# "AcuConvertIdtf" : AcuConvertIdtf class
#
#========================================================================

class AcuConvertIdtf:

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     sceneGraphs             = None,
                                ivFileNames             = None,
                                mergeGroups             = True,
                                merge                   = True,
                                regroup                 = True,                                
                                flatten                 = True,
                                reduced                 = True,
                                lineSetQuality          = -1.0,
                                timeStep                = 1,
                                createDisplayControl    = True,
                                fct                     = None,
                                verbose                 = 0     ):

            self.mergeGroups = mergeGroups

            if self.mergeGroups == True:
                    self.merge = True
            else:
                    self.merge = merge
            
            if self.merge == True:
                    self.regroup = True
                    self.flatten = True
            else:
                    self.regroup = regroup
                    self.flatten = flatten

            self.reduced = reduced

            if lineSetQuality < 0:
                    self.numOfLinesPerModel = -1                 
            else:
                    if lineSetQuality > 1:
                        lineSetQuality = 1.0        
                    self.numOfLinesPerModel = 1 - lineSetQuality                     
                    self.numOfLinesPerModel =  int( round( 9 * self.numOfLinesPerModel ) + 1 )

            self.nameOfAnimationStepNodes = []

            #----- Load or clone scene graph
                    
            if sceneGraphs == None:
                if not isinstance( ivFileNames, list ) and not isinstance( ivFileNames, tuple ):
                        self.sceneGraph = self._loadInventorFile( ivFileNames )
                else:
                        ### self.animation = True
                        self.numOfAnimationSteps = len( ivFileNames )
                        ### ivFileNames.reverse( )
                        self.sceneGraph = SoSeparator( )                        
                        for ivFile in ivFileNames:
                                scene = self._loadInventorFile( ivFile )
                                name = os.path.splitext( os.path.basename( ivFile ) )\
                                       .replace( '.', '_' ).replace( ' ', '_' )
                                nodeName = "File_" + name
                                scene.setName( nodeName )
                                self.nameOfAnimationStepNodes.append( nodeName );                                
                                self.sceneGraph.addChild( scene ) 
            else:
                if not isinstance( sceneGraphs, list ) and not isinstance( sceneGraphs, tuple ):    
                        self.sceneGraph = sceneGraphs.copy( )
                else:
                        ### self.animation = True 
                        self.numOfAnimationSteps = len( sceneGraphs )
                        ### sceneGraphs.reverse( )
                        self.sceneGraph = SoSeparator( )
                        for i in range( len ( sceneGraphs ) ):
                                scene = sceneGraphs[i]
                                nodeName = str( scene.getName( ) )
                                if nodeName == "":                                        
                                        nodeName = "Mesh_TimeStep_%d" % ( i + 1 )
                                        scene.setName( nodeName )
                                self.nameOfAnimationStepNodes.append( nodeName );
                                self.sceneGraph.addChild( scene.copy( ) )

            self.timeStep       = timeStep

            self.createDisplayControl = createDisplayControl
            
            ### self.animation      = False

            self.center         = None
            self.bounds         = None

            self.nameMap                = {}
            self.unamedNodes            = { 'Mesh'      : 1,    'Line_Set'      : 1,
                                            'Group'     : 1,    'Light'         : 1,
                                            'Camera'    : 1                             }

            #----- Regulate iv scene graph
                
            self.trimGroupNodes         = []
            self.trimUnsupportedNodes   = []
            
            self.names                  = {}            
            self.groups                 = []
            self.mergedGroups           = []            

            self._cleanModel( self.sceneGraph )

            self._mergeCoordinate3( self.sceneGraph )

            if fct != None and fct < 1.0:
                    acuIvDecimate.decimateIvSceneGraph(  self.sceneGraph,
                                                         fct,
                                                         verbose )
                    
            if self.flatten:
                    self._flattenModel( self.sceneGraph )            

            if self.regroup:
                    self._regroupModelByName( self.sceneGraph )

            if self.numOfLinesPerModel != -1:
                    self._splitLineSets( self.sceneGraph )         

            if self.merge:
                    self._mergeModelByName( )

            if self.reduced: 
                self._reduceModel( self.sceneGraph )

            #----- Initialize idtf containers

            self.idtfRoot           = None
        
            self.viewNodes          = []
            self.groupNodes         = []
            self.modelNodes         = []
            self.lightNodes         = []

            self.viewResources      = ResourceCollection(   "VIEW"      )
            self.lightResources     = ResourceCollection(   "LIGHT"     )
            self.modelResources     = ResourceCollection(   "MODEL"     )
            self.shaderResources    = ResourceCollection(   "SHADER"    )
            self.materialResources  = ResourceCollection(   "MATERIAL"  )
            self.motionResources    = ResourceCollection(   "MOTION"    )

            self.animationModifiers = []
            self.shadingModifiers   = []

            self.nodesMap           = {}

            self.displayNameMap     = []

#------------------------------------------------------------------------
# "_loadInventorFile"
#------------------------------------------------------------------------

        def _loadInventorFile( self,    ivFileName ):

            #----- Initialize selection nodes
            
            SoInteraction.init( )

            #----- Open and load the input file
            
            inputIV = SoInput( )
            
            if not inputIV.openFile( ivFileName ):
                    print "Cannot open file:", ivFileName
                    sys.exit( 1 )
                    
            sceneGraph = SoDB.readAll( inputIV )
            if not sceneGraph:
                    print "A problem occured while loading", ivFileName
                    sys.exit( 1 )
                    
            #----- close the input file
                    
            inputIV.closeFile( )

            return sceneGraph

#------------------------------------------------------------------------
# "_findUnusabaleNodes"
#------------------------------------------------------------------------

        def _findUnusabaleNodes( self,       curNode,
                                        parent                  = None,
                                        removeInvisNodes        = True ):

                drawStyleInvisible = False
                
                for i in range( curNode.getNumChildren( ) ):
                         
                        node = curNode.getChild( i )
                        removed = False

                        #----- Convert SoExtSelection to SoSeparator
                        
                        if isinstance( node, SoExtSelection ):                       
                                sep = SoSeparator( )
                                for j in range( node.getNumChildren( ) ):
                                        sep.addChild( node.getChild( j ) )                        
                                sep.setName( node.getName( ) )
                                curNode.replaceChild( node, sep )
                                node = sep

                        #----- Remove invisible models
                                
                        if removeInvisNodes and isinstance( node, SoDrawStyle ):                       
                                drawStyleInvisible = ( node.style.getValue() == SoDrawStyle.INVISIBLE )                                                        

                        #----- Find and append unsupported or non-group empty nodes
                                
                        if not ( str( type( node ) ) in SupportedNodes ) or \
                           ( not isinstance( node, SoGroup ) and \
                             not isinstance( node, SoCamera ) and \
                             not isinstance( node, SoLight ) and \
                             not isinstance( node, SoShape ) and \
                             node.hasDefaultValues( ) ) or \
                           ( isinstance( node, SoIndexedShape ) and node.hasDefaultValues( ) ) or \
                           drawStyleInvisible:                        
                                self.trimUnsupportedNodes.append( ( node, curNode ) )
                                removed = True

                        #----- Remove static objects
                                
                        if isinstance( node, SoCamera ) and \
                           node.viewportMapping.getValue() == SoCamera.LEAVE_ALONE:                                
                                self.trimUnsupportedNodes.append( ( curNode, parent ) )
                                removed = True
           
                        #----- Setting group nodes to default to remove unusable attributes
                        #----- and continue recursive searching for group nodes
                                
                        if isinstance( node, SoGroup ):
                                node.setToDefaults( )
                                self.trimGroupNodes.append( ( node, curNode ) )                        
                                if node.getNumChildren( ) > 0:                        
                                    self._findUnusabaleNodes( node, curNode )
                                    
#------------------------------------------------------------------------
# "_cleanModel"
#------------------------------------------------------------------------

        def _cleanModel( self, root ):

                self._findUnusabaleNodes( root )

                #----- Remove unsupportable nodes
            
                for i in range( len( self.trimUnsupportedNodes ) ):
                        node, parent = self.trimUnsupportedNodes.pop( ) 
                        if parent != None and parent.findChild( node ) != -1:                                               
                                parent.removeChild( node )

                #----- Remove group nodes that have no child or only a material child
                                
                for i in range( len( self.trimGroupNodes ) ):
                        node, parent = self.trimGroupNodes.pop( ) 
                        if parent != None and parent.findChild( node ) != -1 and \
                           node.getNumChildren() <= 0 or \
                           ( node.getNumChildren() == 1 and isinstance( node.getChild( 0 ), SoMaterial ) ):
                                parent.removeChild( node )

#------------------------------------------------------------------------
# "_getGroups"
#------------------------------------------------------------------------

        def _getGroups(  self,  curNode,
                                parent          = None ): 

                if ( curNode, parent ) not in self.groups:
                        self.groups.append( ( curNode, parent ) )
                        
                for i in range( curNode.getNumChildren( ) ):
                        node = curNode.getChild( i )

                        if isinstance( node, SoGroup ) and node.getNumChildren( ) > 0:                                
                                self.groups.append( ( node, curNode ) )
                                self._getGroups( node, curNode )

#------------------------------------------------------------------------
# "_mergeCoordinate3"
#------------------------------------------------------------------------

        def _mergeCoordinate3( self, root ):

                self.groups = []
                self._getGroups( root )

                for ( group, parent ) in self.groups:
                        curCoordinates = None

                        for j in range( group.getNumChildren( ) ):                               
                                node = group.getChild( j )

                                if isinstance( node, SoCoordinate3 ):
                                        if curCoordinates != None and group.findChild( curCoordinates ) != -1:
                                              group.removeChild( curCoordinates )  
                                        curCoordinates = node
                                                                           
                                elif isinstance( node, SoIndexedShape ):                                        
                                        vertProp = node.vertexProperty.getValue( )
                                        
                                        if vertProp == None or vertProp.vertex.getNum( ) == 0 \
                                           and curCoordinates != None and curCoordinates.point.getNum( ) != 0:
                                                if vertProp == None:
                                                        vertProp = SoVertexProperty( )
                                                vertProp.vertex.setValues( 0, curCoordinates.point.toNumarray( ) )
                                                node.vertexProperty.setValue( vertProp )

                        if curCoordinates != None and group.findChild( curCoordinates ) != -1:
                                group.removeChild( curCoordinates )

#------------------------------------------------------------------------
# "_flattenModel"
#------------------------------------------------------------------------

        def _flattenModel( self, root ):

                self.groups = []
                self._getGroups( root )               

                for i in range( len( self.groups ) ):
                        ( group, parent ) = self.groups.pop( )
                        
                        if parent != None:

                                childCnt = 0
                                for j in range( group.getNumChildren() ):
                                        child = group.getChild( j )

                                        if isinstance( child, SoGroup ) or \
                                           isinstance( child, SoCamera ) or \
                                           isinstance( child, SoLight ) or \
                                           isinstance( child, SoShape ):
                                                childCnt += 1
                                           
                                if childCnt == 1:  
                                        insIndex = parent.findChild( group )
                                        name = str( group.getName( ) )
                                        
                                        for j in range( group.getNumChildren( ) ):
                                                child = group.getChild( j )
                                                childName = str( child.getName( ) )

                                                if ( childName == None or childName == '' ) and \
                                                   ( name != None and name != '' ):
                                                        if isinstance( child, SoGroup ) or \
                                                           isinstance( child, SoCamera ) or \
                                                           isinstance( child, SoLight ) or \
                                                           isinstance( child, SoShape ):                                                                
                                                                child.setName( name )
                                                        
                                                parent.insertChild( child, insIndex + j )

                                        if parent.findChild( group ) != -1:
                                                parent.removeChild( group )
                                                
#------------------------------------------------------------------------
# "_regroupModelByName"
#------------------------------------------------------------------------

        def _regroupModelByName( self, root ):                 

                self.groups = []
                self._getGroups( root )
                uniqueNameMap = {}
                                    
                for ( group, parent ) in self.groups:
                       
                        nameMap = {}                        
                        
                        for j in range( group.getNumChildren( ) ):                               
                                node = group.getChild( j )
                                name = str( node.getName( ) )                                

                                if name != None and name != '':                                        
                                        if name in nameMap.keys( ):
                                                nameMap[name].append( node )                                                                                          
                                        else:
                                                nameMap[name] = [ node, ]
                                                
                        for name in nameMap.keys( ):  
                                nodeList = nameMap[name]

                                if name not in self.names.keys( ):                                                
                                        newName = name
                                        uniqueNameMap[name] = []
                                else:
                                        self.names[name] += 1
                                        newName = name + '_' + str( self.names[name] )

                                        if self.names[name] == 2:
                                                for unqNode in uniqueNameMap[name]: # New
                                                        unqName = str( unqNode.getName( ) )
                                                        if unqName.startswith( name ):
                                                               unqName = name + "_1" + unqName[len( name ):]
                                                               unqNode.setName( unqName )
                                                        
                                self.names[newName] = 1

                                nodeCnt = 0
                                for node in nodeList:
                                        if isinstance( node, SoIndexedShape ) or isinstance( node, SoGroup ):
                                                nodeCnt += 1
                         
                                if nodeCnt > 1:                                        
                                        sep = SoSeparator( )
                                        sep.setName( newName )                                        
                                        self.mergedGroups.append( ( sep, group ) )

                                        if newName in uniqueNameMap.keys( ):
                                                uniqueNameMap[name].append( sep ) # New

                                        group.replaceChild( nodeList[0], sep )
                                        for k in range( len( nodeList ) ):
                                                node = nodeList[k]                                                
                                                if isinstance( node, SoIndexedShape ) or isinstance( node, SoGroup ):
                                                        node.setName( newName + '_' + str( k + 1 ) )                                               
                                                        sep.addChild( node )

                                                        if newName in uniqueNameMap.keys( ):
                                                                uniqueNameMap[name].append( node ) # New

                                                        if group.findChild( node ) != -1:
                                                                group.removeChild( node )
                                        
                                else:
                                        nodeList[0].setName( newName )

                                        if newName in uniqueNameMap.keys( ):
                                                uniqueNameMap[name].append( nodeList[0] ) # New
                                        
#------------------------------------------------------------------------
# "_splitLineSets"
#------------------------------------------------------------------------

        def _splitLineSets( self, root ):

                self.groups = []
                self._getGroups( root )

                for ( group, parent ) in self.groups:
                        for j in range( group.getNumChildren( ) ):
                                node = group.getChild( j )

                                if isinstance( node, SoIndexedLineSet ):                                        

                                        lineSep = SoSeparator( )
                                        lineSep.setName( node.getName( ) )

                                        ( modelPositionList,
                                          meshPositionList,
                                          modelNormalList,
                                          meshNormalList,
                                          modelDiffuseColorList,
                                          meshDiffuseColorList ) = self._getMeshProperties( node )                
                                        
                                        lineIndexList = self._splitIndexList( meshPositionList )

                                        if meshNormalList != None:
                                                if meshNormalList != meshPositionList:
                                                        normalIndexList = self._splitIndexList( meshNormalList )
                                                else:
                                                        normalIndexList = lineIndexList
                                        else:
                                                normalIndexList = None

                                        if meshDiffuseColorList != None:
                                                if meshDiffuseColorList != meshPositionList:
                                                        materialIndexList = self._splitIndexList( meshDiffuseColorList )
                                                else:
                                                        materialIndexList = lineIndexList
                                        else:
                                                materialIndexList = None      

                                        for i in range( 0, len( lineIndexList ), self.numOfLinesPerModel ):
                                                        
                                                vertices = []
                                                indices = []
                                                vertMap = {}

                                                normals = []
                                                normIndices = []
                                                normMap = {}

                                                materials = []
                                                matIndices = []
                                                matMap = {}

                                                for j in range( self.numOfLinesPerModel ):
                                                        if i + j < len( lineIndexList ):                                      

                                                                self._mergeVerticesAndIndices( modelPositionList,
                                                                                               lineIndexList[i + j],
                                                                                               vertices,
                                                                                               indices,
                                                                                               vertMap )
                                                                
                                                                if normalIndexList != None and i + j < len( normalIndexList ):
                                                                        self._mergeVerticesAndIndices( modelNormalList,
                                                                                                       normalIndexList[i + j],
                                                                                                       normals,
                                                                                                       normIndices,
                                                                                                       normMap )
                                                                        
                                                                if materialIndexList != None and i + j < len( materialIndexList ):
                                                                        self._mergeVerticesAndIndices( modelDiffuseColorList,
                                                                                                       materialIndexList[i + j],
                                                                                                       materials,
                                                                                                       matIndices,
                                                                                                       matMap,
                                                                                                       True )                       

                                                newLine = SoIndexedLineSet( )
                                                
                                                self._setMeshProperties( newLine,
                                                                         vertices,
                                                                         normals,
                                                                         materials,
                                                                         indices,
                                                                         normIndices,
                                                                         matIndices ) 
                                                            
                                                lineSep.addChild( newLine )                        

                                        group.replaceChild( node, lineSep )

#------------------------------------------------------------------------
# "_mergeModelByName"
#------------------------------------------------------------------------

        def _mergeModelByName( self ):

                for ( group, parent ) in self.mergedGroups:

                        meshVertices    = []
                        meshIndices     = []
                        meshVertMap     = {}

                        meshNormals     = []
                        meshNormIndices = []
                        meshNormMap     = {}

                        meshMaterials   = []
                        meshMatIndices  = []
                        meshMatMap      = {}

                        mergedMesh      = SoIndexedFaceSet( )
                        
                        lineVertices    = []
                        lineIndices     = []
                        lineVertMap     = {}

                        lineNormals     = []
                        lineNormIndices = []
                        lineNormMap     = {}

                        lineMaterials   = []
                        lineMatIndices  = []
                        lineMatMap      = {}

                        mergedLine      = SoIndexedLineSet( )                        

                        curMat          = None
                        meshMat         = None
                        lineMat         = None

                        nodeList        = []
                        
                        for i in range( group.getNumChildren( ) ):
                                node = group.getChild( i )
                                
                                if isinstance( node, SoIndexedShape ):
                                        nodeList.append( node )
                                        
                                #----- Only get first-level chilren                                        
                                elif isinstance( node, SoGroup ) and self.mergeGroups == True:       
                                        for j in range( node.getNumChildren( ) ):
                                                subNode = node.getChild( j )

                                                if isinstance( subNode, SoIndexedFaceSet ):
                                                        nodeList.append( subNode )
                                                        if curMat != None and meshMat == None:
                                                                meshMat = curMat                                                        

                                                elif isinstance( subNode, SoIndexedLineSet ):
                                                        nodeList.append( subNode )
                                                        if curMat != None and lineMat == None:
                                                                lineMat = curMat

                                                #----- Take the first material as the model material
                                                elif isinstance( subNode, SoMaterial ):
                                                        curMat = subNode

                        for node in nodeList:

                                ( modelPositionList,
                                  meshPositionList,
                                  modelNormalList,
                                  meshNormalList,
                                  modelDiffuseColorList,
                                  meshDiffuseColorList ) = self._getMeshProperties( node )

                                if isinstance( node, SoIndexedFaceSet ):

                                        self._mergeVerticesAndIndices( modelPositionList,
                                                                       meshPositionList,
                                                                       meshVertices,
                                                                       meshIndices,
                                                                       meshVertMap )

                                        self._mergeVerticesAndIndices( modelNormalList,
                                                                       meshNormalList,
                                                                       meshNormals,
                                                                       meshNormIndices,
                                                                       meshNormMap )

                                        self._mergeVerticesAndIndices( modelDiffuseColorList,
                                                                       meshDiffuseColorList,
                                                                       meshMaterials,
                                                                       meshMatIndices,
                                                                       meshMatMap,
                                                                       True )

                                elif isinstance( node, SoIndexedLineSet ) and self.numOfLinesPerModel == -1:

                                        self._mergeVerticesAndIndices( modelPositionList,
                                                                       meshPositionList,
                                                                       lineVertices,
                                                                       lineIndices,
                                                                       lineVertMap )

                                        self._mergeVerticesAndIndices( modelNormalList,
                                                                       meshNormalList,
                                                                       lineNormals,
                                                                       lineNormIndices,
                                                                       lineNormMap )

                                        self._mergeVerticesAndIndices( modelDiffuseColorList,
                                                                       meshDiffuseColorList,
                                                                       lineMaterials,
                                                                       lineMatIndices,
                                                                       lineMatMap,
                                                                       True )
                                        
                        if len( meshVertices ) == 0 and len( lineVertices ) == 0:
                                if self.mergeGroups == True and parent.findChild( group ) != -1:
                                        parent.removeChild( group )

                        elif len( meshVertices ) != 0 and len( lineVertices ) == 0:
                                self._setMeshProperties( mergedMesh,
                                                         meshVertices,
                                                         meshNormals,
                                                         meshMaterials,
                                                         meshIndices,
                                                         meshNormIndices,
                                                         meshMatIndices )

                                mergedMesh.setName( group.getName( ) )
                                parent.replaceChild( group, mergedMesh )
                                
                        elif len( meshVertices ) == 0 and len( lineVertices ) != 0:
                                self._setMeshProperties( mergedLine,
                                                         lineVertices,
                                                         lineNormals,
                                                         lineMaterials,
                                                         lineIndices,
                                                         lineNormIndices,
                                                         lineMatIndices )
                                
                                mergedLine.setName( group.getName( ) )
                                parent.replaceChild( group, mergedLine )                                

                        else:                                
                                self._setMeshProperties( mergedMesh,
                                                         meshVertices,
                                                         meshNormals,
                                                         meshMaterials,
                                                         meshIndices,
                                                         meshNormIndices,
                                                         meshMatIndices )
                                mergedMesh.setName( str( group.getName( ) ) + "_Mesh" )
                                
                                self._setMeshProperties( mergedLine,
                                                         lineVertices,
                                                         lineNormals,
                                                         lineMaterials,
                                                         lineIndices,
                                                         lineNormIndices,
                                                         lineMatIndices )
                                mergedLine.setName( str( group.getName( ) ) + "_Line" )                                

                                meshLineSep = SoSeparator( )
                                meshLineSep.setName( group.getName( ) )

                                if meshMat != None:
                                        meshLineSep.addChild( meshMat )                                
                                meshLineSep.addChild( mergedMesh )

                                if lineMat != None:
                                        meshLineSep.addChild( lineMat )
                                meshLineSep.addChild( mergedLine )

                                parent.replaceChild( group, meshLineSep )                           

#------------------------------------------------------------------------
# "_reduceModel"
#------------------------------------------------------------------------

        def _reduceModel( self, root ):

                self.groups = []
                self._getGroups( root )

                for ( group, parent ) in self.groups:
                        for j in range( group.getNumChildren( ) ):
                                node = group.getChild( j )

                                if not isinstance( node, SoIndexedShape ) or \
                                   ( isinstance( node, SoIndexedLineSet ) and self.numOfLinesPerModel != -1 ):
                                        continue
                                
                                ( modelPositionList,
                                  meshPositionList,
                                  modelNormalList,
                                  meshNormalList,
                                  modelDiffuseColorList,
                                  meshDiffuseColorList ) = self._getMeshProperties( node )

                                vertices = []
                                indices = []
                                vertMap = {}

                                normals = []
                                normIndices = []
                                normMap = {}

                                materials = []
                                matIndices = []
                                matMap = {}

                                self._mergeVerticesAndIndices( modelPositionList,
                                                               meshPositionList,
                                                               vertices,
                                                               indices,
                                                               vertMap )

                                self._mergeVerticesAndIndices( modelNormalList,
                                                               meshNormalList,
                                                               normals,
                                                               normIndices,
                                                               normMap )

                                self._mergeVerticesAndIndices( modelDiffuseColorList,
                                                               meshDiffuseColorList,
                                                               materials,
                                                               matIndices,
                                                               matMap,
                                                               True )

                                self._setMeshProperties( node,
                                                         vertices,
                                                         normals,
                                                         materials,
                                                         indices,
                                                         normIndices,
                                                         matIndices )

#------------------------------------------------------------------------
# "_getCameraName"
#------------------------------------------------------------------------

        def _getCameraName( self, camera ):

            name = str( camera.getName( ) )     
            
            if name == None or name == '':            
                if len ( self.viewNodes ) > 0:
                        name = 'Camera_' + str( self.unamedNodes['Camera'] )
                        self.unamedNodes['Camera'] += 1
                else:
                        name = 'Camera'                
            else:                
                if name in self.nameMap.keys( ):
                        self.nameMap[name] += 1
                        name += "_" + str( self.nameMap[name] )
                else:
                        self.nameMap[name] = 1

            return name
        
#------------------------------------------------------------------------
# "_getLightName"
#------------------------------------------------------------------------

        def _getLightName( self, light ):

            name = str( light.getName( ) )
                 
            if name == None or name == '':
                if len ( self.lightNodes ) > 0:
                        name = 'Light_' + str( self.unamedNodes['Light'] )
                        self.unamedNodes['Light'] += 1
                else:
                        name = 'Light'                            
            else:
                if name in self.nameMap.keys( ):
                        self.nameMap[name] += 1
                        name += "_" + str( self.nameMap[name] )
                else:
                        self.nameMap[name] = 1
            return name

#------------------------------------------------------------------------
# "_getMeshNameModel"
#------------------------------------------------------------------------

        def _getMeshNameModel( self, mesh ):
        
            name = str( mesh.getName( ) )
            tName = True

            if isinstance( mesh, SoIndexedFaceSet):
                if name == None or name == '':
                        name = 'Mesh_' + str( self.unamedNodes['Mesh'] )
                        self.unamedNodes['Mesh'] += 1
                        tName = False
                model = "MESH"
            else:
                if name == None or name == '':
                        name = 'Line_Set_' + str( self.unamedNodes['Line_Set'] )
                        self.unamedNodes['Line_Set'] += 1
                        tName = False
                model = "LINE_SET"

            if tName == True:
                    if name in self.nameMap.keys( ):                            
                            self.nameMap[name] += 1
                            name += "_" + str( self.nameMap[name] )
                    else:
                            self.nameMap[name] = 1
                            
            return name, model
                                
#------------------------------------------------------------------------
# "_convertGroup"
#------------------------------------------------------------------------

        def _convertGroup( self, group, parent ):

            name = str( group.getName( ) )
                        
            if name == None or name == '':
                name = 'Group_' + str( self.unamedNodes['Group'] )
                
                #---- Not Model Parent
                
                if parent != None:      
                        self.unamedNodes['Group'] += 1
            else:               
                if name in self.nameMap.keys( ):
                        self.nameMap[name] += 1
                        name += "_" + str( self.nameMap[name] )
                else:
                        self.nameMap[name] = 1 

            groupNode = GroupNode( name,
                                   parent )

            self.groupNodes.append( groupNode )

            return groupNode
        
#------------------------------------------------------------------------
# "_convertCamera"
#------------------------------------------------------------------------

        def _convertCamera( self, camera, parent ):

            name = self._getCameraName( camera )
            
            if isinstance( camera, SoPerspectiveCamera  ):
                viewNode = ViewNode( name,
                                     parent,
                                     viewType = 'PERSPECTIVE',
                                     viewProjection = camera.heightAngle.getValue( ) )

            else:               
                viewNode = ViewNode( name,
                                     parent,
                                     viewType = 'ORTHO',
                                     viewProjection = camera.height.getValue( ) )

            self.viewNodes.append( viewNode )

            return viewNode

#------------------------------------------------------------------------
# "_convertLight"
#------------------------------------------------------------------------

        def _convertLight( self, light, parent ):            

            name = self._getLightName( light );           
                    
            resName = name + "Resource"
            intensity = light.intensity.getValue( )
            
            if isinstance( light, SoDirectionalLight ):
                lightRes = LightResource( resName,
                                          "DIRECTIONAL",
                                          intensity )
                
            elif isinstance( light, SoSpotLight ):
                lightRes = LightResource( resName,
                                          "SPOT",
                                          intensity,
                                          light.cutOffAngle.getValue() )
                
            else:
                lightRes = LightResource( resName,
                                          "POINT",
                                          intensity )                
                
            lightNode = LightNode( name,
                                   parent,
                                   resource = lightRes )           

            self.lightNodes.append( lightNode )
            self.lightResources.addResource( lightRes )

            return lightNode

#------------------------------------------------------------------------
# "_convertShape"
#------------------------------------------------------------------------

        def _convertShape( self, shape, parent ):

                shapeModel = None

                if isinstance( shape, SoIndexedShape ):
                        shapeModel = shape
                        
                elif isinstance( shape, SoSphere ):                        
                        shapeModel = convertSphere( shape )

                elif isinstance( shape, SoCube ):                        
                        shapeModel = convertCube( shape )

                elif isinstance( shape, SoCone ):                        
                        shapeModel = convertCone( shape )

                elif isinstance( shape, SoCylinder ):                        
                        shapeModel = convertCylinder( shape )                        

                if shapeModel != None:     
                        return self._convertMeshModel( shapeModel, parent )
                else:
                        return None

#------------------------------------------------------------------------
# "_convertMeshModel"
#------------------------------------------------------------------------

        def _convertMeshModel( self, mesh, parent ):

            ( modelPositionList,
              meshPositionList,
              modelNormalList,
              meshNormalList,
              modelDiffuseColorList,
              meshDiffuseColorList ) = self._getMeshProperties( mesh )
            
            #----- Create mesh model

            name, model = self._getMeshNameModel( mesh )
            
            resName = name + "Resource"
                
            meshModel = Mesh (  model,
                                modelPositionList,
                                meshPositionList,
                                modelNormalList,
                                meshNormalList,
                                modelDiffuseColorList,
                                meshDiffuseColorList )            
            
            modelRes = ModelResource( resName,
                                      model,
                                      meshModel )

            modelNode = ModelNode( name,
                                   parent,
                                   resource = modelRes )           

            self.modelNodes.append( modelNode )            
            self.modelResources.addResource( modelRes )                             

            return modelNode

#------------------------------------------------------------------------
# "_getMeshProperties"
#------------------------------------------------------------------------

        def _getMeshProperties( self, mesh ):

                #----- Convert Model Data (vertex properties)

                vertProp = mesh.vertexProperty.getValue( )
                if  vertProp != None:
                        if vertProp.vertex.getNum( ) != 0:
                            modelPositionList = vertProp.vertex.toNumarray( )               
                        else:                   
                            raise acuConvertIdtfError, "No model position list found for the mesh."
                        
                        if vertProp.normal.getNum( ) != 0:
                            modelNormalList = vertProp.normal.toNumarray( )
                        else:
                            modelNormalList = None

                        if vertProp.orderedRGBA.getNum( ) != 0:
                            modelDiffuseColorList = vertProp.orderedRGBA.toNumarray( )
                        else:
                            modelDiffuseColorList = None                              
                else:
                       raise acuConvertIdtfError, "No model position list found for the mesh."
            
                #----- Convert Mesh Data (indices)
            
                if mesh.coordIndex.getNum( ) != 1:
                        meshPositionList = mesh.coordIndex.toNumarray( ).tolist( )
                else:
                        raise acuConvertIdtfError, "No mesh position list found for the mesh."

                if modelNormalList != None:
                        if mesh.normalIndex.getNum( ) != 1:
                                meshNormalList = mesh.normalIndex.toNumarray( ).tolist( )
                        else:
                                meshNormalList = meshPositionList
                else:
                        meshNormalList = None 
                
                if modelDiffuseColorList != None:
                        if mesh.materialIndex.getNum( ) != 1:
                                meshDiffuseColorList = mesh.materialIndex.toNumarray( ).tolist( )
                        else:
                                meshDiffuseColorList = meshPositionList
                else:
                        meshDiffuseColorList = None 

                return ( modelPositionList,
                         meshPositionList,
                         modelNormalList,
                         meshNormalList,
                         modelDiffuseColorList,
                         meshDiffuseColorList )

#------------------------------------------------------------------------
# "_setMeshProperties"
#------------------------------------------------------------------------

        def _setMeshProperties( self,   mesh,
                                        vertices,
                                        normals,
                                        materials,
                                        indices,
                                        normIndices,
                                        matIndices ):

                vertProp = SoVertexProperty( )
                vertProp.vertex.setValues( 0, vertices )
                if normals != []:
                        vertProp.normal.setValues( 0, normals )
                if materials != []:
                        vertProp.orderedRGBA.setValues( 0, materials )
                mesh.vertexProperty.setValue( vertProp )
                
                mesh.coordIndex.setValues( 0, indices )
                if normIndices != [] and normIndices != indices:
                        mesh.normalIndex.setValues( 0, normIndices )
                if matIndices != [] and matIndices != indices:
                        mesh.materialIndex.setValues( 0, matIndices )

#------------------------------------------------------------------------
# "_mergeVerticesAndIndices"
#------------------------------------------------------------------------

        def _mergeVerticesAndIndices( self,     modelPositionList,
                                                meshPositionList,
                                                vertices,
                                                indices,
                                                vertMap,
                                                isColor = False         ):

                if modelPositionList == None or meshPositionList == None:
                        return

                reducedModelPositionList = []
                usedIndices = []
                
                for index in meshPositionList:
                        if index != -1:
                                if index < len( modelPositionList ):
                                        if index not in usedIndices:                       
                                                usedIndices.append( index )
                                                
                                                vert = modelPositionList[index]
                                                if isColor:
                                                        key = vert
                                                else:
                                                        key = "%.6f %.6f %.6f" % tuple( vert )
                                                        
                                                if key not in vertMap.keys( ):
                                                        vertMap[key] = len( vertices )
                                                        vertices.append( vert )

                                        if isColor:
                                                key = modelPositionList[index]
                                        else:
                                                key = "%.6f %.6f %.6f" % tuple( modelPositionList[index] )
                                        indices.append( vertMap[ key ] )
                                else:
                                        indices.append( -1 )
                        else:
                                indices.append( index )

                if meshPositionList[-1] != -1:
                        indices.append( -1 )
        
#------------------------------------------------------------------------
# "_splitIndexList"
#------------------------------------------------------------------------

        def _splitIndexList( self, indices ):
                
                splittedIndexList = []
                indexList = []
                for index in indices:
                        if index != -1:
                                indexList.append( index )
                        elif len( indexList ) != 0:
                                splittedIndexList.append( indexList )
                                indexList = []

                return splittedIndexList
                        
#------------------------------------------------------------------------
# "_createDummyMaterial"
#------------------------------------------------------------------------

        def _createDummyMaterial( self, material, parent ):

            parent.currentMaterial = MaterialResource( None,
                                                       material.diffuseColor.toNumarray( )[0],
                                                       material.transparency.toNumarray( )[0] )

#------------------------------------------------------------------------
# "_convertMaterialForModel"
#------------------------------------------------------------------------

        def _convertMaterialForModel( self, model, parent ):

            if model == None or parent == None or parent.currentMaterial == None:
                return            

            matResName = model.name + 'MatResource'
            shadResName = model.name + 'ShadResource'

            matRes = MaterialResource( matResName,
                                       parent.currentMaterial.diffuseColor,
                                       parent.currentMaterial.opacity )
            shadRes = ShaderResource( shadResName,
                                      matRes )
            shadMod = ShadingModifier( model,
                                       shadRes )

            self.materialResources.addResource( matRes )
            self.shaderResources.addResource( shadRes )
            self.shadingModifiers.append( shadMod )

#------------------------------------------------------------------------
# "_convertDummyTransformation"
#------------------------------------------------------------------------

        def _convertDummyTransformation( self, transform, parent ):

                if isinstance( transform, SoTranslation ):
                        resTrans = self._convertDummyTranslation( transform, parent )
                        
                elif isinstance( transform, SoRotation ):                        
                        resTrans = self._convertDummyRotation( transform, parent )
                        
                elif isinstance( transform, SoScale ):                        
                        resTrans = self._convertDummyScale( transform, parent )

                else:
                        if isinstance( transform, SoMatrixTransform ):
                                translation     = SbVec3f( )
                                rotation        = SbRotation( )
                                scaleFactor     = SbVec3f( )
                                scaleOrient     = SbRotation( )

                                transMat        = transform.matrix.getValue().getTransform( translation,
                                                                                            rotation,
                                                                                            scaleFactor,
                                                                                            scaleOrient )

                                trans = SoTransform( )
                                trans.translation.setValue( translation )
                                trans.rotation.setValue ( rotation )
                                trans.scaleFactor.setValue( scaleFactor )
                                
                        elif isinstance( transform, SoTransform ):
                                trans = transform
                                
                        translationTM = numarray.transpose( self._convertDummyTranslation( trans, parent ) )
                        rotationTM = numarray.transpose( self._convertDummyRotation( trans, parent ) )
                        scaleTM = numarray.transpose( self._convertDummyScale( trans, parent ) )

                        trm = numarray.matrixmultiply(translationTM, rotationTM )
                        trm = numarray.matrixmultiply(trm, scaleTM )
                        
                        resTrans = numarray.transpose( trm )

                if parent.currentTransform == None:
                        parent.currentTransform = resTrans
                else:
                        tpMat = numarray.transpose( parent.currentTransform )
                        trMat = numarray.transpose( resTrans )
                        parent.currentTransform = numarray.transpose( numarray.matrixmultiply( tpMat, trMat ) )

#------------------------------------------------------------------------
# "_convertDummyTranslation"
#------------------------------------------------------------------------

        def _convertDummyTranslation( self, translation, parent ):

                tx, ty, tz = translation.translation.getValue().getValue()              

                trans = [ [  1,  0,  0,  0 ],
                          [  0,  1,  0,  0 ],
                          [  0,  0,  1,  0 ],
                          [ tx, ty, tz,  1 ] ]
                
                return trans
                    
#------------------------------------------------------------------------
# "_convertDummyScale"
#------------------------------------------------------------------------

        def _convertDummyScale( self, scale, parent ):

                sx, sy, sz = scale.scaleFactor.getValue().getValue()
                
                trans = [ [ sx,  0,  0,  0 ],
                          [  0, sy,  0,  0 ],
                          [  0,  0, sz,  0 ],
                          [  0,  0,  0,  1 ] ]

                return trans

#------------------------------------------------------------------------
# "_convertDummyRotation"
#------------------------------------------------------------------------

        def _convertDummyRotation( self, rotation, parent ):

                #----- Get rotation quaternion
                
                w, x, y, z = rotation.rotation.getValue().getValue()
                
                trans = [ [ 1 - 2 * y ** 2 - 2 * z ** 2,
                            2 * x * y + 2 * z * w,
                            2 * x * z - 2 * y * w,
                            0 ],
                                            
                          [ 2 * x * y - 2 * z * w,
                            1 - 2 * x ** 2 - 2 * z ** 2,
                            2 * y * z + 2 * x * w,
                            0 ],
                                            
                          [ 2 * x * z + 2 * y * w,
                            2 * y * z - 2 * x * w,
                            1 - 2 * x ** 2 - 2 * y ** 2,
                            0 ],
                                            
                          [ 0,
                            0,
                            0,
                            1 ] ]

                return trans

#------------------------------------------------------------------------
# "_createTransformForNode"
#------------------------------------------------------------------------

        def _createTransformForNode( self, node, parent ):

                if node == None or parent == None or parent.currentTransform == None:
                        return

                node.tm = parent.currentTransform
                
#------------------------------------------------------------------------
# "_convertIV2IDTFHelper"
#------------------------------------------------------------------------

        def _convertIV2IDTFHelper( self,    curNode,    parent ):

                #----- Convert curNode to group node

                if curNode in self.nodesMap.keys( ):
                        groupParent = self.nodesMap[curNode]
                else:
                        groupParent = self._convertGroup( curNode, parent )
                        self.nodesMap[curNode] = groupParent
                        
                if parent != None:
                    groupParent.currentMaterial = parent.currentMaterial
                self._createTransformForNode( groupParent, parent )

                if parent == None:
                        self.idtfRoot           = groupParent
                        self.idtfRoot.name      = 'Model'                        
                else:
                        parent.addChild( groupParent )
            
                for i in range( curNode.getNumChildren( ) ):
                        node = curNode.getChild( i )
      
                        if isinstance( node, SoMaterial ):
                                self._createDummyMaterial( node, groupParent )

                        elif isinstance( node, SoTransformation ):    
                                self._convertDummyTransformation( node, groupParent )

                        elif isinstance( node, SoGroup ) and node.getNumChildren( ) > 0:
                                self._convertIV2IDTFHelper( node, groupParent )                             
                            
                        elif isinstance( node, SoCamera ):
                                if node in self.nodesMap.keys( ):
                                        model = self.nodesMap[node]
                                else:
                                        model =  self._convertCamera( node, groupParent )
                                        self.nodesMap[node] = model
                                        
                                groupParent.addChild( model )
                                self._createTransformForNode( model, groupParent )
                            
                        elif isinstance( node, SoLight ):
                                if node in self.nodesMap.keys( ):
                                        model = ModelNode( self._getLightName( node ),
                                                           groupParent,
                                                           resource = self.nodesMap[node].resource )
                                        self.lightNodes.append( model )
                                else:
                                        model = self._convertLight( node, groupParent )
                                        self.nodesMap[node] = model
                                        
                                groupParent.addChild( model )
                                self._createTransformForNode( model, groupParent )
                            
                        elif isinstance( node, SoShape ):
                                if node in self.nodesMap.keys( ):
                                        model = ModelNode( self._getMeshNameModel( node )[0],
                                                           groupParent,
                                                           resource = self.nodesMap[node].resource )
                                        self.modelNodes.append( model )
                                else:
                                        model = self._convertShape( node, groupParent )
                                        self.nodesMap[node] = model
                                
                                groupParent.addChild( model )
                                self._convertMaterialForModel( model, groupParent )
                                self._createTransformForNode( model, groupParent )
                                        
#------------------------------------------------------------------------
# "_translateByBBoxMidPoint"
#------------------------------------------------------------------------             
            
        def _translateByBBoxMidPoint( self ):

                #----- Calculate the Overall Bounding Box
                
                vp                  = SbViewportRegion( )
                bbox                = SoGetBoundingBoxAction( vp )
                bbox.apply( self.sceneGraph )
                xL,yL,zL,xR,yR,zR   = bbox.getBoundingBox( ).getBounds( )

                tx                      = ( xL + xR ) / 2
                ty                      = ( yL + yR ) / 2
                tz                      = ( zL + zR ) / 2

                self.center             = numarray.array( ( tx, ty, tz ) )
                self.bounds             = ( xR - xL, yR - yL, zR - zL ) 

                self.idtfRoot.tm        = [ [  1,  0,  0,  0 ],
                                            [  0,  1,  0,  0 ],
                                            [  0,  0,  1,  0 ],
                                            [ tx, ty, tz,  1 ] ]

#------------------------------------------------------------------------
# "_createAnimation"
#------------------------------------------------------------------------

        def _createAnimation( self ):

                step = 0
                frames = self.idtfRoot.children
                frames.reverse()
                
                for i in range( len( frames ) ):
                        frame = frames[i]
                        motResName = frame.name + 'MotResource-Key'
                        
                        if i != len( frames ) - 1 :
                                motRes = MotionResource( motResName, [step, step + self.timeStep], True )
                        else:
                                motRes = MotionResource( motResName, [step, step + self.timeStep] )
                                
                        self.motionResources.addResource( motRes )
                        
                        animMod = AnimationModifier( frame, motRes )
                        self.animationModifiers.append( animMod )

                        step += self.timeStep

#------------------------------------------------------------------------
# "_setRecursiveVisibility"
#------------------------------------------------------------------------        

        def _setRecursiveVisibile( self, parent ):

            for model in self.modelNodes:
                if model.parent == parent:
                    model.visibility = "BOTH"

            for group in self.groupNodes:
                if group.parent == parent:
                    self._setRecursiveVisibile( group )

#------------------------------------------------------------------------
# "_getNodeTypeString"
#------------------------------------------------------------------------ 

        def _getNodeTypeString( self, node ):

                if isinstance( node, GroupNode ):
                        return "Group"
                elif isinstance( node, LightNode ):
                        return "Light"
                elif isinstance( node, ViewNode ):
                        return "View"
                else:
                        return "Model"

#------------------------------------------------------------------------
# "_createNullDisplayNode"
#------------------------------------------------------------------------ 

        def _createNullDisplayNode( self,       name,
                                                parent,
                                                nodeType,
                                                prepend         = False ):

                if nodeType == "Group":                        
                        nodeList = self.groupNodes
                        node = GroupNode( name, parent )
                        
                elif nodeType == "Light":
                        nodeList = self.lightNodes
                        node = LightNode( name, parent )
                        
                elif nodeType == "View":
                        nodeList = self.viewNodes
                        node = ViewNode( name, parent ) 
                else:
                        nodeList = self.modelNodes
                        node = ModelNode( name, parent )

                if prepend:
                        nodeList.insert( 0, node )
                else:
                        nodeList.append( node )

                return node

#------------------------------------------------------------------------
# "_createDisplayControl"
#------------------------------------------------------------------------ 

        def _createDisplayControl( self ):

                self.displayNameMap  = []
                newNodeMap           = {}

                self.idtfRoot.name = "Time_Steps"
                displayRoot = self._createNullDisplayNode( "Display_Control", None, "Group", True )
                
                nodeList = self.idtfRoot.children # Instead of [self.idtfRoot] to remove time-step roots
                for child in self.idtfRoot.children:
                        newNodeMap[child] = displayRoot
                
                while len( nodeList ) != 0:
                        nameMap = {}		
                        initLen = len( nodeList )
                                
                        for i in range( initLen ):        # Breadth-First traverse
                                curNode = nodeList[i]
                                curParent = newNodeMap[curNode]
                                
                                for node in curNode.children:
                                        if node.name.find( "_" ) != -1:
                                                suffix = node.name[node.name.rindex( "_" ) + 1 : ]
                                                if suffix.isdigit( ):
                                                        name = node.name[ : node.name.rindex( "_" )]
                                                else:
                                                        name = node.name + "_Display"
                                        else:
                                                name = node.name + "_Display"
                                        if name in [row[0] for row in self.displayNameMap]:
                                                name += "_" + str( len( self.displayNameMap ) )
                                        
                                        if name not in nameMap.keys( ):                                                
                                                nameMap[name] = {       "Group" :[curParent, []],
                                                                        "Light"	:[curParent, []],
                                                                        "View"	:[curParent, []],
                                                                        "Model"	:[curParent, []]        }	
                                                
                                        nameMap[name][self._getNodeTypeString( node )][1].append( node )

                                        if isinstance( node, GroupNode ):
                                                nodeList.append( node )			
                      
                        nodeList = nodeList[initLen : ]
                       
                        newNameMap = {}	
                        
                        for name in nameMap.keys( ):
                                curName = nameMap[name]
                                
                                singleType = 0
                                whatType = ""
                                for nodeType in curName.keys( ):
                                        if len( curName[nodeType][1] ) != 0:
                                                singleType += 1
                                                whatType = nodeType
                                
                                if singleType == 1:
                                        newNameMap[name] = [curName[whatType][0], curName[whatType][1], whatType]				
                                else:
                                        for nodeType in curName.keys( ):
                                                if len( curName[nodeType][1] ) != 0:
                                                        newNameMap[name + "_" + nodeType] = [curName[nodeType][0], curName[nodeType][1], nodeType]
                                        
                        for name in newNameMap.keys( ):
                                parent, nodes, nodeType = newNameMap[name]			
                                newNode = self._createNullDisplayNode( name, parent, nodeType )

                                nnList = []
                                self.displayNameMap.append( [name, nnList] )
                                for n in nodes:
                                        newNodeMap[n] = newNode
                                        nnList.append( n.name ) 
                
#------------------------------------------------------------------------
# "_convertIV2IDTF"
#------------------------------------------------------------------------

        def _convertIV2IDTF( self ):

            self._convertIV2IDTFHelper( self.sceneGraph, None )

            #----- Only show the first animation frame at start-up
            
            if len( self.nameOfAnimationStepNodes ) != 0:                    
                for model in self.modelNodes:
                    model.visibility = "NONE"

                for group in self.groupNodes: 
                    if group.name == self.nameOfAnimationStepNodes[0]:
                        self._setRecursiveVisibile( group )
                        break

                if self.createDisplayControl:
                        self._createDisplayControl( )
            
            self._translateByBBoxMidPoint( )

            ### if self.animation == True:
            ###        self._createAnimation( )
        
#------------------------------------------------------------------------
# "_writeIdtfToFile"
#------------------------------------------------------------------------

        def _writeIdtfToFile( self, fileName ):

            dirName = os.path.dirname( fileName )
            if dirName and not os.path.exists( dirName ):
                os.makedirs( dirName )

            idtfFile = open( fileName, 'wt' )

            #----- Write IDTF Header
            
            idtfFile.write( 'FILE_FORMAT "IDTF"\n' )
            idtfFile.write( 'FORMAT_VERSION 100\n\n' )

            #----- Write IDTF Nodes

            for node in self.groupNodes:
                idtfFile.write( str( node ) )
            
            for node in self.viewNodes:
                idtfFile.write( str( node ) )

            for node in self.lightNodes:
                idtfFile.write( str( node ) )
                
            for node in self.modelNodes:
                idtfFile.write( str( node ) ) 

            #----- Write IDTF Resources
                
            idtfFile.write( str( self.viewResources ) )

            idtfFile.write( str( self.lightResources ) )

            idtfFile.write( str( self.modelResources ) )

            idtfFile.write( str( self.shaderResources ) )

            idtfFile.write( str( self.materialResources ) )

            idtfFile.write( str( self.motionResources ) )

            #----- Write IDTF Modifiers

            for modifier in self.animationModifiers:
                idtfFile.write( str( modifier ) )
                
            for modifier in self.shadingModifiers:
                idtfFile.write( str( modifier ) )

            #----- Close IDTF File

            idtfFile.flush( )
            idtfFile.close( )
            
#------------------------------------------------------------------------
# "saveAsIV"
#------------------------------------------------------------------------
                                
        def saveAsIV( self, fileName ):
                
                writeAction = SoWriteAction( )
                writeAction.getOutput( ).setBinary( False )
                
                writeAction.getOutput( ).openFile( fileName )
                writeAction.apply( self.sceneGraph )
                
                writeAction.getOutput( ).closeFile( )

#------------------------------------------------------------------------
# "saveAsVRML"
#------------------------------------------------------------------------

        def saveAsVRML( self, fileName ):

                vrml2Action = SoToVRML2Action( )   
                vrml2Action.apply( self.sceneGraph )
                vrml2SceneGraph = vrml2Action.getVRML2SceneGraph( )
                
                writeAction = SoWriteAction( )
                writeAction.getOutput( ).setBinary( False )
                
                writeAction.getOutput( ).openFile( fileName )
                writeAction.getOutput( ).setHeaderString( "#VRML V2.0 utf8" )
                writeAction.apply( vrml2SceneGraph )
                
                writeAction.getOutput( ).closeFile( )

#------------------------------------------------------------------------
# "saveAsIDTF"
#------------------------------------------------------------------------

        def saveAsIDTF( self, fileName ):

            self._convertIV2IDTF( )             
            self._writeIdtfToFile( fileName )

#========================================================================
#
# Test
#
#========================================================================

if __name__ == '__main__':
        
        conIdtf = AcuConvertIdtf( ivFileNames = 'HeatSinkMain.iv' )
        
        conIdtf.saveAsIV(   'HeatSink.iv'   )
        conIdtf.saveAsVRML( 'HeatSink.wrl'  )
        conIdtf.saveAsIDTF( 'HeatSink.idtf' )
        
