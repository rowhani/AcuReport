#---------------------------------------------------------------------------
# Get the modules
#---------------------------------------------------------------------------

import  re
import  os
import  acupu
import  sys
import __builtin__

#---------------------------------------------------------------------------
# Define Constants.
#---------------------------------------------------------------------------

False       = 0
FALSE	    = 0
false	    = 0

True        = 1
TRUE	    = 1
true	    = 1

#===========================================================================
# Set up string to clean string and back conversion process
#===========================================================================

#---- string to clean string dictionary

_str2CsDic    = {
    '*' :   '___0',
    '`' :   '___1',
    '.' :   '___2',
    '~' :   '___3',
    '!' :   '___4',
    '@' :   '___5',
    '#' :   '___6',
    '$' :   '___7',
    '%' :   '___8',
    '^' :   '___9',
    '&' :   '___A',
    '(' :   '___B',
    ')' :   '___C',
    '+' :   '___D',
    '|' :   '___E',
    '\\':   '___F',
    '[' :   '___G',
    ']' :   '___H',
    '{' :   '___I',
    '}' :   '___J',
    "'" :   '___K',
    '"' :   '___L',
    ';' :   '___M',
    ':' :   '___N',
    '/' :   '___O',
    '?' :   '___P',
    '>' :   '___Q',
    ',' :   '___R',
    '<' :   '___S',
    '-' :   '___T',
    '=' :   '___U',
    ' ' :   '___V'
}

#---- clean string to string dictionary

_cs2StrDic    = {}
for k,v in _str2CsDic.items():
    _cs2StrDic[v]	= k

#---- regular expressions

_str2CsReg = re.compile('|'.join(map(re.escape, _str2CsDic)))
_cs2StrReg = re.compile('|'.join(map(re.escape, _cs2StrDic)))

#---- inner loop functions

def _str2CsTr(match): return _str2CsDic[match.group(0)]
def _cs2StrTr(match): return _cs2StrDic[match.group(0)]

#---- Convert string to clean string

def str2Cs( str ):
    """
    Convert a string to a clean string by replacing all the special
    characters to a clean code "_?" where "?" is 0 to z.

    Arguments:
	str	- original string
    Return
	cs	- clean string
    """

    return _str2CsReg.sub( _str2CsTr, str )

#---- Convert clean string to string

def cs2Str( cs ):
    """
    Convert a string from a clean string by replacing all the "_?" tags 
    to the original ones.  This is the revese of str2Cs()

    Arguments:
	cs	- coded string
    Return
	str	- original string
    """

    return _cs2StrReg.sub( _cs2StrTr, cs )

#===========================================================================
#
# getUnixPath
#
#===========================================================================

def getUnixPath( file ):
    """ Replace '\' with '/' in the file path"""

    if file == None:
	return file

    reg	= re.compile(			r'\\'				)
    str	= reg.sub(			r'\\\\',	file		)
    str	= str.replace(			'\\\\', '/'			)
    file	= str.replace(		'\\', '/'			)

    return file

#===========================================================================
#
# killPid
#
#===========================================================================

def killPid( pid = None, ppid = True ):

    """
    Kill a process given the process Id(pid),
    and optionally all its children(if ppid = True)

    Arguments:
	pid	- The process Id.
	ppid	- If True kill all its children.
    Return:
        None
        
    """

    if sys.platform == 'win32':
        if ppid:
            er  = os.popen3( "taskkill /F /T /PID %s" %pid  )[2]
        else:
            er  = os.popen3( "taskkill /F /PID %s" %childId )[2]
    else:
        if ppid:
            er  = os.popen3( "kill -%s" %childId )[2]
        else:
            er  = os.popen3("kill %s" %childId )[2]
            
    error       = er.readlines(                                         )
    if len(  error ) != 0:
        raise  error[0]

#===========================================================================
#
# findChilds
#
#===========================================================================

def findChilds( pid, pids, childlist = [ ] ):

    """
    Find all childrens of one process and return the childs list.

    Arguments:
	pid	    - The process Id.
	pids	    - The list of all processes.
	childlist   - The list that each process children is
                      placed in it.    
    Return:
        childlist   - The list of process childs.
        
    """
    
    for i in pids:
        pidNum  = i[0]
        ppidNum = i[1]
        if ppidNum == pid and pidNum not in childlist:
            childlist.append( pidNum )
            findChilds( pidNum,pids,childlist)
    return childlist

#===========================================================================
#
# getPpid
#
#===========================================================================

def getPpid(  pid ):

    """
    Get the id of the process parent.

    Arguments:
	pid     - The process Id.

    Return:
        ppid    - The pid of the parent(if the pid not found return -1).
        
    """

    ppid    = -1
    pids    = acupu.getProcIds()
    for id in pids:
        if id[0] == pid :
            ppid = id[1]
            break
    return ppid

#===========================================================================
#
# str
#
#===========================================================================

def str(txt):
    
    try:
        ret = __builtin__.str(                  txt                     )
    except:
        sys.exc_clear(                                                  )
        ret = __builtin__.unicode(              txt                     )
    return ret

#===========================================================================
#
# Test
#
#===========================================================================

if __name__ == '__main__':

    a = 'here is a line with {}  -~//\\!$ characters'
    b = str2Cs( a )
    c = cs2Str( b )
    e = 0
    if a == b: 
	print "Error in str2Cs"
	e = 1
    if a != c:
	print "Error in cs2Str"
	e = 1
    if e == 0:
	print "Pass"


