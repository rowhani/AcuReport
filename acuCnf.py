import os
import sys
import string
import re
import os.path

#===========================================================================
#
# Errors
#
#===========================================================================

CnfError	= "ERROR from cnf module"

#===========================================================================
#
# "cnfData":  CNF data
#
#===========================================================================

_cnfData = {}
_cnfKeys = {}
_cnfList = {}
_cnfBool = {}
_prog    = ""
_version = "1.8"
_relDate = '8/6/2009'

#===========================================================================
#
# "cnfSetVersion":  Set the version
#
#	cnfSetVersion( version ) ;
#
#===========================================================================

def cnfSetVersion( version ):
    """Set the version.

    Argument:

    version : The version.

    """
    global _cnfData, _cnfKeys, _cnfList, _cnfBool, _prog, _version

    _version = version

#===========================================================================
#
# "cnfGetVersion":  Get the version
#
#	cnfGetVersion( ) ;
#
#===========================================================================

def cnfGetVersion( ):
    """Get the version."""

    global _cnfData, _cnfKeys, _cnfList, _cnfBool, _prog, _version

    return _version

#===========================================================================
#
# "cnfSetReleaseDate":  Set the release date
#
#	cnfSetReleaseDate( date ) ;
#
#===========================================================================

def cnfSetReleaseDate( date ):
    """Set the release date."""

    global _relDate

    _relDate    = date

#===========================================================================
#
# "cnfGetReleaseDate":  Get the release date
#
#	cnfGetReleaseDate( ) ;
#
#===========================================================================

def cnfGetReleaseDate( ):
    """Get the release date."""

    global _relDate

    return _relDate

#===========================================================================
#
# "cnfNew":  Initialize CNF.
#
#	cnfNew( @cnfTable ) ;
#
#===========================================================================

def cnfNew( cnfTable ):

    global _cnfData, _cnfKeys, _cnfList, _cnfBool, _prog, _version

    cnfTypes = { "int":0, "real":0, "str":0, "bool":0, "enum":0 }

#---------------------------------------------------------------------------
# Get the program and machine name
#---------------------------------------------------------------------------

    _prog = sys.argv[0]  # The name of program
    if os.environ.has_key("ACUSIM_PROG_NAME"):
	_prog = os.environ["ACUSIM_PROG_NAME"]

    reg   = re.compile( r"\A.*/([^/]+)\Z" )
    parts = reg.match(_prog)
    if parts: _prog	= parts.group(1)

    reg   = re.compile( r"\A.*\\([^\\]+)\Z" )
    parts = reg.match(_prog)
    if parts: _prog	= parts.group(1)

    reg   = re.compile( r"\A(.+)\..*\Z" )
    parts = reg.match(_prog)
    if parts: _prog	= parts.group(1)

    if os.environ.has_key("ACUSIM_MACHINE"):
	machine = os.environ["ACUSIM_MACHINE"]
    else:
	raise CnfError, 'ACUSIM_MACHINE not defined; find and source .acusim'

#---------------------------------------------------------------------------
# Set the defaults
#---------------------------------------------------------------------------

    k = 0
    i = 0
    n = len(cnfTable)
    while i < n:
	line = cnfTable[i]
	while re.search( ':\+\Z', line ):
	    i = i + 1
	    line = line[:-1] + cnfTable[i]
	i = i + 1

	(key,name,abbr,value,type,enum,text) = \
	    tuple(string.splitfields(line,':'))

	if _cnfData.has_key(key):
	    raise CnfError, "Configuration key <%s> already defined" % key

	_cnfKeys[name] = key
	_cnfKeys[abbr] = key

	if type == "bool":
	    _cnfBool[name]       = "1"
	    _cnfBool[abbr]       = "1"
	    _cnfBool["no_"+name] = "0"
	    _cnfBool["no_"+abbr] = "0"
	    _cnfKeys["no_"+name] = key
	    _cnfKeys["no_"+abbr] = key

	_cnfData[key]   = (value, type, name, abbr, enum, text, "default" )
	_cnfList[k]     = key
	cnfSet( name, value, "default", 0, 1 )

	k = k + 1

#---------------------------------------------------------------------------
# Process the command line arguments
#---------------------------------------------------------------------------

    n = len(sys.argv)
    i = 1
    while i < n:
	name = sys.argv[i]
	if name[0] != '-':
	    raise CnfError, "Invalid command-line option <%s>" % name
	name = name[1:]
	if not _cnfKeys.has_key(name):
	    raise CnfError, "Invalid command-line option <-%s>" % name
	if _cnfBool.has_key(name):
	    cnfSet( name, _cnfBool[name], "command-line", 0, 1 )
	else:
	    i = i + 1
	    if i >= n:
		raise CnfError, \
		    "Value missing for command-line option <-%s>" % name
	    value = sys.argv[i]
	    cnfSet( name, value, "command-line", 0, 1 )
	i = i + 1

#---------------------------------------------------------------------------
# Set up the directory
#---------------------------------------------------------------------------

    if cnfQuery("pDir"):
	pDir = cnfGet("pDir")
	if pDir != ".":
	   os.chdir( pDir )
	else:
	    (value, type, name, abbr, enum, text, place) = _cnfData["pDir"]
	    value = os.getcwd()
	    _cnfData["pDir"] = (value, type, name, abbr, enum, text, place)

#---------------------------------------------------------------------------
# Process the configuration files
#---------------------------------------------------------------------------

    if os.environ.has_key("ACUSIM_CNF_FILES"):
	files = os.environ["ACUSIM_CNF_FILES"]
    else:
        file1 = os.path.join( ".", "Acusim.cnf" )
        file2 = os.path.join( os.environ["HOME"], "Acusim.cnf" )
	files = file1 + ":" + file2

    pat = '((' + machine + '|' + _prog + ')\.)?'
    pat = '\A\s*' + pat + pat + '(\w+)(\s*[=:]\s*|\s+)(.*\S)\s*\Z'
    reg = re.compile( pat )
    names = string.splitfields( files, ':' )
    i   = len(names)
    while i > 0:
	i	= i - 1
	file	= names[i]
	if i > 0 and len(names[i-1]) == 1:
	    i	= i -1
	    file= names[i] + ":" + file
	try:
	    if file[0] == '~':
		file = os.environ["HOME"] + file[1:]
	except: continue
	try: iop = open( file, 'r' )
	except: continue
	while 1:
	    line  = iop.readline()
	    if not line: break
	    line  = line[:-1]
	    parts = reg.match(line)
	    if parts:
		cnfSet( parts.group(5), parts.group(7), file, 0, 0 )
	iop.close()

#---------------------------------------------------------------------------
# Set up the directory
#---------------------------------------------------------------------------

    if cnfQuery("pDir"):
	pDir = cnfGet("pDir")
	if pDir != ".":
	   os.chdir( pDir )
	else:
	    (value, type, name, abbr, enum, text, place) = _cnfData["pDir"]
	    value = os.getcwd()
	    _cnfData["pDir"] = (value, type, name, abbr, enum, text, place)

#---------------------------------------------------------------------------
# Print usage
#---------------------------------------------------------------------------

    help = cnfGet( "help" )
    if help:
	cnfUsage()
	sys.exit(0)

#===========================================================================
#
# "cnfSet":  Set the value
#
#	cnfSet( key, value, place, flag, overwrite )
#
#===========================================================================

def cnfSet( iname, ivalue, iplace, flag, overwrite ):

    global _cnfData, _cnfKeys, _cnfList, _cnfBool, _prog, _version

    boolTypes = {}
    for i in [ "0", "f", "false", "off", "no" ]:
	boolTypes[i] = 0
	boolTypes[string.upper(i)] = 0
    for i in [ "1", "t", "true", "on", "yes" ]:
	boolTypes[i] = 1
	boolTypes[string.upper(i)] = 1

    iname = string.strip(iname)
    if iname[-1] == ':' or iname[-1] == "=":
	iname = iname[:-1]

    if not _cnfKeys.has_key(iname):
	if flag:
	    raise CnfError, 'Option <%s> given in <%s> not found' % \
		(iname,iplace)
	else:
	    return

    key = _cnfKeys[iname]

    (value, type, name, abbr, enum, text, place) = _cnfData[key]

    if not overwrite and place == "command-line":
	return

    err = 0
    if type == "int":
	if re.match('\A[-+]?\d+\Z',ivalue) == None:
	    err = 1

    pat = '\A[-+]?(\d+|\d+.|\d+.\d+|.\d+)([edED][+-]?\d+)?\Z'
    if type == "real":
	if re.match(pat,ivalue) == None:
	    err = 1

    if type == "bool":
	if boolTypes.has_key(ivalue):
	    ivalue = boolTypes[ivalue]
	else:
	    err = 1

    pat = '\A(.*,)?%s(,.*)?\Z' % ivalue
    if type == "enum":
	if re.match(pat,enum) == None:
	    err = 1

    if type == "str":
	if ivalue[0]  == '"': ivalue = ivalue[1:]
	if ivalue[-1] == '"': ivalue = ivalue[0:-1]

    if err == 1:
	str = '<%s> is an invalid value for option <%s>'
	str = str + ' of type <%s> of source <%s>'
	raise CnfError, str % (ivalue,iname,type,iplace)

    _cnfData[key] = (ivalue, type, name, abbr, enum, text, iplace)

#===========================================================================
#
# "cnfUsage":  Print usage
#
#	cnfUsage() ;
#
#===========================================================================

def cnfUsage():

    global _cnfData, _cnfKeys, _cnfList, _cnfBool, _prog, _version

    prog = _prog + ":"

    print prog
    print prog, "Usage:"
    print prog
    print prog, "   ", _prog, " [options]"
    print prog
    print prog, "Options:"
    print prog

    for i in range(0,len(_cnfList)):
	key = _cnfList[i]
	(value, type, name, abbr, enum, text, place) = _cnfData[key]
	t1 = "%s <%s>" % (abbr,type)
	t2 = ""
	if type == "bool":
	    t1 = abbr
	    if value == 1:
		value = "TRUE"
	    else:
		value = "FALSE"
	if type == "enum":
	    t2 = ": " + enum
	print "%s:  -%-12s %s%s" % (_prog,t1,text,t2)
	print "%s:   %-14s %s= %s [%s]" % (_prog,"",name,value,place)

    print prog
    print prog, "Configuration Files:"
    print prog
    if os.environ.has_key("ACUSIM_CNF_FILES"):
	files = os.environ["ACUSIM_CNF_FILES"]
    else:
        file1 = os.path.join( ".", "Acusim.cnf" )
        file2 = os.path.join( os.environ["HOME"], "Acusim.cnf" )
	files = file1 + ":" + file2
    print prog, "    ", files
    print prog
    print prog, "Release:", _version
    print prog

#===========================================================================
#
# "cnfGet":  Get the data
#
#	value = cnfGet( key )
#
#===========================================================================

def cnfGet( key ):

    global _cnfData, _cnfKeys, _cnfList, _cnfBool, _prog, _version

    if _cnfData.has_key(key):
	(value, type, name, abbr, enum, text, place) = _cnfData[key]
	return value
    else:
	raise CnfError, 'Invalid configuration key <%s>' % key

#===========================================================================
#
# "cnfGetStr":  Get the data
#
#	value = cnfGetStr( key )
#
#===========================================================================

def cnfGetStr( key ):

    global _cnfData, _cnfKeys, _cnfList, _cnfBool, _prog, _version

    if _cnfData.has_key(key):
	(value, type, name, abbr, enum, text, place) = _cnfData[key]
	if type != 'str':
	    raise CnfError, 'Configuration <%s> not a string' % key
	return value
    else:
	raise CnfError, 'Invalid configuration key <%s>' % key

#===========================================================================
#
# "cnfGetInt":  Get the data
#
#	value = cnfGetInt( key )
#
#===========================================================================

def cnfGetInt( key ):

    global _cnfData, _cnfKeys, _cnfList, _cnfBool, _prog, _version

    if _cnfData.has_key(key):
	(value, type, name, abbr, enum, text, place) = _cnfData[key]
	if type != 'int':
	    raise CnfError, 'Configuration <%s> not an int' % key
	return string.atoi( value )
    else:
	raise CnfError, 'Invalid configuration key <%s>' % key

#===========================================================================
#
# "cnfGetReal":  Get the data
#
#	value = cnfGetReal( key )
#
#===========================================================================

def cnfGetReal( key ):

    global _cnfData, _cnfKeys, _cnfList, _cnfBool, _prog, _version

    if _cnfData.has_key(key):
	(value, type, name, abbr, enum, text, place) = _cnfData[key]
	if type != 'real':
	    raise CnfError, 'Configuration <%s> not a real' % key
	return string.atof( value )
    else:
	raise CnfError, 'Invalid configuration key <%s>' % key

#===========================================================================
#
# "cnfGetBool":  Get the data
#
#	value = cnfGetBool( key )
#
#===========================================================================

def cnfGetBool( key ):

    global _cnfData, _cnfKeys, _cnfList, _cnfBool, _prog, _version

    if _cnfData.has_key(key):
	(value, type, name, abbr, enum, text, place) = _cnfData[key]
	if type != 'bool':
	    raise CnfError, 'Configuration <%s> not a bool' % key
	return value
    else:
	raise CnfError, 'Invalid configuration key <%s>' % key

#===========================================================================
#
# "cnfGetEnum":  Get the data
#
#	value = cnfGetEnum( key )
#
#===========================================================================

def cnfGetEnum( key ):

    global _cnfData, _cnfKeys, _cnfList, _cnfBool, _prog, _version

    if _cnfData.has_key(key):
	(value, type, name, abbr, enum, text, place) = _cnfData[key]
	if type != 'enum':
	    raise CnfError, 'Configuration <%s> not a enum' % key
	return value
    else:
	raise CnfError, 'Invalid configuration key <%s>' % key

#===========================================================================
#
# "cnfQuery":  Is there such a command?
#
#	bool = cnfQuery( key )
#
#===========================================================================

def cnfQuery( key ):

    global _cnfData, _cnfKeys, _cnfList, _cnfBool, _prog, _version

    return _cnfData.has_key(key)

#===========================================================================
#
# "cnfFromCmdLine":  Did this option come from command line?
#
#	bool = cnfFromCmdLine( key )
#
#===========================================================================

def cnfFromCmdLine( key ):

    global _cnfData, _cnfKeys, _cnfList, _cnfBool, _prog, _version

    if _cnfData.has_key(key):
	(value, type, name, abbr, enum, text, place) = _cnfData[key]
	return place == "command-line"
    else:
	return 0

