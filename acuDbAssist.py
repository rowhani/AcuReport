#=========================================================================
#
# importing required modules
#
#=========================================================================

import  os
import  types
import  numarray

import  acuUnit
import  acuUnitTable

import  acudb2       as acudb

#===========================================================================
#
# Events
#
#===========================================================================

_EVENT_TS		= 1
_EVENT_TIME		= 2
_EVENT_TIMEINC		= 3
_EVENT_STG_NAME		= 4
_EVENT_RES_RAT		= 5
_EVENT_SOL_RAT		= 6
_EVENT_REDO_STEP	= 7
_EVENT_END_RUN		= 8
_EVENT_RES_NORM		= 9
_EVENT_SOL_NORM		= 10
_EVENT_EQN_NAME		= 11
_EVENT_LHS_UPD		= 12
_EVENT_N_ITERS		= 13
_EVENT_LES_RED		= 14
_EVENT_CPU_TIME		= 15
_EVENT_ELAPSED_TIME	= 16

#===========================================================================
#
# Units
#
#===========================================================================

_adbUnit    = {
    "acceleration"			: (('acceleration'  ,
                                           'oei'                ),),
    "air_temperature"			: (('temperature'   ,
                                           'ohc'                ),),
    "area"				: (('area'          ,
                                           'osi,ori,oqi,ofc,ohc'),),
    "convective_species_flux"		: (('mass_flux'     ,
                                           'osi'                ),),
    "convective_temperature_flux"	: (('heat_rate'     ,
                                           'osi'                ),),
    "coolant_heat"			: (('heat_flux'     ,
                                           'ohc'                ),),
    "coolant_temperature"		: (('temperature'   ,
                                           'ohc'                ),),
    "dissipation"			: (('dissipation'   ,
                                           'osi,oei,oth'        ),),
    "mass_averaged_dissipation"		: (('dissipation'   ,
                                           'oei'        	),),
    "dissipation_rate"			: (('inverse_time'  ,
                                           'osi,oei,oth'        ),),
    "mass_averaged_dissipation_rate"	: (('inverse_time'  ,
                                           'oei'        	),),
    "eddy_viscosity"			: (('eddy_viscosity',
                                           'osi,oei,oth'        ),),
    "mass_averaged_eddy_viscosity"	: (('eddy_viscosity',
                                           'oei'        	),),
    "grad_pressure"			: (('grad_pressure' ,
                                           'oei'                ),),
    "grad_species"			: (('inverse_length',
                                           'oei'                ),),
    "grad_temperature"			: (('grad_temperature',
                                           'oei'                ),),
    "grad_velocity"			: (('grad_velocity' ,
                                           'oei'                ),),
    "heat_flux"				: (('heat_flux'     ,
                                           'oei'                ),
                                           ('heat_rate'     ,
                                           'osi,ori,oqi'        ),),
    "kinetic_energy"			: (('kinetic_energy',
                                           'si,oei,oth'         ),),
    "mass_flux"				: (('mass_flux'     ,
                                           'osi,ofc,ohc'        ),),
    "mean_radiant_temperature"		: (('temperature'   ,
                                           'ori'                ),),
    "mesh_displacement"			: (('displacement'  ,
                                           'osi,oei,oth'        ),),
    "mesh_velocity"			: (('velocity'      ,
                                           'osi,oei,oth'        ),),
    "moment"				: (('torque'        ,
                                           'osi'                ),),
    "momentum_flux"			: (('force'         ,
                                           'osi'                ),),
    "pressure"				: (('pressure'      ,
                                           'osi,oei,oth'        ),),
    "species"				: (('None'          ,
                                           'osi,oei,oth'        ),),
    "mass_averaged_species"		: (('None'          ,
                                           'oei'        	),),
    "species_flux"			: (('species_flux'  ,
                                           'osi,oei'            ),),
    "stress"				: (('pressure'      ,
                                           'oei'                ),),
    "surface_film_coefficient"		: (('convective_heat_flux',
                                           'osi'                ),),
    "surface_y_plus"			: (('None'          ,
                                           'osi'                ),),
    "temperature"			: (('temperature'   ,
                                           'osi,ori,oei,oth,ohc'),),
    "mass_averaged_temperature"		: (('temperature'   ,
                                           'oei'),),
    "time"			        : (('time'          ,
                                           'all'                ),),
    "time_step"			        : (('None'          ,
                                           'all'                ),),
    "total_pressure"			: (('pressure'      ,
                                           'osi,oei'            ),),
    "traction"				: (('force'         ,
                                           'osi'                ),),
    "user_output"			: (('None'          ,
                                           'oei'                ),),
    "velocity"				: (('velocity'      ,
                                           'osi,oei,oth'        ),),
    "velocity_scale"			: (('velocity'      ,
                                           'osi,oei,oth'        ),),
    "volume"				: (('volume'        ,
                                           'oei'                ),),
}

#=========================================================================
#
# "Errors":
#
#=========================================================================

AcuDbAssistError = "Error from acuDbAssist module"

#=========================================================================
#
# "AcuDbAssist" class: The main class of the module  
#
#=========================================================================

class AcuDbAssist :

    """ Opens and extracts the database file and transferrs it to
        the Report and Plot it.    
    """
    
#-------------------------------------------------------------------------
# "__init__"      :   Initialize AcuDbAssist class 
#-------------------------------------------------------------------------
    
    def __init__( self, problemName, dirName, runId ):
        
        """ Get problem name and working directory name and run name
        
         Arguments:
                problemName     -  name of the problem
                dirName         -  name of the working directory  
                runId           -  run number
        Output:
                None
        """

        if not os.path.exists( dirName ):
            raise AcuDbAssistError,"\"" + dirName + "\" Directory does not exist." 
        
        #-----------------------------------------------------------------
        # Creating an acudb object to open the data base and get its data
        #-----------------------------------------------------------------        

        try:
            self.adb        = acudb.Acudb(  problemName,    dirName, 0  )
        except:
            raise AcuDbAssistError, "Error opening the data base"
         
 	self.adb.openRun(                   runId                       )

        #-----------------------------------------------------------------
        # Creating dictionaries to save _adbOuts data
        #-----------------------------------------------------------------

	self.osiNames       = {}
	self.osiVarNames    = {}

	self.oeiNames       = {}
	self.oeiVarNames    = {}

	self.ofcNames       = {}
	self.ofcVarNames    = {}
       
	self.ohcNames       = {}
	self.ohcVarNames    = {}
       
	self.oriNames       = {}
	self.oriVarNames    = {}

	self.oqiNames       = {}
	self.oqiVarNames    = {}

	self.othNames       = {}
	self.othNodes       = {}
	self.othVarNames    = {}

        #-----------------------------------------------------------------
        # Creating dictionaries to save convergence data
        #-----------------------------------------------------------------

	self.initAdb	    = False
	self.resNames       = {}
	self.solNames	    = {}
	self.iterNames	    = {}

	self.ratioType      = {}
	self.ratioType["initial"]= 1
	self.ratioType["final"] = 2
	self.ratioType["all"]   = 3
       
#-------------------------------------------------------------------------
# "getOsiNames": Return a list of osi names.
#-------------------------------------------------------------------------
    
    def getOsiNames( self ):
        """ Return a list of osi names.

            Arguments:
                None
            Output:
                A list of osi names.
        """

        if self.osiNames:
            return self.osiNames.keys()
        
        n   = self.adb.get(                         "nOsfs"             )
        for indx in xrange( n ):
            name                    = self.adb.get( "osfName",  indx    )
            self.osiNames[ name ]   = indx

        return self.osiNames.keys()

#-------------------------------------------------------------------------
# "getOsiVarNames":  Return a list of osi variable names.
#-------------------------------------------------------------------------
   
    def getOsiVarNames( self ):
        """ Return a list of osi variable names.

            Arguments:
                None
            Output:
                A list of osi variable names
        """

        if self.osiVarNames:
            return self.osiVarNames.keys()
        
        n   = self.adb.get(                         "nOsiVars"          )
        for indx in xrange( n ):
            name                    = self.adb.get( "osiVarName",
                                                    indx                ) 
            self.osiVarNames[ name ]= indx

        return self.osiVarNames.keys()

#-------------------------------------------------------------------------
# "getOsiNameIndx": Return the osi index.
#-------------------------------------------------------------------------        
       
    def getOsiNameIndx( self, name ):
        """ Map the osi name into an index.

            Argument:
                name    - The osi name/index.

            Output:
                The mapped index.
        """
        
        if not self.osiNames:
            self.getOsiNames(                                           )

        if name in self.osiNames:
            return self.osiNames[ name ]
        elif name in self.osiNames.values():
            return name
        else:
            return -1
        
#-------------------------------------------------------------------------
# "getOsiSteps": Return the osi steps.
#-------------------------------------------------------------------------        
       
    def getOsiSteps( self, name ):
        """ Return the acudb.osiSteps.

            Argument:
                name    - The osi name/index.

            Output:
                The related osi steps values.
        """

        indx    = self.getOsiNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get osiSteps."

        return self.adb.get(        "osiSteps",     indx                )
        
#-------------------------------------------------------------------------
# "getOsiTimes": Return the osi times.
#-------------------------------------------------------------------------        
   
    def getOsiTimes( self, name ):
        """ Return the acudb.osiTimes.

            Argument:
                name    - The osi name/index.

            Output:
                The related osi times values.
        """
        
        indx    = self.getOsiNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get osiTimes."

        return self.adb.get(        "osiTimes",     indx                )
                
#-------------------------------------------------------------------------
# "getOsiValues": Return the osi values
#------------------------------------------------------------------------- 
    
    def getOsiValues( self, name, var, unit = None  ):
        """ Return the acudb.osiValues.

            Argument:
                name    - The osi name/index.
                var     - The osi variable name/index.
                unit    - The osi variable unit.

            Output:
                values  - The related osi variable values.
        """

        #----------------------------------------------------------------
        # Searching for name index
        #----------------------------------------------------------------

        id1         = self.getOsiNameIndx(          name                )
        if id1 == -1:
            raise AcuDbAssistError, "Invalid name argument to get osiValues."

        #----------------------------------------------------------------
        # Searching for variable index
        #----------------------------------------------------------------

        if not self.osiVarNames:
            self.getOsiVarNames(                                        )

        if var in self.osiVarNames:
            id2     = self.osiVarNames[ var ]
        elif var in self.osiVarNames.values():
            id2     = var
        else:
            raise AcuDbAssistError, "Invalid variable argument to get osiValues."

        #----------------------------------------------------------------
        # Return the acudb.osiValues
        #----------------------------------------------------------------

        values      = self.adb.get( "osiValues",    id1,    id2         )
        
        if unit != None:
            bsUnit  = self.getOsiVarUnit(           var                 )
            values  = self.convert( values,         bsUnit,     unit    )

        return values

#-------------------------------------------------------------------------
# "getOsiVarUnit" : Returns the SI unit of osi variable
#-------------------------------------------------------------------------
    
    def getOsiVarUnit( self, name ):
        """ Returns the SI unit of the osi variable.
        
            Argument:
                name    - Varable name
            Output:
                unit    - SI unit
        """

        if not self.osiVarNames:
            self.getOsiVarNames(                                        )

        if name not in self.osiVarNames:
            for k, v in self.osiVarNames.items():
                if name == v:
                    name = k
                    break
                
        unit    = self.getVarUnit(      name,               "osi"       )
        if not unit:
            raise AcuDbAssistError, "Invalid variable name."
        return unit

#-------------------------------------------------------------------------
# "getOeiNames": Return a list of oei names.
#-------------------------------------------------------------------------
    
    def getOeiNames( self ):
        """ Return a list of oei names.

            Arguments:
                None
            Output:
                A list of oei names.
        """

        if self.oeiNames:
            return self.oeiNames.keys()
        
        n   = self.adb.get(                         "nOels"             )
        for indx in xrange( n ):
            name                    = self.adb.get( "oelName",  indx    )
            self.oeiNames[ name ]   = indx

        return self.oeiNames.keys()

#-------------------------------------------------------------------------
# "getOeiVarNames":  Return a list of oei variable names.
#-------------------------------------------------------------------------
   
    def getOeiVarNames( self ):
        """ Return a list of oei variable names.

            Arguments:
                None
            Output:
                A list of oei variable names
        """

        if self.oeiVarNames:
            return self.oeiVarNames.keys()

        n   = self.adb.get(                         "nOeiVars"          )
        for indx in xrange( n ):
            name                    = self.adb.get( "oeiVarName",
                                                    indx                ) 
            self.oeiVarNames[name]  = indx

        return self.oeiVarNames.keys()
  
#-------------------------------------------------------------------------
# "getOeiNameIndx": Return the oei index.
#-------------------------------------------------------------------------        
       
    def getOeiNameIndx( self, name ):
        """ Map the oei name into an index.

            Argument:
                name    - The oei name/index.

            Output:
                The mapped index.
        """
        
        if not self.oeiNames:
            self.getOeiNames(                                           )

        if name in self.oeiNames:
            return self.oeiNames[ name ]
        elif name in self.oeiNames.values():
            return name
        else:
            return -1

#-------------------------------------------------------------------------
# "getOeiSteps": Return the oei steps.
#-------------------------------------------------------------------------        
   
    def getOeiSteps( self, name ):
        """ Return the acudb.oeiSteps.

            Argument:
                name    - The oei name/index.

            Output:
                The related oei steps values.
        """

        indx    = self.getOeiNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get oeiSteps."

        return self.adb.get(        "oeiSteps",     indx                )

#-------------------------------------------------------------------------
# "getOeiTimes": Return the oei times.
#-------------------------------------------------------------------------        
   
    def getOeiTimes( self, name ):
        """ Return the acudb.oeiTimes.

            Argument:
                name    - The oei name/index.

            Output:
                The related oei times values.
        """
        
        indx    = self.getOeiNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get oeiTimes."

        return self.adb.get(        "oeiTimes",     indx                )
        
#-------------------------------------------------------------------------
# "getOeiValues": Return the oei values
#------------------------------------------------------------------------- 
    
    def getOeiValues( self, name, var, unit = None  ):
        """ Return the acudb.oeiValues.

            Argument:
                name    - The oei name/index.
                var     - The oei variable name/index.
                unit    - The oei variable unit.

            Output:
                values  - The related oei variable values.
        """

        #----------------------------------------------------------------
        # Searching for name index
        #----------------------------------------------------------------

        id1         = self.getOeiNameIndx(          name                )
        if id1 == -1:
            raise AcuDbAssistError, "Invalid name argument to get oeiValues."

        #----------------------------------------------------------------
        # Searching for variable index
        #----------------------------------------------------------------

        if not self.oeiVarNames:
            self.getOeiVarNames(                                        )

        if var in self.oeiVarNames:
            id2     = self.oeiVarNames[ var ]
        elif var in self.oeiVarNames.values():
            id2     = var
        else:
            raise AcuDbAssistError, "Invalid variable argument to get oeiValues."

        #----------------------------------------------------------------
        # Return the acudb.oeiValues
        #----------------------------------------------------------------

        values      = self.adb.get( "oeiValues",    id1,    id2         )
        
        if unit != None:
            bsUnit  = self.getOeiVarUnit(           var                 )
            values  = self.convert( values,         bsUnit,     unit    )

        return values

#-------------------------------------------------------------------------
# "getOeiVarUnit" : Returns the SI unit of oei variable
#-------------------------------------------------------------------------
    
    def getOeiVarUnit( self, name ):
        """ Returns the SI unit of the oei variable.
        
            Argument:
                name    - Varable name
            Output:
                unit    - SI unit
        """

        if not self.oeiVarNames:
            self.getOeiVarNames(                                        )

        if name not in self.oeiVarNames:
            for k, v in self.oeiVarNames.items():
                if name == v:
                    name = k
                    break
                
        unit    = self.getVarUnit(      name,               "oei"       )
        if not unit:
            raise AcuDbAssistError, "Invalid variable name."
        return unit

#-------------------------------------------------------------------------
# "getOfcNames": Return a list of ofc names.
#-------------------------------------------------------------------------
    
    def getOfcNames( self ):
        """ Return a list of ofc names.

            Arguments:
                None
            Output:
                A list of ofc names.
        """

        if self.ofcNames:
            return self.ofcNames.keys()
        
        n   = self.adb.get(                         "nFans"             )
        for indx in xrange( n ):
            name                    = self.adb.get( "fanName",  indx    )
            self.ofcNames[ name ]   = indx

        return self.ofcNames.keys()

#-------------------------------------------------------------------------
# "getOfcVarNames":  Return a list of ofc variable names.
#-------------------------------------------------------------------------
   
    def getOfcVarNames( self ):
        """ Return a list of ofc variable names.

            Arguments:
                None
            Output:
                A list of ofc variable names
        """

        if self.ofcVarNames:
            return self.ofcVarNames.keys()
  
        n   = self.adb.get(                         "nOfcVars"          )
        for indx in xrange( n ):
            name                    = self.adb.get( "ofcVarName",
                                                    indx                ) 
            self.ofcVarNames[name]  = indx

        return self.ofcVarNames.keys()

#-------------------------------------------------------------------------
# "getOfcNameIndx": Return the ofc index.
#-------------------------------------------------------------------------        
       
    def getOfcNameIndx( self, name ):
        """ Map the ofc name into an index.

            Argument:
                name    - The ofc name/index.

            Output:
                The mapped index.
        """
        
        if not self.ofcNames:
            self.getOfcNames(                                           )

        if name in self.ofcNames:
            return self.ofcNames[ name ]
        elif name in self.ofcNames.values():
            return name
        else:
            return -1

#-------------------------------------------------------------------------
# "getOfcSteps": Return the ofc steps.
#-------------------------------------------------------------------------        
   
    def getOfcSteps( self, name ):
        """ Return the acudb.ofcSteps.

            Argument:
                name    - The ofc name/index.

            Output:
                The related ofc steps values.
        """

        indx    = self.getOfcNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get ofcSteps."

        return self.adb.get(        "ofcSteps",     indx                )

#-------------------------------------------------------------------------
# "getOfcTimes": Return the ofc times.
#-------------------------------------------------------------------------        
   
    def getOfcTimes( self, name ):
        """ Return the acudb.ofcTimes.

            Argument:
                name    - The ofc name/index.

            Output:
                The related ofc times values.
        """
        
        indx    = self.getOfcNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get ofcTimes."

        return self.adb.get(        "ofcTimes",     indx                )

#-------------------------------------------------------------------------
# "getOfcValues": Return the ofc values.
#------------------------------------------------------------------------- 
    
    def getOfcValues( self, name, var, unit = None  ):
        """ Return the acudb.ofcValues.

            Argument:
                name    - The ofc name/index.
                var     - The ofc variable name/index.
                unit    - The ofc variable unit.

            Output:
                values  - The related ofc variable values.
        """

        #----------------------------------------------------------------
        # Searching for name index
        #----------------------------------------------------------------

        id1         = self.getOfcNameIndx(          name                )
        if id1 == -1:
            raise AcuDbAssistError, "Invalid name argument to get ofcValues."

        #----------------------------------------------------------------
        # Searching for variable index
        #----------------------------------------------------------------

        if not self.ofcVarNames:
            self.getOfcVarNames(                                        )

        if var in self.ofcVarNames:
            id2     = self.ofcVarNames[ var ]
        elif var in self.ofcVarNames.values():
            id2     = var
        else:
            raise AcuDbAssistError, "Invalid variable argument to get ofcValues."

        #----------------------------------------------------------------
        # Return the acudb.ofcValues
        #----------------------------------------------------------------

        values      = self.adb.get( "ofcValues",    id1,    id2         )
        
        if unit != None:
            bsUnit  = self.getOfcVarUnit(           var                 )
            values  = self.convert( values,         bsUnit,     unit    )

        return values

#-------------------------------------------------------------------------
# "getOfcVarUnit" : Returns the SI unit of ofc variable
#-------------------------------------------------------------------------
    
    def getOfcVarUnit( self, name ):
        """ Returns the SI unit of the ofc variable.
        
            Argument:
                name    - Varable name
            Output:
                unit    - SI unit
        """

        if not self.ofcVarNames:
            self.getOfcVarNames(                                        )

        if name not in self.ofcVarNames:
            for k, v in self.ofcVarNames.items():
                if name == v:
                    name = k
                    break
                
        unit    = self.getVarUnit(      name,               "ofc"       )
        if not unit:
            raise AcuDbAssistError, "Invalid variable name."
        return unit

#-------------------------------------------------------------------------
# "getOhcNames": Return a list of ohc names.
#-------------------------------------------------------------------------
    
    def getOhcNames( self ):
        """ Return a list of ohc names.

            Arguments:
                None
            Output:
                A list of ohc names.
        """

        if self.ohcNames:
            return self.ohcNames.keys()
        
        n   = self.adb.get(                         "nHecs"             )
        for indx in xrange( n ):
            name                    = self.adb.get( "hecName",  indx    )
            self.ohcNames[ name ]   = indx

        return self.ohcNames.keys()

#-------------------------------------------------------------------------
# "getOhcVarNames":  Return a list of ohc variable names.
#-------------------------------------------------------------------------
   
    def getOhcVarNames( self ):
        """ Return a list of ohc variable names.

            Arguments:
                None
            Output:
                A list of ohc variable names
        """

        if self.ohcVarNames:
            return self.ohcVarNames.keys()
  
        n   = self.adb.get(                         "nOhcVars"          )
        for indx in xrange( n ):
            name                    = self.adb.get( "ohcVarName",
                                                    indx                ) 
            self.ohcVarNames[name]  = indx

        return self.ohcVarNames.keys()

#-------------------------------------------------------------------------
# "getOhcNameIndx": Return the ohc index.
#-------------------------------------------------------------------------        
       
    def getOhcNameIndx( self, name ):
        """ Map the ohc name into an index.

            Argument:
                name    - The ohc name/index.

            Output:
                The mapped index.
        """
        
        if not self.ohcNames:
            self.getOhcNames(                                           )

        if name in self.ohcNames:
            return self.ohcNames[ name ]
        elif name in self.ohcNames.values():
            return name
        else:
            return -1

#-------------------------------------------------------------------------
# "getOhcSteps": Return the ohc steps.
#-------------------------------------------------------------------------        
   
    def getOhcSteps( self, name ):
        """ Return the acudb.ohcSteps.

            Argument:
                name    - The ohc name/index.

            Output:
                The related ohc steps values.
        """

        indx    = self.getOhcNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get ohcSteps."

        return self.adb.get(        "ohcSteps",     indx                )

#-------------------------------------------------------------------------
# "getOhcTimes": Return the ohc times.
#-------------------------------------------------------------------------        
   
    def getOhcTimes( self, name ):
        """ Return the acudb.ohcTimes.

            Argument:
                name    - The ohc name/index.

            Output:
                The related ohc times values.
        """
        
        indx    = self.getOhcNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get ohcTimes."

        return self.adb.get(        "ohcTimes",     indx                )
                
#-------------------------------------------------------------------------
# "getOhcValues": Return the ohc values.
#------------------------------------------------------------------------- 
    
    def getOhcValues( self, name, var, unit = None  ):
        """ Return the acudb.ohcValues.

            Argument:
                name    - The ohc name/index.
                var     - The ohc variable name/index.
                unit    - The ohc variable unit.

            Output:
                values  - The related ohc variable values.
        """

        #----------------------------------------------------------------
        # Searching for name index
        #----------------------------------------------------------------

        id1         = self.getOhcNameIndx(          name                )
        if id1 == -1:
            raise AcuDbAssistError, "Invalid name argument to get ohcValues."

        #----------------------------------------------------------------
        # Searching for variable index
        #----------------------------------------------------------------

        if not self.ohcVarNames:
            self.getOhcVarNames(                                        )

        if var in self.ohcVarNames:
            id2     = self.ohcVarNames[ var ]
        elif var in self.ohcVarNames.values():
            id2     = var
        else:
            raise AcuDbAssistError, "Invalid variable argument to get ohcValues."

        #----------------------------------------------------------------
        # Return the acudb.ohcValues
        #----------------------------------------------------------------

        values      = self.adb.get( "ohcValues",    id1,    id2         )
        
        if unit != None:
            bsUnit  = self.getOhcVarUnit(           var                 )
            values  = self.convert( values,         bsUnit,     unit    )

        return values

#-------------------------------------------------------------------------
# "getOhcVarUnit" : Returns the SI unit of ohc variable
#-------------------------------------------------------------------------
    
    def getOhcVarUnit( self, name ):
        """ Returns the SI unit of the ohc variable.
        
            Argument:
                name    - Varable name
            Output:
                unit    - SI unit
        """

        if not self.ohcVarNames:
            self.getOhcVarNames(                                        )

        if name not in self.ohcVarNames:
            for k, v in self.ohcVarNames.items():
                if name == v:
                    name = k
                    break
                
        unit    = self.getVarUnit(      name,               "ohc"       )
        if not unit:
            raise AcuDbAssistError, "Invalid variable name."
        return unit

#-------------------------------------------------------------------------
# "getOriNames": Return a list of ori names.
#-------------------------------------------------------------------------
    
    def getOriNames( self ):
        """ Return a list of ori names.

            Arguments:
                None
            Output:
                A list of ori names.
        """

        if self.oriNames:
            return self.oriNames.keys()

        n   = self.adb.get(                         "nRsfs"             )
        for indx in xrange( n ):
            name                    = self.adb.get( "rsfName",  indx    )
            self.oriNames[ name ]   = indx

        return self.oriNames.keys()
        
#-------------------------------------------------------------------------
# "getOriVarNames":  Return a list of ori variable names.
#-------------------------------------------------------------------------
   
    def getOriVarNames( self ):
        """ Return a list of ori variable names.

            Arguments:
                None
            Output:
                A list of ori variable names
        """

        if self.oriVarNames:
            return self.oriVarNames.keys()

        n   = self.adb.get(                         "nOriVars"          )
        for indx in xrange( n ):
            name                    = self.adb.get( "oriVarName",
                                                    indx                ) 
            self.oriVarNames[name]  = indx

        return self.oriVarNames.keys()

#-------------------------------------------------------------------------
# "getOriNameIndx": Return the ori index.
#-------------------------------------------------------------------------        
       
    def getOriNameIndx( self, name ):
        """ Map the ori name into an index.

            Argument:
                name    - The ori name/index.

            Output:
                The mapped index.
        """
        
        if not self.oriNames:
            self.getOriNames(                                           )

        if name in self.oriNames:
            return self.oriNames[ name ]
        elif name in self.oriNames.values():
            return name
        else:
            return -1

#-------------------------------------------------------------------------
# "getOriSteps": Return the ori steps.
#-------------------------------------------------------------------------        
   
    def getOriSteps( self, name ):
        """ Return the acudb.oriSteps.

            Argument:
                name    - The ori name/index.

            Output:
                The related ori steps values.
        """

        indx    = self.getOriNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get oriSteps."

        return self.adb.get(        "oriSteps",     indx                )

#-------------------------------------------------------------------------
# "getOriTimes": Return the ori times.
#-------------------------------------------------------------------------        
   
    def getOriTimes( self, name ):
        """ Return the acudb.oriTimes.

            Argument:
                name    - The ori name/index.

            Output:
                The related ori times values.
        """
        
        indx    = self.getOriNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get oriTimes."

        return self.adb.get(        "oriTimes",     indx                )

#-------------------------------------------------------------------------
# "getOriValues": Return the ori values.
#------------------------------------------------------------------------- 
    
    def getOriValues( self, name, var, unit = None  ):
        """ Return the acudb.oriValues.

            Argument:
                name    - The ori name/index.
                var     - The ori variable name/index.
                unit    - The ori variable unit.

            Output:
                values  - The related ori variable values.
        """

        #----------------------------------------------------------------
        # Searching for name index
        #----------------------------------------------------------------

        id1         = self.getOriNameIndx(          name                )
        if id1 == -1:
            raise AcuDbAssistError, "Invalid name argument to get oriValues."

        #----------------------------------------------------------------
        # Searching for variable index
        #----------------------------------------------------------------

        if not self.oriVarNames:
            self.getOriVarNames(                                        )

        if var in self.oriVarNames:
            id2     = self.oriVarNames[ var ]
        elif var in self.oriVarNames.values():
            id2     = var
        else:
            raise AcuDbAssistError, "Invalid variable argument to get oriValues."

        #----------------------------------------------------------------
        # Return the acudb.oriValues
        #----------------------------------------------------------------

        values      = self.adb.get( "oriValues",    id1,    id2         )
        
        if unit != None:
            bsUnit  = self.getOriVarUnit(           var                 )
            values  = self.convert( values,         bsUnit,     unit    )

        return values

#-------------------------------------------------------------------------
# "getOriVarUnit" : Returns the SI unit of ori variable
#-------------------------------------------------------------------------
    
    def getOriVarUnit( self, name ):
        """ Returns the SI unit of the ori variable.
        
            Argument:
                name    - Varable name
            Output:
                unit    - SI unit
        """

        if not self.oriVarNames:
            self.getOriVarNames(                                        )

        if name not in self.oriVarNames:
            for k, v in self.oriVarNames.items():
                if name == v:
                    name = k
                    break
                
        unit    = self.getVarUnit(      name,               "ori"       )
        if not unit:
            raise AcuDbAssistError, "Invalid variable name."
        return unit

#-------------------------------------------------------------------------
# "getOqiNames": Return a list of oqi names.
#-------------------------------------------------------------------------
    
    def getOqiNames( self ):
        """ Return a list of oqi names.

            Arguments:
                None
            Output:
                A list of oqi names.
        """

        if self.oqiNames:
            return self.oqiNames.keys()

        n   = self.adb.get(                         "nSrss"             )
        for indx in xrange( n ):
            name                    = self.adb.get( "srsName",  indx    )
            self.oqiNames[ name ]   = indx

        return self.oqiNames.keys()

#-------------------------------------------------------------------------
# "getOqiVarNames":  Return a list of oqi variable names.
#-------------------------------------------------------------------------
   
    def getOqiVarNames( self ):
        """ Return a list of oqi variable names.

            Arguments:
                None
            Output:
                A list of oqi variable names
        """

        if self.oqiVarNames:
            return self.oqiVarNames.keys()

        n   = self.adb.get(                         "nOqiVars"          )
        for indx in xrange( n ):
            name                    = self.adb.get( "oqiVarName",
                                                    indx                ) 
            self.oqiVarNames[name]  = indx

        return self.oqiVarNames.keys()

#-------------------------------------------------------------------------
# "getOqiNameIndx": Return the oqi index.
#-------------------------------------------------------------------------        
       
    def getOqiNameIndx( self, name ):
        """ Map the oqi name into an index.

            Argument:
                name    - The oqi name/index.

            Output:
                The mapped index.
        """
        
        if not self.oqiNames:
            self.getOqiNames(                                           )

        if name in self.oqiNames:
            return self.oqiNames[ name ]
        elif name in self.oqiNames.values():
            return name
        else:
            return -1

#-------------------------------------------------------------------------
# "getOqiSteps": Return the oqi steps.
#-------------------------------------------------------------------------        
   
    def getOqiSteps( self, name ):
        """ Return the acudb.oqiSteps.

            Argument:
                name    - The oqi name/index.

            Output:
                The related oqi steps values.
        """

        indx    = self.getOqiNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get oqiSteps."

        return self.adb.get(        "oqiSteps",     indx                )

#-------------------------------------------------------------------------
# "getOqiTimes": Return the oqi times.
#-------------------------------------------------------------------------        
   
    def getOqiTimes( self, name ):
        """ Return the acudb.oqiTimes.

            Argument:
                name    - The oqi name/index.

            Output:
                The related oqi times values.
        """
        
        indx    = self.getOqiNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get oqiTimes."

        return self.adb.get(        "oqiTimes",     indx                )
       
#-------------------------------------------------------------------------
# "getOqiValues": Return the oqi values.
#------------------------------------------------------------------------- 
    
    def getOqiValues( self, name, var, unit = None  ):
        """ Return the acudb.oqiValues.

            Argument:
                name    - The oqi name/index.
                var     - The oqi variable name/index.
                unit    - The oqi variable unit.

            Output:
                values  - The related oqi variable values.
        """

        #----------------------------------------------------------------
        # Searching for name index
        #----------------------------------------------------------------

        id1         = self.getOqiNameIndx(          name                )
        if id1 == -1:
            raise AcuDbAssistError, "Invalid name argument to get oqiValues."

        #----------------------------------------------------------------
        # Searching for variable index
        #----------------------------------------------------------------

        if not self.oqiVarNames:
            self.getOqiVarNames(                                        )

        if var in self.oqiVarNames:
            id2     = self.oqiVarNames[ var ]
        elif var in self.oqiVarNames.values():
            id2     = var
        else:
            raise AcuDbAssistError, "Invalid variable argument to get oqiValues."

        #----------------------------------------------------------------
        # Return the acudb.oqiValues
        #----------------------------------------------------------------

        values      = self.adb.get( "oqiValues",    id1,    id2         )
        
        if unit != None:
            bsUnit  = self.getOqiVarUnit(           var                 )
            values  = self.convert( values,         bsUnit,     unit    )

        return values

#-------------------------------------------------------------------------
# "getOqiVarUnit" : Returns the SI unit of oqi variable
#-------------------------------------------------------------------------
    
    def getOqiVarUnit( self, name ):
        """ Returns the SI unit of the oqi variable.
        
            Argument:
                name    - Varable name
            Output:
                unit    - SI unit
        """

        if not self.oqiVarNames:
            self.getOqiVarNames(                                        )

        if name not in self.oqiVarNames:
            for k, v in self.oqiVarNames.items():
                if name == v:
                    name = k
                    break
                
        unit    = self.getVarUnit(      name,               "oqi"       )
        if not unit:
            raise AcuDbAssistError, "Invalid variable name."
        return unit

#-------------------------------------------------------------------------
# "getOthNames": Return a list of oth names.
#-------------------------------------------------------------------------
    
    def getOthNames( self ):
        """ Return a list of oth names.

            Arguments:
                None
            Output:
                A list of oth names.
        """

        if self.othNames:
            return self.othNames.keys()
        
        nSets       = self.adb.get(         "nOths"                     )
        for id1 in range( nSets ):
            name    = self.adb.get(         "othName",      id1         )
            self.othNames[ name ] = id1

        return self.othNames.keys()

#-------------------------------------------------------------------------
# "getOthNodes": Return a list of oth nodes.
#-------------------------------------------------------------------------
    
    def getOthNodes( self ):
        """ Return a list of oth nodes.

            Arguments:
                None
            Output:
                A list of oth nodes.
        """

        if self.othNodes:
            return self.othNodes.keys()

        if not self.othNames:
            self.getOthNames(                                           )

        for id1 in self.othNames.values():
            nNodes  = self.adb.get(	        "nOthNodes",    id1	)
            for id3 in range(nNodes):
                nd  = self.adb.get(	        "othNode",      id1,id3 )
                self.othNodes[ nd ]         = id3
                self.othNodes[ str( nd ) ]  = id3

        return self.othNodes.keys()

#-------------------------------------------------------------------------
# "getOthVarNames": Return a list of oth variable names.
#-------------------------------------------------------------------------
   
    def getOthVarNames( self ):
        """ Return a list of oth variable names.

            Arguments:
                None
            Output:
                A list of oth variable names
        """

        if self.othVarNames:
            return self.othVarNames.keys()

        n   = self.adb.get( "nOthVars" )
        for indx in range( n ):
            name                     = self.adb.get( "othVarName",
                                                     indx               ) 
            self.othVarNames[ name ] = indx

        return self.othVarNames.keys()

#-------------------------------------------------------------------------
# "getOthNameIndx": Return the oth index.
#-------------------------------------------------------------------------        
       
    def getOthNameIndx( self, name ):
        """ Map the oth name into an index.

            Argument:
                name    - The oth name/index.

            Output:
                The mapped index.
        """
        
        if not self.othNames:
            self.getOthNames(                                           )

        if name in self.othNames:
            return self.othNames[ name ]
        elif name in self.othNames.values():
            return name
        else:
            return -1

#-------------------------------------------------------------------------
# "getOthSteps": Return the oth steps.
#-------------------------------------------------------------------------        
       
    def getOthSteps( self, name ):
        """ Return the acudb.othSteps.

            Argument:
                name    - The oth name.

            Output:
                The related oth steps values.
        """

        indx    = self.getOthNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get othSteps."

        return self.adb.get(        "othSteps",     indx                )

#-------------------------------------------------------------------------
# "getOthTimes": Return the oth times.
#-------------------------------------------------------------------------        
   
    def getOthTimes( self, name ):
        """ Return the acudb.othTimes.

            Argument:
                name    - The oth name.

            Output:
                The related oth times values.
        """

        indx    = self.getOthNameIndx(              name                )
        if indx == -1:
            raise AcuDbAssistError, "Invalid name/index to get othTimes."

        return self.adb.get(        "othTimes",     indx                )

#-------------------------------------------------------------------------
# "getOthValues": Return the oth values
#------------------------------------------------------------------------- 
    
    def getOthValues( self, name, node, var, unit = None  ):
        """ Return the acudb.othValues.

            Argument:
                name    - The oth name.
                var     - The oth variable name.
                unit    - The oth variable unit.

            Output:
                values  - The related oth variable values.
        """

        #----------------------------------------------------------------
        # Searching for name index
        #----------------------------------------------------------------

        id1         = self.getOthNameIndx(          name                )
        if id1 == -1:
            raise AcuDbAssistError, "Invalid name argument to get othValues."
        
        #----------------------------------------------------------------
        # Searching for variable index
        #----------------------------------------------------------------

        if not self.othVarNames:
            self.getOthVarNames(                                        )

        if var in self.othVarNames.values( ):
            id2     = var
        elif var in self.othVarNames:
            id2     = self.othVarNames[ var ]
        else:
            raise AcuDbAssistError, "Invalid var argument to get othValues"

        #----------------------------------------------------------------
        # Searching for node name index
        #----------------------------------------------------------------

        if not self.othNodes:
            self.getOthNodes(                                           )

        if node in self.othNodes.values( ):
            id3     = node
        elif node in self.othNodes:
            id3     = self.othNodes[ node ]
        else:
            raise AcuDbAssistError, "Invalid node argument to get othValues"

        #----------------------------------------------------------------
        # Return the acudb.othValues
        #----------------------------------------------------------------

        values      = self.adb.get( "othValues",    id1,    id2,    id3 )
        
        if unit != None:
            bsUnit  = self.getOthVarUnit(           var                 )
            values  = self.convert( values,         bsUnit,     unit    )

        return values
                
#-------------------------------------------------------------------------
# "getOthVarUnit" : Returns the SI unit of oth variable
#-------------------------------------------------------------------------
    
    def getOthVarUnit( self, name ):
        """ Returns the SI unit of the oth variable.
        
            Argument:
                name    - Varable name
            Output:
                unit    - SI unit
        """

        if not self.othVarNames:
            self.getOthVarNames(                                        )

        if name not in self.othVarNames:
            for k, v in self.othVarNames.items():
                if name == v:
                    name = k
                    break
                
        unit    = self.getVarUnit(      name,           "oth"           )
        if not unit:
            raise AcuDbAssistError, "Invalid variable name."
        return unit
            
#-------------------------------------------------------------------------
# "getVarUnit": returns the SI unit of adb variable
#-------------------------------------------------------------------------
    
    def getVarUnit( self, name, adbOut ):
        """ Returns the SI unit of the variable according to
            its adb name.
        
            Argument:
                name    - Varable name
                adbOut  - Related adb out name
            Output:
                unit    - SI unit
        """

        if name not in _adbUnit: return None

        unit            = None
        for item in _adbUnit[name]:
            if item[1] == 'all' or adbOut.lower() in item[1].split(','):
                if item[0] == "None":
                    unit= "nondim"
                else:
                    unit= acuUnit.getDefUnit(           item[0]         )
                    
                break
        return unit

#-------------------------------------------------------------------------
# "get": calls acudb get method
#-------------------------------------------------------------------------

    def get(self, name, indx = None, val = None):
        
        if indx == None and val == None:
            return self.adb.get(name)

        elif val == None:
            return self.adb.get(name, indx)

        else:
            return self.adb.get(name, indx, val)

#---------------------------------------------------------------------------
# "updateAdb": Update Adb variables
#---------------------------------------------------------------------------

    def updateAdb( self ):
        """ Update Adb variables.

            Arguments:
                None
            Output:
                None
        """
        adb             = self.adb        
	if self.initAdb and not adb.update(): return

	self.initAdb	= True
	events	        = adb.get(	        'logEvents'		)

	for i in xrange( events.shape[0] ):
            if events[i,0] == _EVENT_RES_RAT:
                indx    = int(                  events[i,1]             )
                name    = adb.get(              'logStr',       indx	)
                self.resNames[name] = indx
		    
	    elif events[i,0] == _EVENT_SOL_RAT:
                indx    = int(                  events[i,1]             )
                name    = adb.get(              'logStr',       indx	)
                self.solNames[name] = indx
	    
	    elif events[i,0] == _EVENT_STG_NAME:
                indx    = int(                  events[i,1]             )
                name    = adb.get(              'logStr',       indx	)
                self.iterNames[name]= indx

#---------------------------------------------------------------------------
# "adbGetEvent": Get the event data
#---------------------------------------------------------------------------

    def adbGetEvent( self, pars ):
        """ Get the event data.

            Arguments:
                pars    - Event info.
            Output:
                Event steps, times and values
        """
        
	( id1, id2, id3, flag ) = pars

	if id3 == 1:

	    e	= self.adb.get( 'logEvents' )
	    x	= []
	    y	= []
	    nx	= 0
	    ny	= 0
	    for j in range(e.shape[0]):
		if e[j,0] == id1 and e[j,1] == id2:
		    if ny <= nx:
			y.append( e[j,2] )
			ny	+= 1
		if e[j,0] == _EVENT_TS and nx < ny:
		    x.append( e[j,2] )
		    nx	+= 1

	elif id3 == 2:

	    e	= self.adb.get( 'logEvents' )
	    x	= []
	    y	= []
	    nx	= 0
	    ny	= 0
	    for j in range(e.shape[0]):
		if e[j,0] == id1 and e[j,1] == id2:
		    if ny <= nx:
			y.append( e[j,2] )
			ny	+= 1
		    else:
			y[-1]	= e[j,2]
		if e[j,0] == _EVENT_TS and nx < ny:
		    x.append( e[j,2] )
		    nx	+= 1

	elif id3 == 3:

	    e	= self.adb.get( 'logEvents' )
	    x	= []
	    y	= []
	    nx	= 0
	    ny	= 0
	    for j in range(e.shape[0]):
		if e[j,0] == id1 and e[j,1] == id2:
		    y.append( e[j,2] )
		    ny	+= 1
		if e[j,0] == _EVENT_TS and nx < ny:
		    n	= ny - nx
		    dx	= 1. / n
		    for i in range(1,n+1):
			x.append( e[j,2] - dx * (n-i) )
		    nx	+= n

	else:

	    e	= self.adb.get( 'logEvents' )
	    x	= self.adb.get( 'steps' )
	    y	= []
	    for j in range(e.shape[0]):
		if e[j,0] == id1 and e[j,1] == id2:
		    y.append( e[j,2] )

	if flag == 1:
	    y	= numarray.array( y, 'd' )
	    y	= numarray.maximum( y, 1.e-20 )

        steps   = self.adb.get( 'steps' )
        times   = self.adb.get( 'times' )
        tIncs   = self.adb.get( 'timeIncs' )
        nSteps  = len( steps )
        xt      = []
        i       = 0
        for j in range(len(x)):
            while i < nSteps and steps[i] < x[j]:
                i += 1
            t   = times[i] + (x[j] - steps[i]) * tIncs[i]
            xt.append( t )
            
	x  	= numarray.array( x  ).flat
	xt  	= numarray.array( xt ).flat
	y   	= numarray.array( y  ).flat
        return( x, xt, y )

#-------------------------------------------------------------------------
# "getSteps": Return the "Run Data" steps.
#-------------------------------------------------------------------------        
       
    def getSteps( self ):
        """ Return the "Run Data" steps value.

            Argument:
                None
            Output:
                The related steps values.
        """

        return self.adb.get(                    'steps'                 )

#-------------------------------------------------------------------------
# "getTimes": Return the "Run Data" times.
#-------------------------------------------------------------------------        
       
    def getTimes( self ):
        """ Return the "Run Data" times value.

            Argument:
                None
            Output:
                The related times values.
        """

        pars	= (     _EVENT_TIME,        0,      0,          0       )
        values  = self.adbGetEvent(                 pars                )
        return values[2]

#-------------------------------------------------------------------------
# "getTimeIncs": Return the "Run Data" Time Increment.
#-------------------------------------------------------------------------        
       
    def getTimeIncs( self ):
        """ Return the "Time Increment" value.

            Argument:
                None
            Output:
                The related "Time Increment" values.
        """

        pars	= (     _EVENT_TIMEINC,     0,      0,          0       )
        values  = self.adbGetEvent(                 pars                )
        return values[2]

#-------------------------------------------------------------------------
# "getCpuTimes": Return the "Run Data" CPU Time.
#-------------------------------------------------------------------------        
       
    def getCpuTimes( self ):
        """ Return the "Run Data" CPU Time value.

            Argument:
                None
            Output:
                The "CPU Time" values.
        """

        pars	= (     _EVENT_CPU_TIME,    0,      0,          0       )
        values  = self.adbGetEvent(                 pars                )
        return values[2]

#-------------------------------------------------------------------------
# "getElapseTimes": Return the "Run Data" getElapseTimes.
#-------------------------------------------------------------------------        
       
    def getElapseTimes( self ):
        """ Return the "Run Data" Elapsed Time value.

            Argument:
                None
            Output:
                The "Elapsed Time" values.
        """

        pars	= (     _EVENT_ELAPSED_TIME,0,      0,          0       )
        values  = self.adbGetEvent(                 pars                )
        return values[2]

#-------------------------------------------------------------------------
# "getVarNames":  Return a list of "Residual Ratio" variable names.
#-------------------------------------------------------------------------
   
    def getResRatioVarNames( self ):
        """ Return a list of "Residual Ratio" variable names.

            Arguments:
                None
            Output:
                A list of "Residual Ratio" variable names
        """

        self.updateAdb(                                                 )

        return self.resNames.keys()

#-------------------------------------------------------------------------
# "getResRatioVarIndx": Return the "Residual Ratio" variable index.
#-------------------------------------------------------------------------        
       
    def getResRatioVarIndx( self, var ):
        """ Map the "Residual Ratio" variable into an index.

            Argument:
                name    - The "Residual Ratio" variable name/index.

            Output:
                The mapped index.
        """
        
        self.updateAdb(                                                 )

        if var in self.resNames:
            return self.resNames[ var ]
        elif var in self.resNames.values():
            return var
        else:
            return -1

#-------------------------------------------------------------------------
# "getResRatioData": Return the "Residual Ratio" data.
#-------------------------------------------------------------------------        
       
    def getResRatioData( self, var, type = "all" ):
        """ Return the "Residual Ratio" steps, times and values data.

            Argument:
                var     - The "Residual Ratio" variable name/index
                type    - The type value; 'all', 'initial' and 'final'
            Output:
                The "Residual Ratio" data.
        """

        indx    = self.getResRatioVarIndx(          var                 )
        if indx == -1:
            raise AcuDbAssistError, "Invalid variable name."

        typeIndx= self.ratioType[type.lower()]
        pars	= (     _EVENT_RES_RAT,     indx,   typeIndx,   1       )

        return self.adbGetEvent(                    pars                )

#-------------------------------------------------------------------------
# "getResRatioSteps": Return the "Residual Ratio" steps.
#-------------------------------------------------------------------------        
       
    def getResRatioSteps( self, var, type = "all" ):
        """ Return the "Residual Ratio" steps value.

            Argument:
                var     - The "Residual Ratio" variable name/index
                type    - The type value; 'all', 'initial' and 'final'
            Output:
                The related steps values.
        """

        values  = self.getResRatioData(     var,    type                )
        return values[0]

#-------------------------------------------------------------------------
# "getResRatioTimes": Return the "Residual Ratio" times.
#-------------------------------------------------------------------------        
       
    def getResRatioTimes( self, var, type = "all" ):
        """ Return the "Residual Ratio" times value.

            Argument:
                var     - The "Residual Ratio" variable name/index
                type    - The type value; 'all', 'initial' and 'final'
            Output:
                The related times values.
        """

        values  = self.getResRatioData(     var,    type                )
        return values[1]

#-------------------------------------------------------------------------
# "getResRatioValues": Return the "Residual Ratio" values.
#-------------------------------------------------------------------------        
       
    def getResRatioValues( self, var, type = "all", unit = None ):
        """ Return the related "Residual Ratio" values.

            Argument:
                var     - The "Residual Ratio" variable name/index
                type    - The type value; 'all', 'initial' and 'final'
                unit    - The variable unit.
            Output:
                The related "Residual Ratio" values.
        """

        values  = self.getResRatioData(     var,    type            )[2]
    
        if unit != None:
            bsUnit  = self.getResRatioVarUnit(      var                 )
            values  = self.convert( values,         bsUnit,     unit    )
            
        return values

#-------------------------------------------------------------------------
# "getResRatioVarUnit" : Returns the SI unit of Residual Ratio variable
#-------------------------------------------------------------------------
    
    def getResRatioVarUnit( self, name ):
        """ Returns the SI unit of the "Residual Ratio" variable.
        
            Argument:
                name    - Varable name
            Output:
                unit    - SI unit
        """

        if not self.resNames:
            self.updateAdb(                                             )

        if name not in self.resNames:
            for k, v in self.resNames.items():
                if name == v:
                    name = k
                    break
                
        unit    = self.getVarUnit(      name,               "all"       )
        if not unit:
            raise AcuDbAssistError, "Invalid variable name."
        return unit

#-------------------------------------------------------------------------
# "getVarNames": Return a list of "Solution Ratio" variable names.
#-------------------------------------------------------------------------
   
    def getSolRatioVarNames( self ):
        """ Return a list of "Solution Ratio" variable names.

            Arguments:
                None
            Output:
                A list of "Solution Ratio" variable names
        """

        self.updateAdb(                                                 )

        return self.solNames.keys()

#-------------------------------------------------------------------------
# "getSolRatioVarIndx": Return the "Solution Ratio" variable index.
#-------------------------------------------------------------------------        
       
    def getSolRatioVarIndx( self, var ):
        """ Map the "Solution Ratio" variable into an index.

            Argument:
                name    - The "Solution Ratio" variable name/index.

            Output:
                The mapped index.
        """
        
        self.updateAdb(                                                 )

        if var in self.solNames:
            return self.solNames[ var ]
        elif var in self.solNames.values():
            return var
        else:
            return -1

#-------------------------------------------------------------------------
# "getSolRatioData": Return the "Solution Ratio" data.
#-------------------------------------------------------------------------        
       
    def getSolRatioData( self, var, type = "all" ):
        """ Return the "Solution Ratio" steps, times and values data.

            Argument:
                var     - The "Solution Ratio" variable name/index
                type    - The type value; 'all', 'initial' and 'final'
            Output:
                The "Solution Ratio" data.
        """

        indx    = self.getSolRatioVarIndx(          var                 )
        if indx == -1:
            raise AcuDbAssistError, "Invalid variable name."

        typeIndx= self.ratioType[type.lower()]
        pars	= (     _EVENT_SOL_RAT,     indx,   typeIndx,   1       )

        return self.adbGetEvent(                    pars                )

#-------------------------------------------------------------------------
# "getSolRatioSteps": Return the "Solution Ratio" steps.
#-------------------------------------------------------------------------        
       
    def getSolRatioSteps( self, var, type = "all" ):
        """ Return the "Solution Ratio" steps value.

            Argument:
                var     - The "Solution Ratio" variable name/index
                type    - The type value; 'all', 'initial' and 'final'
            Output:
                The related steps values.
        """

        values  = self.getSolRatioData(     var,    type                )
        return values[0]

#-------------------------------------------------------------------------
# "getSolRatioTimes": Return the "Solution Ratio" times.
#-------------------------------------------------------------------------        
       
    def getSolRatioTimes( self, var, type = "all" ):
        """ Return the "Solution Ratio" times value.

            Argument:
                var     - The "Solution Ratio" variable name/index
                type    - The type value; 'all', 'initial' and 'final'
            Output:
                The related times values.
        """

        values  = self.getSolRatioData(     var,    type                )
        return values[1]

#-------------------------------------------------------------------------
# "getSolRatioValues": Return the "Solution Ratio" values.
#-------------------------------------------------------------------------        
       
    def getSolRatioValues( self, var, type = "all", unit = None ):
        """ Return the related "Solution Ratio" values.

            Argument:
                var     - The "Solution Ratio" variable name/index
                type    - The type value; 'all', 'initial' and 'final'
                unit    - The variable unit.
            Output:
                The related "Solution Ratio" values.
        """

        values  = self.getSolRatioData(     var,    type            )[2]
    
        if unit != None:
            bsUnit  = self.getSolRatioVarUnit(      var                 )
            values  = self.convert( values,         bsUnit,     unit    )
            
        return values

#-------------------------------------------------------------------------
# "getSolRatioVarUnit" : Returns the SI unit of Solution Ratio variable
#-------------------------------------------------------------------------
    
    def getSolRatioVarUnit( self, name ):
        """ Returns the SI unit of the "Solution Ratio" variable.
        
            Argument:
                name    - Varable name
            Output:
                unit    - SI unit
        """

        if not self.solNames:
            self.updateAdb(                                             )

        if name not in self.solNames:
            for k, v in self.solNames.items():
                if name == v:
                    name = k
                    break
                
        unit    = self.getVarUnit(      name,               "all"       )
        if not unit:
            raise AcuDbAssistError, "Invalid variable name."
        return unit

#-------------------------------------------------------------------------
# "getLinIterVarNames": Return a list of "Linear Iterations" variable names.
#-------------------------------------------------------------------------
   
    def getLinIterVarNames( self ):
        """ Return a list of "Linear Iterations" variable names.

            Arguments:
                None
            Output:
                A list of "Solution Ratio" variable names
        """

        self.updateAdb(                                                 )

        return self.iterNames.keys()

#-------------------------------------------------------------------------
# "getLinIterVarIndx": Return the "Linear Iterations" variable index.
#-------------------------------------------------------------------------        
       
    def getLinIterVarIndx( self, var ):
        """ Map the "Linear Iterations" variable into an index.

            Argument:
                name    - The "Linear Iterations" variable name/index.

            Output:
                The mapped index.
        """
        
        self.updateAdb(                                                 )

        if var in self.iterNames:
            return self.iterNames[ var ]
        elif var in self.iterNames.values():
            return var
        else:
            return -1

#-------------------------------------------------------------------------
# "getLinIterData": Return the "Linear Iterations" data.
#-------------------------------------------------------------------------        
       
    def getLinIterData( self, var, index = 0 ):
        """ Return the "Linear Iterations" steps, times and values data.

            Argument:
                var     - The "Linear Iterations" variable name/index
                index   - The index of nIters
            Output:
                The "Linear Iterations" data.
        """

        varIndx = self.getLinIterVarIndx(           var                 )
        if varIndx == -1:
            raise AcuDbAssistError, "Invalid variable name."

        e	= self.adb.get(                     'logEvents'         )
        x	= []
        y	= []
        nx	= 0
        ny      = 0
        stagId  = None
        
        for j in xrange( e.shape[0] ):
            if e[j,0] == _EVENT_STG_NAME and e[j,1] == varIndx:
                stagId = 0

            elif e[j,0] == _EVENT_N_ITERS and stagId != None:
                if index == stagId:
                    y.append( e[j,2] )
                    ny	+= 1

                stagId += 1

	    elif e[j,0] == _EVENT_TS and nx < ny:
		n	= ny - nx
		dx	= 1. / n
		for i in range(1,n+1):
		    x.append( e[j,2] - dx * (n-i) )
		nx	+= n

        steps   = self.adb.get(                     'steps'             )
        times   = self.adb.get(                     'times'             )
        tIncs   = self.adb.get(                     'timeIncs'          )
        nSteps  = len(                              steps               )
        xt      = []
        i       = 0
        for j in xrange( len(x) ):
            while i < nSteps and steps[i] < x[j]:
                i += 1
            t   = times[i] + (x[j] - steps[i]) * tIncs[i]
            xt.append( t )
            
	x  	= numarray.array( x  ).flat
	xt  	= numarray.array( xt ).flat
	y   	= numarray.array( y  ).flat
        return ( x, xt, y )
                    
#-------------------------------------------------------------------------
# "getLinIterSteps": Return the "Linear Iterations" steps.
#-------------------------------------------------------------------------        
       
    def getLinIterSteps( self, var, index = 0 ):
        """ Return the "Linear Iterations" steps value.

            Argument:
                var     - The "Linear Iterations" variable name/index
                index   - The "Linear Iterations" index
            Output:
                The related steps values.
        """

        values  = self.getLinIterData(      var,    index               )
        return values[0]

#-------------------------------------------------------------------------
# "getLinIterTimes": Return the "Linear Iterations" times.
#-------------------------------------------------------------------------        
       
    def getLinIterTimes( self, var, index = 0 ):
        """ Return the "Linear Iterations" times value.

            Argument:
                var     - The "Solution Ratio" variable name/index
                index   - The "Linear Iterations" index
            Output:
                The related times values.
        """

        values  = self.getLinIterData(      var,    index               )
        return values[1]

#-------------------------------------------------------------------------
# "getLinIterValues": Return the "Linear Iterations" values.
#-------------------------------------------------------------------------        
       
    def getLinIterValues( self, var, index = 0 ):
        """ Return the related "Linear Iterations" values.

            Argument:
                var     - The "Linear Iterations" variable name/index
                index   - The "Linear Iterations" index
            Output:
                The related "Linear Iterations" values.
        """

        values  = self.getLinIterData(      var,    index               )
        return values[2]

#---------------------------------------------------------------------------
# convert : Convert the value from one unit to another.
#---------------------------------------------------------------------------

    def convert( self, values, unit, toUnit ):
        """ Convert the value from one unit to another.

            Arguments:
                values      - value to convert from (eg., 100 )
                unit        - from unit (eg., 'm')
                toUnit      - to unit (eg., 'cm')
            Return:
                Converted values (eg., 1.e+2)
        """

        if unit == toUnit: return values

        #-----------------------------------------------------------------
        # Check for unit validity 
        #-----------------------------------------------------------------

        if unit != acuUnit.getBaseUnit( toUnit ):
            raise AcuDbAssistError, "Invalid unit argument to get adbValues."
        
        #-----------------------------------------------------------------
        # Convert base unit to given unit
        #-----------------------------------------------------------------

        return self.cnvValues(      values,         unit,       toUnit  )

#---------------------------------------------------------------------------
# cnvValues : Convert values
#---------------------------------------------------------------------------

    def cnvValues( self, values, unit, toUnit ):
        """ Convert the value from one unit to another using acuUnit.

            Arguments:
                values      - value to convert from (eg., 100 )
                unit        - from unit (eg., 'm')
                toUnit      - to unit (eg., 'cm')
            Return:
                Converted values (eg., 1.e+2)
        """

        if type( values ) == types.IntType or \
           type( values ) == types.FloatType:
            return  acuUnit.convert(    values,     unit,       toUnit  )

        else:
            for i in xrange( values.shape[0] ):
                values[i]   = self.cnvValues(       values[i],   unit,
                                                    toUnit              )
            return values

#=========================================================================
#
# Test the code
#
#=========================================================================

if __name__ == '__main__':
    problemName = "slosh"
    dirName = "ACUSIM.DIR"
    runId = 1
    adb = AcuDbAssist( problemName , dirName , runId )
    print

##    pars	= ( _EVENT_TIME, 0, 0, 0 )
##    print adb.adbGetEvent( pars )[1]
##    print
##
##    pars	= ( _EVENT_TIMEINC, 0, 0, 0 )
##    print adb.adbGetEvent( pars )[1]
##
##    print
##
##    pars	= ( _EVENT_CPU_TIME, 0, 0, 0 )
##    print adb.adbGetEvent( pars )[1]
##    print
##
##    pars	= ( _EVENT_ELAPSED_TIME, 0, 0, 0 )
##    print adb.adbGetEvent( pars )[1]
##
##    print
##    print


##    print adb.adb.get(      'steps'         )
##    print adb.adb.get(      'times'         )
##    print adb.adb.get(      'timeIncs'         )
##
##    adb.getOthNodes()
##    adb.getOthVarNames()
##    print adb.othNames
##    print adb.othNodes
##    print adb.othVarNames
##    print
##    print adb.getOthSteps( 0 )
##    print adb.getOthTimes( "top nodes" )
##    print adb.getOthVarUnit( "pressure" )
##    print adb.getOthVarUnit( "time_step" )
##    print adb.getOthVarUnit( "mesh_velocity" )
##    try:
##        print adb.getOthVarUnit( "species_flux" )
##    except:
##        print "Error"
##
##    try:
##        print adb.getOthVarUnit( "species_ggggflux" )
##    except:
##        print "Error"
##    print "*" * 20
##    print adb.getOthValues( 0, 1, 3 )
##    print "-" * 20
    print adb.getOthValues( "top nodes", "23", "mesh_velocity", "cm/sec")

