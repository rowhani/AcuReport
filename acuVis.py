#===========================================================================
#
# Include files
#
#===========================================================================

import  os
import  sys
import  math
import  glob
import  acupu
import  acuQt
import  types
import  acuprj
import  acuiso
import  acuisl
import  string
import  numarray
import  acudb2          as      acudb

from    qt              import  *
from    iv              import  SoQt

from    acuAnim         import  AcuAnim
from    acuSgIso        import  AcuSgIso
from    acuSgCpl        import  AcuSgCpl
from    acuSgTufts      import  AcuSgTufts
from    acuItemObj      import  AcuItemObj
from    acuSgIsoLine    import  AcuSgIsoLine
from    acuSceneGraph   import  AcuSceneGraph
from    acuAnim         import  AcuAnim

#===========================================================================
#
# Errors
#
#===========================================================================

acuVisError   = "ERROR from acuVis module"

#===========================================================================
#
# _adbSets
#
#===========================================================================

_adbSets = [
    (	        'nOsfs',	'osfName',	'osfCnn',	        ),
    (	        'nCbcs',	'cbcName',	'cbcCnn',               ),
    (	        'nSsis',	'ssiName',	'ssiCnn',               ),
    (	        'nEcis',	'eciName',	'eciCnn',               ),
    (	        'nEbcs',	'ebcName',	'ebcCnn',	        ),
    (	        'nSbcs',	'sbcName',	'sbcCnn',               ),
    (	        'nAfss',	'afsName',	'afsCnn',               ),
    (	        'nTwss',	'twsName',	'twsCnn',               ),
    (	        'nRsfs',	'rsfName',	'rsfCnn',               ),
    (	        'nPsfs',	'psfName',	'psfCnn',               ),
    (	        'nSrss',	'srsName',	'srsCnn',               ),
    (	        'nGsfs',	'gsfName',	'gsfCnn',               ),

]

#===========================================================================
#
# _imgFileFormat :  Image file formats
#
#===========================================================================

_imgFileFormat = [      ('PNG','png'),  ('GIF','gif'),
                        ('JPG','jpeg'), ('Post Script','ps'),
                        ('IV','iv'),    ('VRML','wrl')                  ]

#===========================================================================
#
# _modelsInfo :  Default info for different models
#
#===========================================================================

_modelsDefInfo = { # displayType, visibility, transparency, transValue
                   # color, topology, state
    'Volumes'   :( 'solid', True, False, 0.5, QColor(   255, 0,     128 ),
                   'four_node_tet'                                      ),
    'Surfaces'  :( 'solid', True,  False, 0.5, QColor(  255, 0,     0   ),
                  'three_node_triangle'                                 ),
    'Nodes'     :( 'point', False, False, 0.5, QColor(  0,   255,   255 ),
                   'point'                                              ),
    'Periodics' :( 'solid', False, False, 0.5, QColor(  0,   128,   0   ),
                   'line'                                               ),
}

#===========================================================================
#
# "AcuVis":  AcuVis post processing package
#
#===========================================================================

class AcuVis:

    '''
        AcuVis post processing package.
    '''

    def __init__(   self,   problem,    dir = 'ACUSIM.DIR', run = 0,
                    outPutDir   = '.'                                   ):
        '''
	    Arguments:
	        problem	    - AcuSolve solved problem
	        dir	    - Working directory
	        run         - Run ID
	    Output:
	        None
        '''

	if not problem:
            raise acuVisError, "Problem is not defined"

        if not os.path.exists(      dir     ):
            raise acuVisError, "Working directory does not exist"

        self.problem    = problem

        parent          = SoQt.init(	        sys.argv[0]		)

        acuQt.initSettings(                     'acuVis'                )

        self.asg        = AcuSceneGraph(        parent,     None        )
        self.asg.viewer.bgColor(                0.78,       0.78,   0.78)

        self.adb        = acudb.Acudb(          problem,    dir,    0   )
        self.adb.openRun(                       run                     )

        self.outPutDir      = outPutDir
        if not os.path.exists( outPutDir ):
            os.makedirs(                        outPutDir               )

        self.step           = 0
        self.stepId         = 0
        self.sclrId         = 0
        self.vecId          = 0
        self.cplActors      = []
        self.isoActors      = []
        self.isoLnActors    = []
        self.tuftActors     = []
        self.steps          = []
        self.sclrVarNames   = []
        self.vecVarNames    = []
        self.aleId          = None
        self.varValues      = {}

        # Check the list of variables for initializing aleId

        self.getNSteps(                                                 )
        self.getNVars(                                                  )
        self.getNSclrVars(                                              )
        self.getNVecVars(                                               )
        if "mesh_displacement" in self.varNames:
            self.aleId  = self.varNames.index(   "mesh_displacement"    )

        if self.aleId   == None:
            self.aleId  = -1

        self.refCrd     = self.adb.get(         "crd"                   )
        self.crd        = self.refCrd

        self.populateVols(                                              )
        self.populateSrfs(                                              )
        self.populateNbcs(                                              )
        self.populatePbcs(                                              )

        self.home(                                                      )

#---------------------------------------------------------------------------
# populateVols: Populate the Scene Graph with Volumes
#---------------------------------------------------------------------------

    def populateVols( self ):
        '''
	    Populate the Scene Graph with Volumes actors
	
	    Arguments:
	        None

	    Output:
	        None
        '''

        self.usrIds     = self.adb.get(         "usrIds"                )
        self.invMap     = acupu.getInvMap(      self.usrIds             )

        nElms	        = self.adb.get(         "nElms"                 )
        self.elmNames	= []
        self.elmMap	= {}
        self.elmActors	= []
        self.elmCnns    = {}
        self.isos       = {}

        info            = _modelsDefInfo[       'Volumes'               ]

        for i in range( nElms ):
            name	= self.adb.get(         "elmName",  i           )
            cnn		= self.adb.get(         "elmCnn",   i           )
            cnn		= acupu.invMap(         self.invMap,cnn         )
            self.elmCnns[ name ]= cnn
            self.elmNames.append(	        name	                )
            self.elmMap[name]   = i

            item        = AcuItemObj(           name,       info[0],
                                                info[1],    info[2],
                                                info[3],    info[4]     )

            actor	= self.asg.addVolSet(   self.crd,
                                                cnn,
                                                info[5],
                                                item,
                                                None,
                                                'mesh'                  )
            self.elmActors.append(              actor                   )

            self.isos[name] = acuiso.Acuiso(    self.usrIds, self.crd,
                                                cnn                     )

#---------------------------------------------------------------------------
# populateSrfs: Populate the Scene Graph with Surfaces
#---------------------------------------------------------------------------

    def populateSrfs( self ):
        '''
	    Populate the Scene Graph with Surfaces actors
	
	    Arguments:
	        None

	    Output:
	        None
        '''

        self.srfCksum	= {}
        self.srfActors	= []
        self.srfNames	= []
        self.srfMap	= {}
        self.srfCnns    = {}

        self.isoLns     = {}

        info            = _modelsDefInfo[       'Surfaces'              ]

        for item in _adbSets:
            nSrfsTag	= item[0]
            srfNameTag  = item[1]
            srfCnnTag	= item[2]

            nSrfs       = self.adb.get(         nSrfsTag                )

            for i in range(nSrfs):
                name	= self.adb.get(         srfNameTag, i           )
                cnn     = self.adb.get(         srfCnnTag,  i           )
                cnn	= acupu.invMap(         self.invMap,cnn         )
                self.srfCnns[ name ]= cnn
                cksum	= acupu.cksumArray(     cnn                     )
                shape	= cnn.shape
                if self.srfCksum.has_key( (shape, cksum) ):
                    continue
                self.srfCksum[ shape,cksum ]   = 1

                self.srfNames.append(	        name	                )
                self.srfMap[name]   = i

                item    = AcuItemObj(           name,       info[0],
                                                info[1],    info[2],
                                                info[3],    info[4]     )

                actor	= self.asg.addSrfSet(   self.crd,
                                                cnn,
                                                info[5],
                                                item,
                                                None,
                                                'mesh'                  )
                self.srfActors.append(          actor                   )

                self.isoLns[name] = acuisl.Acuisl(  self.usrIds, self.crd,
                                                    cnn                 )

#---------------------------------------------------------------------------
# populateNbcs: Populate the Scene Graph with Nodes
#---------------------------------------------------------------------------

    def populateNbcs( self ):
        '''
	    Populate the Scene Graph with Nodes actors
	
	    Arguments:
	        None

	    Output:
	        None
        '''

        nNbcs	        = self.adb.get(         "nNbcs"                 )

        self.nbcActors	= []
        self.nbcNames	= []
        self.nbcMap	= {}

        info            = _modelsDefInfo[       'Nodes'                 ]

        for i in range( nNbcs ):
            name	= self.adb.get(         "nbcName",  i           )
            cnn		= self.adb.get(         "nbcNodes", i           )

            self.nbcNames.append(	        name	                )
            self.nbcMap[name]   = i

            item        = AcuItemObj(           name,       info[0],
                                                info[1],    info[2],
                                                info[3],    info[4]     )

            actor	= self.asg.addPntSet(   self.crd,
                                                cnn,
                                                info[5],
                                                item,
                                                'mesh'                  )
            self.nbcActors.append(              actor                   )

#---------------------------------------------------------------------------
# populatePbcs: Populate the Scene Graph with Periodics
#---------------------------------------------------------------------------

    def populatePbcs( self ):
        '''
	    Populate the Scene Graph with Periodics actors
	
	    Arguments:
	        None

	    Output:
	        None
        '''

        nPbcs	= self.adb.get(                 "nPbcs"                 )

        self.pbcActors	= []
        self.pbcNames	= []
        self.pbcMap	= {}

        info            = _modelsDefInfo[       'Periodics'             ]

        for i in range( nPbcs ):
            name	= self.adb.get(         "pbcName",  i           )
            cnn		= self.adb.get(         "pbcPairs", i           )

            self.pbcNames.append(	        name	                )
            self.pbcMap[name]   = i

            item        = AcuItemObj(           name,       info[0],
                                                info[1],    info[2],
                                                info[3],    info[4]     )

            actor	= self.asg.addLinSet(   self.crd,
                                                cnn,
                                                info[5],
                                                item,
                                                'mesh'                  )
            self.pbcActors.append(              actor                   )

#---------------------------------------------------------------------------
# saveImage: Save the image of the screen in a file
#---------------------------------------------------------------------------

    def saveImage( self, width = 600, height = 400, fileName = None,
                   fileType = 'png', dirName = None                     ):
        '''
	    Save the image of the screen in a file
	
	    Arguments:
	        width       - Width of image
	        height      - Height of image
	        fileName    - Image file name
	        fileType    - Image type( png, bmp, jpg, ... )
	        dirName     - The directory that image will be saved in it

	    Output:
	        fileName    - Saved image file name
        '''

        if not dirName:
            dirName     = self.outPutDir
        if dirName and not os.path.exists( dirName ):
            os.makedirs(                        dirName                 )
        self.dirName    = dirName

        if not fileName:
            prefix      = "Image_"
            suffix      = '.' + fileType
            indx	= self.getMaxFileInd(	prefix, suffix		)
            fileName    = prefix + str( indx + 1) + suffix

            fileName    = os.path.join(     dirName, fileName           )

        else:
            fileName    = os.path.join(     dirName, fileName           )
            fileInfo    = QFileInfo(        fileName                    )
            fileType    = str( QFileInfo(fileName).extension( False)    )
        self.asg.saveFile(          fileName,   fileType,
                                    width,      height                  )

        return fileName

#---------------------------------------------------------------------------
# getMaxFileInd
#---------------------------------------------------------------------------

    def getMaxFileInd( self, prefix, suffix ):
	""" Get maximum index of existing image files
	    Arguments:
	        prefix		-	string value of prefix
		suffix		-	string value of suffix
	    Output:
	        index		-	int value of the max index

		If there are no files matching the pattern, returns -1	
	"""

	ind	= -1
	maxInd	= -1

	searchStr	= str(prefix) + '*[0-9]' + str(suffix)

	fileList	= glob.glob( os.path.join(self.dirName,
                                                  searchStr	    )	)

	if len( fileList ) == 0:
	    return -1

	for mFile in fileList:
	    preFile = string.split(	mFile, str( prefix )		)
	    if len( preFile ) == 2:
	        sufFile = string.split(		preFile[1], str(suffix)	)
		if len(sufFile) == 2:
		    try:
		        ind = int( sufFile[0] )
			if ind > maxInd:
			    maxInd = ind
		    except:
		        pass
	return maxInd

#---------------------------------------------------------------------------
# getNVols: Return the number of Volumes
#---------------------------------------------------------------------------

    def getNVols( self  ):
        '''
	    Return the number of Volumes
	
	    Arguments:
	        None

	    Output:
	        nVols   - Number of Volumes
        '''

        return len(                     self.elmMap.keys()              )

#---------------------------------------------------------------------------
# getNSrfs: Return the number of Surfaces
#---------------------------------------------------------------------------

    def getNSrfs( self  ):
        '''
	    Return the number of Surfaces
	
	    Arguments:
	        None

	    Output:
	        nSrfs   - Number of Surfaces
        '''

        return len(                     self.srfMap.keys()              )

#---------------------------------------------------------------------------
# getNNbcs: Return the number of Nodes
#---------------------------------------------------------------------------

    def getNNbcs( self  ):
        '''
	    Return the number of Nodes
	
	    Arguments:
	        None

	    Output:
	        nNbcs   - Number of Nodes
        '''

        return len(                     self.nbcMap.keys()              )

#---------------------------------------------------------------------------
# getNPbcs: Return the number of Periodics
#---------------------------------------------------------------------------

    def getNPbcs( self  ):
        '''
	    Return the number of Periodics
	
	    Arguments:
	        None

	    Output:
	        nPbcs   - Number of Periodics
        '''

        return len(                     self.pbcMap.keys()              )

#---------------------------------------------------------------------------
# getVolName: Return the name of a volume
#---------------------------------------------------------------------------

    def getVolName( self, volId  ):
        '''
	    Return the Name of a volume
	
	    Arguments:
	        volId   - Volume Id

	    Output:
	        volName - Volume name corresponding to the volume id
        '''

        volName = None

        for key, value in  self.elmMap.items():
            if volId    == value:
                volName = key
                break

        if not volName:
            raise acuVisError, "Invalid volume id"

        return volName

#---------------------------------------------------------------------------
# getSrfName: Return the name of a surface
#---------------------------------------------------------------------------

    def getSrfName( self, srfId  ):
        '''
	    Return the Name of a surface
	
	    Arguments:
	        srfId   - Surface Id

	    Output:
	        srfName - Surface name corresponding to the surface id
        '''

        srfName = None

        for key, value in  self.srfMap.items():
            if srfId    == value:
                srfName = key
                break

        if not srfName:
            raise acuVisError, "Invalid surface id"

        return srfName

#---------------------------------------------------------------------------
# getNbcName: Return the name of a Node
#---------------------------------------------------------------------------

    def getNbcName( self, nbcId  ):
        '''
	    Return the Name of a node
	
	    Arguments:
	        nbcId   - Node Id

	    Output:
	        nbcName - Node name corresponding to the node id
        '''

        nbcName = None

        for key, value in  self.nbcMap.items():
            if nbcId    == value:
                nbcName = key
                break

        if not nbcName:
            raise acuVisError, "Invalid node id"

        return nbcName

#---------------------------------------------------------------------------
# getPbcName: Return the name of a Periodic
#---------------------------------------------------------------------------

    def getPbcName( self, pbcId  ):
        '''
	    Return the Name of a periodic
	
	    Arguments:
	        pbcId   - Periodic Id

	    Output:
	        pbcName - Periodic name corresponding to the periodic id
        '''

        pbcName = None

        for key, value in  self.pbcMap.items():
            if pbcId    == value:
                pbcName = key
                break

        if not pbcName:
            raise acuVisError, "Invalid periodic id"

        return pbcName

#---------------------------------------------------------------------------
# getVolActor: Return a volume actor
#---------------------------------------------------------------------------

    def getVolActor( self, volInfo  ):
        '''
	    Return a volume actor
	
	    Arguments:
	        volInfo     - Volume Name or Id

	    Output:
	        volActor    - Volume actor corresponding to the volInfo
        '''

        if type( volInfo )  == types.IntType and \
           volInfo in range(len(self.elmActors)):
            volActor        = self.elmActors[       volInfo             ]
        elif type( volInfo )== types.StringType and \
             self.elmMap.has_key( volInfo ):
            volId           = self.elmMap[          volInfo             ]
            volActor        = self.elmActors[       volId               ]
        else:
            raise acuVisError, "Invalid name or id for volume."

        return volActor

#---------------------------------------------------------------------------
# getSrfActor: Return a surface actor
#---------------------------------------------------------------------------

    def getSrfActor( self, srfInfo  ):
        '''
	    Return a surface actor
	
	    Arguments:
	        srfInfo     - Surface Name or Id

	    Output:
	        srfActor    - Surface actor corresponding to the srfInfo
        '''

        if type( srfInfo )  == types.IntType and \
           srfInfo in range(len(self.srfActors)):
            srfActor        = self.srfActors[       srfInfo             ]
        elif type( srfInfo )== types.StringType and \
             self.srfMap.has_key( srfInfo ):
            srfId           = self.srfMap[          srfInfo             ]
            srfActor        = self.srfActors[       srfId               ]
        else:
            raise acuVisError, "Invalid name or id for surface."

        return srfActor

#---------------------------------------------------------------------------
# getNbcActor: Return a Node actor
#---------------------------------------------------------------------------

    def getNbcActor( self, nbcInfo  ):
        '''
	    Return a Node actor
	
	    Arguments:
	        nbcInfo     - Node Name or Id

	    Output:
	        nbcActor    - Node actor corresponding to the nbcInfo
        '''

        if type( nbcInfo )  == types.IntType and \
           nbcInfo in range(len(self.nbcActors)):
            nbcActor        = self.nbcActors[       nbcInfo             ]
        elif type( nbcInfo )== types.StringType and \
             self.nbcMap.has_key( nbcInfo ):
            nbcId           = self.nbcMap[          nbcInfo             ]
            nbcActor        = self.nbcActors[       nbcId               ]
        else:
            raise acuVisError, "Invalid name or id for node."

        return nbcActor

#---------------------------------------------------------------------------
# getPbcActor: Return a periodic actor
#---------------------------------------------------------------------------

    def getPbcActor( self, pbcInfo  ):
        '''
	    Return a Periodic actor
	
	    Arguments:
	        pbcInfo     - Periodic Name or Id

	    Output:
	        pbcActor    - Periodic actor corresponding to the pbcInfo
        '''

        if type( pbcInfo )  == types.IntType and \
           pbcInfo in range(len(self.pbcActors)):
            pbcActor        = self.pbcActors[       pbcInfo             ]
        elif type( pbcInfo )== types.StringType and \
             self.pbcMap.has_key( pbcInfo ):
            pbcId           = self.pbcMap[          pbcInfo             ]
            pbcActor        = self.pbcActors[       pbcId               ]
        else:
            raise acuVisError, "Invalid name or id for periodic."

        return pbcActor

#---------------------------------------------------------------------------
# getNVars: Return the number of Variables
#---------------------------------------------------------------------------

    def getNVars( self  ):
        '''
	    Return the number of Variables
	
	    Arguments:
	        None

	    Output:
	        nVars   - Number of Variables
        '''

        self.varNames   = []
        nVars           = self.adb.get(     "nOutVars"                  )

        for i in range( nVars ):
            varName     = self.getVarName(  i                           )
            self.varNames.append(           varName                     )
            try:
                self.varValues[ varName ]  = self.adb.get('outValues',i,
                                                     self.stepId        )
            except:
                raise acuVisError, "Index for call to acudb "\
                        "function is out of range"

        return nVars

#---------------------------------------------------------------------------
# getVarName: Return a variable name corresponds to varId
#---------------------------------------------------------------------------

    def getVarName( self, varId  ):
        '''
	    Return a variable name corresponds to varId
	
	    Arguments:
	        varId   - Variable id

	    Output:
	        varName - Name of the variable corresponding to the varId
        '''

        varName = self.adb.get(             "outVarName",   varId       )

        return varName

#---------------------------------------------------------------------------
# getVarDim: Return the Dimension of a Variable
#---------------------------------------------------------------------------

    def getVarDim( self, varInfo  ):
        '''
	    Return the Dimension of a Variable corresponds to varInfo
	
	    Arguments:
	        varInfo - Variable id or variable name

	    Output:
	        varDim  - Dimension of the variable corresponding to the varInfo
        '''

        nVars   = self.getNVars(                                        )

        if type( varInfo ) == types.IntType:
            if varInfo in range(nVars):
                varId       = varInfo
            else:
                raise acuVisError, "Invalid variable index.It should "\
                      "be between 0 and %d" % nVars

        elif type( varInfo )== types.StringType and \
             varInfo in self.varNames:
            varId   = self.varNames.index(          varInfo             )

        else:
            raise acuVisError, "Invalid variable name or id (%s)" \
                  %varInfo

        varDim  = self.adb.get(             "outVarDim",   varId        )

        return varDim

#---------------------------------------------------------------------------
# getNSclrVars: Return the number of scalar variables
#---------------------------------------------------------------------------

    def getNSclrVars( self ):
        '''
	    Return the number of scalar variables
	
	    Arguments:
	        None

	    Output:
	        nSVars  - Number of scalar variables
        '''

        nSVars              = 0

        for i in range( self.getNVars() ):
            if self.getVarDim( i ) == 1:
                nSVars += 1
                varName     = self.getVarName(              i           )
                self.sclrVarNames.append(                   varName     )
        return nSVars

#---------------------------------------------------------------------------
# getNVecVars: Return the number of vector variables
#---------------------------------------------------------------------------

    def getNVecVars( self ):
        '''
	    Return the number of vector variables
	
	    Arguments:
	        None

	    Output:
	        nVVars  - Number of vector variables
        '''

        nVVars              = 0

        for i in range( self.getNVars() ):
            if self.getVarDim( i ) > 1:
                nVVars += 1
                varName = self.getVarName(                  i           )
                self.vecVarNames.append(                    varName     )
        return nVVars

#---------------------------------------------------------------------------
# getSclrVarName: Return a scalar variable name corresponds to varId
#---------------------------------------------------------------------------

    def getSclrVarName( self, varId  ):
        '''
	    Return a scalar variable name corresponds to varId
	
	    Arguments:
	        varId   - Variable id

	    Output:
	        sclrVar - Name of the scalar variable corresponding to the varId
        '''

        if self.sclrVarNames:
            return self.sclrVarNames[           varId                   ]

#---------------------------------------------------------------------------
# getVecVarName: Return a vector variable name corresponds to varId
#---------------------------------------------------------------------------

    def getVecVarName( self, varId  ):
        '''
	    Return a vector variable name corresponds to varId
	
	    Arguments:
	        varId   - Variable id

	    Output:
	        vecVar  - Name of the vector variable corresponding to the varId
        '''

        if self.vecVarNames:
            return self.vecVarNames[        varId                       ]

#---------------------------------------------------------------------------
# setSclrVar: Sets the current scalar variable
#---------------------------------------------------------------------------

    def setSclrVar( self, varInfo  ):
        '''
	    Sets the current scalar variable to varInfo( variable name or id)
	
	    Arguments:
	        varInfo   - Variable id or variable name

	    Output:
	        None
        '''

        if type( varInfo ) == types.IntType:
            if varInfo in range(len(self.sclrVarNames)):
                self.sclrId = varInfo
            else:
                raise acuVisError, "Invalid scalar variable index.It should be"\
                      "between %d and %s" %( 0, len(self.sclrVarNames)  )

        elif type( varInfo )== types.StringType and \
             varInfo in self.sclrVarNames:
            self.sclrId     = self.sclrVarNames.index(      varInfo     )

        else:
            raise acuVisError, "Invalid scalar variable name or id (%s)" \
                  %varInfo

        ##sclrValue   = self.varValues[self.getSclrVarName( self.sclrId )]
        ##name        = self.getSclrVarName( self.sclrId )
        ##self.setScalar( sclrValue, name                                 )
        ##
        ##for actor in self.cplActors + self.isoActors + \
        ##    self.isoLnActors + self.tuftActors:
        ##    actor[1].setScalar( sclrValue                               )
        ##    if actor[1].display( ) == 'contour':
        ##        actor[1].display( 'contour'                             )
        ##
        ##for actor in self.asg.actors.values( ):
        ##    actor.setScalar( sclrValue                                  )
        ##    if actor.display( ) == 'contour':
        ##        actor.display( 'contour'                                )

        self.setStepId( self.stepId                                     )

#---------------------------------------------------------------------------
# setVecVar: Sets the current vector variable
#---------------------------------------------------------------------------

    def setVecVar( self, varInfo  ):
        '''
	    Sets the current vector variable to varInfo( variable name or id)
	
	    Arguments:
	        varInfo      - Variable id or variable name

	    Output:
	        None
        '''

        if type( varInfo ) == types.IntType:
            if varInfo in range(len(self.vecVarNames)):
                self.vecId  = varInfo
            else:
                raise acuVisError, "Invalid vector variable index.It should be"\
                      "between %d and %s" %( 0, len(self.vecVarNames)   )

        elif type( varInfo ) == types.StringType and \
             varInfo in self.vecVarNames:
            self.vecId      = self.vecVarNames.index(      varInfo      )

        else:
            raise acuVisError, "Invalid vector variable name or id (%s)" \
                  %varInfo

        ##vecValue   = self.varValues[self.getVecVarName( self.vecId )]
        ##self.setVel( vecValue                                           )
        ##self.setVelScalar( velScalarType   = "magnitude"                )
        ##
        ##for actor in self.cplActors + self.isoActors + \
        ##    self.isoLnActors + self.tuftActors:
        ##    actor[1].setVel( vecValue                                   )
        ##    actor[1].setVelScalar( velScalarType   = "magnitude"        )
        ##    if actor[1].velDisplayed == True:
        ##        actor[1].velDisplay( True                               )
        ##
        ##for actor in self.asg.actors.values( ):
        ##    actor.setVel( vecValue                                      )
        ##    actor.setVelScalar( velScalarType = "magnitude"             )
        ##   if actor.velDisplayed == True:
        ##        actor.velDisplay( True                                  )

        self.setStepId( self.stepId                                     )

#---------------------------------------------------------------------------
# addIsoSurface: Adds an IsoSurface actor
#---------------------------------------------------------------------------

    def addIsoSurface( self, isoVec, isoVal, name, vols = None  ):
        '''
	    Adds an IsoSurface actor
	
	    Arguments:
	        isoVec  - Iso-surface vector
	        isoVol  - Iso-surface value
	        name    - Optional name
	        vols    - List of volumes

	    Output:
	        isoActor- Iso-surface actor
        '''

        if not vols:
            vols        = self.elmNames

        if type( vols ) not in ( types.TupleType, types.ListType ):
            vols    = [ vols ]

        isoObj  = AcuSgIso(                 self                        )

        if not self.sclrVarNames:
            self.getNSclrVars(                                          )

        for vol in vols:

            if type( vol ) not in ( types.IntType, types.StringType ) or\
               type( vol ) == types.IntType and vol not in self.elmMap.values()  :
                raise acuVisError, "Invalid name or id for volumes."

            if type( vol ) == types.IntType:
                vol = self.getVolName(                  vol             )

            isoObj.addIsoSet(           self.isos[vol], isoVec,
                                        isoVal,         name            )

        if isoObj:
            self.isoActors.append(      ( name, isoObj )                )

        return isoObj

#---------------------------------------------------------------------------
# addCPlane: Adds a cut plane actor
#---------------------------------------------------------------------------

    def addCPlane( self, point1, point2, point3, name, vols = None  ):
        '''
	    Adds a cut plane actor
	
	    Arguments:
	        point1  - point1
	        point2  - point2
	        point3  - point3
	        name    - Optional name
	        vols    - List of volumes

	    Output:
	        cplActor- cut-plane actor
        '''

        if not vols:
            vols        = self.elmNames

        if type( vols ) not in ( types.TupleType, types.ListType ):
            vols    = [ vols ]

        self.pnts   = [         point1,     point2,     point3          ]

        nx, ny, nz  = self.getNormal(	                                )
        isoVec      = nx * self.crd[:,0] + \
                      ny * self.crd[:,1] + \
                      nz * self.crd[:,2]
        isoVal      = nx * self.pnts[0][0] + \
                      ny * self.pnts[0][1] + \
                      nz * self.pnts[0][2]

        cplObj  = AcuSgCpl(                 self                        )

        for vol in vols:

            if type( vol ) not in ( types.IntType, types.StringType ) or\
               type( vol ) == types.IntType and \
               vol not in self.elmMap.values()  :
                raise acuVisError, "Invalid name or id for volumes."

            if type( vol ) == types.IntType:
                vol = self.getVolName(      vol                         )

            cplObj.addIsoSet(               self.isos[vol], isoVec,
                                            isoVal,         name        )

        if cplObj:
            self.cplActors.append(          ( name, cplObj )            )

        return cplObj

#---------------------------------------------------------------------------
# getNormal:
#---------------------------------------------------------------------------

    def getNormal( self ):

        ''' Get the normal from the plane corners and transformation object'''

	oax	= self.pnts[1][0] - self.pnts[0][0]
	oay	= self.pnts[1][1] - self.pnts[0][1]
	oaz	= self.pnts[1][2] - self.pnts[0][2]

	obx	= self.pnts[2][0] - self.pnts[0][0]
	oby	= self.pnts[2][1] - self.pnts[0][1]
	obz	= self.pnts[2][2] - self.pnts[0][2]

	abx	= oay * obz - oaz * oby
	aby	= oaz * obx - oax * obz
	abz	= oax * oby - oay * obx

	mag	= math.sqrt(            abx*abx + aby*aby + abz*abz     )
	abx,aby,abz	= abx/mag, aby/mag, abz/mag

	return (                        abx, aby , abz                  )

#---------------------------------------------------------------------------
# getNIsos: Return the number of iso-surface actors
#---------------------------------------------------------------------------

    def getNIsos( self ):
        '''
	    Return the number of iso-surface actors
	
	    Arguments:
	        None

	    Output:
	        nIsos   - Number of iso-surface actors
        '''

        return len(                     self.isoActors                  )

#---------------------------------------------------------------------------
# getIsoName: Return the name of an iso-surface
#---------------------------------------------------------------------------

    def getIsoName( self, isoId ):
        '''
	    Return the name of an iso-surface
	
	    Arguments:
	        isoId   - Iso-surface id

	    Output:
	        isoName - Iso-surface name
        '''

        if self.isoActors:
            return self.isoActors[  isoId ][0]

#---------------------------------------------------------------------------
# getIsoActor: Return an iso-surface actor
#---------------------------------------------------------------------------

    def getIsoActor( self, isoInfo  ):
        '''
	    Return an iso-surface actor
	
	    Arguments:
	        isoInfo     - Iso-surface Name or Id

	    Output:
	        isoActor    - Iso-surface actor corresponding to the isoInfo
        '''

        found   = False

        if type( isoInfo )  == types.IntType and \
           isoInfo in range(len(self.isoActors)):
            isoActor        = self.isoActors[   isoInfo     ][1]
        elif type( isoInfo )== types.StringType:
            for item in self.isoActors:
                if isoInfo == item[0]:
                    isoActor    = item[1]
                    found       = True
                    break
            if not found:
                raise acuVisError, "Invalid name for get iso-surface "\
                      "<%s>." % isoInfo
        else:
            raise acuVisError, "Invalid name or id for get iso-surface "\
                  "<%s>." % isoInfo

        return isoActor

#---------------------------------------------------------------------------
# delIsoActor: Remove an iso-surface actor
#---------------------------------------------------------------------------

    def delIsoActor( self, isoInfo  ):
        '''
	    Remove an iso-surface actor from acuVis and the scene graph
	
	    Arguments:
	        isoInfo     - Iso-surface Name or Id which should be removed

	    Output:
	        None
        '''

        found   = False

        if type( isoInfo )  == types.IntType and \
           isoInfo in range(len(self.isoActors)):
            pass

        elif type( isoInfo )== types.StringType :
            for item in self.isoActors:
                if isoInfo == item[0]:
                    isoInfo = self.isoActors.index(     item            )
                    found   = True
                    break
            if not found:
                raise acuVisError, "Invalid name for delete "\
                      "iso-surface actor <%s>." % isoInfo

        else:
            raise acuVisError, "Invalid name or id for delete "\
                  "iso-surface actor <%s>." % isoInfo

        self.isoActors[ isoInfo ][1].removeIsoSet(                      )
        del self.isoActors[                         isoInfo             ]

#---------------------------------------------------------------------------
# getNCpls: Return the number of cut-plane actors
#---------------------------------------------------------------------------

    def getNCpls( self ):
        '''
	    Return the number of cut-plane actors
	
	    Arguments:
	        None

	    Output:
	        nCpls   - Number of cut-plane actors
        '''

        return len(                     self.cplActors                  )

#---------------------------------------------------------------------------
# getCplName: Return the name of a cut-plane
#---------------------------------------------------------------------------

    def getCplName( self, cplId ):
        '''
	    Return the name of a cut-plane
	
	    Arguments:
	        cplId   - cut-plane id

	    Output:
	        cplName - cut-plane name
        '''

        if self.cplActors:
            return self.cplActors[  cplId ][0]

#---------------------------------------------------------------------------
# getCplActor: Return a cut-plane actor
#---------------------------------------------------------------------------

    def getCplActor( self, cplInfo  ):
        '''
	    Return a cut-plane actor
	
	    Arguments:
	        cplInfo     - Cut-plane Name or Id

	    Output:
	        cplActor    - Cut-plane actor corresponding to the cplInfo
        '''

        found   = False

        if type( cplInfo )  == types.IntType and \
           cplInfo in range(len(self.cplActors)):
            cplActor        = self.cplActors[   cplInfo     ][1]
        elif type( cplInfo )== types.StringType:
            for item in self.cplActors:
                if cplInfo == item[0]:
                    cplActor    = item[1]
                    found       = True
                    break
            if not found:
                raise acuVisError, "Invalid name for get cut-plane "\
                      "<%s>." % cplInfo
        else:
            raise acuVisError, "Invalid name or id for get cut-plane "\
                  "<%s>." % cplInfo

        return cplActor

#---------------------------------------------------------------------------
# delCplActor: Remove a cut-plane actor
#---------------------------------------------------------------------------

    def delCplActor( self, cplInfo  ):
        '''
	    Remove a cut-plane actor from acuVis and the scene graph
	
	    Arguments:
	        cplInfo     - Cut-plane Name or Id which should be removed

	    Output:
	        None
        '''

        found   = False

        if type( cplInfo )  == types.IntType and \
           cplInfo in range(len(self.cplActors)):
            pass

        elif type( cplInfo )== types.StringType :
            for item in self.cplActors:
                if cplInfo == item[0]:
                    cplInfo = self.cplActors.index(     item            )
                    found   = True
                    break
            if not found:
                raise acuVisError, "Invalid name for delete "\
                      "cut-plane actor <%s>." % cplInfo

        else:
            raise acuVisError, "Invalid name or id for delete "\
                  "cut-plane actor <%s>." % cplInfo

        self.cplActors[ cplInfo ][1].removeIsoSet(                      )
        del self.cplActors[                         cplInfo             ]

#---------------------------------------------------------------------------
# getNSteps: Returns the number of time steps
#---------------------------------------------------------------------------

    def getNSteps( self ):
        '''
	    Returns the number of time steps
	
	    Arguments:
	        None

	    Output:
	        nSteps   - Number of time steps
        '''

        steps   = self.getSteps(                                        )

        return len(                                 steps               )

#---------------------------------------------------------------------------
# getSteps: Returns the list of time steps
#---------------------------------------------------------------------------

    def getSteps( self ):
        '''
	    Returns the list of time steps
	
	    Arguments:
	        None

	    Output:
	        steps   - List of time steps
        '''

        self.steps  = []
        steps       = self.adb.get(                 'steps'             )
        for step in steps:
            self.steps.append(                      step                )

        return self.steps

#---------------------------------------------------------------------------
# getTimes: Returns the list of times
#---------------------------------------------------------------------------

    def getTimes( self ):
        '''
	    Returns the list of times
	
	    Arguments:
	        None

	    Output:
	        times   - List of times
        '''

        self.times      = self.adb.get(             'times'             )

        return self.times

#---------------------------------------------------------------------------
# setStep: Set the time step
#---------------------------------------------------------------------------

    def setStep( self, step ):
        '''
	    Set the time step
	
	    Arguments:
	        step    - The time step which should be set

	    Output:
	        None
        '''

        if self.steps and step in self.steps:
            self.step       = step
            self.stepId     = self.steps.index(     step                )

            self.updateCrds(                                            )
            self.updateSclrFld(                                         )
            self.updateVecFld(                                          )
            self.updateIsoObjs(                                         )
            self.updateIsoLnObjs(                                       )

        else:
            raise acuVisError, "Steps list is empty or step is out of range"

#---------------------------------------------------------------------------
# setStepId: Set the time step id
#---------------------------------------------------------------------------

    def setStepId( self, stepId ):
        '''
	    Set the time step id
	
	    Arguments:
	        stepId    - The time step id which should be set

	    Output:
	        None
        '''

        if self.steps and stepId in range(len( self.steps )):
            self.step       = self.steps[ stepId ]
            self.stepId     = stepId

            self.updateCrds(                                            )
            self.updateSclrFld(                                         )
            self.updateVecFld(                                          )
            self.updateIsoObjs(                                         )
            self.updateIsoLnObjs(                                       )

        else:
            raise acuVisError, "Steps list is empty or stepId is out of range"

#---------------------------------------------------------------------------
# updateCrds: Update Coordinates and all data depends on it
#---------------------------------------------------------------------------

    def updateCrds( self ):
        '''
	    Update Coordinates and all data depends on it when
	    time step is changed
	
	    Arguments:
	        None

	    Output:
	        None
        '''

        self.setDeform(                     deform = True               )

        # Update all the data depends on Crds only if Crds were changed

        if not numarray.all( self.crd == self.refCrd ):

            actors  = []
            actors  = self.elmActors + self.srfActors + \
                      self.nbcActors + self.pbcActors

            for actor in actors:
                actor.resetCrd(             self.crd                    )

#---------------------------------------------------------------------------
# updateIsoObjs: Update Iso-surface and cut-plane objects
#---------------------------------------------------------------------------

    def updateIsoObjs( self ):
        '''
	    Update Iso-surface and cut-plane objects when Crds is changed
	
	    Arguments:
	        None

	    Output:
	        None
        '''

        isoVols = []

        # ----- Save the volumes we have iso-surface for them

        for iso in self.isoActors:
            if not iso[1].isoVecName: continue
            for key, value in self.isos.items():
                if iso[1].isoObj == self.isos[key] and \
                   key not in isoVols:
                    isoVols.append(         key                         )

        if not isoVols: return

        # ----- Update AcuIso Objects

        for elem in self.elmNames:
            self.isos[elem] = acuiso.Acuiso( self.usrIds, self.crd,
                                             self.elmCnns[elem]         )

        # ----- Update iso-surface objects

        for iso in self.isoActors:
            iso[1].removeIsoSet(                                        )
            if iso[1].isoVecName:
                iso[1].setScalar(   self.varValues[ iso[1].isoVecName]  )
                if iso[1].display( ) == 'contour':
                    iso[1].display( 'contour'                           )

            for vol in isoVols:
                iso[1].addIsoSet(       self.isos[ vol ],   iso[1].isoVec,
                                        iso[1].isoVal,      iso[1].name )

#---------------------------------------------------------------------------
# updateIsoLnObjs: Update Iso-line objects
#---------------------------------------------------------------------------

    def updateIsoLnObjs( self ):
        '''
	    Update Iso-line objects when Crds is changed
	
	    Arguments:
	        None

	    Output:
	        None
        '''

        isoSrfs = []

        # ----- Save the surfaces we have iso-line for them

        for iso in self.isoLnActors:
            if not iso[1].isoVecName: continue
            for key, value in self.isoLns.items():
                if iso[1].isoLnObj == self.isoLns[key] and \
                   key not in isoSrfs:
                    isoSrfs.append(         key                         )

        if not isoSrfs: return

        # ----- Update AcuIsl Objects

        for srf in self.srfNames:
            self.isoLns[srf] = acuisl.Acuisl(  self.usrIds, self.crd,
                                               self.srfCnns[srf]        )

        # ----- Update iso-line objects

        for iso in self.isoLnActors:
            iso[1].removeIsoLnSet(                                      )
            if iso[1].isoVecName:
                iso[1].setScalar(   self.varValues[ iso[1].isoVecName]  )
                if iso[1].display( ) == 'contour':
                    iso[1].display( 'contour'                           )

            for srf in isoSrfs:
                iso[1].addIsoLnSet( self.isoLns[ srf ], iso[1].isoVec,
                                    iso[1].isoVal,      iso[1].name     )

#---------------------------------------------------------------------------
# updateSclrFld: Update Scalar field
#---------------------------------------------------------------------------

    def updateSclrFld( self ):
        '''
	    Update Scalar field when time step is changed
	
	    Arguments:
	        None

	    Output:
	        None
        '''

        try:
            currSclrVarName = self.getSclrVarName(      self.sclrId     )
            varIdx          = self.varNames.index(      currSclrVarName )

            self.varValues[ currSclrVarName ]  = self.adb.get( \
                                                        'outValues',
                                                        varIdx,
                                                        self.stepId     )
            sclrValue  = self.varValues[ currSclrVarName ]

            self.setScalar( sclrValue, name = currSclrVarName           )

            for iso in self.cplActors + self.isoActors + \
                self.isoLnActors + self.tuftActors:
                iso[1].setScalar( sclrValue                             )
                if iso[1].display( ) == 'contour':
                    iso[1].display( 'contour'                           )

            for actor in self.asg.actors.values( ):
                actor.setScalar( sclrValue                              )
                if actor.display( ) == 'contour':
                    actor.display( 'contour'                            )

        except:
            raise acuVisError, "Index for call to acudb function is"\
                  " out of range"

#---------------------------------------------------------------------------
# updateVecFld: Update Vector field
#---------------------------------------------------------------------------

    def updateVecFld( self ):
        '''
	    Update Vector field when time step is changed
	
	    Arguments:
	        None

	    Output:
	        None
        '''

        try:
            currVecVarName  = self.getVecVarName(       self.vecId      )
            varIdx          = self.varNames.index(      currVecVarName  )

            self.varValues[ currVecVarName ]  = self.adb.get( \
                                                        'outValues',
                                                        varIdx,
                                                        self.stepId     )

            self.setVel( self.varValues[ currVecVarName ], currVecVarName )
            self.setVelScalar( velScalarType = "magnitude"              )

            for iso in self.cplActors + self.isoActors + \
                self.isoLnActors + self.tuftActors:
                iso[1].setVel( self.varValues[ currVecVarName ]         )
                iso[1].setVelScalar( velScalarType = "magnitude"        )
                if iso[1].velDisplayed == True:
                    iso[1].velDisplay( True                             )

            for actor in self.asg.actors.values( ):
                actor.setVel( self.varValues[ currVecVarName ]          )
                actor.setVelScalar( velScalarType = "magnitude"         )
                if actor.velDisplayed == True:
                    actor.velDisplay( True                              )

        except:
            raise acuVisError, "Index for call to acudb function is"\
                  " out of range"

#---------------------------------------------------------------------------
# setDeform: Turns on/off the deform geometry
#---------------------------------------------------------------------------

    def setDeform( self, deform = True ):
        '''
	    Turns on/off the deform geometry
	
	    Arguments:
	        deform  - deform geometry ( on/off )

	    Output:
	        None
        '''

        if deform and self.aleId != -1:
            self.meshDisp   = self.adb.get( "outValues", self.aleId,
                                            self.stepId                 )
            self.crd        = self.refCrd + self.meshDisp

#---------------------------------------------------------------------------
# home: Sets the camera to its home position
#---------------------------------------------------------------------------

    def home( self ):
        '''
	    Sets the camera to its home position
	
	    Arguments:
	        None

	    Output:
	        None
        '''

        self.asg.acuTform.home(                                         )

#---------------------------------------------------------------------------
# fit: Sets the camera to fit all the actors in the scenegraph
#---------------------------------------------------------------------------

    def fit( self ):
        '''
	    Sets the camera to fit all the actors in the scenegraph
	
	    Arguments:
	        None

	    Output:
	        None
        '''

        self.asg.acuTform.fit(                                          )

#---------------------------------------------------------------------------
# snap: Compute and align the camera to closest principal axis
#---------------------------------------------------------------------------

    def snap( self ):
        '''
	    Compute and align the camera to closest principal axis
	
	    Arguments:
	        None

	    Output:
	        None
        '''

        self.asg.acuTform.snap(                                         )

#---------------------------------------------------------------------------
# snapz: Compute and align the camera to closest z plane
#---------------------------------------------------------------------------

    def snapz( self ):
        '''
	    Compute and align the camera to closest z plane
	
	    Arguments:
	        None

	    Output:
	        None
        '''

        self.asg.acuTform.snapz(                                        )

#---------------------------------------------------------------------------
# alignDir: Sets the camera to look up in a special direction
#---------------------------------------------------------------------------

    def alignDir( self, dir ):
        '''
	    Sets the camera to look up in a special direction
	
	    Arguments:
	        dir - A direction ( 'x+', '+x', 'xplus',
                                    'y+', '+y', 'yplus',
                                    'z+', '+z', 'zplus',
                                    'x-', '-x', 'xminus',
                                    'y-', '-y', 'yminus',
                                    'z-', '-z', 'zminus'    )
                        It is in case insensitive manor

	    Output:
	        None
        '''

        direction     = string.lower(           dir                     )

        if direction in [ 'x+', '+x', 'xplus' ]:
            self.asg.acuTform.setXp(                                    )

        elif direction in [ 'x-', '-x', 'xminus' ]:
            self.asg.acuTform.setXm(                                    )

        elif direction in [ 'y+', '+y', 'yplus' ]:
            self.asg.acuTform.setYp(                                    )

        elif direction in [ 'y-', '-y', 'yminus' ]:
            self.asg.acuTform.setYm(                                    )

        elif direction in [ 'z+', '+z', 'zplus' ]:
            self.asg.acuTform.setZp(                                    )

        elif direction in [ 'z-', '-z', 'zminus' ]:
            self.asg.acuTform.setZm(                                    )

        else:
            raise acuVisError, "Direction argument '%s' in alignView is "\
                                "undefined." %dir

#---------------------------------------------------------------------------
# rotate: Rotate the camera by special degrees in special direction
#---------------------------------------------------------------------------

    def rotate( self, dir, angle = 45 ):
        '''
	    Rotate the camera by special degrees in special direction
	
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

        self.asg.acuTform.rotate(       dir, angle                      )

#---------------------------------------------------------------------------
# zoom: Zoom the camera by special scale
#---------------------------------------------------------------------------

    def zoom( self, scale = 1. ):
        '''
	    Zoom the camera by special scale
	
	    Arguments:
	        scale   - Zoom scale

	    Output:
	        None
        '''

        self.asg.viewer.zoom(           scale                           )

#---------------------------------------------------------------------------
# addTxtActor: Add 2D text actor to the scene graph
#---------------------------------------------------------------------------

    def addTxtActor(    self,   text            = "ACUSIM",
                                position        = [0.5,0.5],
                                style           = "Times New Roman:bold",
                                fontSize        = 12,
                                color           = [1,0,0],
                                horAlignment    = "CENTER",
                                verAlignment   = "BOTTOM"               ):
        '''
	    Add 2D text actor to the scene graph
	
	    Arguments:
	        text        - Annotation text
	        position    - Annotation position
	        style       - Annotation style
	        fontSize    - Annotation font size
	        color       - Annotation color
	        horAlignment- Annotation horizontal alignment
	        verAlignment- Annotation vertical alignment

	    Output:
	        txtActor    - The 2D text actor
				
        '''

	txtActor    = self.asg.addTxtActor(     text,       position,
                                                style,      fontSize,
                                                color,      horAlignment,
                                                verAlignment            )

	return txtActor

#---------------------------------------------------------------------------
# addImgActor: Add Image actor to the scene graph
#---------------------------------------------------------------------------

    def addImgActor( self,  filename	    = None,
                            image	    = None,
                            position	    = [0.5,0.5],
                            width	    = -1,
                            height	    = -1,
                            horAlignment    = "CENTER",
                            verAlignment    = "BOTTOM"                  ):
        '''
	    Add image actor to the scene graph
	
	    Arguments:
	        fileName    - Image file name
	        image       - Image to be added
	        position    - Image actor position
	        width       - Image width
	        height      - Image height
	        horAlignment- Image horizontal alignment
	        verAlignment- Image vertical alignment

	    Output:
	        imgActor    - The 2D text actor
				
        '''

	imgActor    = self.asg.addImgActor(     filename,   image,
                                                position,   width,
                                                height,     horAlignment,
                                                verAlignment            )

	return imgActor

#---------------------------------------------------------------------------
# setBgColor: Set the background of the scene graph
#---------------------------------------------------------------------------

    def setBgColor( self,   color       = None,
                            bottomColor = None,
                            fileName    = None,
                            image       = None,
                            type        = "solid" ):
        '''
	    Set the background of the scene graph
	
	    Arguments:
                color       - Solid Background Color
                              or Top Color for Two-Tone Type [deafult = None]
                bottomColor - Bottom Color for Two-Tone Type [deafult = None]
                fileName    - The Background Image File Name [deafult = None]
                image       - The Backgroung Image object [deafult = None]
                type        - The Background Type [default = solid]
                              valid: "solid" , "two-tone", "filename", "image"

	    Output:
	        None
				
        '''

        if type == "solid":
            if color == None:
                raise acuVisError, "Invalid solid background color"
            else:
                self.asg.viewer.bgColor( type   = type,
                                         red    = color[0],
                                         green  = color[1],
                                         blue   = color[2] )

        elif type == "two-tone":
            if color == None:
                raise acuVisError, "Invalid top background color"

            elif bottomColor == None:
                raise acuVisError, "Invalid bottom background color"

            else:
                self.asg.viewer.bgColor( type       = type,
                                         red        = color[0],
                                         green      = color[1],
                                         blue       = color[2],
                                         red_bot    = bottomColor[0],
                                         green_bot  = bottomColor[1],
                                         blue_bot   = bottomColor[2] )

        elif type == "filename":
            if fileName == None:
                raise acuVisError, "Invalid background image filename"

            else:
                self.asg.viewer.bgColor( type       = type,
                                         fileName   = fileName )

        elif type == "image":
            if image == None:
                raise acuVisError, "Invalid background image object"

            else:
                self.asg.viewer.bgColor( type   = type,
                                         image  = image )

        else:
            raise acuVisError, "Invalid background type"

#---------------------------------------------------------------------------
# setAxis: Set axis size of the scene graph
#---------------------------------------------------------------------------

    def setAxis( self, size = None ):
        '''
	    Set axis size of the scene graph
	
	    Arguments:
                size    - Axis size to set

	    Output:
	        None
				
        '''

	self.asg.axisSize(                  size                        )
	
#---------------------------------------------------------------------------
# remTxtActor: Remove 2D text actor from the scene graph
#---------------------------------------------------------------------------

    def remTxtActor( self, txtActor ):
        '''
	    Remove 2D text actor from the scene graph
	
	    Arguments:
                txtActor       - The text actor which should be removed

	    Output:
	        None
				
        '''

	self.asg.remTxtActor(   txtActor                                )

#---------------------------------------------------------------------------
# remImgActor: Remove image actor from the scene graph
#---------------------------------------------------------------------------

    def remImgActor( self, imgActor ):
        '''
	    Remove image actor from the scene graph
	
	    Arguments:
                imgActor       - The image actor which should be removed

	    Output:
	        None
				
        '''

	self.asg.remImgActor(   imgActor                                )

#---------------------------------------------------------------------------
# addCmapLegendActor: Add 2D color map legend at a specified location
#---------------------------------------------------------------------------

    def addCmapLegendActor( self,
                            text        = "Color Map Legend",
			    textFont    = "Times-Roman",
			    minVal      = 0,
			    maxVal	= 5,
			    nVals	= 3,
                            textFontSize= 12,
			    valFont     = "Times-Roman",
                            valFontSize = 12,
			    xpos        = 0.05,
			    ypos        = 0.15,
			    xsize       = 2,
			    ysize       = 10,
                            valXOffset  = 0.07,
                            valYOffset  = 0.05                  ):
        '''
	    Add 2D color map legend at a specified location
	
	    Arguments:
	        text        - Colormap text
	        textFont    - Colormap text font
	        minVal      - Colormap minimum value
	        maxVal      - Colormap maximum value
	        nVals       - Number of vals in colormap
	        valFont     - Colormap values font
	        xpos        - Colormap X position
	        ypos        - Colormap Y position
	        xsize       - Colormap X size
	        ysize       - Colormap Y size
	        valXOffset  - Colormap text X offset
                valYOffset  - Colormap text Y offset

	    Output:
	        cmapActor   - The 2D color map actor
				
        '''

	cmapActor   = self.asg.addCmapActor(     text       = text,
                                                 textFont   = textFont,
                                                 minVal     = minVal,
                                                 maxVal	    = maxVal,
                                                 nVals	    = nVals,
                                                 textFontSize=textFontSize,
                                                 valFont    = valFont,
                                                 valFontSize= valFontSize,
                                                 xpos       = xpos,
                                                 ypos       = ypos,
                                                 xsize      = xsize,
                                                 ysize      = ysize,
                                                 valXOffset = valXOffset,
                                                 valYOffset = valYOffset )

	return cmapActor

#---------------------------------------------------------------------------
# delCmapLegendActor: Remove color map actor from scene graph
#---------------------------------------------------------------------------

    def delCmapLegendActor( self, cmapActor ):
        '''
	    Remove color map actor from the scene graph
	
	    Arguments:
                cmapActor   - The color map actor which should be removed

	    Output:
	        None
				
        '''

	self.asg.remCmapActor(          cmapActor                       )

#---------------------------------------------------------------------------
# addSphereActor: Add a sphere to the scene graph
#---------------------------------------------------------------------------

    def addSphereActor(    self,    center	    = [0,0,0],
                                    radius	    = None,
                                    color	    = [0,1,0],
                                    text	    = None,
                                    pointSize	    = 2,
                                    lineWidth       = 2,
                                    fontSize	    = None,
                                    vis             = True,
                                    trans           = False,
                                    transVal        = 0.5    ):
        '''
	    Add a sphere to the scene graph
	
	    Arguments:
	        center      - Center of the sphere
                radius	    - Sphere radius
                color	    - Sphere color
                text	    - Sphere text
                pointSize   - Size of point
                lineWidth   - Line width
                fontSize    - The text font size
                vis         - Visibility
                trans       - Transparency flag
                transVal    - Transparency Value

	    Output:
	        sphActor    - The created sphere actor
				
        '''

	sphActor   = self.asg.addGeomActor(     type	    = "sphere",
                                                center	    = center,
                                                radius	    = radius,
                                                color	    = color,
                                                text	    = text,
                                                pointSize   = pointSize,
                                                lineWidth   = lineWidth,
                                                fontSize    = fontSize,
                                                vis         = vis,
                                                trans       = trans,
                                                transVal    = transVal  )

	return sphActor

#---------------------------------------------------------------------------
# delSphereActor: Remove Sphere actor from scene graph
#---------------------------------------------------------------------------

    def delSphereActor( self, sphereActor ):
        '''
	    Remove Sphere actor from the scene graph
	
	    Arguments:
                sphereActor   - The Sphere actor which should be removed

	    Output:
	        None
				
        '''

	self.asg.remGeomActor(          sphereActor                     )

#---------------------------------------------------------------------------
# addGeomActor: Add a geom actor to the scene graph
#---------------------------------------------------------------------------

    def addGeomActor(   self,
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
                        vis             = True,
                        trans           = False,
                        transVal        = 0.5,
                        points          = None  ):
        '''
	    Add a geom actor to the scene graph
	
	    Arguments:
                type        - Type of geom actor
	        center      - Center of the actor
                normal	    - Geom normal vector
                normalX     - Geom normalX
                normalY     - Geom normalY
                normalZ     - Geom normalZ
                radius	    - Geom radius
                height	    - Geom height
                width	    - Geom width
                depth	    - Geom depth
                xangle	    - Geom xangle
                yangle	    - Geom yangle
                zangle	    - Geom zangle
                color	    - Geom color
                point	    - Geom point
                pntList	    - Geom pntList
                point1	    - Geom point1
                point2	    - Geom point2
                text	    - Geom text
                pointSize   - Size of point
                lineWidth   - Line width
                fontSize    - The text font size
                arrowLength - Length of arrow
                triSize	    - Triangle Size
                tetSize	    - TetSize
                vis         - Visibility
                trans       - Transparency flag
                transVal    - Transparency Value
                points      - Points

	    Output:
	        geomActor   - The created geom actor
				
        '''

	geomActor   = self.asg.addGeomActor(    type	    = type,
                                                center	    = center,
                                                normal	    = normal,
                                                normalX     = normalX,
                                                normalY     = normalY,
                                                normalZ     = normalZ,
                                                radius	    = radius,
                                                height	    = height,
                                                width	    = width,
                                                depth	    = depth,
                                                xangle	    = xangle,
                                                yangle	    = yangle,
                                                zangle	    = zangle,
                                                color	    = color,
                                                point	    = point,
                                                pntList	    = pntList,
                                                point1	    = point1,
                                                point2	    = point2,
                                                text	    = text,
                                                pointSize   = pointSize,
                                                lineWidth   = lineWidth,
                                                fontSize    = fontSize,
                                                arrowLength = arrowLength,
                                                triSize	    = triSize,
                                                tetSize	    = tetSize,
                                                vis         = vis,
                                                trans       = trans,
                                                transVal    = transVal,
                                                points      = points    )

	return geomActor

#---------------------------------------------------------------------------
# delGeomActor: Remove Geom actor from scene graph
#---------------------------------------------------------------------------

    def delGeomActor( self, geomActor ):
        '''
	    Remove Geom actor from the scene graph
	
	    Arguments:
                geomActor   - The Geom actor which should be removed

	    Output:
	        None
				
        '''

	self.asg.remGeomActor(          geomActor                       )
	
#---------------------------------------------------------------------------
# setLineWidth: Set the line width used in various actors
#---------------------------------------------------------------------------

    def setLineWidth( self, width = None ):
        '''
	    Set the line width used in various actors
	
	    Arguments:
                width   - The line width which should be set

	    Output:
	        None
				
        '''

	self.asg.setLineWidth(          width                           )

#---------------------------------------------------------------------------
# setShading: Set the shading used in various actors
#---------------------------------------------------------------------------

    def setShading( self, shading = None ):
        '''
	    Set the shading used in various actors
	
	    Arguments:
                shading   - The shading which should be set
                            ('Flat', 'Gouraud', 'Phong')

	    Output:
	        None
				
        '''

	self.asg.setShading(            shading                         )

#---------------------------------------------------------------------------
# setPointSize: Set the point size used in various actors
#---------------------------------------------------------------------------

    def setPointSize( self, size = None ):
        '''
	    Set the point size used in various actors
	
	    Arguments:
                size   - The point size which should be set

	    Output:
	        None
				
        '''

	self.asg.setPointSize(          size                            )

#---------------------------------------------------------------------------
# setTransType: Set the transparency type to be used
#---------------------------------------------------------------------------

    def setTransType( self, type ):
        '''
	    Set the transparency type to be used
	
	    Arguments:
                type   - Transparency type it can be "SCREEN_DOOR","ADD",
                         "DELAYED_ADD","SORTED_OBJECT_ADD","BLEND",
                         "DELAYED_BLEND" and "SORTED_OBJECT_BLEND"

	    Output:
	        None
				
        '''

	self.asg.viewer.setTransType(   type                            )

#---------------------------------------------------------------------------
# bndBox: Get the bounding box of the objects
#---------------------------------------------------------------------------

    def bndBox( self ):
        '''
	    Get the bounding box of the objects
	
	    Arguments:
                None

	    Output:
	        None
				
        '''

	boundBox    = []
	bndVal      = self.asg.getBoundingBox(                          )

	for i in range( 3 ):
            boundBox.append(    (bndVal[i], bndVal[i + 3])              )

        return boundBox

#---------------------------------------------------------------------------
# toggleLogo: Toggle the Acusim logo
#---------------------------------------------------------------------------

    def toggleLogo( self ):
        '''
	    Toggle the Acusim logo
	
	    Arguments:
                None

	    Output:
	        None
				
        '''

	self.asg.acuTform.toggleLogo(                                   )

#---------------------------------------------------------------------------
# genPoints: Generate points
#---------------------------------------------------------------------------

    def genPoints(  self,   type,
                            point1,
                            point2,
                            point3,
                            nXPoints,
                            nYPoints                                    ):
        '''
	    Generate points
	
	    Arguments:
	        type        - Type for generating points
	        point1      - Point1
	        point2      - Point2
	        point3      - Point3
	        nXPoints    - Number of X points
	        nYPoints    - Number of Y points
	

	    Output:
	        genPnts     - Generated points
        '''

        pnts        = [         point1,     point2,     point3          ]

	self.cpnts  = numarray.array(	    type='d',   shape=(4,3)	)
        self.buildRectangle(                pnts                        )

        indxs       = []
        genPnts     = []
        fixElemIdx  = None
        for i in range(3):
            indxs.append(                   i                           )
            fixElmList  = numarray.where( self.cpnts[:,i] != \
                                          self.cpnts[0,i] )[0]
            if not len( fixElmList ):
                fixElemIdx  = i

        if fixElemIdx != None:
            indxs.remove(                   fixElemIdx                  )
            minIdx  = min(                  indxs                       )
            maxIdx  = max(                  indxs                       )

        xMin        = self.cpnts[:,minIdx].min(                         )
        xMax        = self.cpnts[:,minIdx].max(                         )
        yMin        = self.cpnts[:,maxIdx].min(                         )
        yMax        = self.cpnts[:,maxIdx].max(                         )

        xDist       = ( xMax - xMin )/nXPoints
        yDist       = ( yMax - yMin )/nYPoints

        for i in range(nXPoints):
            for j in range(nYPoints):
                pnt                 = []
                pnt.insert(                 minIdx, xMin + j * xDist    )
                pnt.insert(                 maxIdx, yMin + i * yDist    )
                pnt.insert(                 fixElemIdx,
                                            self.cpnts[0][fixElemIdx]   )
                genPnts.append(             pnt                         )

        numOfDummyPnts = len(self.crd) - len(genPnts)
        for i in range( numOfDummyPnts ):
           genPnts.append(                  (0, 0, 0)                   )

        return genPnts

#---------------------------------------------------------------------------
# buildRectangle:
#---------------------------------------------------------------------------

    def buildRectangle( self, points ):
        ''' build the rectangle representing the plane from a 3 points '''

	pnt	= None

	if type(points) == types.ListType or type(points) == types.TupleType:
	    if len(points) != 3:
	        raise acuVisError, "invalid data passed to buildRectangle"
	    if len(points[0]) != 3 or len(points[1]) != 3 or \
	       len(points[2]) != 3:
	        raise acuVisError, "invalid data passed to buildRectangle"
            pnt	= points
	    pnt.append(				1*pnt[0]		)

	elif isinstance( points, numarray.numarraycore.NumArray ):
	    try:
	        ( nDim1 , nDim2 ) = points.shape
		if nDim1 != 3 or nDim2 != 3:
	            raise acuVisError, "invalid data passed to buildRectangle"
	    except:
	        raise acuVisError, "invalid data passed to buildRectangle"
	    pnt	= numarray.array(	type='d', shape=(4,3)		)
	    pnt[0]	= points[0]
	    pnt[1]	= points[1]
	    pnt[2]	= points[2]
	    pnt[3]	= points[0]
	else:
	    raise acuVisError, "invalid data passed to buildRectangle"


	aDir1	= pnt[1][0] - pnt[0][0]
	aDir2	= pnt[1][1] - pnt[0][1]
	aDir3	= pnt[1][2] - pnt[0][2]


	tmp	= math.sqrt(	aDir1**2 + aDir2**2 + aDir3**2		)
	aDir1	= aDir1 / tmp
	aDir2	= aDir2 / tmp
	aDir3	= aDir3 / tmp

	tmp	= aDir1 * ( pnt[2][0] - pnt[1][0]  ) \
		+ aDir2 * ( pnt[2][1] - pnt[1][1]  ) \
		+ aDir3 * ( pnt[2][2] - pnt[1][2]  )

	pnt[2][0]	-= aDir1 * tmp
	pnt[2][1]	-= aDir2 * tmp
	pnt[2][2]	-= aDir3 * tmp

	pnt[3][0] = pnt[0][0] - pnt[1][0] + pnt[2][0]
	pnt[3][1] = pnt[0][1] - pnt[1][1] + pnt[2][1]
	pnt[3][2] = pnt[0][2] - pnt[1][2] + pnt[2][2]

	self.cpnts[0][0]	= pnt[0][0]
	self.cpnts[0][1]	= pnt[0][1]
	self.cpnts[0][2]	= pnt[0][2]

	self.cpnts[1][0]	= pnt[1][0]
	self.cpnts[1][1]	= pnt[1][1]
	self.cpnts[1][2]	= pnt[1][2]

	self.cpnts[2][0]	= pnt[2][0]
	self.cpnts[2][1]	= pnt[2][1]
	self.cpnts[2][2]	= pnt[2][2]

	self.cpnts[3][0]	= pnt[3][0]
	self.cpnts[3][1]	= pnt[3][1]
	self.cpnts[3][2]	= pnt[3][2]

#---------------------------------------------------------------------------
# addTufts: Adds a tufts actor
#---------------------------------------------------------------------------

    def addTufts( self, points, name, vols = None  ):
        '''
	    Adds a tufts actor
	
	    Arguments:
	        points  - points
	        name    - Optional name
	        vols    - List of volumes

	    Output:
	        tuftsActor- tufts actor
        '''

        if not vols:
            vols        = self.elmNames

        if type( vols ) not in ( types.TupleType, types.ListType ):
            vols    = [ vols ]

        tuftObj     = AcuSgTufts(               self                    )

        points      = numarray.array(           points                  )

        srfs        = [ srfCnn for srfCnn in self.srfCnns.values()      ]
        cnns        = [ elmCnn for elmCnn in self.elmCnns.values()      ]
        prj         = acuprj.Acuprj( self.crd, cnns = cnns, srfs = srfs )

        info        = _modelsDefInfo[           'Nodes'                 ]

        for vol in vols:
            if type( vol ) not in ( types.IntType, types.StringType ) or\
               type( vol ) == types.IntType and \
               vol not in self.elmMap.values()  :
                raise acuVisError, "Invalid name or id for volumes."

            if type( vol ) == types.IntType:
                vol = self.getVolName(          vol                     )

            if vol in self.elmCnns:
                cnn     = self.elmCnns[         vol                     ]
            cnn         = acupu.getCnnNodes(    cnn                     )

            prjPnts     = prj.project(          points, self.crd[cnn]   )

            tuftObj.addTufts(   prjPnts, cnn, info, prj,    name        )


        if tuftObj:
            self.tuftActors.append(             ( name, tuftObj )       )

        return tuftObj

#---------------------------------------------------------------------------
# delTufts: Remove tuft actor
#---------------------------------------------------------------------------

    def delTufts( self, tuftInfo  ):
        '''
	    Remove a tuft actor from acuVis and the scene graph
	
	    Arguments:
	        tuftInfo     - Tuft Name or Id which should be removed

	    Output:
	        None
        '''

        found   = False

        if type( tuftInfo )  == types.IntType and \
           tuftInfo in range(len(self.tuftActors)):
            pass

        elif type( tuftInfo )== types.StringType :
            for item in self.tuftActors:
                if tuftInfo == item[0]:
                    tuftInfo = self.tuftActors.index(     item          )
                    found   = True
                    break
            if not found:
                raise acuVisError, "Invalid name for delete "\
                      "tuft actor <%s>." % tuftInfo

        else:
            raise acuVisError, "Invalid name or id for delete "\
                  "tuft actor <%s>." % tuftInfo

        self.tuftActors[ tuftInfo ][1].removeTufts(                     )
        del self.tuftActors[                        tuftInfo            ]

#---------------------------------------------------------------------------
# addIsoLine: Adds an IsoLine actor
#---------------------------------------------------------------------------

    def addIsoLine( self, isoVec, isoVal, name, srfs = None  ):
        '''
	    Adds an IsoLine actor
	
	    Arguments:
	        isoVec          - Iso-line vector
	        isoVol          - Iso-line value
	        name            - Optional name
	        srfs            - List of surfaces

	    Output:
	        isoLineActor    - Iso-line actor
        '''

        if not srfs:
            srfs        = self.srfNames

        if type( srfs ) not in ( types.TupleType, types.ListType ):
            srfs    = [ srfs ]

        isoLnObj    = AcuSgIsoLine(         self                        )

        if not self.sclrVarNames:
            self.getNSclrVars(                                          )

        for srf in srfs:

            if type( srf ) not in ( types.IntType, types.StringType ) or\
               type( srf ) == types.IntType and srf not in self.srfMap.values()  :
                raise acuVisError, "Invalid name or id for surfaces."

            if type( srf ) == types.IntType:
                srf = self.getSrfName(                  srf             )

            isoLnObj.addIsoLnSet(       self.isoLns[srf], isoVec,
                                        isoVal,         name            )

        if isoLnObj:
            self.isoLnActors.append(    ( name, isoLnObj )              )

        return isoLnObj

#---------------------------------------------------------------------------
# getNIsoLns: Return the number of iso-line actors
#---------------------------------------------------------------------------

    def getNIsoLns( self ):
        '''
	    Return the number of iso-line actors
	
	    Arguments:
	        None

	    Output:
	        nIsoLns   - Number of iso-line actors
        '''

        return len(                     self.isoLnActors                )

#---------------------------------------------------------------------------
# getIsoLnName: Return the name of an iso-line
#---------------------------------------------------------------------------

    def getIsoLnName( self, isoLnId ):
        '''
	    Return the name of an iso-line
	
	    Arguments:
	        isoLnId   - Iso-line id

	    Output:
	        isoLnName - Iso-line name
        '''

        if self.isoLnActors:
            return self.isoLnActors[  isoLnId ][0]

#---------------------------------------------------------------------------
# getIsoLnActor: Return an iso-line actor
#---------------------------------------------------------------------------

    def getIsoLnActor( self, isoLnInfo  ):
        '''
	    Return an iso-line actor
	
	    Arguments:
	        isoLnInfo     - Iso-line Name or Id

	    Output:
	        isoLnActor    - Iso-line actor corresponding to the isoLnInfo
        '''

        found   = False

        if type( isoLnInfo )  == types.IntType and \
           isoLnInfo in range(len(self.isoLnActors)):
            isoLnActor        = self.isoLnActors[   isoLnInfo     ][1]
        elif type( isoLnInfo )== types.StringType:
            for item in self.isoLnActors:
                if isoLnInfo == item[0]:
                    isoLnActor    = item[1]
                    found       = True
                    break
            if not found:
                raise acuVisError, "Invalid name for get iso-line "\
                      "<%s>." % isoLnInfo
        else:
            raise acuVisError, "Invalid name or id for get iso-line "\
                  "<%s>." % isoLnInfo

        return isoLnActor

#---------------------------------------------------------------------------
# delIsoLnActor: Remove an iso-line actor
#---------------------------------------------------------------------------

    def delIsoLnActor( self, isoLnInfo  ):
        '''
	    Remove an iso-line actor from acuVis and the scene graph
	
	    Arguments:
	        isoLnInfo     - Iso-line Name or Id which should be removed

	    Output:
	        None
        '''

        found   = False

        if type( isoLnInfo )  == types.IntType and \
           isoLnInfo in range(len(self.isoLnActors)):
            pass

        elif type( isoLnInfo )== types.StringType :
            for item in self.isoLnActors:
                if isoLnInfo == item[0]:
                    isoLnInfo = self.isoLnActors.index( item            )
                    found   = True
                    break
            if not found:
                raise acuVisError, "Invalid name for delete "\
                      "iso-line actor <%s>." % isoLnInfo

        else:
            raise acuVisError, "Invalid name or id for delete "\
                  "iso-line actor <%s>." % isoLnInfo

        self.isoLnActors[ isoLnInfo ][1].removeIsoLnSet(                )
        del self.isoLnActors[                       isoLnInfo           ]


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

        self.asg.setScalar( scalar, name, sclrMinVal, sclrMaxVal )

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

        return self.asg.setSclrLimits( sclrMinVal, sclrMaxVal )
			
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

        return self.asg.setSclrMinVal( sclrMinVal )

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

        return self.asg.setSclrMaxVal( sclrMaxVal )

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

        self.asg.setCmap( cmap )

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

        self.asg.setVel( vel, name, velScale )

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

        self.asg.setVelScale( velScale )

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

        self.asg.setVelScalar( velScalar,       velScalarType,
                               velSclrMinVal,   velSclrMaxVal )

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

        return self.asg.setVelSclrLimits( velSclrMinVal, velSclrMaxVal )
			
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

        return self.asg.setVelSclrMinVal( self, velSclrMinVal )

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

        return self.asg.setVelSclrMaxVal( self, velSclrMaxVal )

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

        return self.asg.setVelWidth( velWidth )

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

        return self.asg.setVelArrowType( velArrowType )

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

        return self.asg.setVelColorType( velColorType )

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

        return self.asg.setVelColor( velColor )

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

        return self.asg.setVelCmap( velCmap )

#---------------------------------------------------------------------------
# addClipPlane: Add a clip plane for a special actor
#---------------------------------------------------------------------------

    def addClipPlane( self, center,
                            direction,
                            side    = 'up',
                            actor   = None,
                            name    = None  ):

        '''
            Add a clip plane for a special actor

            Arguments:
                center      - A point in clip plane
                direction   - Direction of unclipped half-space
                side        - Side of the clip plane ( 'up' [default] or 'down' )
                actor       - The actor containing the clip plane
                              ( if None [default], then applys to dynObjects )
                name        - Name of the clip plane

            Output:
                a AcuSgClipShape object containing the clip plane
        '''

        return self.asg.addClipPlane( center,
                                      direction,
                                      side,
                                      actor,
                                      name                              )

#---------------------------------------------------------------------------
# delClipPlane: Remove a clip plane
#---------------------------------------------------------------------------

    def delClipPlane( self, clipPlane ):

        '''
	    Remove a clip plane
	
	    Arguments:
	        clipPlane   - The AcuSgClipShape clip plane object to be removed

	    Output:
	        None
        '''

        self.asg.delClipPlane( clipPlane                                )

#---------------------------------------------------------------------------
# addClipBox: Add a clip box for a special actor
#---------------------------------------------------------------------------

    def addClipBox( self,   xmin,
                            xmax,
			    ymin,
                            ymax,
                            zmin,
                            zmax,			
                            actor   = None,
                            name    = None  ):

        '''
            Add a clip box for a special actor

            Arguments:
                xmin    - minimum x value of the box bounding box
                xmax    - maximum x value of the box bounding box
                ymin    - minimum y value of the box bounding box
                ymax    - maximum y value of the box bounding box
                zmin    - minimum z value of the box bounding box
                zmax    - maximum z value of the box bounding box
                actor   - The actor containing the clip box
                          ( if None [default], then applys to dynObjects )
                name    - name of the clip box

            Output:
                a AcuSgClipShape object containing the clip box
        '''

        return self.asg.addClipBox(  xmin,
                                     xmax,
                                     ymin,
                                     ymax,
                                     zmin,
                                     zmax,
                                     actor,
                                     name                               )

#---------------------------------------------------------------------------
# delClipBox: Remove a clip box
#---------------------------------------------------------------------------

    def delClipBox( self, clipBox ):

        '''
	    Remove a clip box
	
	    Arguments:
	        clipBox   - The AcuSgClipShape clip box object to be removed

	    Output:
	        None
        '''

        self.asg.delClipBox( clipBox                                    )

#---------------------------------------------------------------------------
# setClipTrans: Set the clipping transparency level of a special actor
#---------------------------------------------------------------------------

    def setClipTrans( self, transparent   = False,
                            transVal      = 0.5,
                            actor         = None  ):

        '''
            Set the clipping transparency level of a special actor

            Arguments:
                transparent - If true, set the clipped section as fully-transparent ( invisible )
                transVal    - The transparency level of clipped section
                actor       - The actor whose transparency should be set
                              ( if None [default], then applys to dynObjects )

            Output:
                None
        '''	

        self.asg.setClipTrans( transparent, transVal, actor             )

#---------------------------------------------------------------------------
# setClipMode: Set the clipping mode of all clip shape objects for a special actor
#---------------------------------------------------------------------------

    def setClipMode( self,  mode    = 'max',
                            actor   = None  ):

        '''
	    Set the clipping mode of all clip shape objects for a special actor
	
	    Arguments:
	        mode    - mode of clipping ( 'max' [default] or 'min' )	
	        actor   - The actor whose clipping mode should be set
	
	    Output:
	        None
        '''

        self.asg.setClipMode( mode, actor      	                        )

#---------------------------------------------------------------------------
# getSceneGraph: Get the view scene graph
#---------------------------------------------------------------------------

    def getSceneGraph( self ):

        return self.asg.viewer.getSceneGraph(                           )

#---------------------------------------------------------------------------
# getSceneGraphListForTimeSteps: Get list of scene graphs for a step list
#---------------------------------------------------------------------------

    def getSceneGraphListForTimeSteps( self,    timeStepList    = None,
                                                timeStepRange   = [0, 1] ):               

        if timeStepList != None:
            steps = timeStepList
        else:
            steps = range( timeStepRange[0], timeStepRange[1] )

        currentStepId = self.stepId 

        sceneGraphList = []
        for stepId in steps:            
            self.setStepId( stepId )
            sg = self.getSceneGraph( ).copy( )
            #sg.setName( "%s_TimeStep_%d" % ( self.problem, stepId + 1 ) )
            sg.setName( "Time_Step_%d" % ( stepId + 1 ) )
            sceneGraphList.append( sg )
                                                
        self.setStepId( currentStepId )

        return sceneGraphList

#-------------------------------------------------------------------------
# getOutValues: A simple function to get nodal output.
#-------------------------------------------------------------------------

    def getOutValues( self,     varInfo,
                      stepId    = None
                    ):
        
        """ A simple function to get nodal output values
            according to the step id.

            Arguments:
                varInfo - Variable id or variable name
                stepId  - Step id

            Output:
                Nodal output values.
        """

        varIndx     = self.chkUsrVarInfo(           varInfo             )
        stepId      = self.chkUsrStpId(             stepId              )

        return self.adb.get( 'outValues',           varIndx,    stepId  )

#-------------------------------------------------------------------------
# getOutLimits: Returns the min/max values
#-------------------------------------------------------------------------

    def getOutLimits( self,     varInfo,
                      stepId    = None
                    ):
        
        """ A simple function to get the min/max nodal output values
            according to the step id.

            Arguments:
                varInfo - Variable id or variable name
                stepId  - Step id

            Output:
                Nodal output min/max values.
        """

        values      = self.getOutValues(            varInfo,    stepId  )

        return int( values.min() ), int( values.max() ) + 1
        
#-------------------------------------------------------------------------
# chkUsrStpId: Check the user stepId value.
#-------------------------------------------------------------------------

    def chkUsrStpId( self,    stepId = None ):
        
        """ A function to check the validity of the stepId value.

            Arguments:
                stepId - Step id

            Output:
                Step id
        """

        if stepId == None:
            stepId          = self.stepId

        else:
            if not self.steps or stepId not in xrange(len( self.steps )):
                raise acuVisError, "Steps list is empty or "\
                                      "stepId is out of range."
        
        return stepId

#-------------------------------------------------------------------------
# chkUsrVarInfo: Check the user varInfo value.
#-------------------------------------------------------------------------

    def chkUsrVarInfo( self,    varInfo ):
        
        """ A function to check the validity of the varInfo value.

            Arguments:
                varInfo - Variable id or variable name

            Output:
                Variable index
        """

        if type( varInfo ) == types.IntType:
            nVars           = self.adb.get(             "nOutVars"      )
            if varInfo in xrange( nVars ):
                varIndx     = varInfo
            else:
                raise acuVisError, "Invalid variable index.It should "\
                                      "be between 0 and %d" % nVars

        elif type( varInfo )== types.StringType and varInfo in self.varNames:
            varIndx         = self.varNames.index(      varInfo         )

        else:
            raise acuVisError, "Invalid variable name or id (%s)" %varInfo
        
        return varIndx

#================================================================================
#
# Test
#
#================================================================================

if __name__ == '__main__':

    # ----- Creating the AcuVis Object
    av      = AcuVis(                       "pump"                   )

    # ----- Playing with Surface actors

    inflow  = av.getSrfActor(               0                           )
    wall    = av.getSrfActor(               "wall"                      )
    inflow.display(                         "wireframe"                 )
    wall.color(                             r = 0.5,
                                            g = 0.5,
                                            b = 0.5                     )
    wall.transparency(                      True                        )

    # ----- Playing with Scalar and Vector Variables

    nVars   = av.getNVars(                                              )
    nSVars  = av.getNSclrVars(                                          )
    nVVars  = av.getNVecVars(                                           )

    for i in range(nVars):
        print av.getVarName( i ),"with dimension:",av.getVarDim( i      )
    for i in range(nSVars):
        print "Sacalar Vars = ",av.getSclrVarName(      i               )
    for i in range(nVVars):
        print "Vector Vars = ",av.getVecVarName(        i               )

    av.setSclrVar(                          1                           )
    av.setSclrVar(                          'pressure'                  )
    av.setSclrLimits(                                             )
    av.setVecVar(                           0                           )
    av.setVecVar(                           'velocity'                  )
    av.setVecScale(                         5                           )


    # ----- Craeting Cut Plane Actor
    cpl         = av.addCPlane(             [5.0, 1.0, 0.0],
                                            [0.0, 1.0, 0.0],
                                            [0.0, 0.0, 0.0],
                                            "cut-plane 1"               )

    cpl.display(                            'wireframe'                 )
    cpl.transparencyVal(                    0.1                         )
    cpl.color(                              1, 0, 0                     )
    cpl.pointSize(                          10                          )
##    cpl.setIsoVal(                          0.4                         )

    nCpls       = av.getNCpls(                                          )

    av.saveImage(                                                       )

    for i in range(nCpls):
        name    = av.getCplName(            i                           )
        actor   = av.getCplActor(           name                        )
        actor2  = av.getCplActor(           i                           )
##        av.delCplActor(                     i                           )
        av.delCplActor(                     name                        )

    av.saveImage(                                                       )

    # ----- Adding Iso Surface Actor
##    pres        = av.addIsoSurface(         "pressure",
##                                            0.1,
##                                            "pres-iso"                  )
##    for id in range(av.getNVols()):
##        av.getVolActor(id).setVisibility('off')
##    pres        = av.addIsoLine(        av.crd[:,0] * av.crd[:,0] + av.crd[:,1] * av.crd[:,1] + av.crd[:,2] * av.crd[:,2],
##                                        0.015,
##                                        "pres-iso" ,
##                                        'wall'                          )
##
##    pres.lineWidth(                           12                     )
##    av.setSclrVar( "pressure" )
##    pres.display('contour')
##    pres.transparencyVal(                   0.1                         )
##    pres.color(                             0, 0, 1                     )
##    pres.pointSize(                         10                          )
##    pres.setIsoVal(                         0.19                        )

##    nIsos       = av.getNIsos(                                          )
##
##    for i in range(nIsos):
##        name    = av.getIsoName(            i                           )
##        actor   = av.getIsoActor(           name                        )
##        actor2  = av.getIsoActor(           i                           )
##        av.delIsoActor(                     i                           )
##        av.delIsoActor(                     name                        )
##
##    # ----- Changing Time step
##
##    av.getSteps(                                                        )
##    av.setStep(                             2                           )

    # ----- Testing Orientation methods

    av.home(                                                            )
    av.fit(                                                             )
    av.snap(                                                            )
    av.snapz(                                                           )
    av.alignView(                           dir = '+x'                  )
    av.alignView(                           dir = '-x'                  )
    av.alignView(                           dir = '+y'                  )
    av.alignView(                           dir = '-y'                  )
    av.alignView(                           dir = '+z'                  )
    av.alignView(                           dir = '-z'                  )
    av.rotate(                              dir = '+x'                  )
    av.rotate(                              dir = '-x'                  )
    av.rotate(                              dir = '+y'                  )
    av.rotate(                              dir = '-y'                  )
    av.rotate(                              dir = '+z'                  )
    av.rotate(                              dir = '-z'                  )

    # ----- Adding text and Image actors

    av.addTxtActor( text = 'Test', color = [0,0,1], fontSize = 20       )
    av.addImgActor( filename = "logo_med.jpg", position = [0.73,0.78,0.5],
                    width = 300 , height = 60                           )

    # ----- Creating animation from a seri of images

##    images      = []
##    for temp in range( 10, 50, 5 ):
##        temp    = float( temp )/ 1000
##        pres.setIsoVal(                     temp                        )
##        image   = av.saveImage(                                         )
##        images.append(                      image                       )

##    anim        = AcuAnim(                'test.mpg',
##                                            images,
##                                            delay = 20                  )

    # ----- Saving the Image

    av.saveImage(                                                       )



