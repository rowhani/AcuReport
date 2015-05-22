import  string
import  acuUnitTable
from    acuUtil         import str

#===========================================================================
#
# Errors
#
#===========================================================================

ERROR   = "ERROR from acuUnit module"

#===========================================================================
#
# Constants
#
#===========================================================================

RAW_UNIT    = 0
# Misc. 8/07 :M2
_butnSize   = 40
_butnColor  = [255, 170, 85]

#---------------------------------------------------------------------------
# getCats : Get a list of all categories.
#---------------------------------------------------------------------------

def getCats( ):
    ''' Get a list of all categories.

        Arguments:
            none

        Return:
            cats        - list of all categories, sorted
    '''

    cats = acuUnitTable._untCats.keys(                                  )
    cats.sort(                                                          )
    return cats

#---------------------------------------------------------------------------
# getCatName : Return a category name human readable form.
#---------------------------------------------------------------------------

def getCatName( cat ):
    ''' Return a category name human readable form.

        Arguments:
            cat         - origin cat name (eg., 'eddy_viscosity')
        Return:
            name        - human readable name (eg., 'Eddy Viscosity')
    '''

    try:
        name            = ''
        tmp             = cat.split(            '_'                     )
        for item in tmp:
            if item != '':
                name    += string.capitalize( item ) + ' '
        name    = name[:-1]
        return name

    except:
        raise ERROR, " category <%s> is not defined." % cat

#---------------------------------------------------------------------------
# getCat : Return the category of a human readable form.
#---------------------------------------------------------------------------

def getCat( catName ):
    ''' Return the category of a human readable form.

        Arguments:
            catName     - human readable name (eg., 'Eddy Viscosity')
        Return:
            cat         - origin cat name (eg., 'eddy_viscosity')
    '''

    try:
        category    = string.lower(                 catName             )
        category    = string.replace(   category,   ' ',    '_'         )
        return category
    except:
        raise ERROR, " category <%s> is not defined." % catName

#---------------------------------------------------------------------------
# getDefUnit : Return the default unit for a category.
#---------------------------------------------------------------------------

def getDefUnit( cat ):
    ''' Return the default unit for a category.

        Arguments:
            cat         - cat name (eg., 'eddy_viscosity')
        Return:
            defUnit     - default unit (eg., 'm2/sec')
    '''

    defUnit = acuUnitTable._untCats[str(cat)][0]
    return defUnit

#---------------------------------------------------------------------------
# getUnits : Return all the units of a category.
#---------------------------------------------------------------------------

def getUnits( cat ):
    ''' Return all the units of a category.

        Arguments:
            cat         - cat name (eg., 'length')
        Return:
            units       - all units (eg., ('mm', 'cm', 'inch', ...) )
    '''

    units = acuUnitTable._untCats[cat][1]
    return units

#---------------------------------------------------------------------------
# getUnitDesc : Return the long descriptive name of a unit.
#---------------------------------------------------------------------------

def getUnitDesc( unit ):
    ''' Return the long descriptive name of a unit.

        Arguments:
            unit        - unit name (eg., 'm')
        Return:
            longName    - long name (eg., 'meter')
    '''

    longName = acuUnitTable._untFcts[unit][0]
    return longName

#---------------------------------------------------------------------------
# convert : Convert the value from one unit to another.
#---------------------------------------------------------------------------

def convert( value, fromUnit, toUnit = None):
    ''' Convert the value from one unit to another.
        if toUnit=None (default), convert to base unit.

        Arguments:
            value       - value to convert from (eg., 100 )
            fromUnit    - from unit (eg., 'cm')
            toUnit      - to unit (eg., 'km')
        Return:
            retValue    - return value (eg., 1.e-3)
    '''

    baseVal = "None"

    #----- Conver fromUnit to baseUnit


    fromUnit    = str(                      fromUnit                    )
    values      = acuUnitTable._untFcts[fromUnit]
    baseVal     = value * values[2] + values[3]

    if not toUnit:
        return baseVal

    toUnit      = str(                      toUnit                      )

    if baseVal == "None":
        return None

    #----- Conver baseUnit to toUnit

    values      = acuUnitTable._untFcts[toUnit]
    retValue    = ( baseVal - values[3] ) / values[2]

    return retValue

#---------------------------------------------------------------------------
# setUntButnInfo : Set acuUnit button info.
#---------------------------------------------------------------------------

def setUntButnInfo( butnSize = None, butnColor = None ):
    ''' Set acuUnit button info.

        Arguments:
            butnSize    - button size; default values "5" 
            butnColor   - button color; default value "[255,170,85]"

        Return:
            None
    '''

    global _butnSize, _butnColor
    
    if butnSize != None:
        _butnSize   = butnSize
    
    if butnColor != None:
        _butnColor  = butnColor

#---------------------------------------------------------------------------
# getUntButnInfo : Get acuUnit button info.
#---------------------------------------------------------------------------

def getUntButnInfo():
    ''' Get acuUnit button info.

        Arguments:
            None

        Return:
            butnSize    - button size
            butnColor   - button color
    '''

    global _butnSize, _butnColor
    
    return _butnSize, _butnColor

#----- Misc. 12/06  L1
#---------------------------------------------------------------------------
# getBaseUnit : Return the default unit for a category.
#---------------------------------------------------------------------------

def getBaseUnit( unit ):
    ''' Return the default / base unit of a unit.

        Arguments:
            unit         - unit name (eg., 'mm')
        Return:
            baseUnit     - base unit (eg., 'm')
    '''

    baseUnit = acuUnitTable._untFcts[str(unit)][1]
    return baseUnit

#---------------------------------------------------------------------------
# convertCoefs : Returns the required coefficients for conversion.
#---------------------------------------------------------------------------

def convertCoefs( fromUnit, toUnit = None):
    ''' Returns the required coefficients for conversion.

        Arguments:
            fromUnit    - from unit (eg., 'cm')
            toUnit      - to unit (eg., 'km')
        Return:
            multVal     - multiplicative coefficient
            addVal      - additive coefficient
    '''

    fromUnit    = str(                      fromUnit                    )
    values      = acuUnitTable._untFcts[fromUnit]
    multVal     = values[2]
    addVal      = values[3]
    
    if not toUnit or toUnit == values[1]:
        return ( multVal, addVal )
    
    toUnit      = str(                      toUnit                      )
  

    values      = acuUnitTable._untFcts[toUnit]

    multVal     = float( multVal ) / values[2]
    addVal      = float( addVal - values[3] ) / values[2]
    
    return ( multVal, addVal )

#===========================================================================
#
# Test
#
#===========================================================================

if __name__ == '__main__':
##        print getCats(                                                  )
##        print getDefUnit(               'length'                        )
##        print getUnits(                 'length'                        )
##        print getUnits(                 'lenght'                        )
##        print getUnitDesc(              'm'                             )
##        print getUnitDesc(              'mi'                            )
##        print convert(                  100, 'cm'                       )
##        print convert(                  100, 'cm', 'km'                 )
    print getCatName(                   'eddy_viscosity'                )
    print getCatName(                   'eddyviscosity'                 )
