#---------------------------------------------------------------------------
# Errors
#---------------------------------------------------------------------------

repWinError = "Error from AcuReport repWin module"

#---------------------------------------------------------------------------
# Import needed modules
#---------------------------------------------------------------------------

import os
import repWin

#---------------------------------------------------------------------------
# Check for required software
#---------------------------------------------------------------------------

ACUSIM_ROOT = os.path.join( os.getenv( "ACUSIM_HOME", "" ),
                            os.getenv( "ACUSIM_MACHINE", "" ),
                            os.getenv( "ACUSIM_VERSION", "" ) )

REPORT_BIN = os.path.join( ACUSIM_ROOT, "base", "bin" )

isWin = ( os.name == 'nt' )

if isWin:
    files	= ( REPORT_BIN + "/miktex/texmf/miktex/bin/pdflatex.exe",
		    REPORT_BIN + "/tth/tth.exe",
		    REPORT_BIN + "/latex2rtf/latex2rtf.exe" )
else:
    files	= ( REPORT_BIN + "/pdflatex", 
    		    REPORT_BIN + "/tth/tth", 
		    REPORT_BIN + "/latex2rtf/latex2rtf" )

for file in files:
    if not os.path.exists( file ):          
	raise repWinError, "%s not found; AcuReport cannot start." % file
    
#---------------------------------------------------------------------------
# Set up the global configuration
#---------------------------------------------------------------------------

import  acuCnf

cnfTable = [
            "help:help:h:0:bool:-:print usage and exit",
            
            "fileName:file:file:_auto:str:-:" \
            + "file name of the report generation script;" + \
            "(_auto, use <problem>.rep)",
            
            "problem:problem:pb:_undefined:str:-:problem name",
            
            "working_directory:working_directory:dir:ACUSIM.DIR:str:-:" \
            + "working directory",
            
            "run_id:run_id:run:0:int:-:run number",
            
            "acuconsole_data_base:acuconsole_data_base:acs:_auto:str:-:" \
            + "AcuConsole data base name; (_auto, use <problem>.acs)",
            
            "pdf:create_pdf_file:pdf:0:bool:-:create pdf file",
            
            "rtf:create_rtf_file:rtf:0:bool:-:create rtf file",
            
            "html:create_html_file:html:0:bool:-:create html file",
            
            "usr1:user_option_1:usr1:none:str:-:" \
            + "user specific option 1, accessible in the report",
            
            "usr2:user_option_2:usr2:none:str:-:" \
            + "user specific option 2, accessible in the report",
            
            "verbose:verbose:v:2:int:-:verbose level"             
           ]
 
acuCnf.cnfNew(                              cnfTable                    )

#---------------------------------------------------------------------------
# Run the problem
#---------------------------------------------------------------------------

win     = repWin.RepWin(                                                 )
win.run(                                                                 )
