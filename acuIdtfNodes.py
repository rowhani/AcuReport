#===========================================================================
#
# Include files
#
#===========================================================================

import  random
import  types

#===========================================================================
#
# Errors
#
#===========================================================================

acuIdtfNodesError   = "ERROR from acuIdtfNodes module"

#========================================================================
#
# "Node" : Node superclass
#
#========================================================================

class Node:

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     name,
                                parent            = None,
                                tm                = None ):

                self.name       = name
                self.parent     = parent

                if tm == None:
                        self.tm = ( ( 1.0, 0.0, 0.0, 0.0 ),
                                    ( 0.0, 1.0, 0.0, 0.0 ),
                                    ( 0.0, 0.0, 1.0, 0.0 ),
                                    ( 0.0, 0.0, 0.0, 1.0 ) ) 
                else:
                        self.tm  = tm

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):

                if self.parent == None:
                        prName = '<NULL>'
                else:
                        prName = self.parent.name               
                      
                parentStr = ''
                parentStr += '\tNODE_NAME "' + self.name + '"\n'
                
                parentStr += '\tPARENT_LIST {\n'                     
                parentStr += '\t\tPARENT_COUNT 1\n'                  
                parentStr += '\t\tPARENT 0 {\n'                      
                parentStr += '\t\t\tPARENT_NAME "' + prName + '"\n'    
                parentStr += '\t\t\tPARENT_TM {\n'

                for tmRow in self.tm:
                        parentStr += '\t\t\t\t%.6f %.6f %.6f %.6f\n' % tuple( tmRow )
                 
                parentStr += '\t\t\t}\n\t\t}\n\t}\n'

                return parentStr
                   
#========================================================================
#
# "ViewNode" : View Node class
#
#========================================================================

class ViewNode( Node ):

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     name,
                                parent            = None,
                                tm                = None,
                                resource          = None,
                                viewType          = 'PERSPECTIVE',
                                viewProjection    = 34 ):

                Node.__init__( self, name, parent, tm )

                self.resource = resource
                self.viewType = viewType
                self.viewProjection = viewProjection
        
#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):

                if self.resource == None:
                    resName = 'NULL'
                else:
                    resName = self.resource.name

                viewStr = ''
                viewStr += 'NODE "VIEW" {\n'             
                
                viewStr += Node.__str__( self )
                
                viewStr += '\tRESOURCE_NAME "' + resName + '"\n'
                viewStr += '\tVIEW_DATA {\n'
                viewStr += '\t\tVIEW_TYPE "' + self.viewType + '"\n'
                viewStr += '\t\tVIEW_PROJECTION ' + str( self.viewProjection ) + '\n'
                viewStr += '\t}\n}\n\n'

                return viewStr

#========================================================================
#
# "GroupNode" : Group Node class
#
#========================================================================

class GroupNode( Node ):

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     name,
                                parent            = None,
                                tm                = None ):                                

                Node.__init__( self, name, parent, tm )

                self.children           = []                            

                self.currentMaterial    = None
                self.currentTransform   = None

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):                

                groupStr = ''
                groupStr += 'NODE "GROUP" {\n'             
                
                groupStr += Node.__str__( self )                
                
                groupStr += '}\n\n'

                return groupStr

#------------------------------------------------------------------------
# "addChild" : 
#------------------------------------------------------------------------

        def addChild( self,     node ):

                node.parent = self
                self.children.append( node )

#------------------------------------------------------------------------
# "getNumChildren" : 
#------------------------------------------------------------------------

        def getNumChildren( self ):

                return len( self.children )

#------------------------------------------------------------------------
# "replaceChild" : 
#------------------------------------------------------------------------

        def replaceChild( self, oldChild, newChild ):
       
                for i in range( self.getNumChildren() ):                       
                        if self.children[i] == oldChild:
                              self.children[i] = newChild
                              self.children[i].parent  = self
                              break

#========================================================================
#
# "ModelNode" : Model Node class
#
#========================================================================

class ModelNode( Node ):

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     name,
                                parent            = None,
                                tm                = None,
                                resource          = None,
                                visibility        = "BOTH"      ):                                

                Node.__init__( self, name, parent, tm )

                self.resource   = resource

                self.visibility = visibility

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):

                if self.resource == None:
                    resName = 'NULL'
                else:
                    resName = self.resource.name

                modelStr = ''
                modelStr += 'NODE "MODEL" {\n'             
                
                modelStr += Node.__str__( self )                
                
                modelStr += '\tRESOURCE_NAME "%s"\n'% resName
                modelStr += '\tMODEL_VISIBILITY "%s"\n' % self.visibility
                modelStr += '}\n\n'                         

                return modelStr

#========================================================================
#
# "LightNode" : Light Node class
#
#========================================================================

class LightNode( Node ):

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     name,
                                parent            = None,
                                tm                = None,
                                resource          = None ):                                

                Node.__init__( self, name, parent, tm )

                self.resource = resource

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):

                if self.resource == None:
                    resName = 'NULL'
                else:
                    resName = self.resource.name

                modelStr = ''
                modelStr += 'NODE "LIGHT" {\n'             
                
                modelStr += Node.__str__( self )                
                
                modelStr += '\tRESOURCE_NAME "' + resName + '"\n' 
                modelStr += '}\n\n'                         

                return modelStr

#========================================================================
#
# "Mesh" : Mesh class
#
#========================================================================

class Mesh:

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     meshType,
                                modelPositionList,
                                meshPositionList,
                                modelNormalList         = None,
                                meshNormalList          = None,
                                modelDiffuseColorList   = None,
                                meshDiffuseColorList    = None ):

                self.meshType = meshType
                
                #----- Model Position
                
                self.modelPositionList  = modelPositionList
                self.modelPositionCount = len( self.modelPositionList )

                #----- Mesh Position

                self.meshPositionList   = self._convertIndicesToTuples( meshPositionList )
                self.meshCount = len( self.meshPositionList )

                #----- Model Normal
                
                self.modelNormalList    = modelNormalList

                if self.modelNormalList != None:
                        self.modelNormalCount = len( self.modelNormalList )
                        
                        if ( self.meshType == "MESH" and self.modelNormalCount != self.meshCount * 3 ) \
                           or ( self.meshType != "MESH" and self.modelNormalCount != self.meshCount * 2 ):
                                raise acuIdtfNodesError, "Invalid model normal list length."
                       
                else:
                        self.modelNormalCount = 0                

                #----- Mesh Normal

                if meshNormalList != None:
                        self.meshNormalList = self._convertIndicesToTuples( meshNormalList )
                        if len( self.meshNormalList ) != self.meshCount:
                                raise acuIdtfNodesError, "Invalid mesh normal list length."                       
                else: 
                        if self.modelNormalList != None:
                                self.meshNormalList     = self.meshPositionList        #self._createMeshNormalList( )
                        else:
                                self.meshNormalList     = meshNormalList            

                #----- Model Diffuse Color
                
                if modelDiffuseColorList != None:
                        self.modelDiffuseColorList = self._convertRgbaToRgb( modelDiffuseColorList )
                        self.modelDiffuseColorCount = len( self.modelDiffuseColorList )
                else:
                        self.modelDiffuseColorList = modelDiffuseColorList
                        self.modelDiffuseColorCount = 0

                #----- Mesh Diffuse Color                                

                if meshDiffuseColorList != None:
                        self.meshDiffuseColorList = self._convertIndicesToTuples( meshDiffuseColorList )
                        if len( self.meshDiffuseColorList ) != self.meshCount:
                                raise acuIdtfNodesError, "Invalid mesh diffuse color list length."
                else:
                        if self.modelDiffuseColorList != None:                              
                                self.meshDiffuseColorList = self.meshPositionList
                        else:
                                self.meshDiffuseColorList = meshDiffuseColorList
                        
                #----- Mesh Shading List
                
                self.meshShadingList = []
                for i in range( self.meshCount ):
                        self.meshShadingList.append( [0] )                

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):          

                meshStr = ''

                meshStr += '\t\t' + self.meshType + ' {\n'

                #----- Write primitives
                
                if self.meshType == "MESH":                        
                        meshStr += '\t\t\tFACE_COUNT ' + str( self.meshCount ) + '\n'
                        meshTypeStr = 'MESH_FACE'
                else:
                        meshStr += '\t\t\tLINE_COUNT ' + str( self.meshCount ) + '\n'
                        meshTypeStr = 'LINE'
      
                meshStr += '\t\t\tMODEL_POSITION_COUNT ' + str( self.modelPositionCount ) + '\n'
                meshStr += '\t\t\tMODEL_NORMAL_COUNT ' + str( self.modelNormalCount ) + '\n'
                meshStr += '\t\t\tMODEL_DIFFUSE_COLOR_COUNT ' + str( self.modelDiffuseColorCount ) + '\n'
                meshStr += '\t\t\tMODEL_SPECULAR_COLOR_COUNT 0\n'
                meshStr += '\t\t\tMODEL_TEXTURE_COORD_COUNT 0\n'
                
                if self.meshType == "MESH":
                        meshStr += '\t\t\tMODEL_BONE_COUNT 0\n'
                        
                meshStr += '\t\t\tMODEL_SHADING_COUNT 1\n'                
                meshStr += '\t\t\tMODEL_SHADING_DESCRIPTION_LIST {\n'
                meshStr += '\t\t\t\tSHADING_DESCRIPTION 0 {\n'
                meshStr += '\t\t\t\t\tTEXTURE_LAYER_COUNT 0\n'
                meshStr += '\t\t\t\t\tSHADER_ID 0\n'
                meshStr += '\t\t\t\t}\n\t\t\t}\n'

                #----- Write mesh position list
                
                meshStr += '\t\t\t' + meshTypeStr + '_POSITION_LIST {\n'
                meshStr += self._getTupleListStr( self.meshPositionList, isIndex = True )               
                meshStr += '\t\t\t}\n'

                #----- Write mesh normal list
                
                if self.meshNormalList != None:                        
                        meshStr += '\t\t\t' + meshTypeStr + '_NORMAL_LIST {\n'
                        meshStr += self._getTupleListStr( self.meshNormalList, isIndex = True )                        
                        meshStr += '\t\t\t}\n'

                #----- Write mesh shading list                        
                
                meshStr += '\t\t\t' + meshTypeStr + '_SHADING_LIST {\n'
                meshStr += self._getTupleListStr( self.meshShadingList, isIndex = True )
                meshStr += '\t\t\t}\n'

                 #----- Write mesh diffuse color list

                if self.meshDiffuseColorList != None:                        
                        meshStr += '\t\t\t' + meshTypeStr + '_DIFFUSE_COLOR_LIST {\n'
                        meshStr += self._getTupleListStr( self.meshDiffuseColorList, isIndex = True )                       
                        meshStr += '\t\t\t}\n'

                #----- Write model position list
                        
                meshStr += '\t\t\tMODEL_POSITION_LIST {\n'  
                meshStr += self._getTupleListStr( self.modelPositionList )     #isCoords = True          
                meshStr += '\t\t\t}\n'

                #----- Write model normal list
                
                if self.modelNormalList != None:
                        meshStr += '\t\t\tMODEL_NORMAL_LIST {\n'                        
                        meshStr += self._getTupleListStr( self.modelNormalList )                      
                        meshStr += '\t\t\t}\n'

                #----- Write model diffuse color list
                        
                if self.modelDiffuseColorList != None:
                        meshStr += '\t\t\tMODEL_DIFFUSE_COLOR_LIST {\n'
                        meshStr += self._getTupleListStr( self.modelDiffuseColorList, isRGBA = True )
                        meshStr += '\t\t\t}\n'                       

                meshStr += '\t\t}\n'

                return meshStr

#------------------------------------------------------------------------
# "_getTupleListStr" : 
#------------------------------------------------------------------------

        def _getTupleListStr( self,     tupleList,
                                        isIndex         = False,
                                        isRGBA          = False,
                                        isCoords        = False ):

                tupStr = ''                

                for tup in tupleList:
                        if isCoords:
                                tupStr += '\t\t\t\t% .6f % .6f % .6f\n' % ( -tup[0], tup[2], tup[1] )
                                
                        elif isIndex:
                                tupStr += '\t\t\t\t'
                                for t in tup:
                                        tupStr += str( t ) + ' '
                                tupStr += '\n'
                                
                        elif isRGBA:
                                tupStr += '\t\t\t\t% .6f % .6f % .6f % .6f\n' % tuple( tup )
                                
                        else:        
                                tupStr += '\t\t\t\t% .6f % .6f % .6f\n' % tuple( tup )                                

                return tupStr
        
#------------------------------------------------------------------------
# "_convertIndicesToTuples" : 
#------------------------------------------------------------------------

        def _convertIndicesToTuples( self,  meshPositionList ):

                meshList = []

                #----- Separate indices by -1
                
                indexList = []
                for inx in meshPositionList:
                        if inx != -1:
                                indexList.append( inx )

                        # Check the final extra -1 
                        elif len( indexList ) != 0:                              
                                meshList.append( indexList )    
                                indexList = []
                if inx != -1:
                    meshList.append( indexList )
                                
                #----- Convert each index list into a triple list
                
                tripleFaceInx = []
                
                for inxRow in meshList:
                        irLen = len( inxRow )
                        
                        if irLen == 1:
                                tripleFaceInx.append( [ inxRow[0] ] )
                        elif irLen == 2:
                                tripleFaceInx.append( [ inxRow[0], inxRow[1] ] )
                        else:
                                lastTriple = [ inxRow[0], inxRow[1], inxRow[2] ]
                                tripleFaceInx.append( lastTriple )
                                for i in range( 3, irLen ):
                                        lastTriple = [ lastTriple[0], lastTriple[2], inxRow[i] ]
                                        tripleFaceInx.append( lastTriple )
                                        
                return tripleFaceInx

#------------------------------------------------------------------------
# "_convertRgbaToRgb" : 
#------------------------------------------------------------------------

        def _convertRgbaToRgb( self,  modelDiffuseColorList ):

                rgbList = []
                for rgba in modelDiffuseColorList:
                        R = ( ( rgba & 0xff000000 ) >> 24 ) / 255.0
                        G = ( ( rgba & 0x00ff0000 ) >> 16 ) / 255.0
                        B = ( ( rgba & 0x0000ff00 ) >>  8 ) / 255.0
                        A = ( ( rgba & 0x000000ff )       ) / 255.0
                        #rgbList.append( [ R, G, B, A ] ) Probabily wrong order
                        rgbList.append( [ B, G, R, A ] )

                return rgbList

#------------------------------------------------------------------------
# "_createMeshNormalList" : 
#------------------------------------------------------------------------

        def _createMeshNormalList( self ):

                meshNormalList = []
                counter = 0

                for i in range( len( self.meshPositionList ) ):
                        normals = []
                        for j in range( len( self.meshPositionList[i] ) ):
                                normals.append( counter )
                                counter += 1
                        meshNormalList.append( normals )                 
                        
                return meshNormalList        

#========================================================================
#
# "Resource" : Resource superclass
#
#========================================================================

class Resource:

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     name ):

                self.name       = name
                self.index      = 0

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):

                resStr = ''
                resStr += '\tRESOURCE ' + str( self.index ) + ' {\n'
                resStr += '\t\tRESOURCE_NAME "' + self.name + '"\n'

                return resStr

#------------------------------------------------------------------------
# "setIndex" : 
#------------------------------------------------------------------------               

        def setIndex( self, index ):

                self.index = index

#========================================================================
#
# "ModelResource" : Model Resource class
#
#========================================================================

class ModelResource( Resource ):

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     name,
                                modelType,
                                modelData ):

                Resource.__init__( self, name )
                
                self.modelType          = modelType
                self.modelData          = modelData

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):

                resModStr = ''
                resModStr += Resource.__str__( self )
                
                resModStr += '\t\tMODEL_TYPE "' + self.modelType + '"\n'
                resModStr += str( self.modelData )

                resModStr += '\t}\n'

                return resModStr

#========================================================================
#
# "LightResource" : Light Resource class
#
#========================================================================

class LightResource( Resource ):

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     name,
                                lightType,
                                lightIntensity,
                                lightSpotAngle = None ):

                Resource.__init__( self, name )
                
                self.lightType          = lightType
                self.lightIntensity     = lightIntensity
                self.lightSpotAngle     = lightSpotAngle

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):

                resModStr = ''
                resModStr += Resource.__str__( self )
                
                resModStr += '\t\tLIGHT_TYPE "' + self.lightType + '"\n'
                resModStr += '\t\tLIGHT_COLOR 1.000000 1.000000 1.000000\n'                
                resModStr += '\t\tLIGHT_ATTENUATION 1.000000 0.000000 0.000000\n'
                if self.lightType == 'SPOT':
                        resModStr += '\t\tLIGHT_SPOT_ANGLE %.6f\n' % self.lightSpotAngle 
                resModStr += '\t\tLIGHT_INTENSITY %.6f\n' % self.lightIntensity
                
                resModStr += '\t}\n'

                return resModStr

#========================================================================
#
# "MaterialResource" : Material Resource class
#
#========================================================================

class MaterialResource( Resource ):

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     name,
                                diffuseColor    = None,
                                transparency    = 0.0   ):

                Resource.__init__( self, name )

                if diffuseColor == None:
                        self.diffuseColor = ( random.random(), random.random(), random.random() )
                elif type( diffuseColor ) == types.ListType:
                        self.diffuseColor = tuple( self.diffuseColor )
                else:
                        self.diffuseColor = diffuseColor

                if name == None: # dummy material
                        self.opacity = transparency
                else:
                        self.opacity = 1.0 - transparency

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):

                resMatStr = ''
                resMatStr += Resource.__str__( self )

                resMatStr += '\t\tMATERIAL_AMBIENT 0 0 0\n'                  
                resMatStr += '\t\tMATERIAL_DIFFUSE %.6f %.6f %.6f\n' % tuple( self.diffuseColor )
                resMatStr += '\t\tMATERIAL_SPECULAR 0 0 0\n'                 
                resMatStr += '\t\tMATERIAL_EMISSIVE 0 0 0\n'                 
                resMatStr += '\t\tMATERIAL_REFLECTIVITY 0.100000\n'          
                resMatStr += '\t\tMATERIAL_OPACITY %.6f\n' % self.opacity
                
                resMatStr += '\t}\n'   

                return resMatStr 

#========================================================================
#
# "ShaderResource" : Shader Resource class
#
#========================================================================

class ShaderResource( Resource ):

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     name,
                                materialResource ):

                Resource.__init__( self, name )
                
                self.materialResource  = materialResource

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):

                resShadStr = ''
                resShadStr += Resource.__str__( self )

                resShadStr += '\t\tSHADER_MATERIAL_NAME "' + self.materialResource.name + '"\n' 
                resShadStr += '\t\tSHADER_ACTIVE_TEXTURE_COUNT 0\n'                   

                resShadStr += '\t}\n'   

                return resShadStr

#========================================================================
#
# "MotionResource" : Motion Resource class
#
#========================================================================

class MotionResource( Resource ):

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     name,
                                keyFrameTimes   = [0],
                                hide            = False):

                Resource.__init__( self, name )
                
                self.keyFrameTimes      = keyFrameTimes
                self.hide               = hide

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):

                resMotStr = ''
                resMotStr += Resource.__str__( self )

                resMotStr += '\t\tMOTION_TRACK_COUNT 1\n'
                resMotStr += '\t\tMOTION_TRACK_LIST {\n'
                resMotStr += '\t\t\tMOTION_TRACK 0 {\n'
                resMotStr += '\t\t\t\tMOTION_TRACK_NAME "' + self.name + '-Track"\n'
                resMotStr += '\t\t\t\tMOTION_TRACK_SAMPLE_COUNT %d\n' %len( self.keyFrameTimes )
                resMotStr += '\t\t\t\tKEY_FRAME_LIST {\n'

                for i in range( len( self.keyFrameTimes ) ):
                        keyFrame = self.keyFrameTimes[i]
                        resMotStr += '\t\t\t\t\tKEY_FRAME %d {\n' %i
                        resMotStr += '\t\t\t\t\t\tKEY_FRAME_TIME %.1f\n' %keyFrame
                        resMotStr += '\t\t\t\t\t\tKEY_FRAME_DISPLACEMENT 0.0 0.0 0.0\n'
                        resMotStr += '\t\t\t\t\t\tKEY_FRAME_ROTATION 1.0 0.0 0.0 0.0\n'

                        if self.hide and i == len( self.keyFrameTimes ) - 1:
                                resMotStr += '\t\t\t\t\t\tKEY_FRAME_SCALE 0.0 0.0 0.0\n'
                        else:
                                resMotStr += '\t\t\t\t\t\tKEY_FRAME_SCALE 1.0 1.0 1.0\n'
                                
                        resMotStr += '\t\t\t\t\t}\n'
                        
                resMotStr += '\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n'               

                return resMotStr 

#========================================================================
#
# "ResourceCollection" : Resource Collection class
#
#========================================================================

class ResourceCollection:

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     resourceType,
                                resources         = None ):

                self.resourceType       = resourceType

                if resources == None:
                        self.resources  = []
                else:
                        self.resources  =  resources                

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):

                resColStr = ''

                if len( self.resources ) == 0:
                        return resColStr

                resColStr += 'RESOURCE_LIST "' + self.resourceType + '" {\n'
                resColStr += '\tRESOURCE_COUNT ' + str( len( self.resources ) ) + '\n'

                for i in range( len( self.resources ) ):
                        resource = self.resources[i]
                        resource.setIndex( i )
                        resColStr += str( resource )
                
                resColStr += '}\n\n'                         

                return resColStr

#------------------------------------------------------------------------
# "addResource" : 
#------------------------------------------------------------------------

        def addResource( self,  resource ):

                self.resources.append( resource )

#========================================================================
#
# "AnimationModifier" : Animation Modifier class
#
#========================================================================

class AnimationModifier:

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     model,
                                animationResource ):

                self.model              = model
                self.animationResource  = animationResource

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):

                modAnimStr = ''
                modAnimStr += 'MODIFIER "ANIMATION" {\n'                                   
                modAnimStr += '\tMODIFIER_NAME "' + self.model.name + '"\n'
                modAnimStr += '\tPARAMETERS {\n'
                modAnimStr += '\t\tATTRIBUTE_ANIMATION_PLAYING "TRUE"\n'
                modAnimStr += '\t\tATTRIBUTE_ROOT_BONE_LOCKED "FALSE"\n'
                modAnimStr += '\t\tATTRIBUTE_SINGLE_TRACK "TRUE"\n'
                modAnimStr += '\t\tATTRIBUTE_AUTO_BLEND "TRUE"\n'
                modAnimStr += '\t\tTIME_SCALE 1.0\n'
                modAnimStr += '\t\tBLEND_TIME 0.5\n'
                modAnimStr += '\t\tMOTION_COUNT 1\n'
                modAnimStr += '\t\tMOTION_INFO_LIST {\n'
                modAnimStr += '\t\t\tMOTION_INFO 0 {\n'
                modAnimStr += '\t\t\t\tMOTION_NAME "' + self.animationResource.name + '"\n'
                modAnimStr += '\t\t\t\tATTRIBUTE_LOOP "TRUE"\n'
                modAnimStr += '\t\t\t\tATTRIBUTE_SYNC "FALSE"\n'
                modAnimStr += '\t\t\t\tTIME_OFFSET 0.0\n'
                modAnimStr += '\t\t\t\tTIME_SCALE 1.0\n'
                
                modAnimStr += '\t\t\t}\n\t\t}\n\t}\n}\n\n' 

                return modAnimStr

#========================================================================
#
# "ShadingModifier" : Shading Modifier class
#
#========================================================================

class ShadingModifier:

#------------------------------------------------------------------------
# "__init__" : 
#------------------------------------------------------------------------
        
        def __init__( self,     model,
                                shaderResource ):

                self.model              = model
                self.shaderResource     = shaderResource

#------------------------------------------------------------------------
# "__str__" : 
#------------------------------------------------------------------------

        def __str__( self ):

                modShadStr = ''
                modShadStr += 'MODIFIER "SHADING" {\n'                                   
                modShadStr += '\tMODIFIER_NAME "' + self.model.name + '"\n'
                modShadStr +=  '\tPARAMETERS {\n'                      
                modShadStr += '\t\tSHADER_LIST_COUNT 1\n'             
                modShadStr += '\t\tSHADER_LIST_LIST {\n'              
                modShadStr += '\t\t\tSHADER_LIST 0 {\n'               
                modShadStr += '\t\t\t\tSHADER_COUNT 1\n'              
                modShadStr += '\t\t\t\tSHADER_NAME_LIST {\n'          
                modShadStr += '\t\t\t\t\tSHADER 0 NAME: "' + self.shaderResource.name + '"\n'
                
                modShadStr += '\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}\n\n' 

                return modShadStr
                
#========================================================================
#
# Test
#
#========================================================================

if __name__ == '__main__':
        
        print ShadingModifier ( ModelNode ( "Model" ),
                                ShaderResource( "Shader", MaterialResource( "Mat" ) ) )
        print Mesh( [[1,1,1]], [[2,2,2]] )
