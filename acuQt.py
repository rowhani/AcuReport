#---------------------------------------------------------------------------
# Get the modules
#---------------------------------------------------------------------------

import  os
import  qt
import  types
import	acuCnf
import  re
import  sys
import  pstats 
import  profile
import  datetime
import  traceback

from	string	import  atof,atoi
from    acuUtil import  str


FALSE   	= 0
False   	= 0
false	        = 0
TRUE    	= 1
True    	= 1
true	        = 1

#===========================================================================
#
# Errors
#
#===========================================================================

acuQtError      = "ERROR from acuQt module"

#---------------------------------------------------------------------------
# Global variables
#---------------------------------------------------------------------------

_assistant      = None
_helpBaseURL    = None
_settings       = None
_settingsPath   = None
_messWidget     = None
_app            = None
_langAppName    = None
_lang           = None
_appName        = None
_translator     = None
_langCode       = {    'english':          'en' ,
                       'farsi':            'fa' ,
                       'japanese':         'jp' ,     }

_semiModalObj   = None

#---------------------------------------------------------------------------
# Initialize the assitant
#---------------------------------------------------------------------------

def initAssistant( appName , basePage = None , adpFile = None ):
    """
    Initialize assistant and help base URL.
    Arguments:
    appName     : application name
    basePage    : base help page of application
    adpFile     : profile of application help (.adp)
    """

    #-----------------------------------------------------------------------
    # Get the directory addresses
    #-----------------------------------------------------------------------

    currDir = os.getcwd(						)

    _hdir = acuCnf.cnfGet(	            "hdir"			)
    if _hdir == '_undefined':
        _hdir = os.path.join(               currDir , "doc"             )

    _adir = acuCnf.cnfGet(	            "adir"			)
    if _adir == '_undefined':
        _adir = os.path.join(               currDir , "bin"             )

    #-----------------------------------------------------------------------
    # Set the helpBaseURL
    #-----------------------------------------------------------------------

    if basePage == None :
        basePage = str( appName ) + '.htm'

    global _helpBaseURL
    _helpBaseURL = os.path.join(            _hdir , basePage            )

    #-----------------------------------------------------------------------
    # Set up the assistant
    #-----------------------------------------------------------------------

    if adpFile == None :
        adpFile = str( appName ) + '.adp'

    profilePath = os.path.join(             _hdir , adpFile             )
    cmdList = qt.QStringList( 					        )
    cmdList.append(	                    "-profile"		        )
    cmdList.append(                 qt.QString( profilePath )           )

    global _assistant
    _assistant = qt.QAssistantClient(           _adir		        )
    _assistant.setArguments(		        cmdList		        )

    return _assistant

#---------------------------------------------------------------------------
# Get helpBaseURL
#---------------------------------------------------------------------------

def getBaseURL( ):
    """
    Get the help Base URL of application.
    """

    global _helpBaseURL
    return _helpBaseURL

#---------------------------------------------------------------------------
# Get assistant
#---------------------------------------------------------------------------

def getAssistant( ):
    """
    Get the assistant handle.
    """

    global _assistant

    return _assistant

#---------------------------------------------------------------------------
# Initialize settings
#---------------------------------------------------------------------------

def initSettings( name ):
    """
    Initialize settings.
    Arguments:
    name        : Settings name ( to set path of settings in the registry )
    """

    global _settings , _settingsPath

    _settings = qt.QSettings(				                )
    _settingsPath = '/ACUSIM/' + str( name ) + '/'

#---------------------------------------------------------------------------
# Reset settings
#---------------------------------------------------------------------------

def resetSettings():
    """
    Reset the settings.
    """

    global _settings , _settingsPath

    _settings = qt.QSettings(				                )

#---------------------------------------------------------------------------
# set setting
#---------------------------------------------------------------------------

def setSetting( name , value ):
    """
    Store a single atrribute using QSetting.
    Arguments:
    name        : Setting name.
    value       : Setting value.
    """

    global _settings , _settingsPath

    if _settingsPath == None :
        raise acuQtError, ": Store path of settings is not valid !"

    name    = _settingsPath +  name

    if type( value ) == types.IntType :
        value	= "%d" % value
    elif type( value ) == types.FloatType :
        value	= "%.17g " % value
    elif type( value ) == types.BooleanType :
        if value :
            value   = "%d" % 1
        else:
            value   = "%d" % 0
    else :
        value = str(                value                               )

    _settings.writeEntry(	    name , value	                )

#---------------------------------------------------------------------------
# get setting integer
#---------------------------------------------------------------------------

def getSettingInt( name , default = 0 ):
    """
    Load an integer attribute.
    Arguments:
    name        : Setting name.
    default     : Setting default value.
    """

    global _settings , _settingsPath

    if _settingsPath == None :
        raise acuQtError, ": Load path of settings is not valid !"

    name    = _settingsPath +  name
    value   = _settings.readEntry(	        name	                )

    if value[1]:
        value	= atoi(                         str( value[0] )         )
    else:
        value	= default

    return(                                     value                   )

#---------------------------------------------------------------------------
# get setting real
#---------------------------------------------------------------------------

def getSettingReal( name , default = 0.0 ):
    """
    Load a real attribute.
    Arguments:
    name        : Setting name.
    default     : Setting default value.
    """

    global _settings , _settingsPath

    if _settingsPath == None :
        raise acuQtError, ": Load path of settings is not valid !"

    name    = _settingsPath +  name
    value   = _settings.readEntry(	        name	                )

    if value[1]:
        value	= atof(                         str( value[0] )         )
    else:
        value	= default

    return(                                     value                   )
	
#---------------------------------------------------------------------------
# get setting string
#---------------------------------------------------------------------------

def getSettingStr( name , default = "" ):
    """
    Load a string attribute.
    Arguments:
    name        : Setting name.
    default     : Setting default value.
    """

    global _settings , _settingsPath

    if _settingsPath == None :
        raise acuQtError, ": Load path of settings is not valid !"

    name    = _settingsPath +  name
    value	= _settings.readEntry(	    name                	)

    if value[1]:
        value	= str(                      value[0]                    )
    else:
        value	= default

    return(                                 value                       )

#---------------------------------------------------------------------------
# Clear all settings
#---------------------------------------------------------------------------

def clearAllSettings( name = '' ):
    """
    Clear all the application settings stored before.
    Argument:
    name    : The name of control which the settings are stored for.
    """

    global _settings , _settingsPath

    if _settingsPath == None :
        raise acuQtError, ": Path of settings is not valid !"

    name = _settingsPath + name

    _clearSettings_(                        name                        )

    if name == _settingsPath :
        _settings   = qt.QSettings(				        )

#---------------------------------------------------------------------------
# Clear settings
#---------------------------------------------------------------------------

def _clearSettings_( name ):
    """
    Clear the settings stored before.
    Argument:
    name    : The name of control which the settings are stored for.
    """

    global _settings

    keyList = _settings.subkeyList(	    name			)
    for i in range( len( keyList ) ) :
        key = name + str( keyList[i] ) + '/'
        _clearSettings_(		    key	                        )
        _settings.removeEntry(		    key	                        )

    entryList	= _settings.entryList(	    name			)
    for k in range( len( entryList ) ) :
        entry = name + str( entryList[k] )
        _settings.removeEntry(		    entry	                )

#---------------------------------------------------------------------------
# initMess
#---------------------------------------------------------------------------

def initApp( app, appName = None ):
    """
        Initialize the main application.

    """
    global _app,_appName

    _app    = app
    
    if appName:
        _appName    = appName

#---------------------------------------------------------------------------
# getApp
#---------------------------------------------------------------------------

def getApp( ):
    """
        Get the main application .

    """

    global _app

    return _app

#---------------------------------------------------------------------------
# initMess
#---------------------------------------------------------------------------

def initMess( messWidget ):
    """
        Initialize the status bar.

    """

    global _messWidget

    _messWidget =   messWidget
    _messWidget.setSizeGripEnabled(         TRUE			)
    
#---------------------------------------------------------------------------
# mess
#---------------------------------------------------------------------------

def mess( str, delay = 2000, update = False ):
    """
        Set the message of the status bar.

    """

    global _messWidget, _app

    if _messWidget:
	_messWidget.message(		    str,	delay		)
        if update and _app:
	    _messWidget.repaint(					)
	    _app.processEvents(					        )

#---------------------------------------------------------------------------
# setTranslator
#---------------------------------------------------------------------------

def setTranslatorLang( lang = None ):

    """
        Set the translator of the program.

    """


    global _langAppName,_lang,_langCode,_translator,_app

    _translator =    qt.QTranslator(None)

    currDir = os.getcwd(						)

    if not _app:
        print 'Application is not set'
    
    if _appName and lang:
        _lang           = lang
        _langAppName    = _appName + "_" + _langCode[_lang] + ".qm"

    _ldir = acuCnf.cnfGet(	            "ldir"			)
    if _ldir == '_undefined':
        _ldir   = os.path.join(               currDir                   )
        
    filePath   = os.path.join(               _ldir,     _langAppName    )
    
    if not os.path.exists(  filePath  ):
        print 'The .qm file dose not exist in the specified directory'

    _translator.load(                _langAppName,_ldir                 )
    

    _app.installTranslator(                    _translator              )
    
#---------------------------------------------------------------------------
# profile
#---------------------------------------------------------------------------

def getProfile( func, *args ):

    """
        Create a profile.

        Arguments:
            func    - name of the function

        OutPut:
            None

        Example 1:  changing the call PnlLoadGeom() in
                    pnlWin.py to get profile

                    please change the code to:

                        acuQt.getProfile( PnlLoadGeom, self, fn )
                        #PnlLoadGeom(  self,  fn             )

        Example 2:  calling item.newModelItem() in
                    Panels/Utility.cmdNewModel()

                    Please change the code to:
                    
                        import acuQt
                        acuQt.getProfile( item.newModelItem )
                        #item.newModelItem()

        Example 3:  calling AcuPackMesh() in pnlWin.py

                    Please change the code to:
                    
                        import acuQt
                        arm = acuPackMesh.AcuPackMesh( self )
			r = acuQt.getProfile( arm.exec_loop )
			#r = arm.exec_loop()
    """
    
    now             = datetime.datetime.now()
    curDate         = now.strftime('%m%d%y')

    prefix          = 'prof'

    indx	    = 0
    files	    = os.listdir(		'.'			)
    reg		    = re.compile(  prefix+'_(\d+)_(\d+)_time.txt'	)
    for file in files:
	parts	    = reg.match(	   	 file			)
	if parts:
            indx    = max(	indx,	int( parts.group( 2 ))		)

    fileHead	    = prefix + '_' + curDate + '_' + str( indx+1 )

    fileTime	    = fileHead + '_time.txt'
    fileMom	    = fileHead + '_mom.txt'
    fileKid	    = fileHead + '_kid.txt'
    prof            = profile.Profile()
    retVal	    = prof.runcall( func, *args )
    
    stat            = pstats.Stats( prof )
    stat.strip_dirs()
    stat.sort_stats('time','name')
    
    stdout 	    = sys.stdout
    sys.stdout 	    = open( fileTime, 'w' )
    stat.print_stats()
    
    sys.stdout	    = stdout
    stdout 	    = sys.stdout
    sys.stdout 	    = open( fileMom, 'w' )
    stat.print_callers()
    
    sys.stdout	    = stdout
    stdout 	    = sys.stdout
    sys.stdout 	    = open( fileKid, 'w' )
    stat.print_callees()
    
    sys.stdout	    = stdout
    print "Created profile files %s %s %s" % (fileTime,fileMom,fileKid)
    print "In directory %s" % os.getcwd()

    return( retVal )

#---------------------------------------------------------------------------
# setTr
#---------------------------------------------------------------------------

def setTr( trDef ):

    """
        
    """

    global  _tr

    _tr     = trDef

#---------------------------------------------------------------------------
# getTr
#---------------------------------------------------------------------------

def getTr( ):

    """
        
    """

    global  _tr

    return  _tr

#---------------------------------------------------------------------------
# initSemiModalObj
#---------------------------------------------------------------------------

def initSemiModalObj( semiModalObj ):
    """
        Initialize the semi modal object.

    """
    
    global _semiModalObj

    _semiModalObj   = semiModalObj

#---------------------------------------------------------------------------
# setSemiModal
#---------------------------------------------------------------------------

def setSemiModal( modal ):
    """
        Set semiModal; disable all the window parts except IV.
    """

    global _semiModalObj

    if _semiModalObj:
        _semiModalObj.semiModal(	        modal	                )

#---------------------------------------------------------------------------
# Override the handling of uncaught exceptions.
#---------------------------------------------------------------------------

def uncaughtExce( type, value, tb ):
    """ Override the handling of uncaught exceptions.
        Set the cursor to the original value and reset the semi modal.

        Argumrnts:
            type    - exception type
            value   - exception value
            tb      - exception information (traceback)
    """

    getApp().restoreOverrideCursor(                                     )
    setSemiModal(                       True                            )

    #----- Print exception information
    
    traceback.print_exception(          type,   value,  tb              )
    sys.exc_clear(                                                      )
    
#---------------------------------------------------------------------------
# A class used for setting the cursor.
#---------------------------------------------------------------------------

class AcuBusyCursor:
    """ This class is used for setting the cursor
        busy and reset it again.
    """
    
    def __init__( self ):
        pass
        #getApp().setOverrideCursor(  qt.QCursor( qt.Qt.WaitCursor )     )

    def __del__( self ):
        pass
        #getApp().restoreOverrideCursor(                                 )

#---------------------------------------------------------------------------
# A class used for setting semi modal.
#---------------------------------------------------------------------------

class AcuSemiModal:
    """ This class is used for setting the semi modal
        and reset it again.
    """

    def __init__( self ):
        setSemiModal(                   False                           )

    def __del__( self ):
        setSemiModal(                   True                            )
        
#---------------------------------------------------------------------------
# Converts the color from RGB to HSV.
#---------------------------------------------------------------------------

def cnvRgb2Hsv( r, g, b ):
    """ Converts the color from RGB (Red/Green/Blue) to
        HSV (Hue/Saturation/Value). 

        Argumrnts:
            r   - The red value
            g   - The green value
            b   - The blue value

        return:
            The color value in HSV value
    """

    clr = qt.QColor(                                                    )
    clr.setRgb(                             r,  g,  b                   )
    return clr.getHsv()
    
#---------------------------------------------------------------------------
# Converts the color from HSV to RGB.
#---------------------------------------------------------------------------

def cnvHsv2Rgb( h, s, v ):
    """ Converts the color from HSV (Hue/Saturation/Value) to
        RGB (Red/Green/Blue).HSV (Hue/Saturation/Value). 

        Argumrnts:
            h   - The Hue value
            s   - The Saturation value
            v   - The Value value

        return:
            The color value in HSV value
    """

    clr = qt.QColor(                                                    )
    clr.setHsv(                             h,  s,  v                   )
    return clr.getRgb()

#---------------------------------------------------------------------------
# Set opposite color
#---------------------------------------------------------------------------

def setOpsClr( r, g, b ):
    """ Set the opposite (negative) color.

        Argumrnts:
            r   - The red value
            g   - The green value
            b   - The blue value

        return:
            The negative color
    """

    h, s, v = cnvRgb2Hsv(                   r, g, b                     )
    h       = ( 180 + h ) % 360
    v       = ( 128 + v ) % 255
    return cnvHsv2Rgb(                      h, s, v                     )
    
