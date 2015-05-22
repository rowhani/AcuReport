#===========================================================================
#
# "AcuItemObj":  Models item Class
#
#===========================================================================

class AcuItemObj:

    '''
        Models item class
    '''

    def __init__( self,     name,       display,    vis,
                  trans,    transVal,   color                       ):

        self.name           = name
        self.dataId         = name
        self.display        = display
        self.visiblityFlg   = vis
        self.transparencyFlg= trans
        self.transVal       = transVal
        self.color          = color
