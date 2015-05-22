#---------------------------------------------------------------------------
# Get the modules
#---------------------------------------------------------------------------

import os
import sys
import string

import acuCnf
import acu2DPlot
import acuReport
import repAcs
import repAcsRep
import repScope
import acuVis
import acuDbAssist
import acuConvertU3D

#===========================================================================
#
# "Report Window Errors":
#
#===========================================================================

repWinError = "Error in repWin module"

#===========================================================================
#
# "RepWin": Class for setting acuReport configuration.
#
#===========================================================================

class RepWin:

    """Class for setting acuReport configuration."""

#---------------------------------------------------------------------------
# Initialize
#---------------------------------------------------------------------------

    def __init__( self ):

        """
	initialize repWin with command-line parameters.
	
	Argument:
            None

        Output:
            None	
        """

        self.repObj             = None
        self.acsDB              = None
        self.scopeDic           = dict()

        self.scopeDic["ROOT"]   = repAcs.ROOT
        self.scopeDic["RS"]     = repAcs.RS

        self.scope              = repScope.RepScope(self                 )

        self.working_directory  = acuCnf.cnfGetStr("working_directory"   )
        self.problem            = acuCnf.cnfGetStr( "problem"            )
        self.fileName           = acuCnf.cnfGetStr( "fileName"           )
        self.verbose            = acuCnf.cnfGetInt( "verbose"            )

        #-----------------------------------------------------------------
        # Set problem and fileName variable
        #-----------------------------------------------------------------

        if self.fileName == '_auto' and self.problem == '_undefined':
            raise repWinError, "Both problem and fileName have not been set"

        if self.fileName == '_auto':
            self.fileName       = self.problem + ".rep"

        if self.problem == '_undefined':
            if self.fileName[-4:]  == '.rep' :
                self.problem    = self.fileName[:-4]
            else:
                self.problem    = self.fileName

#-----------------------------------------------------------------------
# "getCnf()": Get a command-line argument
#-----------------------------------------------------------------------

    def getCnf(self, name):

        """
	Get a command-line argument
	
	Argument:
            name    - name of the variable

        Output:
            None	
        """

        return acuCnf.cnfGetStr( name )

#-----------------------------------------------------------------------
# "run()": Run the acuReport module
#-----------------------------------------------------------------------

    def run( self ):

        """
        Run the acuReport module

            Argument:
                None

            Output:
                 None
        """

        if sys.platform == 'win32':
            self.checkRegistery(                                        )
        self.scope.defScope(                                            )
        self.compileAndRun(                                             )
        self.createOutputFiles(                                         )
        self.deleteTempFiles(                                           )

#-----------------------------------------------------------------------
# "setReportFile()": Set report name and object
#-----------------------------------------------------------------------

    def setReportFile( self,    fileName,   packages,
                                docClass,   docClassOpt,
                                fullPage                ):

        """
        Set report name and object

            Argument:
                AcuReport arguments

            Output:
                 A report object
        """

        if fileName == None:
            fileName    = os.path.splitext( self.fileName   )[0] + ".tex"
        else:
            fileName    = os.path.splitext( fileName        )[0] + ".tex"

        

        self.repObj     = acuReport.AcuReport( fileName,    packages,
                                               docClass,    docClassOpt,
                                               fullPage,    self.verbose )
        return self.repObj

#-----------------------------------------------------------------------
# "setVis()": Set acuVis
#-----------------------------------------------------------------------

    def setVis( self,       problem,   dir,
                            run,        outDir ):

        """
        Set acuVis

            Argument:
                AcuVis arguments

            Output:
                 An acuVis object
        """

        if problem == None:
            problem     = self.problem

        if dir == None:
            dir         = self.working_directory

        if run == None:
            run         = acuCnf.cnfGetInt( "run_id"                    )

        if outDir == None:
            outDir     = self.repObj.basePath + "/Figures"

        vis  = acuVis.AcuVis( problem,      dir,
                              run ,         outDir                      )

        return vis

#-----------------------------------------------------------------------
# "curve()": Create a curve
#-----------------------------------------------------------------------

    def curve( self,    x,              y,
                        name,           lineType,
                        lineWidth,      symbol,
                        symbolSize,     color ):

        """
        Create a curve

            Argument:
                acu2DPlot.curve arguments

            Output:
                 A curve
        """

        crv             = acu2DPlot.curve( x,              y,
                                           name,           lineType,
                                           lineWidth,      symbol,
                                           symbolSize,     color         )
        return crv

#-----------------------------------------------------------------------
# "plot()": Plot the curves and return output file name
#-----------------------------------------------------------------------

    def plot( self,       curves,       title,
                          legend,       legendPos,
                          xLabel,       xLog,
                          xRange,       yLabel,
                          yLog,         yRange,
                          width,        height,
                          fileName,     fileType,
                          dirName,      fontSize,
                          fontScale,    resolution,
                          resScale,     tickSize,
                          tickScale                 ):

        """
        Plot the curves and return output file name

            Argument:
                acu2DPlot.plot arguments

            Output:
                 output image file name
        """

        if dirName == None:
            dirName     = self.repObj.basePath + "/Figures"

        output          = acu2DPlot.plot( curves,       title,
                                          legend,       legendPos,
                                          xLabel,       xLog,
                                          xRange,       yLabel,
                                          yLog,         yRange,
                                          width,        height,
                                          fileName,     fileType,
                                          dirName,      fontSize,
                                          fontScale,    resolution,
                                          resScale,     tickSize,
                                          tickScale                     )

        return output

#-----------------------------------------------------------------------
# "openDB()": Create an instance of RepAcs DB
#-----------------------------------------------------------------------

    def openDB( self,   fileName ):

        """
        Create an instance of RepAcs DB

            Argument:
                RepAcs arguments

            Output:
                 A RepAcs DB instance
        """

        if fileName == None:
            fileName        = acuCnf.cnfGetStr( "acuconsole_data_base"   )
            if fileName == '_auto':
                fileName    = self.problem + ".acs"

        self.acsDB          = repAcs.RepAcs( fileName                    )

        return self.acsDB

#-----------------------------------------------------------------------
# "setRepAcs()": Create an instance of RepAcs
#-----------------------------------------------------------------------

    def setRepAcs( self,    report,     acs ):

        """
        Create an instance of RepAcsRep

            Argument:
                RepAcsRep arguments

            Output:
                 A RepAcsRep instance
        """

        if report == None:
            report      = self.repObj
        if acs == None:
            acs         = self.acsDB

        rps             = repAcsRep.RepAcsRep(report, acs                )

        return rps

#-----------------------------------------------------------------------
# "createOutputFiles()": Check conversion options and convert accordingly
#-----------------------------------------------------------------------

    def createOutputFiles( self ):

        """
        Check conversion options and convert accordingly

            Argument:
                None

            Output:
                None
        """

        if acuCnf.cnfGetBool("pdf"):
            self.repObj.writePdf(                                        )

        if acuCnf.cnfGetBool("html"):
            self.repObj.writeHtml(                                       )

        if acuCnf.cnfGetBool("rtf"):
            self.repObj.writeRtf(                                        )

#-----------------------------------------------------------------------
# "setDbAssist()": Set Set acuDbAssist
#-----------------------------------------------------------------------

    def setDbAssist( self,      problemName,   dirName,
                                runId ):

        """
        Set acuDbAssist

            Argument:
                AcuDbAssist arguments

            Output:
                 An AcuDbAssist object
        """

        if problemName == None:
            problemName     = self.problem

        if dirName == None:
            dirName         = self.working_directory

        if runId == None:
            runId           = acuCnf.cnfGetInt( "run_id"                 )

        adb                 = acuDbAssist.AcuDbAssist(      problemName,
                                                            dirName,
                                                            runId        )

        return adb
			
#---------------------------------------------------------------------------
# "compileAndRun()": Compiles and runs the code in the .rep file
#---------------------------------------------------------------------------

    def compileAndRun( self ):

        """
        This function compiles and runs the code in the .rep file

            Argument:
                None

            Output:
                None
        """

        code = open(self.fileName, "rt").read().replace(    "\r", ''    )

        byteCode = compile( code, "<string>", 'exec'                    )

        eval(                   byteCode, self.scopeDic                 )

#-----------------------------------------------------------------------
# "deleteTempFiles()": Delete temporary files
#-----------------------------------------------------------------------

    def deleteTempFiles( self ):

        """
        Delete temporary files

            Argument:
                None

            Output:
                None
        """

        if self.verbose > 0: print "Deleting temporary files...",

        acuConvertU3D.removeAnimationControlImages(                     )
        acuConvertU3D.removeAnimationControlScripts(                    )
        
        extensions = [".toc", ".aux", ".out",
                      ".dvi", ".tlg", ".log", ".con"]
        
        tmpPath = os.path.splitext(self.repObj.fileName)[0]       

        for ext in extensions:   
            if os.path.exists(tmpPath + ext):
                os.remove(          tmpPath  + ext                      )
                
        if self.verbose > 0: print "done.\n"

#-----------------------------------------------------------------------
# "checkRegistery()": Check registry for right path of MiKTeX
#-----------------------------------------------------------------------

    def checkRegistery( self ):

        """
        Check registry for right path of MiKTeX

            Argument:
                None

            Output:
                None
        """

        import _winreg

        try:
            doFlg   = False
            root    = _winreg.HKEY_CURRENT_USER

            key_values      = [
              (r"Software\MiKTeX.org\MiKTeX\2.7\Core", "Install"),
              (r"Software\MiKTeX.org\MiKTeX\2.7\Core", "Roots"),
              (r"Software\MiKTeX.org\MiKTeX\2.7\Core", "UserConfig"),
              (r"Software\MiKTeX.org\MiKTeX\2.7\Core", "UserData"),     ]

            ACUSIM_ROOT = os.path.join( os.getenv("ACUSIM_HOME", ""),
                                        os.getenv("ACUSIM_MACHINE", ""),
                                        os.getenv("ACUSIM_VERSION", "") )

            for keypath, value_name in key_values:
              hKey          = _winreg.OpenKey( root, keypath, 0,
                                               _winreg.KEY_READ         )
              value, type   = _winreg.QueryValueEx( hKey,   value_name  )

              if value.find(    ACUSIM_ROOT     ) == -1:
                  doFlg = True
                  break

            if doFlg:
		cmd = os.path.join( ACUSIM_ROOT, 'base\\bin\\miktex\\reset.bat')
		#print "Executing: " + cmd
		os.system( cmd )
        except:
            pass
