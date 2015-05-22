#===========================================================================
#
# Include files
#
#===========================================================================

from    acuSgIso  import  AcuSgIso

#===========================================================================
#
# "acuSgCpl": Cut-Plane actor
#
#===========================================================================

class AcuSgCpl( AcuSgIso ):
    '''
	class AcuSgCpl creates objects of Cut-Plane actors
    '''

    def __init__( self, parent ):
	'''
            AcuSgCpl is used to create cut-plane actors.

	    Arguments:
	        parent  - parent object		
		
	'''
                                                                        
	AcuSgIso.__init__(                  self, parent                        ) 	
