#---------------------------------------------------------------------------
# get the modules
#---------------------------------------------------------------------------

import os
import pnlDb

#===========================================================================
#
# "Constants":
#
#===========================================================================
ROOT    = pnlDb.ROOT
RS      = pnlDb.RS

#===========================================================================
#
# "Acs Errors":
#
#===========================================================================

RepAcsError = "Error in repAcs module"

#===========================================================================
#
# "RepAcs":  Faciliate access to AcuConsole database file
#
#===========================================================================

class RepAcs:

    """Faciliate access to AcuConsole database file."""

#---------------------------------------------------------------------------
# Initialize
#---------------------------------------------------------------------------

    def __init__( self, fileName ):

        """
	Load an Acs database file

        Argument:		
            fileName    - Acs database file name
			
        """

        if not os.path.exists( fileName ):
            raise RepAcsError, repr(fileName) + " file does not exist."

        self.fileName   = fileName
        self.db         = pnlDb.PnlDb(              fileName, 'old'      )


#---------------------------------------------------------------------------
# "getBool()": get a bool Par value.
#---------------------------------------------------------------------------

    def getBool( self, par, path ):

        """
        get a bool Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The bool par value.

        """

        return self.db.getBoolPar(                   par, path           )

#---------------------------------------------------------------------------
# "getInt()": get an integer Par value.
#---------------------------------------------------------------------------

    def getInt( self, par, path ):

        """
        get an integer Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The integer par value.

        """

        return self.db.getIntPar(                   par, path            )

#---------------------------------------------------------------------------
# "getReal()": get a real Par value.
#---------------------------------------------------------------------------

    def getReal( self, par, path, unit = None ):

        """
        get a real Par value.

        Argument:

            par     - The par name.
            path    - The par path.
            unit    - The par unit.

        Return:

            The real par value.

        """

        return self.db.getRealPar(           par, path, unit = unit      )

#---------------------------------------------------------------------------
# "getStr()": get a string Par value.
#---------------------------------------------------------------------------

    def getStr( self, par, path ):

        """
        get a string Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The string par value.

        """

        return self.db.getStrPar(                   par, path            )

#---------------------------------------------------------------------------
# "getEnum()": get an enum Par value.
#---------------------------------------------------------------------------

    def getEnum( self, par, path ):

        """
        get an enum Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The enum par value.

        """

        return self.db.getEnumPar(                   par, path           )

#---------------------------------------------------------------------------
# "getArray()": get an array Par value.
#---------------------------------------------------------------------------

    def getArray( self, par, path, unit = None ):

        """
        get an array Par value.

        Argument:

            par     - The par name.
            path    - The par path.
            unit    - The par unit.

        Return:

            The array par value.

        """

        return self.db.getArrayPar(         par, path, unit = unit      )

#---------------------------------------------------------------------------
# "getColor()": get a color Par value.
#---------------------------------------------------------------------------

    def getColor( self, par, path ):

        """
        get a color Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The color par value.

        """

        return self.db.getColorPar(                   par, path          )

#---------------------------------------------------------------------------
# "getDic()": get a dictionary Par value.
#---------------------------------------------------------------------------

    def getDic( self, par, path ):

        """
        get a dictionary Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The dictionary par value.

        """

        return self.db.getDicPar(                   par, path            )

#---------------------------------------------------------------------------
# "getDir()": get a directory Par value.
#---------------------------------------------------------------------------

    def getDir( self, par, path ):

        """
        get a directory Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The directory par value.

        """

        return self.db.getDirPar(                   par, path            )

#---------------------------------------------------------------------------
# "getFileData()":  get a file data Par value.
#---------------------------------------------------------------------------

    def getFileData( self, par, path ):

        """
        The content of the par is put in the file, and the name
        of the file is returned.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The file data par value.

        """

        return self.db.getFileDataPar(                   par, path       )

#---------------------------------------------------------------------------
# "getFile()": get a file Par value.
#---------------------------------------------------------------------------

    def getFile( self, par, path ):

        """
        get a file Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The file par value.

        """

        return self.db.getFilePar(                   par, path           )

#---------------------------------------------------------------------------
# "getFont()": get a font Par value.
#---------------------------------------------------------------------------

    def getFont( self, par, path ):

        """
        get a font Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The font par value.

        """

        return self.db.getFontPar(                   par, path           )

#---------------------------------------------------------------------------
# "getList()": get a list Par value.
#---------------------------------------------------------------------------

    def getList( self, par, path ):

        """
        get a list Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The list par value.

        """

        return self.db.getListPar(                   par, path           )

#---------------------------------------------------------------------------
# "getPasswd()": get a password Par value.
#---------------------------------------------------------------------------

    def getPasswd( self, par, path ):

        """
        get a password Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The password par value.

        """

        return self.db.getPasswdPar(                   par, path         )

#---------------------------------------------------------------------------
# "getRef()": get a ref Par value.
#---------------------------------------------------------------------------

    def getRef( self, par, path ):

        """
        get a ref Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The ref par value.

        """

        return self.db.getRefPar(                   par, path            )

#---------------------------------------------------------------------------
# "getRefs()": get a reference Par value.
#---------------------------------------------------------------------------

    def getRefs( self, par, path ):

        """
        get a reference Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The reference par value.

        """

        return self.db.getRefsPar(                   par, path           )

#---------------------------------------------------------------------------
# "getTab()": get a tab Par value.
#---------------------------------------------------------------------------

    def getTab( self, par, path ):

        """
        get a tab Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The tab par value.

        """

        return self.db.getTabPar(                   par, path            )

#---------------------------------------------------------------------------
# "getTarea()": get a tarea (Text Area) Par value.
#---------------------------------------------------------------------------

    def getTarea( self, par, path ):

        """
        get a tarea Par value.

        Argument:

            par     - The par name.
            path    - The par path.

        Return:

            The tarea par value.

        """

        return self.db.getTareaPar(                   par, path          )

#---------------------------------------------------------------------------
# "getType()": get the type of the Par.
#---------------------------------------------------------------------------

    def getType( self, par, path ):

        """
        get the type of the Par.

        Argument:

            name        - The par name.
            path        - The par path.

        Return:

            The type of the Par.

        """

        return self.db.getParType(               par, path               )

#---------------------------------------------------------------------------
# "getPar()": get a Par value.
#---------------------------------------------------------------------------

    def getPar( self, name, path, parType = pnlDb.BOOL ):

        """
        get a par value.

        Argument:

            name        - The par name.
            path        - The par path.
            parType     - The par type.

        Return:

            The par value.

        """

        return self.db.getPar(              name, path, parType          )

#---------------------------------------------------------------------------
# "getVals()": get a Par values.
#---------------------------------------------------------------------------

    def getVals( self, par, path, parType = pnlDb.BOOL ):

        """
        get a par values.

        Argument:

            name        - The par name.
            path        - The par path.
            parType     - The par type.

        Return:

            A dictionary contains a par values.

        """

        return self.db.getParVals(           par, path, parType          )

#----------------------------------------------------------------------------
# "getChildNodes()": get a list of child nodes.
#----------------------------------------------------------------------------

    def getChildNodes( self, path ):

        """
        get a list of child nodes.

        Argument:

            path        - The node path.

        Return:

            The list of child nodes.

        """

        return self.db.childNodes(                  path                 )

#----------------------------------------------------------------------------
# "getChildPars()": get a list of child pars.
#----------------------------------------------------------------------------

    def getChildPars( self, path ):

        """
        get a list of child pars.

        Argument:

            path        - The node path.

        Return:

            The list of child pars.

        """

        return self.db.childPars(                  path                  )

#===========================================================================
# Test the code
#===========================================================================

if __name__ == '__main__':
    rps = RepAcs(           "invalid.acs"                                )
