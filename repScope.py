#===========================================================================
#
# "RepScope": Class for defining scope for acuReport.
#
#===========================================================================

class RepScope:

    """Class for defining scope for acuReport."""

#---------------------------------------------------------------------------
# Initialize
#---------------------------------------------------------------------------

    def __init__( self, repWin ):

        """
	initialize repScope with repWin instance.
	
	Argument:
            repWin - the repWin instance

        Output:
            None	
        """

        self.repWin = repWin

#---------------------------------------------------------------------------
# "defScope()": Define global variables in the scope.
#---------------------------------------------------------------------------

    def defScope( self ):

        """
        Define scopes.

            Argument:
                None

            Output:
                None
        """

        self.repWin.scopeDic["GetCnf"] = lambda name: \
                                        self.repWin.getCnf( name         )

        self.repWin.scopeDic["Report"]  = lambda  fileName = None , \
                                         packages   = (), \
                                         docClass   = 'article', \
                                         docClassOpt= 'letterpaper,12pt', \
                                         fullPage   = True: \
                                         self.repWin.setReportFile(
                                                             fileName,
                                                             packages,
                                                             docClass,
                                                             docClassOpt,
                                                             fullPage )

        self.repWin.scopeDic["Curve"]   = lambda  x, \
                                         y, \
                                         name        = None, \
                                         lineType    = "solid", \
                                         lineWidth   = 1, \
                                         symbol      = None, \
                                         symbolSize  = 1, \
                                         color       = "blue": \
                                         self.repWin.curve( x,
                                                            y,
                                                            name,
                                                            lineType,
                                                            lineWidth,
                                                            symbol,
                                                            symbolSize,
                                                            color        )

        self.repWin.scopeDic["Plot2D"]  = lambda curves, \
                                         title      = "", \
                                         legend     = True, \
                                         legendPos  = "auto", \
                                         xLabel     = "X", \
                                         xLog       = False, \
                                         xRange     = "auto", \
                                         yLabel     = "Y", \
                                         yLog       = False, \
                                         yRange     = "auto", \
                                         width      = 600, \
                                         height     = 400, \
                                         fileName   = None, \
                                         fileType   = "png", \
                                         dirName    = None, \
                                         fontSize   = 14, \
                                         fontScale  = 1.0, \
                                         resolution = 80, \
                                         resScale   = 1.0, \
                                         tickSize   = 12, \
                                         tickScale  = 1.0: \
                                         self.repWin.plot( curves,
                                                           title,
                                                           legend,
                                                           legendPos,
                                                           xLabel,
                                                           xLog,
                                                           xRange,
                                                           yLabel,
                                                           yLog,
                                                           yRange,
                                                           width,
                                                           height,
                                                           fileName,
                                                           fileType,
                                                           dirName,
                                                           fontSize,
                                                           fontScale,
                                                           resolution,
                                                           resScale,
                                                           tickSize,
                                                           tickScale )

        self.repWin.scopeDic["Acs"]     = lambda fileName = None: \
                                         self.repWin.openDB( fileName    )

        self.repWin.scopeDic["ReportAcs"] = lambda report = None, \
                                           acs     = None: \
                                           self.repWin.setRepAcs( report,
                                                                    acs  )

        self.repWin.scopeDic["Adb"]     = lambda problemName = None, \
                                         dirName = None, \
					 runId	 = None: \
					 self.repWin.setDbAssist( problemName,
                                                                  dirName,
                                                                  runId  )

        self.repWin.scopeDic["AcuVis"]  = lambda problem = None, \
                                         dir    = None, \
                                         run    = 0, \
                                         outDir = None: \
                                         self.repWin.setVis( problem,
                                                             dir,
                                                             run,
                                                             outDir      )
