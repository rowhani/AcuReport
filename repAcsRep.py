#---------------------------------------------------------------------------
# get the modules
#---------------------------------------------------------------------------

import 	acuReport
import 	repAcs 	

#===========================================================================
#
# "RepAcsRep":  Transfer AcuConsole data base data to AcuReport
#
#===========================================================================

class RepAcsRep:

    """Transfer AcuConsole data base data to AcuReport."""

#---------------------------------------------------------------------------
# Initialize
#---------------------------------------------------------------------------

    def __init__( self, report, acs ):

        """
	Create a RepAcs instance

        Argument:		
            report  - AcuReport object
	    acs	    - RepAcs object
			
        """
        self.rep    =   report
	self.acs    =   acs

#---------------------------------------------------------------------------
# "getPrbDesc": Get the problem description and equations
#---------------------------------------------------------------------------

    def getPrbDesc(self):

        nodeAss	= repAcs.ROOT + repAcs.RS + 'AUTO_SOLUTION_STRATEGY'
        nodeAna	= repAcs.ROOT + repAcs.RS + 'ANALYSIS'
        nodeEqn	= repAcs.ROOT + repAcs.RS + 'EQUATION'

        mode	= self.acs.getEnum(	path=nodeAna,
                                        par='type'                       )
        flow	= self.acs.getEnum(	path=nodeEqn,
                                        par='flow'		         )
        temp	= self.acs.getEnum(	path=nodeEqn,
                                        par='temperature'	         )
        rad		= 'none'
        if temp == 'advective_diffusive':
            rad	= self.acs.getEnum(	path=nodeEqn,
                                        par='radiation'		         )

        spec	= self.acs.getEnum(	path=nodeEqn,
                                        par='species_transport'	         )
        nSpecs	= self.acs.getInt(	path=nodeEqn,
                                        par='num_species'	         )
        if spec == "none": nSpecs = 0

        turb	= self.acs.getEnum(	path=nodeEqn,
                                        par='turbulence'	         )
        mesh	= self.acs.getEnum(	path=nodeEqn,
                                        par='mesh'		         )
        ext         = self.acs.getBool(	path=nodeEqn,
                                        par='external_code'              )

        return (mode,flow,temp,rad,spec,nSpecs,turb,mesh,ext             )

#---------------------------------------------------------------------------
# "outToFile()":   Return the formatted version of name-value pair
#---------------------------------------------------------------------------

    def outToFile(self, name, value):

        """Return the formatted version of name-value pair."""

        '''
        outToFile(name, value)

        Argument:
            name    - parameter name
            value   - parameter value

        Retruns:
            formatted name-value pair
        '''

        return '%s = %s' % ( name.replace("_", " ").capitalize(),
                         str(value).replace("_", " ").capitalize()       )

#---------------------------------------------------------------------------
# "outPar()":   Return the formatted version of parameter name-value pair
#---------------------------------------------------------------------------

    def outPar(self, path, par):

        """Return the formatted version of parameter name-value pair."""

        '''
        outPar(path, par)

        Argument:
            path    - parameter path
            par     - parameter name

        Retruns:
            formatted parameter name-value pair
        '''

        return  self.outToFile( par,
                      self.acs.getPar( par, path,
                                       self.acs.getType(par, path) )     )

#----------------------------------------------------------------------------
# "addMaterialModel()": writes out the material model data in the report.
#----------------------------------------------------------------------------

    def addMaterialModel( self, name ):

        """
        Writes out the material model data in the report document.

        Argument:

            name        - The material model name.
                          valid: Air, Aluminum, and Water

        Return:

            None

        """

        nodeMat     = repAcs.ROOT + repAcs.RS + 'MATERIAL_MODEL' \
                      + repAcs.RS + name

        (mode,flow,temp,rad,spec,nSpecs,turb,mesh,ext)=self.getPrbDesc(  )
        parts	= self.acs.getChildNodes( nodeMat                        )
	medium	= self.acs.getEnum(	path=nodeMat,	par='medium'     )


        self.rep.addText("Material Model for Fluid " + repr(name)        )
        self.rep.beginBullet(                                            )

        #---- Density Model
        if 'DENSITY_MODEL' in parts:
            nodeDens    = nodeMat + repAcs.RS + 'DENSITY_MODEL'
            type     = self.acs.getEnum(         "type",  nodeDens       )

            self.rep.addItem("", "Density Model"                         )
            self.rep.beginBullet(                                        )
            self.rep.addItem("",  self.outToFile("type", type)           )

            if type == 'boussinesq' or type == 'constant' or type == 'isentropic':
                self.rep.addItem("",  self.outPar( nodeDens, 'density')  )
            if type == 'boussinesq':
                self.rep.addItem("",  self.outPar( nodeDens,
                                                   'expansivity_type'   ))
                self.rep.addItem("",  self.outPar( nodeDens,
                                                'reference_temperature' ))
                self.rep.addItem("",  self.outPar( nodeDens,
                                                   'expansivity'        ))

            if type == 'isentropic':
                self.rep.addItem("",  self.outPar( nodeDens,
                                                   'reference_pressure' ))
                self.rep.addItem("",  self.outPar( nodeDens,
                                                   'specific_heat_ratio'))
            if type == 'ideal_gas':
                self.rep.addItem("",  self.outPar( nodeDens,
                                                   'gas_constant'       ))
            self.rep.addItem("",  self.outPar( nodeDens,
                                            'isothermal_compressibility'))
            if type == 'piecewise_linear' or type == 'cubic_spline' :
                self.rep.addItem("",  self.outPar( nodeDens,
                                                   'curve_fit_values'   ))
                self.rep.addItem("",  self.outPar( nodeDens,
                                                   'curve_fit_variable' ))
            if type == 'user_function':
                self.rep.addItem("",  self.outPar( nodeDens,
                                                   'user_function'      ))
                self.rep.addItem("",  self.outPar( nodeDens,
                                                   'user_values'        ))
                self.rep.addItem("",  self.outPar( nodeDens,
                                                   'user_strings'       ))

            self.rep.endBullet(                                          )


        #---- Viscosity Model
        if medium == 'fluid' and 'VISCOSITY_MODEL' in parts:
            nodeVisc = nodeMat + repAcs.RS + 'VISCOSITY_MODEL'
            type     = self.acs.getEnum(         "type",  nodeVisc       )

            self.rep.addItem("", "Viscosity Model"                       )
            self.rep.beginBullet(                                        )
            self.rep.addItem("",  self.outToFile("type", type)           )

            if type == 'constant' or type == 'ramped':
                self.rep.addItem("",
                                 self.outPar(  nodeVisc,   'viscosity'  ))

            if type == 'power_law' :
                self.rep.addItem("",
                                 self.outPar(nodeVisc,
                                             'power_law_viscosity'      ))
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                              'power_law_time_constant' ))
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                              'power_law_index'         ))
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                        'power_law_lower_strain_rate'   ))

            if type == 'bingham' :
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                              'bingham_viscosity'       ))
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                              'bingham_yield_stress'    ))
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                        'bingham_stress_growth_exponent'))
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                              'bingham_time_constant'   ))
                self.rep.addItem("",
                                 self.outPar( nodeVisc, 'bingham_index' ))

            if type == 'carreau' :
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                        'carreau_zero_shear_viscosity'  ))
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                    'carreau_infinite_shear_viscosity'  ))
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                              'carreau_time_constant'   ))
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                              'carreau_index'           ))
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                              'carreau_transition_index'))

            if type == 'piecewise_linear' or type == 'cubic_spline' :
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                              'curve_fit_values'        ))
                self.rep.addItem("",
                                 self.outPar( nodeVisc,
                                              'curve_fit_variable'      ))

            if type == 'user_function':
                self.rep.addItem("",
                                 self.outPar( nodeVisc, 'user_function' ))
                self.rep.addItem("",
                                 self.outPar( nodeVisc, 'user_values'   ))
                self.rep.addItem("",
                                 self.outPar( nodeVisc, 'user_strings'  ))

            self.rep.addItem("",
                             self.outPar( nodeVisc,
                                          'multiplier_function'         ))

            self.rep.endBullet(                                          )


        #---- Specific Heat Model
        if temp != 'none' and 'SPECIFIC_HEAT_MODEL' in parts:
            nodeCpm = nodeMat + repAcs.RS + 'SPECIFIC_HEAT_MODEL'
            type      = self.acs.getEnum(         "type",  nodeCpm       )

            self.rep.addItem("", "Specific Heat Model"                   )
            self.rep.beginBullet(                                        )
            self.rep.addItem("",  self.outToFile("type", type)           )

            if type == 'constant':
                self.rep.addItem("",
                                 self.outPar(   nodeCpm,
                                                'specific_heat'         ))

            if type == 'piecewise_linear_enthalpy' or \
               type == 'cubic_spline_enthalpy' :
                self.rep.addItem("",
                                 self.outPar( nodeCpm,
                                                   'curve_fit_values'   ))
                self.rep.addItem("",
                                 self.outPar( nodeCpm,
                                                   'curve_fit_variable' ))

            if type == 'user_function_enthalpy':
                self.rep.addItem("",
                             self.outPar( nodeCpm,
                                          'user_function'               ))
                self.rep.addItem("",
                             self.outPar( nodeCpm,
                                          'user_values'                 ))
                self.rep.addItem("",
                             self.outPar( nodeCpm,
                                          'user_strings'                ))

            self.rep.addItem("",
                         self.outPar(     nodeCpm,
                                          'latent_heat_type'            ))

            LatentHeatType	= self.acs.getEnum(	path=nodeCpm,
                                            par='latent_heat_type'       )

            if LatentHeatType   == 'constant' :
                self.rep.addItem("",
                             self.outPar( nodeCpm,
                                          'latent_heat'                 ))
                self.rep.addItem("",
                             self.outPar( nodeCpm,
                                          'latent_heat_temperature'     ))
                self.rep.addItem("",
                             self.outPar( nodeCpm,
                                    'latent_heat_temperature_interval'  ))

            self.rep.endBullet(                                          )


        #---- Conductivity Model
        if temp != 'none' and 'CONDUCTIVITY_MODEL' in parts:
            nodeCond = nodeMat + repAcs.RS + 'CONDUCTIVITY_MODEL'
            type     = self.acs.getEnum(         "type",  nodeCond       )
            medium   = self.acs.getEnum(         "medium",  nodeMat      )

            self.rep.addItem("", "Conductivity Model"                    )
            self.rep.beginBullet(                                        )
            self.rep.addItem("",  self.outToFile("type", type)           )

            if type == 'constant' or type == 'ramped':
                self.rep.addItem("",
                                 self.outPar(	nodeCond,
                                                    'conductivity'	))

            if type == 'constant_prandtl_number' :
                self.rep.addItem("",
                                 self.outPar( nodeCond,
                                              'prandtl_number'          ))

            if type == 'piecewise_linear' or type == 'cubic_spline' :
                self.rep.addItem("",
                                 self.outPar( nodeCond,
                                              'curve_fit_values'        ))
                self.rep.addItem("",
                                 self.outPar( nodeCond,
                                              'curve_fit_variable'      ))

            if type == 'user_function':
                self.rep.addItem("",
                                 self.outPar( nodeCond,
                                              'user_function'           ))
                self.rep.addItem("",
                                 self.outPar( nodeCond, 'user_values'   ))
                self.rep.addItem("",
                                 self.outPar( nodeCond, 'user_strings'  ))

            self.rep.addItem("",
                             self.outPar(     nodeCond,
                                              'multiplier_function'     ))
            if medium != 'solid':
                self.rep.addItem("",
                                 self.outPar(     nodeCond,
                                            'turbulent_prandtl_number'  ))

            self.rep.endBullet(                                          )


        #---- Diffusivity Model
        if spec != "none":
	    for i in range(nSpecs):
	        diffId	= "%d" % (i+1)
	        diff	= 'DIFFUSIVITY_' + diffId + '_MODEL'
	        if medium == 'fluid' and diff in parts:
                    nodeDiff = nodeMat + repAcs.RS + diff
                    diffName	= 'species ' + diffId + ': ' + name
                    type = selg.acs.getEnum(  path=nodeDiff,  par='type' )

                    self.rep.addItem("", "Diffusivity Model ( " +
                                     diffName + " )"                     )
                    self.rep.beginBullet(                                )
                    self.rep.addItem("",  self.outToFile("type", type)   )

                    if type == 'constant' or type == 'ramped':
                        self.rep.addItem("",
                                 self.OutPar(	nodeDiff, 'diffusivity'	))

                    if type == 'piecewise_linear' or type == 'cubic_spline' :
                        self.rep.addItem("",
                                 self.OutPar( nodeDiff,
                                              'curve_fit_values'        ))
                        self.rep.addItem("",
                                 self.OutPar( nodeDiff,
                                              'curve_fit_variable'      ))

                    if type == 'user_function':
                        self.rep.addItem("",
                                 self.OutPar( nodeDiff, 'user_function' ))
                        self.rep.addItem("",
                                 self.OutPar( nodeDiff, 'user_values'   ))
                        self.rep.addItem("",
                                 self.OutPar( nodeDiff, 'user_strings'  ))

                    self.rep.addItem("",
                                 self.OutPar(nodeDiff,
                                             'multiplier_function'      ))
                    self.rep.addItem("",
                                 self.OutPar(nodeDiff,
                                             'turbulent_schmidt_number' ))


        #---- Porosity Model
        if medium == 'fluid' and 'POROSITY_MODEL' in parts:
            nodePoros = nodeMat + repAcs.RS + 'POROSITY_MODEL'
            type      = self.acs.getEnum(         "type",  nodePoros     )

            if type == 'constant':
                self.rep.addItem("", "Porosity Model"                    )
                self.rep.beginBullet(                                    )
                self.rep.addItem("",  self.outToFile("type", type)       )

                self.rep.addItem("",
                                 self.outPar( nodePoros,   'porosity'   ))
                self.rep.addItem("",
                                 self.outPar( nodePoros,'permeability'  ))
                self.rep.addItem("",
                                 self.outPar( nodePoros,
                                               'permeability_direction' ))
                self.rep.addItem("",
                                 self.outPar( nodePoros,
                                               'darcy_coefficient'      ))
                self.rep.addItem("",
                                 self.outPar( nodePoros,
                                            'darcy_multiplier_function' ))
                self.rep.addItem("",
                                 self.outPar( nodePoros,
                                              'forchheimer_coefficient' ))
                self.rep.addItem("",
                                 self.outPar( nodePoros,
                                    'forchheimer_multiplier_function'   ))

                self.rep.endBullet(                                      )


       # Add the ending bullet
        self.rep.endBullet(                                              )

#----------------------------------------------------------------------------
# "addSimpleBC()": Writes out the simple boundary condition data.
#----------------------------------------------------------------------------

    def addSimpleBC( self, name ):

        """
        Writes out the simple boundary condition data in the report document.

        Argument:

            name        - The simple BC model name.

        Return:

            None

        """

        modelSrf    = repAcs.ROOT + repAcs.RS + "Model" \
                      + repAcs.RS + "Surfaces"
        nodeCbc	    = modelSrf + repAcs.RS + name + repAcs.RS + \
                      'SIMPLE_BOUNDARY_CONDITION'

        inflowType  = 'False'
        tempType    = 'False'
        turWallType = 'False'
        meshDispType= 'False'
        temp        = 'none'
        flow        = 'none'
        doTmf       = False
        type	    = self.acs.getEnum(      "type", nodeCbc		 )

        active	= self.acs.getBool(      "active", nodeCbc               )
        if not active:
            return

        self.rep.addText("Simple Boundary Condition for " + repr(name)   )
        self.rep.beginBullet(                                            )

        self.rep.addItem("",  self.outPar(	    nodeCbc,    "type"	))

        if type == 'inflow':
            self.rep.addItem("",  self.outPar(  nodeCbc,'inflow_type'	))
            inflowType  = self.acs.getEnum(  path=nodeCbc,
                                             par='inflow_type'           )

        backFlow    = False
        if type == 'outflow':
            self.rep.addItem("",  self.outPar(nodeCbc,
                                              'back_flow_conditions'    ))
            backFlow = self.acs.getBool(	path=nodeCbc,
                                        par='back_flow_conditions'       )

        self.rep.addItem("",  self.outPar(	nodeCbc, 'active_type'	))
        self.rep.addItem("",  self.outPar(	nodeCbc,'precedence'	))

        if type != 'free_surface' and type != 'outflow':
            self.rep.addItem("",  self.outPar(   nodeCbc,
                                                 'reference_frame'	))

        velocityType = None

        if type == 'inflow' and inflowType == 'velocity':
            self.rep.addItem("",  self.outPar(nodeCbc,
                                              'inflow_velocity_type'    ))
            inflowVelocityType= self.acs.getEnum( path=nodeCbc,
                                              par='inflow_velocity_type' )
            velocityType = inflowVelocityType

        if type == 'wall':
            self.rep.addItem("",  self.outPar(   nodeCbc,
                                                 'wall_velocity_type'   ))
            wallVelocityType= self.acs.getEnum(	path=nodeCbc,
                                                par='wall_velocity_type' )
            velocityType = wallVelocityType

        # Output mass_flux data in the SIMPLE_BOUNDARY_CONDITION command
        if type == 'inflow' and inflowType == 'mass_flux':
            self.rep.addItem("",  self.outPar(   nodeCbc,    'mass_flux'))
            if doTmf:
                self.rep.addItem("",  self.outPar(	nodeCbc,
                    'mass_flux_multiplier_function'                     ))

        # Output flow_rate data in the SIMPLE_BOUNDARY_CONDITION command
        if type == 'inflow' and inflowType == 'flow_rate':
            self.rep.addItem("",  self.outPar(	nodeCbc,    'flow_rate' ))
            if doTmf:
                self.rep.addItem("",  self.outPar(	nodeCbc,
                    'flow_rate_multiplier_function'                     ))

        if type == 'outflow' or \
           ( type == 'inflow' and ( flow != "none" and \
                                inflowType == 'pressure' )):
            self.rep.addItem("",  self.outPar(   nodeCbc,   'pressure'  ))
            if doTmf:
                self.rep.addItem("",  self.outPar(	nodeCbc,
                                        'pressure_multiplier_function'  ))
            self.rep.addItem("",  self.outPar(nodeCbc,
                                              'pressure_loss_factor'	))

        if type == 'outflow' or \
           ( type == 'inflow'  and (inflowType == 'pressure' or \
            inflowType == 'stagnation_pressure' and flow != "none")):
            self.rep.addItem("",  self.outPar(nodeCbc,
                                              'hydrostatic_pressure'    ))

            if self.acs.getBool(     path=nodeCbc, par='hydrostatic_pressure'):
                self.rep.addItem("",  self.outPar( nodeCbc,
                                        'hydrostatic_pressure_origin'   ))

        if type == 'inflow' and ( flow != "none" and \
            inflowType == 'stagnation_pressure'):
            self.rep.addItem("",  self.outPar(nodeCbc,
                                              'stagnation_pressure'     ))
            if doTmf:
                self.rep.addItem("",  self.outPar(	nodeCbc,
                        'stagnation_pressure_multiplier_function'       ))

        if type == 'wall':
            self.rep.addItem("",  self.outPar(  nodeCbc,
                                                'temperature_type'      ))

            tempType = self.acs.getEnum(path=nodeCbc,
                                        par='temperature_type'           )

        if ( type == 'inflow' and temp != "none" ) or ( type == 'outflow' and \
           ( backFlow and temp != "none")) or \
           ( type == 'wall' and ( temp != "none" and tempType == 'value')):
            self.rep.addItem("",  self.outPar(   nodeCbc, 'temperature' ))
            if doTmf:
                self.rep.addItem("",  self.outPar(	nodeCbc,
                        'temperature_multiplier_function'               ))

        if type == 'wall' and tempType == 'flux':
            self.rep.addItem("",  self.outPar(	nodeCbc,    'heat_flux'	))
            if doTmf:
                self.rep.addItem("",  self.outPar(	nodeCbc,
                        'heat_flux_multiplier_function'                 ))
            self.rep.addItem("",  self.outPar(		nodeCbc,
                        'convective_heat_coefficient'                   ))
            if doTmf:
                self.rep.addItem("",  self.outPar(	nodeCbc,
                        'convective_heat_multiplier_function'           ))
            self.rep.addItem("",  self.outPar(		nodeCbc,
                        'convective_heat_reference_temperature'	        ))

        if type == 'inflow' and \
           ((inflowType == 'velocity' or inflowType == 'pressure' \
            or inflowType == 'stagnation_pressure' ) and \
            ( turb == "spalart_allmaras" or \
              turb == "detached_eddy_simulation" )):
            self.rep.addItem("",  self.outPar(   nodeCbc,
                                                 'eddy_viscosity'       ))
            if doTmf:
                self.rep.addItem("",  self.outPar(	nodeCbc,
                        'eddy_viscosity_multiplier_function'            ))

        if ( type == 'outflow' and backFlow ) and ( turb == "spalart_allmaras" or \
            turb == "detached_eddy_simulation" ):
            self.rep.addItem("",  self.outPar(nodeCbc, 'eddy_viscosity'	))
            if doTmf:
                self.rep.addItem("",  self.outPar(	nodeCbc,
                        'eddy_viscosity_multiplier_function'            ))

        if type == 'wall':
            self.rep.addItem("",  self.outPar(nodeCbc,
                                              'turbulence_wall_type'	))
            turWallType	= self.acs.getEnum(	    path=nodeCbc,
                                            par='turbulence_wall_type'   )

        if type == 'wall' and ( turWallType == 'wall_function' or \
            turWallType == 'running_average_wall_function' ) :
            self.rep.addItem("",  self.outPar(   nodeCbc,
                                                 'roughness_height'     ))

        if type in [ 'inflow', 'outflow' ]:
            if doTmf:
                self.rep.addItem("",  self.outPar(nodeCbc,
                                             'non_reflecting_factor'    ))

        if type == 'free_surface':
            self.rep.addItem("",  self.outPar(nodeCbc,
                                         'surface_tension_model'        ))
            self.rep.addItem("",  self.outPar(nodeCbc,
                                              'contact_angle_model'	))
            self.rep.addItem("",  self.outPar(nodeCbc,
                                              'pressure'		))
            if doTmf:
                self.rep.addItem("",  self.outPar(	nodeCbc,
                                        'pressure_multiplier_function'  ))
            self.rep.addItem("",  self.outPar(nodeCbc,
                                              'pressure_loss_factor'    ))


        if (type != 'free_surface'):
            self.rep.addItem("",  self.outPar(   nodeCbc,
                                            'mesh_displacement_type'    ))

            meshDispType    = self.acs.getEnum(  path=nodeCbc,
                                             par='mesh_displacement_type')

        if meshDispType == 'flexible_body' :
            self.rep.addItem("",  self.outPar(nodeCbc, 'flexible_body'  ))
            self.rep.addItem("",  self.outPar(   nodeCbc, 'mesh_motion' ))

        if meshDispType == 'guide_surface' :
            self.rep.addItem("",  self.outPar( nodeCbc, 'guide_surface' ))

        if meshDispType == 'fixed':
            self.rep.addItem("",  self.outPar(nodeCbc,   'mesh_motion'  ))

        self.rep.endBullet(                                              )

#===========================================================================
#
# "main()":  Test the module
#
#===========================================================================

if __name__ == "__main__":
    report = acuReport.AcuReport("test.tex",
                                 packages=("graphicx", "hyperref"       ))

    report.modifyPackageOptions("hypersetup",
                                optionMap={"pdfborder":"{0 0 0}"        })

    acs = repAcs.RepAcs("pump.acs"                                       )

    pap = RepAcsRep(report, acs                                          )

    pap.addMaterialModel("Water"                                         )
    print pap.getPrbDesc(                                                )
