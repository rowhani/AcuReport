#===========================================================================
#
# Include files
#
#===========================================================================

from    iv      import   *

#===========================================================================
#
# Errors
#
#===========================================================================

acuSgClipShapeError   = "ERROR from acuSgClipShape module"

#===========================================================================
#
# "AcuSgClipShape": clip shape actor
#
#===========================================================================

class AcuSgClipShape( SoSeparator ):

     def __init__( self, sceneGraph,
                         actor,
                         clipShapeType,
                         clipSide            = 'up',
                         clipPlanePointList  = None,
                         clipBoxBoundList    = None,
                         name                = None ):

          SoSeparator.__init__( self )

          self.sceneGraph          = sceneGraph
          self.actor               = actor
          self.clipShapeType       = clipShapeType
          self.clipSide            = clipSide
          self.clipPlanePointList  = clipPlanePointList
          self.clipBoxBoundList    = clipBoxBoundList
          self.name                = name

          if self.name != None:
               self.setName( self.name )
               self.prefName       = self.name + "_"
          else:
               self.prefName       = ''

          self.planeList           = None
          self.pointList           = None
          self.activated           = False

          #----- Get the center of actor

          vp   = self.sceneGraph.viewer.getViewportRegion( )
          bbox = SoGetBoundingBoxAction( vp )
          bbox.apply( self.actor )
          xL, yL, zL, xR, yR, zR = bbox.getBoundingBox( ).getBounds( )
          cx   = 0.5 * ( xL + xR )
          cy   = 0.5 * ( yL + yR )
          cz   = 0.5 * ( zL + zR )
          self.center = SbVec3f( cx, cy, cz )

          #----- Create the clip shape

          if self.clipShapeType == 'plane':
               if self.clipPlanePointList == None:
                    raise acuSgClipShapeError, \
                          "No point exists for creating the clip plane."

               elif self.clipSide not in [ 'up', 'down' ]:
                    raise acuSgClipShapeError, \
                          "Invalid side for the clip plane."

               else:
                    self._addClipPlane( self.clipPlanePointList[0],
                                        self.clipPlanePointList[1],
                                        self.clipSide )

          elif self.clipShapeType == 'box':
               if self.clipBoxBoundList == None:
                    raise acuSgClipShapeError, \
                          "No bound exists for creating the clip box."

               else:
                    self._addClipBox( self.clipBoxBoundList[0],
                                      self.clipBoxBoundList[1],
                                      self.clipBoxBoundList[2],
                                      self.clipBoxBoundList[3],
                                      self.clipBoxBoundList[4],
                                      self.clipBoxBoundList[5] )

          else:
               raise acuSgClipShapeError, \
                     "Invalide type for the clip shape."

#---------------------------------------------------------------------------
# __deepcopy__
#---------------------------------------------------------------------------

     def __deepcopy__( self, memo ):

          return self

#---------------------------------------------------------------------------
# _createPlaneByMode
#---------------------------------------------------------------------------

     def _createPlaneByMode( self, center, direction, mode ):

          plane = SbPlane( direction, center )

          if mode == 'min':
               if plane.isInHalfSpace( self.center ):
                    plane = SbPlane( -direction, center )
                    return plane
               else:
                    return plane

          else:
               if plane.isInHalfSpace( self.center ):
                    return plane
               else:
                    plane = SbPlane( -direction, center )
                    return plane

#---------------------------------------------------------------------------
# _createClipPlane
#---------------------------------------------------------------------------

     def _createClipPlane( self, center, direction, side = 'up', mode = None ):

          direction = list( SbVec3f( direction ).getValue( ) )
          center    = list( SbVec3f( center ).getValue( ) )

          if direction[0] == 0 and direction[1] == 0 and direction[2] == 0:
               raise acuSgClipShapeError, \
                     "Clip Plane direction cannot be ( 0, 0, 0 )."

          for i in range( 3 ):
               if center[i] == self.center[i]:
                    center[i] -= 0.000001 * direction[i]

          direction = SbVec3f( direction )
          center    = SbVec3f( center )

          if mode != None:
               plane = self._createPlaneByMode( center, direction, mode )

          else:
               if side == 'up':
                    plane = SbPlane(  direction, center )
               else:
                    plane = SbPlane( -direction, center )

          clipPlane = SoClipPlane( )
          clipPlane.plane.setValue( plane )
          clipPlane.on.setValue( False )
          clipPlane.setName( '' )

          if mode == None:
               if self.pointList == None:
                    self.pointList = []
               self.pointList.append( ( center, direction ) )

          return clipPlane

#---------------------------------------------------------------------------
# _addClipPlane
#---------------------------------------------------------------------------

     def _addClipPlane( self, center, direction, side ):

          clipPlane = self._createClipPlane( center, direction, side )
          clipPlane.setName( self.prefName + "Single_Plane" )

          self.planeList = [ clipPlane, ]

          self.addChild( clipPlane )
          self.addChild( self.actor )

#---------------------------------------------------------------------------
# _addClipBox
#---------------------------------------------------------------------------

     def _addClipBox( self, xmin, xmax, ymin, ymax, zmin, zmax ):

          xmid = 0.5 * ( xmin + xmax )
          ymid = 0.5 * ( ymin + ymax )
          zmid = 0.5 * ( zmin + zmax )

          #----- Create Planes

          negXPlane = self._createClipPlane( ( xmax, ymid, zmid ),
                                             ( -1,  0,  0 ) )
          negXPlane.setName( self.prefName + "NEGX_Plane" )

          posXPlane = self._createClipPlane( ( xmin, ymid, zmid ),
                                             (  1,  0,  0 ) )
          posXPlane.setName( self.prefName + "POSX_Plane" )

          negYPlane = self._createClipPlane( ( xmid, ymax, zmid ),
                                             (  0, -1,  0 ) )
          negYPlane.setName( self.prefName + "NEGY_Plane" )

          posYPlane = self._createClipPlane( ( xmid, ymin, zmid ),
                                             (  0,  1,  0 ) )
          posYPlane.setName( self.prefName + "POSY_Plane" )

          negZPlane = self._createClipPlane( ( xmid, ymid, zmax ),
                                             (  0,  0, -1 ) )
          negZPlane.setName( self.prefName + "NEGZ_Plane" )

          posZPlane = self._createClipPlane( ( xmid, ymid, zmin ),
                                             (  0,  0,  1 ) )
          posZPlane.setName( self.prefName + "POSZ_Plane" )

          self.planeList = [ negXPlane, posXPlane,
                             negYPlane, posYPlane,
                             negZPlane, posZPlane ]

          #----- Add the Clip Box with Default Mode = max

          for plane in self.planeList:
               self.addChild( plane )
          self.addChild( self.actor )

#---------------------------------------------------------------------------
# prependClipPlane: Prepend a clip plane to the current clip shape
#---------------------------------------------------------------------------

     def prependClipPlane( self,   center,
                                   direction,
                                   side      = 'up',
                                   name      = None    ):

          '''
            Prepend a clip plane to the current clip shape

            Arguments:
                center      - A point in clip plane
                direction   - Direction of unclipped half-space
                side        - Side of the clip plane
                              ( 'up' [default] or 'down' )
                name        - Name of the clip plane

            Output:
                None
          '''

          clipPlane = self._createClipPlane( center, direction, side )
          if name != None:
               clipPlane.setName( self.prefName + name )
          if self.activated == True:
               clipPlane.on.setValue( True )

          self.planeList.insert( 0, clipPlane )

          self.insertChild( clipPlane, 0 )

#---------------------------------------------------------------------------
# setClipMode: Set the clipping mode of the clip shape
#---------------------------------------------------------------------------

     def setClipMode( self, mode = 'max' ):

          '''
            Set the clipping mode of the clip shape

            Arguments:
                mode    - mode of clipping ( 'max' [default] or 'min' )

            Output:
                None
          '''

          if mode not in [ 'min', 'max' ]:
               raise acuSgClipShapeError, "Invalid mode for clipping."

          self.removeAllChildren( )
          self.planeList = []

          for center, direction in self.pointList:
               clipPlane = self._createClipPlane( center,
                                                  direction,
                                                  mode = mode )
               self.planeList.append( clipPlane )

          if mode == 'max':
               for plane in self.planeList:
                    self.addChild( plane )
               self.addChild( self.actor )

          else:
               for plane in self.planeList:
                    planeSep = SoSeparator( )
                    planeSep.addChild( plane )
                    planeSep.addChild( self.actor )
                    self.addChild( planeSep )

          if self.activated == True:
               self.active( True )

#---------------------------------------------------------------------------
# active: Activate/Deactivate the clip shape
#---------------------------------------------------------------------------

     def active( self, activate = True ):

          '''
            Activate/Deactivate the clip shape

            Arguments:
                activate - If true, activates the clip shape;
                           deactivates it otherwise ( True [default], False )

            Output:
                None
          '''

          self.activated = activate

          for plane in self.planeList:
               plane.on.setValue( activate )

          self.sceneGraph._activeClipShape( self, activate )

#---------------------------------------------------------------------------
# delete: Remove the clip shape
#---------------------------------------------------------------------------

     def delete( self ):

          '''
            Remove the clip shape

            Arguments:
                None

            Output:
                None
          '''

          if self.clipShapeType == 'plane':
               self.sceneGraph.delClipPlane( self )

          else:
               self.sceneGraph.delClipBox( self )
