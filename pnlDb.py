#---------------------------------------------------------------------------
# Get the modules
#---------------------------------------------------------------------------

import      re
import      acuUnit
import      acuhdf
import      shutil
import      os.path
import      numarray
import      time
import      types

#---------------------------------------------------------------------------
# Define Constants.
#---------------------------------------------------------------------------

VERSION     = 1.0

ROOT	    = acuhdf.ROOT
RS	    = acuhdf.RS

coordinates = ROOT + RS + 'Mesh'    + RS + 'Coordinate'

modelSrf    = ROOT + RS + 'Model'   + RS + 'Surfaces'
meshSrf     = ROOT + RS + 'Mesh'    + RS + 'Surfaces'
geomSrf     = ROOT + RS + 'Geom'    + RS + 'Surfaces'
tdaSrf      = ROOT + RS + "Template"+ RS + "Surfaces"

modelVol    = ROOT + RS + 'Model'   + RS + 'Volumes'
meshVol     = ROOT + RS + 'Mesh'    + RS + 'Volumes'
geomVol     = ROOT + RS + 'Geom'    + RS + 'Volumes'
tdaVol      = ROOT + RS + "Template"+ RS + "Volumes"

modelNbc    = ROOT + RS + 'Model'   + RS + 'Nodes'#'NBCs'
meshNbc     = ROOT + RS + 'Mesh'    + RS + 'Nodes'#'NBCs'
geomNbc     = ROOT + RS + 'Geom'    + RS + 'Nodes'

modelPbc    = ROOT + RS + 'Model'   + RS + 'Periodics'
meshPbc     = ROOT + RS + 'Mesh'    + RS + 'Periodics' 
geomPbc     = ROOT + RS + 'Geom'    + RS + 'Periodics'

modelLine   = ROOT + RS + 'Model'   + RS + 'Lines'
meshLine    = ROOT + RS + 'Mesh'    + RS + 'Lines'

header      = ROOT + RS + 'data base header'

mainPath    = ROOT + RS + 'main' 

#===========================================================================
# Errors
#===========================================================================

ParValueError= \
         "Path = %s, par = %s, The value and default value are both None."

PnlDbError  = "ERROR from pnlDb module"

#---------------------------------------------------------------------------
# Define types
#---------------------------------------------------------------------------

INT	    = 0x101
BOOL	    = 0x102
REAL	    = 0x201
STR	    = 0x301
ENUM	    = 0x302
REF	    = 0x303
TAB	    = 0x304
TAREA	    = 0x305
FILE        = 0x306
DIR         = 0x307
FONT        = 0x308
PASSWD      = 0x309
LIST	    = 0x401
REFS	    = 0x402
ARY	    = 0x501
COLOR	    = 0x502
FDATA       = 0x601

#===========================================================================
#
# "PnlDb": DB class.
#
#===========================================================================

class PnlDb:

    """
    Database for acuPanel application.

    Database structure:
        The database supports the following types:

        INT     : Integer parameter.
        STR     : String parameter.
        REF     : A reference.
        TAB     : A String (for now).
        REFS    : A list of references.
        BOOL    : Boolean parameter.
        REAL    : Double parameter.
        ENUM    : A String (for now).
        LIST    : An Array of strings.
        ARRAY   : An integer or read array.

        The database stores each par as a leaf which name
        is equal to par's name.
        The other information is stored in leaf's attributeSet,
        which does not take much disk space.

        Note: This database converts all the path types to a standard form
        and uses the standard form to traverse the tree.
        An exapmle of standard path: ROOT + RS + volume + RS + pipe
    """

    def __init__(   self,   fileName,   mode = 'new' ):

        """
        Initialize the database layer.

        Argument:

            fileName    :   The data base name.
            mode        :   The mode of data base which will be opened.

        Return:
            None
        
        """

        #----- Define data base special variables



        self.RS             = RS
        self.ROOT           = ROOT
        self.coordinates    = coordinates

        self.modelSrf       = modelSrf
        self.meshSrf        = meshSrf
        self.geomSrf        = geomSrf
        self.tdaSrf         = tdaSrf

        self.modelVol       = modelVol
        self.meshVol        = meshVol
        self.geomVol        = geomVol
        self.tdaVol         = tdaVol

        self.modelNbc       = modelNbc
        self.meshNbc        = meshNbc
        self.geomNbc        = geomNbc

        self.modelPbc       = modelPbc
        self.meshPbc        = meshPbc 
        self.geomPbc        = geomPbc

        self.modelMex       = self.ROOT + self.RS + 'Model' + self.RS + 'Mesh Extrusions'
        self.meshMex        = self.ROOT + self.RS + 'Mesh'  + self.RS + 'Mesh Extrusions'
        self.geomMex        = self.ROOT + self.RS + 'Geom'  + self.RS + 'Mesh Extrusions'

        self.modelLine      = modelLine
        self.meshLine       = meshLine

        self.nodePev        = self.ROOT + self.RS + 'Eigenmode'

        self.header         = header
        
        self.mainPath       = mainPath
        self.modelPath      = self.ROOT + self.RS + 'Model'
        self.tdaPath        = self.ROOT + self.RS + "Template"

        self.INT	    = INT
        self.BOOL	    = BOOL
        self.REAL	    = REAL
        self.STR	    = STR
        self.ENUM	    = ENUM
        self.REF	    = REF
        self.TAB	    = TAB
        self.TAREA	    = TAREA
        self.FILE	    = FILE
        self.DIR	    = DIR
        self.FONT	    = FONT
        self.PASSWD	    = PASSWD
        self.LIST	    = LIST
        self.REFS	    = REFS
        self.ARY	    = ARY
        self.COLOR	    = COLOR
        self.FDATA          = FDATA

        #----- Open the data base fileName.

        self.fileName       = fileName
        self.state1         = None

        if mode == 'old':
            self.dataFile   = acuhdf.AcuHDF(    str( fileName ),    'a' )

            #----- Misc. 6/07 K2
            try:
                dbAcuhdfVer = self.getRealPar(  'acuhdf_version',
                                                mainPath                )
                if dbAcuhdfVer != acuhdf.version:
                    print "Openning an older data base"
            except:
                pass

        else:
            self.dataFile   = acuhdf.AcuHDF(    str( fileName ),    'w' )
            timeValue       = time.time(  				)
            self.putRealPar(    'lastMod',      timeValue,      header  )
            self.putRealPar(    'version',      VERSION,        header  )

            #----- Misc. 6/07 K2
            self.putRealPar(    'acuhdf_version',
                                acuhdf.version, mainPath                )

##        #----- Misc. 6/07 K3
##        self.putIntPar(         'initDbMId',
##                                self.dataFile.currMId(),        mainPath)

        #----- Misc. 1/08 J11 ; as the above code cause a new mId and we
        #----- need to show data base dialog.
            
        self.initDbMIdVal   = self.dataFile.currMId(                    )

#---------------------------------------------------------------------------
# "version": Return the version of database.
#---------------------------------------------------------------------------

    def version( self ):

        """

        Return the version of database.

        Argument:

            None

        Return:

            version     :   The data base version.

        """

        version = self.getRealPar(  'version',  header                  ) 
        return  version

#---------------------------------------------------------------------------
# "lastMod": Return the last modify date as an integer.
#---------------------------------------------------------------------------

    def lastMod( self ):

        """

        Return the last modify date as an integer.
        
        Argument:

            None

        Return:

            lastMod     :   The last modify date.

        """

        lastMod = self.getRealPar(  'lastMod',  header                  ) 
        return lastMod

#---------------------------------------------------------------------------
# "getInitDbMIdVal": Return the initial mId value as an integer.
#---------------------------------------------------------------------------

    def getInitDbMIdVal( self ):

        """

        Return the initial mId value as an integer.
        
        Argument:

            None

        Return:

            initDbMIdVal:   The initial mId value.

        """

        return self.initDbMIdVal

#---------------------------------------------------------------------------
# "flush": Sync with the disk.
#---------------------------------------------------------------------------

    def flush( self ):

        """

        Sync with the disk.
        
        Argument:

            None

        Return:

            None

        """

        #----- Misc. 1/08 J11
        if self.initDbMIdVal == self.dataFile.currMId() : return

        timeValue           = time.time(  				)
        self.putRealPar( 'lastMod',  timeValue,  header          	)
        
        self.dataFile.flush(                                            )

#---------------------------------------------------------------------------
# "chkNode": check if the Node exists.
#---------------------------------------------------------------------------

    def chkNode( self, path ):

        """

        Check if the node exists and return True if it exists.
        
        Argument:

            path        : The node path

        Return:

            True if the node exists else False.

        """

        return self.dataFile.chkNode(           path                    )

#---------------------------------------------------------------------------
# "delNode": delete a node.
#---------------------------------------------------------------------------

    def delNode( self, path ):

        """

        Delete a node.
        
        Argument:

            path        : The node path.

        Return:

            None

        """

        self.dataFile.delNode(                  path                    )

#---------------------------------------------------------------------------
# "dupNode": duplicate a node.
#---------------------------------------------------------------------------

    def dupNode( self, path, newAddr  ):

        """
        Duplicate a node and all its children.
        
        Argument:

            path        : The node path.
            newAddr     : The node new address.

        Return:

            None

        """

        self.dataFile.dupNode(      path,       newAddr                 )
 
#---------------------------------------------------------------------------
# "mvNode": rename a node.
#---------------------------------------------------------------------------

    def mvNode( self, path, newAddr  ):

        """
        Rename a node.
        
        Argument:

            path        : The node path.
            newAddr     : The node new address.

        Return:

            None

        """

        self.dataFile.moveNode(     path,       newAddr                 )

#----------------------------------------------------------------------------
# "childNodes": get a list of child nodes.
#---------------------------------------------------------------------------

    def childNodes( self, path, reg = None ):

        """
        Get a list of child nodes.
        
        Argument:

            path        : The node path.
            reg         : Regular expression.

        Return:

            The list of child nodes.

        """

        if self.chkNode( path ):
            return self.dataFile.listNodes(         path                )
        
        else:
            return [ ]
    
#----------------------------------------------------------------------------
# "childPars": get a list of child pars.
#---------------------------------------------------------------------------

    def childPars( self, path, reg = None ):

        """
        Get a list of Child Pars.
        
        Argument:

            path        : The node path.
            reg         : Regular expression.

        Return:

            The list of child pars.

        """

        if self.chkNode( path ):
            return self.dataFile.listPars(          path                )
        
        else:
            return [ ]

#---------------------------------------------------------------------------
# "putBoolPar()": Inserts a boolean leaf to the tree.
#---------------------------------------------------------------------------

    def putBoolPar( self, name, value, path = None, clobber = True, **opts ):

        """
        Inserts a boolean leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        if value:
            value   = 1
            
        else:
            value   = 0
            
        self.dataFile.putInt(   name, value, path, BOOL, clobber, **opts)
        
#---------------------------------------------------------------------------
# "putIntPar()": Inserts an integer leaf to the tree.
#---------------------------------------------------------------------------

    def putIntPar( self, name, value, path = None, clobber = True, **opts):

        """
        Inserts an integer leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        self.dataFile.putInt(   name, value, path, INT, clobber, **opts )

#---------------------------------------------------------------------------
# "putRealPar()": Inserts a real leaf to the tree.
#---------------------------------------------------------------------------

    def putRealPar( self, name, value, path = None, clobber = True, **opts ):

        """
        Inserts a real leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        self.dataFile.putReal(  name, value, path, REAL, clobber,**opts )
        

#---------------------------------------------------------------------------
# "putStrPar()": Inserts a string leaf to the tree.
#---------------------------------------------------------------------------

    def putStrPar( self, name, value, path = None, clobber = True, **opts):

        """
        Inserts a string leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        if value == "" :
            value = " "
            
        self.dataFile.putStr(   name, value, path, STR, clobber, **opts )

#---------------------------------------------------------------------------
# "putEnumPar()": Inserts an enum leaf to the tree.
#---------------------------------------------------------------------------

    def putEnumPar( self, name, value, path = None, clobber = True, **opts):

        """
        Inserts an enum leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        self.dataFile.putStr(   name, value, path, ENUM, clobber, **opts )

#---------------------------------------------------------------------------
# "putListPar()": Inserts a list leaf to the tree.
#---------------------------------------------------------------------------

    def putListPar( self, name, value, path = None, clobber = True, **opts):

        """
        Inserts a list leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        self.dataFile.putStrs(   name, value, path, LIST, clobber, **opts )
        
#---------------------------------------------------------------------------
# "putRefsPar()": Inserts a refs leaf to the tree.
#---------------------------------------------------------------------------

    def putRefsPar( self, name, value, path = None, clobber = True, **opts):

        """
        Inserts a refs leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        self.dataFile.putStrs(   name, value, path, REFS, clobber, **opts )
        
#---------------------------------------------------------------------------
# "putArrayPar()": Inserts an array leaf to the tree.
#---------------------------------------------------------------------------

    def putArrayPar( self, name, value, path = None, clobber = True, **opts ):

        """
        Inserts an array leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        if type( value ) != numarray.numarraycore.NumArray:
            value = numarray.array(                 value               )
            
        self.dataFile.putArray( name, value, path,  ARY, clobber, **opts)

#---------------------------------------------------------------------------
# "putRefPar()": Inserts a Ref leaf to the tree.
#---------------------------------------------------------------------------

    def putRefPar( self, name, value, path = None, clobber = True, **opts):

        """
        Inserts a ref leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        if value == "" :
            value = " "
            
        self.dataFile.putStr(   name, value, path, REF, clobber, **opts )
        
#---------------------------------------------------------------------------
# "putTabPar()": Inserts a Tab leaf to the tree.
#---------------------------------------------------------------------------

    def putTabPar( self, name, value, path = None, clobber = True, **opts):

        """
        Inserts a tab leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        self.dataFile.putStr(   name, value, path, TAB, clobber, **opts )

#---------------------------------------------------------------------------
# "putTarePar()": Inserts a Tarea (Text Area) leaf to the tree.
#---------------------------------------------------------------------------

    def putTareaPar( self, name, value, path = None, clobber = True, **opts):

        """
        Inserts a tarea (text area) leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        if value == "":
            value = " "
            
        self.dataFile.putStr( name, value, path, TAREA, clobber, **opts )

#---------------------------------------------------------------------------
# "putFileDataPar()": Inserts a file leaf to the tree.
#---------------------------------------------------------------------------

    def putFileDataPar( self, name, value, path = None, clobber = True, **opts):

        """
        Put the content of the file in the data base and the name of
        the file is store in an attribute
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        self.dataFile.putFile(   name, value, path, FDATA, clobber, **opts)

#---------------------------------------------------------------------------
# "putDicPar()": Inserts a dictionary leaf to the tree.
#---------------------------------------------------------------------------

    def putDicPar( self, name, value, path = None, clobber = True, **opts):

        """
        Put the content of the dictionary in the data base.        
        Argument:

            name        : The par name.
            value       : The par value; a dictionary data type.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        if not type( value ) == types.DictType:
            raise "Value must be dictionary"
            return

        self.delNode(   path + self.RS + name       )
        path        = path + self.RS + name + self.RS
        par         = name
        
        #----- check if the dictionary is empty (i.e.{})
        if value    == {}:
            key     = "empty"
            val     = []
            node    = path + key
            self.putListPar(            par, val, node, clobber, **opts )
        
        for key, val in value.items():
            node    = path + key

            try:            
                if type( val ) == types.BooleanType:
                    self.putBoolPar(    par, val, node, clobber, **opts )

                elif type( val ) in ( types.IntType, types.LongType ):
                    self.putIntPar(     par, val, node, clobber, **opts )
                    
                elif type( val ) == types.FloatType:
                    self.putRealPar(    par, val, node, clobber, **opts )

                elif type( val ) in types.StringTypes:
                    self.putStrPar(     par, val, node, clobber, **opts )

                elif type( val ) == types.ListType:
                    self.putListPar(    par, val, node, clobber, **opts )

                elif type( val ) == numarray.numarraycore.NumArray:
                    self.putArrayPar(   par, val, node, clobber, **opts )
            
                elif type( val ) == types.DictType:
                    self.putDicPar(     par, val, node, clobber, **opts )
                else:
                    raise PnlDbError, \
                        'Unable to put the value of the key "%s" in the dictionary' %key
            except:
                raise PnlDbError, \
                    'Unable to put the value of the key "%s" in the dictionary' %key                

#---------------------------------------------------------------------------
# "putFilePar()": Inserts a file leaf to the tree.
#---------------------------------------------------------------------------

    def putFilePar( self, name, value, path = None, clobber = True, **opts):

        """
        Inserts a file leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        if value == "" :
            value = " "
            
        self.dataFile.putStr(   name, value, path, FILE, clobber, **opts)

#---------------------------------------------------------------------------
# "putDirPar()": Inserts a directory leaf to the tree.
#---------------------------------------------------------------------------

    def putDirPar( self, name, value, path = None, clobber = True, **opts):

        """
        Inserts a directory leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        if value == "" :
            value = " "
            
        self.dataFile.putStr(   name, value, path, DIR, clobber, **opts )

#---------------------------------------------------------------------------
# "putPasswdPar()": Inserts a password leaf to the tree.
#---------------------------------------------------------------------------

    def putPasswdPar( self, name, value, path = None, clobber = True, **opts):

        """
        Inserts a password leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        if value == "" :
            value = " "
            
        self.dataFile.putStr( name, value, path, PASSWD, clobber, **opts)

#---------------------------------------------------------------------------
# "putFontPar()": Inserts a font leaf to the tree.
#---------------------------------------------------------------------------

    def putFontPar( self, name, value, path = None, clobber = True, **opts):

        """
        Inserts a font leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        if value == "" :
            value = " "
            
        self.dataFile.putStr(   name, value, path, FONT, clobber, **opts)

#---------------------------------------------------------------------------
# "putColorPar()": Inserts a color leaf to the tree.
#---------------------------------------------------------------------------

    def putColorPar( self, name, value, path = None, clobber = True, **opts ):

        """
        Inserts a color leaf to the tree.
        
        Argument:

            name        : The par name.
            value       : The par value.
            path        : The par path.
            clobber     : If True, overwite the value.
            opts        : Options like "unit" and etc.

        Return:

            None

        """

        if type( value ) != numarray.numarraycore.NumArray:
            value = numarray.array(                 value               )
            
        self.dataFile.putArray( name, value, path, COLOR, clobber,**opts)

#---------------------------------------------------------------------------
# "getBoolPar()": Get a bool Par value.
#---------------------------------------------------------------------------

    def getBoolPar( self, name, path = None, default = None ):

        """
        Get a bool Par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The bool par value if it exists else return default value.

        """

        parts   = self.dataFile.getInt(     name,       path,   BOOL    )
        
        if parts != None:
            
            if parts[0] == 1:
                return True
            
            else:
                return False
            
        elif default != None:
            self.putBoolPar(    name,       default,    path            )
            return default
        
        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getIntPar()": Get an integer Par value.
#---------------------------------------------------------------------------

    def getIntPar( self, name, path = None,default = None ):

        """
        Get an integer Par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The integer par value if it exists else return default value.

        """

        parts   = self.dataFile.getInt(     name,       path,   INT     )
        
        if parts != None:
            return parts[0]

        elif default != None:
            self.putIntPar(         name,   default,    path            )
            return default
        
        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getRealPar()": Get a real Par value.
#---------------------------------------------------------------------------

    def getRealPar( self, name, path = None, default = None, unit = None ):

        """
        Get a real Par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.
            unit        : The par unit.

        Return:

            The real par value if it exists else return default value.

        """

        parts   = self.dataFile.getReal(    name,       path,   REAL    )
        
        if parts != None:
            retValue    = parts[0] 
                
        elif default != None:
            self.putRealPar(    name,       default,    path,   True    )
            retValue    = default
            
        else:
            raise PnlDbError, ParValueError %(  path,   name            )

        #----- Do conversion if needed.

        if unit == acuUnit.RAW_UNIT : return retValue

        #----- get the source and unit value

        srcUnit = None

        if parts and parts[ 1 ].has_key( 'unit' ):
            srcUnit     = parts[ 1 ]['unit']

        if srcUnit == None and unit == None: return retValue

        if unit == None:
            unit    = acuUnit.getBaseUnit(              srcUnit         )

        if srcUnit == None:
            srcUnit = acuUnit.getBaseUnit(              unit            )

        #----- convert the value

        retValue    = acuUnit.convert(      retValue,   srcUnit, unit   )
        
        return retValue

#---------------------------------------------------------------------------
# "getStrPar()": Get a string Par value.
#---------------------------------------------------------------------------

    def getStrPar( self, name, path = None, default = None ):

        """
        Get a string Par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The string par value if it exists else return default value.

        """

        parts   = self.dataFile.getStr(     name,       path,   STR     )
        
        if parts:
            
            if parts[0] == " ":
                return ""
            return parts[0]

        elif default != None:
            self.putStrPar(     name,       default,    path            )
            return default
        
        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getEnumPar()": Get an integer Par value.
#---------------------------------------------------------------------------

    def getEnumPar( self, name, path = None, default = None ):

        """
        Get an enum par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The enum par value if it exists else return default value.

        """

        parts   = self.dataFile.getStr(     name,       path,   ENUM    )
        
        if parts:
            return parts[0]

        elif default != None:
            self.putEnumPar(    name,       default,    path            )
            return default

        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getListPar()": Get a list Par value.
#---------------------------------------------------------------------------

    def getListPar( self, name, path = None, default = None ):

        """
        Get a list par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The list par value if it exists else return default value.

        """

        parts   = self.dataFile.getStrs(    name,      path,    LIST    )
        
        if parts:
            return parts[0]

        elif default != None:
            self.putListPar(    name,       default,    path            )
            return default
        
        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getArrayPar()": Get an array Par value.
#---------------------------------------------------------------------------

    def getArrayPar( self, name, path = None, default = None, unit = None ):

        """
        Get an array par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The array par value if it exists else return default value.

        """

        parts   = self.dataFile.getArray(   name,       path,   ARY     )
        
        if parts:
            returnVal   = parts[0]
            if type( returnVal ) != numarray.numarraycore.NumArray:
                returnVal = numarray.array(             returnVal       )

        elif default != None:
            
            if type( default ) != numarray.numarraycore.NumArray:
                default = numarray.array(               default         )
                
            self.putArrayPar(   name,       default,    path            )
            returnVal   = default

        else:
            raise PnlDbError, ParValueError %(  path,   name            )

        #----- Do conversion if needed.

        if unit == acuUnit.RAW_UNIT : return returnVal

        #----- get the source and unit value

        srcUnit = None

        if parts and parts[ 1 ].has_key( 'unit' ):
            srcUnit     = parts[ 1 ]['unit']

        if srcUnit == None and unit == None: return returnVal

        if unit == None:
            try:
                srcUnits    = re.split(     ':',    srcUnit             )
                unit        = ''
                for cnt in range(len(srcUnits)):
                    try:
                        unit    += acuUnit.getBaseUnit( srcUnits[cnt] ) + ":"
                    except:
                        unit    += 'nondim' + ":"
                unit        = unit[:-1]
            except:
                unit        = acuUnit.getBaseUnit(  srcUnit             )

        if srcUnit == None:
            try:
                units       = re.split(     ':',    unit                )
                srcUnit     = ''
                for cnt in range(len(units)):
                    try:
                        srcUnit += acuUnit.getBaseUnit(  units[cnt] ) + ":"
                    except:
                        srcUnit += 'nondim' + ":"
                srcUnit     = srcUnit[:-1]
            except:
                srcUnit     = acuUnit.getBaseUnit(  unit                )

        #----- convert the value

        retVal  = []

        units   = re.split(                     ":", unit               )        
        srcUnit = re.split(                     ":", srcUnit            )
        for item in returnVal:
            itemVal = []
            if type(item) == numarray.numarraycore.NumArray:
                if units[0] != 'nondim':
                    itemVal.append( acuUnit.convert( item[0],
                                                     srcUnit[0],
                                                     units[0]       )   )
                else:
                    itemVal.append( item[0]                             )
                for num in range(1, len(item)):
                    try:
                        if units[num] != 'nondim':
                            itemVal.append( acuUnit.convert( item[num],
                                                         srcUnit[num],
                                                         units[num] )   )
                        else:
                            itemVal.append( item[num]                   )
                    except:
                        if units[-1] != 'nondim':
                            itemVal.append( acuUnit.convert( item[num],
                                                         srcUnit[-1],
                                                         units[-1]  )   )
                        else:
                            itemVal.append( item[num]                   )
                    
                retVal.append(                  itemVal                 )
            else:
                if units[0] != 'nondim':
                    retVal.append( acuUnit.convert( item, srcUnit[0],
                                                units[0]            )   )
                else:
                    retVal.append( item                                 )
                    
                

        returnVal    = numarray.array(          retVal                  )
        
        return returnVal

#---------------------------------------------------------------------------
# "getRefPar()": Get a Ref Par value.
#---------------------------------------------------------------------------

    def getRefPar( self, name, path = None, default = None ):

        """
        Get a ref par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The ref par value if it exists else return default value.

        """

        parts   = self.dataFile.getStr(     name,       path,   REF     )
        
        if parts:
            if parts[0] == " ":
                return ""
            return parts[0]

        elif default != None:
            self.putRefPar( name,           default,    path            )
            return default

        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getTabPar()": Get a Tab Par value.
#---------------------------------------------------------------------------

    def getTabPar( self, name, path = None, default = None ):

        """
        Get a tab par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The tab par value if it exists else return default value.

        """

        parts   = self.dataFile.getStr(     name,       path,   TAB     )
        if parts:
            return parts[0]

        elif default != None:
            self.putTabPar(   name,         default,    path            )
            return default

        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getRefsPar()": Get a reference Par value.
#---------------------------------------------------------------------------

    def getRefsPar( self, name, path = None, default = None ):

        """
        Get a refs par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The refs par value if it exists else return default value.

        """

        parts   = self.dataFile.getStrs(    name,       path,   REFS    )
        
        if parts:
            return parts[0]

        elif default != None:
            self.putRefsPar(    name,       default,    path            )
            return default

        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getTareaPar()": Get a Tarea (Text Area) Par value.
#---------------------------------------------------------------------------

    def getTareaPar( self, name, path = None, default = None ):

        """
        Get a tarea par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The tarea par value if it exists else return default value.

        """

        parts   = self.dataFile.getStr(     name,       path,   TAREA   )
        
        if parts:
            
            if parts[0] == " ":
                return ""
            return parts[0]

        elif default != None:
            self.putTareaPar(       name,   default,    path            )
            return default

        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getFileDataPar()": Get a file Par value.
#---------------------------------------------------------------------------

    def getFileDataPar( self, name, path = None, default = None ):

        """
        The content of the par is put in the file, and the name
        of the file is returned.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The integer par value if it exists else return default value.

        """

        parts   = self.dataFile.getFile(     name,       path,   FDATA  )

        if parts:
            return parts[0]

        elif default != None:
            self.putFileDataPar(        name,  default,    path         )
            return default
        
        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getDicPar()": Get a dictionary Par value.
#---------------------------------------------------------------------------

    def getDicPar( self, name, path = None, default = None ):

        """
        Get a dictionary Par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The dictionary par value if it exists else return default value.

        """

        retVal  = {}
        path    = path + self.RS + name
        dicKeys = self.childNodes(	path,		        1	)

        if not dicKeys:
            if default != None:
                self.putDicPar(         name,       default,    path    )
                return default
            else:
                raise PnlDbError, ParValueError  %( path,       name    )

        path    = path + self.RS
        for key in  dicKeys:
            node            = path + key
            if len( self.childNodes( node, 1 ) ) == 0:
                parType         = self.getParType(      name,   node    )
                retVal[ key ]   = self.getPar( name,    node,   parType )
            else:
                retVal[ key ]   = self.getDicPar(       name,   node    )

        #----- check if the dictionary is empty (i.e.{})
        if len( retVal ) == 1:
            if retVal.keys()[0] == "empty" and retVal.values()[0] == []:
                return {}
        
        return retVal
    
#---------------------------------------------------------------------------
# "getFilePar()": Get a file Par value.
#---------------------------------------------------------------------------

    def getFilePar( self, name, path = None, default = None ):

        """
        Get a file Par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The file par value if it exists else return default value.

        """

        parts   = self.dataFile.getStr(     name,       path,   FILE    )
        
        if parts:
            
            if parts[0] == " ":
                return ""
            return parts[0]

        elif default != None:
            self.putFilePar(     name,       default,    path           )
            return default
        
        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getDirPar()": Get a directory Par value.
#---------------------------------------------------------------------------

    def getDirPar( self, name, path = None, default = None ):

        """
        Get a directory Par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The directory par value if it exists else return default value.

        """

        parts   = self.dataFile.getStr(     name,       path,   DIR     )
        
        if parts:
            
            if parts[0] == " ":
                return ""
            return parts[0]

        elif default != None:
            self.putDirPar(     name,       default,    path            )
            return default
        
        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getPasswdPar()": Get a password Par value.
#---------------------------------------------------------------------------

    def getPasswdPar( self, name, path = None, default = None ):

        """
        Get a password Par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The password par value if it exists else return default value.

        """

        parts   = self.dataFile.getStr(     name,       path,   PASSWD  )
        
        if parts:
            
            if parts[0] == " ":
                return ""
            return parts[0]

        elif default != None:
            self.putPasswdPar(  name,       default,    path            )
            return default
        
        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getFontPar()": Get a font Par value.
#---------------------------------------------------------------------------

    def getFontPar( self, name, path = None, default = None ):

        """
        Get a font Par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The font par value if it exists else return default value.

        """

        parts   = self.dataFile.getStr(     name,       path,   FONT    )
        
        if parts:
            
            if parts[0] == " ":
                return ""
            return parts[0]

        elif default != None:
            self.putFontPar(    name,       default,    path            )
            return default
        
        else:
            raise PnlDbError, ParValueError %(  path,   name            )

#---------------------------------------------------------------------------
# "getColorPar()": Get a color Par value.
#---------------------------------------------------------------------------

    def getColorPar( self, name, path = None, default = None ):

        """
        Get a color par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            default     : The defult value.

        Return:

            The color par value if it exists else return default value.

        """

        parts   = self.dataFile.getArray(   name,       path,   COLOR   )
        
        if parts:
            returnVal   = parts[0]
            if type( returnVal ) != numarray.numarraycore.NumArray:
                returnVal = numarray.array(             returnVal       )

            return returnVal

        elif default != None:
            
            if type( default ) != numarray.numarraycore.NumArray:
                default = numarray.array(               default         )
                
            self.putColorPar(   name,       default,    path            )
            return default

        else:
            raise PnlDbError, ParValueError %(  path,   name            )
        
#---------------------------------------------------------------------------
# "getParType()": Get the type of the Par.
#---------------------------------------------------------------------------

    def getParType( self, name, path = None ):

        """
        Get the type of the Par.
        
        Argument:

            name        : The par name.
            path        : The par path.

        Return:

            The tarea par value if it exists else return default value.

        """

        return self.dataFile.getParTag(      name,      path            )

#---------------------------------------------------------------------------
# "getPar()": Get a Par value.
#---------------------------------------------------------------------------

    def getPar( self, name, path = None, parType = BOOL, default = None ):

        """
        Get a par value.
        
        Argument:

            name        : The par name.
            path        : The par path.
            parType     : The par type.
            default     : The defult value.

        Return:

            The tarea par value if it exists else return default value.

        """

        retVal      = None
        
        if parType == BOOL:
            retVal  = self.getBoolPar(      name,   path,   default     )
            
        elif parType == INT :
            retVal  = self.getIntPar(       name,   path,   default     )
            
        elif parType == REAL:
            retVal  = self.getRealPar(      name,   path,   default     )
            
        elif parType == STR :
            retVal  = self.getStrPar(       name,   path,   default     )
            
        elif parType == ENUM:
            retVal  = self.getEnumPar(      name,   path,   default     )
            
        elif parType == REF :
            retVal  = self.getRefPar(       name,   path,   default     )
            
        elif parType == TAB :
            retVal  = self.getTabPar(       name,   path,   default     )
            
        elif parType == TAREA:
            retVal  = self.getTareaPar(     name,   path,   default     )
            
        elif parType == LIST:
            retVal  = self.getListPar(      name,   path,   default     )
            
        elif parType == REFS:
            retVal  = self.getRefsPar(      name,   path,   default     )
            
        elif parType == ARY :
            retVal  = self.getArrayPar(     name,   path,   default     )
            
        elif parType == FDATA :
            retVal  = self.getFileDataPar(  name,   path,   default     )
            
        elif parType == FILE :
            retVal  = self.getFilePar(      name,   path,   default     )

        elif parType == DIR :
            retVal  = self.getDirPar(       name,   path,   default     )

        elif parType == PASSWD :
            retVal  = self.getPasswdPar(    name,   path,   default     )

        elif parType == FONT :
            retVal  = self.getFontPar(      name,   path,   default     )

        elif parType == COLOR :
            retVal  = self.getColorPar(     name,   path,   default     )

        return retVal
        
#---------------------------------------------------------------------------
# "getParVals()": Get a Par values.
#---------------------------------------------------------------------------

    def getParVals( self, name, path = None, parType = BOOL ):

        """
        Get a par values.
        
        Argument:

            name        : The par name.
            path        : The par path.
            parType     : The par type.

        Return:

            A dictionary contains a par values.

        """

        retVal      = None
        
        if parType == BOOL:
            retVal  = self.dataFile.getInt(     name,   path,   BOOL    )
            
        elif parType == INT :
            retVal  = self.dataFile.getInt(     name,   path,   INT     )
            
        elif parType == REAL:
            retVal  = self.dataFile.getReal(    name,   path,   REAL    )
            
        elif parType == STR :
            retVal  = self.dataFile.getStr(     name,   path,   STR     )
            
        elif parType == ENUM:
            retVal  = self.dataFile.getStr(     name,   path,   ENUM    )
            
        elif parType == REF :
            retVal  = self.dataFile.getStr(     name,   path,   REF     )
            
        elif parType == TAB :
            retVal  = self.dataFile.getStr(     name,   path,   TAB     )
            
        elif parType == TAREA:
            retVal  = self.dataFile.getStr(     name,   path,   TAREA   )
            
        elif parType == LIST:
            retVal  = self.dataFile.getStrs(    name,   path,   LIST    )
            
        elif parType == REFS:
            retVal  = self.dataFile.getStrs(    name,   path,   REFS    )
            
        elif parType == ARY :
            retVal  = self.dataFile.getArray(   name,   path,   ARY     )

        elif parType == FDATA :
            retVal  = self.dataFile.getFile(    name,   path,   FDATA   )

        elif parType == FILE:
            retVal  = self.dataFile.getStr(     name,   path,   FILE    )
            
        elif parType == DIR:
            retVal  = self.dataFile.getStr(     name,   path,   DIR     )
            
        elif parType == PASSWD:
            retVal  = self.dataFile.getStr(     name,   path,   PASSWD  )
            
        elif parType == FONT :
            retVal  = self.dataFile.getStr(     name,   path,   FONT    )

        elif parType == COLOR :
            retVal  = self.dataFile.getArray(   name,   path,   COLOR   )

        return retVal

#---------------------------------------------------------------------------
# "putParOpt()": Record an option.
#---------------------------------------------------------------------------

    def putParOpt( self, name, opt, value, path = None, clobber = True ):

        """
        Record an option.
        
        Argument:

            name        : The par name.
            opt         : The par option.
            value       : The value of par option.
            path        : The par path.
            clobber     : If True, overwite the value.

        Return:

            None

        """

        self.dataFile.putParOpt( name,  path, opt, value, clobber       )

#---------------------------------------------------------------------------
# "getUnit()": get the unit option.
#---------------------------------------------------------------------------

    def getUnit( self, path, name ):

        """
        Get the unit option.
        
        Argument:

            name        : The par name.
            path        : The par path.

        Return:

            The unit option.

        """
       
        real    = self.dataFile.getReal(    name,   path,   REAL        )
        
        if real != None:
            if  real[1].has_key( 'unit' ):
                return real[ 1 ][ 'unit' ]
            else:
                raise PnlDbError, "The %s path has not unit option." %path
        
        else:
            raise PnlDbError, "The %s path has not real value." %path

#---------------------------------------------------------------------------
# "getModId()": get the par mod id option.
#---------------------------------------------------------------------------

    def getModId( self, path, name ):

        """
        Get a par ModId option.
        
        Argument:

            name        : The par name.
            path        : The par path.

        Return:

            The mId option.

        """

        parType = self.getParType(          name,           path        )
        parVals = self.getParVals(          name,           path = path,
                                            parType = parType           )
        
        if parVals != None:
            if  parVals[1].has_key( 'mId' ):
                return parVals[ 1 ][ 'mId' ]
            else:
                return None #PnlDbError, "The %s path has not mId option." %path
        
        else:
            return None #PnlDbError, "The %s path has not mId value." %path

#---------------------------------------------------------------------------
# regParTrace: Registers a function for a par.
#---------------------------------------------------------------------------

    def regParTrace( self, path, par, func, args ):

        """
        Registers a function for a par.
        
        Argument:

            path        : The par path.
            par         : The par name.
            func        : The function.
            args        : The function arguments.

        Return:

            None

        """

        self.dataFile.tracePar(     par,    path,   func,   args        )

#---------------------------------------------------------------------------
# clearTracePars: Clear all the trace pars.
#---------------------------------------------------------------------------

    def clearTracePars( self ):

        """
        Clear all the trace pars.
        
        Argument:

            None
            
        Return:

            None

        """

        self.dataFile.initTrace(                                        )
        
#---------------------------------------------------------------------------
# "copyFile()": Copy the file
#---------------------------------------------------------------------------

    def copyFile( self, destFileName, overwrite = True ):

        """
        Flushes the data base and then uses the standard
        python routines to copy the file.
        
        Argument:

            destFileName: Name of the new file.
            overwrite   : Overwrite if true.

        Return:

            None

        """

        self.flush(                                                     )
        
        if os.path.exists( destFileName ):
            if overwrite:
                shutil.copyfile(    self.fileName,  destFileName        )

        else:
            shutil.copyfile(        self.fileName,  destFileName        )
        

#----------------------------------------------------------------------------
# "close file": close the file.
#---------------------------------------------------------------------------

    def closeFile( self ):

        """
        Close the file.
        
        Argument:

            None
            
        Return:

            None

        """

        #----- Misc. 1/08 J11
        if self.initDbMIdVal != self.dataFile.currMId() :
            timeValue       = time.time(  				)
            self.putRealPar('lastMod',      timeValue,      header      )
        
        self.dataFile.close(                                            )

#----------------------------------------------------------------------------
# "addMarker": 
#---------------------------------------------------------------------------

    def addMarker( self, tag, storeState = False ):

        """
        addMarker to the file.
        
        Argument:

            tag : the marker tag.
            
        Return:

            None

        """

        marker  = tag
        if storeState :
            marker  = ( tag, self.state1 )
        #----- Misc 4/08 : E3
        else:
            self.state1 = None
        #----- End of Misc 4/08 : E3
        self.dataFile.addMarker(            marker                      )

#----------------------------------------------------------------------------
# "undoMarker": 
#---------------------------------------------------------------------------

    def undoMarker( self ):

        """
        go back to the state of the last marker.
        
        Argument:

            None
            
        Return:

            tag : the marker tag.

        """

        #----- Misc 4/08 : E3
        self.state1 = None
        #----- End of Misc 4/08 : E3
        marker  = self.dataFile.undoMarker(                             )
        tag     = marker
        if type( marker ) == types.TupleType:
            tag         = marker[ 0 ]
            self.state1 = marker[ 1 ]
        return tag

#----------------------------------------------------------------------------
# "redoMarker": 
#---------------------------------------------------------------------------

    def redoMarker( self ):

        """
        go forward to the next marker.
   
        Argument:

            None
            
        Return:

            tag : the marker tag.

        """

        #----- Misc 4/08 : E3
        self.state1 = None
        #----- End of Misc 4/08 : E3
        marker  = self.dataFile.redoMarker(                             )
        tag     = marker
        if type( marker ) == types.TupleType:
            tag         = marker[ 0 ]
            self.state1 = marker[ 1 ]
        return tag

#----------------------------------------------------------------------------
# "getMarkers": 
#---------------------------------------------------------------------------

    def getMarkers( self ):

        """
        give marker tags and current location.
   
        Argument:

            None
            
        Return:

            markers: the marker tags in the file.

        """

        markers = self.dataFile.getMarkers(                             )
        return markers

#----------------------------------------------------------------------------
# "delMarker": 
#---------------------------------------------------------------------------

    def delMarker( self ):

        """
        Delete the last marker.
   
        Argument:

            None
            
        Return:

            None

        """

        path    = ROOT + RS + "main"
        par     = "del_marker"
        value   = time.time(                                            )
        self.dataFile.undoMarker(                                       )
        self.dataFile.putReal(  par,    value,  path,   REAL,   True    )

#----------------------------------------------------------------------------
# "setState1": 
#---------------------------------------------------------------------------

    def setState1( self, value ):

        """
        Set the state1 value.
   
        Argument:

            value: the value of the state1.
            
        Return:

            None

        """

        self.state1 = value

#----------------------------------------------------------------------------
# "getState1": 
#---------------------------------------------------------------------------

    def getState1( self ):

        """
        Return the state1 value.
   
        Argument:

            None 
            
        Return:

            value: the value of the state1.

        """

        return self.state1
        
#===========================================================================
#
# Test
#
#===========================================================================

if __name__ == '__main__':

    par1	= 'par1'
    node1	= ROOT + RS + 'test'
    a	= PnlDb( 'testDb.h', 'new' )
    val={'1':['1','2','3'],'4':3.45,'3':{'1':1,'2':2}}
    a.putDicPar( name = par1,value=val,path = node1)
    d= a.getDicPar( name = par1,path = node1)
    print d
##    a.getRealPar( 'rjunk2', ROOT+RS+'here', 1.3, unit='m' )
##    print a.lastMod(), "=>", time.ctime(a.lastMod())
##    print a.version()
##    print "mId: ", a.getModId(         ROOT+RS+'here', "rjunk2" )
##    a.flush()
##    print a.lastMod(), "=>", time.ctime(a.lastMod())
##    print a.getRealPar( 'rjunk2', ROOT+RS+'here' )
##    a.putIntPar( "nn", 10, node1 )
##    print "mId: ", a.getModId( node1, "nn" )
    a.closeFile()
