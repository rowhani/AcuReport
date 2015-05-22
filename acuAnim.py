#===========================================================================
#
# Include files
#
#===========================================================================

import  os

#===========================================================================
#
# Errors
#
#===========================================================================

acuAnimationError   = "ERROR from acuAnim module"

#===========================================================================
#
# "AcuAnim":  Create animation file from a series of images
#
#===========================================================================

class AcuAnim:

    '''
        Create animation file from a series of images
    '''

    def __init__(   self,   outputFile, images, delay = 20              ):
        '''
	    Arguments:
	        outputFile  - Output animation file name 
	        images	    - Working directory
	        delay       - Delay after each frame in animation file
	    Output:
	        None
        '''

	if not outputFile:
            outputFile  = 'output.mpeg'

        if not images:
            raise acuAnimationError, "There is no image for creating animation"

        names   = ''

        for image in images:
            image   = os.path.basename(         image                   )
            names   += ' ' + str(               image                   )
            
        os.system('convert -delay '+ str(delay) + ' -loop 1' + \
                  names + ' ' + outputFile                              )
        
#================================================================================
#
# Test              
#
#================================================================================

if __name__ == '__main__':

    from pylab import *

    images = []
    for i in range(20):  
        cla(                                                            )
        imshow( rand(5,5), interpolation='nearest'                      )
        fname = '_tmp%03d.png'%i
        savefig(                            fname                       )
        images.append(                      fname                       )

    animation      = AcuAnim(               'test.mpg',
                                            images,
                                            delay = 20                  )

    for fname in images: os.remove(         fname                       )

