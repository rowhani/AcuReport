#===========================================================================
#
# Include files
#
#===========================================================================

import	os
import	sys
import	math

import  qt
import	numarray

from	iv	    import  *
from    acuCmap     import  AcuCmap

#===========================================================================
#
# Errors
#
#===========================================================================

acuSgCmapError   = "ERROR from acuSgCmapLegend module"
		
#===========================================================================
#
# "AcuSgCmapLegend":  Scene graph open inventor graphics
#
#===========================================================================

class AcuSgCmapLegend ( SoSeparator ):

    '''
         All the open inventor functions,
    '''

    def __init__(   self,
                    parent      = None, 
                    text        = "Temperature",
		    textFont    = "Times-Roman",
                    minVal      = 0.0,
                    maxVal      = 2.0,
                    nVals	= 3,
                    textFontSize= 12,
                    valFont     = "Times-Roman",
                    valFontSize = 12,
                    xpos        = 0.08,
                    ypos        = 0.05,
                    xsize       = 20,
                    ysize       = 100,
                    valXOffset  = 0.07,
                    valYOffset  = 0.05):
        '''
	    Arguments:
	        parent		- parent object
	    Output:
	        None
        '''

        SoSeparator.__init__( self )
			
        self.parent	= parent
        self.viewer	= self.parent.viewer   #self.viewer = self.parent (for unit test)
        self.cmap       = AcuCmap()
		
        self.txt        = text
        self.txtFnt     = textFont
        self.minV       = minVal
        self.maxV       = maxVal
        self.nV         = nVals
        self.valFnt     = valFont
		
        self.xP         = xpos
        self.yP         = ypos
		
        self.xSz        = xsize
        self.ySz        = ysize

        self.valXOffset = valXOffset
        self.valYOffset = valYOffset
		
        screenVp        = self.viewer.getViewportRegion()
        screenSize      = screenVp.getViewportSizePixels()
        screenPixPerInch= screenVp.getPixelsPerInch()
        self.xSz        = self.xSz*320/(screenPixPerInch*screenSize[0])
        self.ySz        = self.ySz*320/(screenPixPerInch*screenSize[1])
			        
        self.cMapColors = self.cmap.getCmap(        self.parent.cmap    )
		
        self.txtColor   = [0,0,1]
        self.txtSize    = textFontSize
        self.verticesPerRow = 256
        self.verticesPerColumn = 2
		
        self.vertexPositions = list()		
        for i in range(0, 256):
            self.vertexPositions.insert(i, (0, i*self.ySz/256, 0))
        for j in range(0, 256):
            self.vertexPositions.insert(256+j, (self.xSz, j*self.ySz/256, 0))
       
        self.vals = list()
        self.valsYPosition = list()
        self.valsSep = list()
        self.valColor = [0,0,1]
        self.valSize = valFontSize
        self.valsTrans = list()
        self.valsTxtObj = list()

	if self.nV > 1:
            for i in range(0, self.nV):
                self.vals.insert(i, SbString(str(round(self.minV+i*(self.maxV-self.minV)/(self.nV-1), 2))))
                self.valsYPosition.insert(i, self.yP+i*self.ySz/(self.nV-1))
 
        self.addColorMap()
		
#---------------------------------------------------------------------------
# 
#---------------------------------------------------------------------------		
    def addColorMap( self ):
	'''
	create the color map in the graphical window
	Arguments:
	    None
	Output:
	    None
    '''
	
	# add colormap to the scene graph    
        self._createLineSet()		
		
	# add title and labels to the scene graph
        self._addText( )
            
        self._addVals()

#-------------------------------------------------------------------------
# _createLineSet: private function to create a LineSet
#-------------------------------------------------------------------------

    def _createLineSet(  self, center = [0,0,0]):
        
        # Line indices
        cnnVel = []
        for i in range(0, 512, 2):
            cnnVel.append(i)
            cnnVel.append(i + 1)
            cnnVel.append(SO_END_LINE_INDEX)

        # Create packed RGBA
        R = (numarray.clip( self.cMapColors[:,0], 0, 1 ) * 255).astype('i')
        G = (numarray.clip( self.cMapColors[:,1], 0, 1 ) * 255).astype('i')
        B = (numarray.clip( self.cMapColors[:,2], 0, 1 ) * 255).astype('i')                   
        self.cmapRGBA = (R << 24) + (G << 16) + (B <<8) + 255        

        # Create data structures
        self.colormapSep = SoSeparator()

	self.style = SoDrawStyle()
        self.style.lineWidth.setValue(5)
        self.colormapSep.addChild(self.style)
        
        self.transform = SoTransform()
        self.transform.translation.setValue( [self.xP, self.yP, 0] )
        self.colormapSep.addChild( self.transform )

        self.vertexPropertyObj    = SoVertexProperty()
        self.vertexPropertyObj.materialBinding.setValue( SoMaterialBinding.PER_VERTEX_INDEXED )
        
        self.contourLineSet = SoIndexedLineSet()          
        self.contourLineSet.vertexProperty.setValue( self.vertexPropertyObj )
        self.contourLineSet.coordIndex.setValues( 0, cnnVel )

        self.colormapSep.addChild( self.contourLineSet )        
        self.addChild( self.colormapSep )
               
        self._updateVertexPosition() 
        
#-------------------------------------------------------------------------
# _updateVertexPosition: private function to update vertex position
#-------------------------------------------------------------------------
    def _updateVertexPosition( self ):
        # Draw Colormap Line set
        self.vertexPositions  = numarray.concatenate( ( self.vertexPositions[0:256],
                                                        self.vertexPositions[256:512]),
                                                        axis = 1 ).copy()            
        self.vertexPositions.setshape( 512, 3 )       
       
        scalar      = self.vertexPositions[:,1]
        sclrMinVal  = scalar.max()
        sclrMaxVal  = scalar.min()

        fct = (len(self.cMapColors)-1) / (sclrMaxVal - sclrMinVal)
        sclrIdx	 = fct * (scalar - sclrMinVal) + 0.5
        sclrIdx	 = numarray.clip( sclrIdx, 0, len(self.cMapColors)-1 )
        colorIdx = self.cmapRGBA[sclrIdx]
        colorIdx = colorIdx.tolist()
        colorIdx.reverse()       
     
        self.vertexPropertyObj.vertex.setValues( 0, self.vertexPositions )        
        self.vertexPropertyObj.orderedRGBA.setValues( 0, colorIdx )         

#-------------------------------------------------------------------------
# _addText: private function to create a Text
#-------------------------------------------------------------------------	
    def _addText(  self ):
	
        self.textSep = SoSeparator()
		    
        self.material= SoMaterial( )
        self.textSep.addChild( self.material )
        self.material.diffuseColor.setValue( self.txtColor[0], self.txtColor[1],self.txtColor[2] )
		
        self.trans	= SoTranslation()
        self.textSep.addChild( self.trans )
        self.trans.translation.setValue( [self.xP, self.yP+self.ySz+self.valYOffset, 0] )
		
        self.fntObj	= SoFont()
        self.textSep.addChild( self.fntObj )
		
        self.fntObj.size.setValue( self.txtSize )
        self.fntObj.name.setValue( self.txtFnt	)
		
        self.txtObj	= SoText2(	)
        self.textSep.addChild( self.txtObj )
        self.txtObj.string.setValue( self.txt ) 
		
        self.addChild(self.textSep)

#-------------------------------------------------------------------------
# _addVals: private function to create a Text
#-------------------------------------------------------------------------	
    def _addVals( self ):
	'''
	Add the left values in to the color map scene graph
	Arguments:
	    None
	Output:
	    None
    '''	
        
        self.valTextSep = SoSeparator()
		
        self.valsMaterial= SoMaterial( )
        self.valTextSep.addChild( self.valsMaterial )
        self.valsMaterial.diffuseColor.setValue( self.valColor[0], self.valColor[1], self.valColor[2]	)
		          
        self.valsFntObj	= SoFont()
        self.valTextSep.addChild( self.valsFntObj )
		
        self.valsFntObj.size.setValue( self.valSize )
        self.valsFntObj.name.setValue( self.valFnt	)
		
	# add left values to the scene graph
        if self.nV > 2:
            for i in range(0, self.nV):
                self.valsSep.insert(i, SoSeparator())

                self.valsTrans.insert(i, SoTranslation() )
                self.valsSep[i].addChild( self.valsTrans[i]	)
                self.valsTrans[i].translation.setValue( [self.xP-self.valXOffset, self.valsYPosition[i], 0] )

                self.valsTxtObj.insert(i, SoText2() )
                self.valsSep[i].addChild( self.valsTxtObj[i] )
                self.valsTxtObj[i].string.setValue( self.vals[i] ) 
		
                self.valTextSep.addChild(self.valsSep[i])
		

        self.addChild( self.valTextSep )
		
#-------------------------------------------------------------------------
# text: public function to change the text
#-------------------------------------------------------------------------	
    def text(  self, text = None):
        '''
	    set the text of the colormap
	    Arguments:
		    text
	    Output:
        '''

        retVal	= self.txt

        if text != None:
            self.txt	= text
            self.txtObj.string.setValue( self.txt )
        return retVal

#-------------------------------------------------------------------------
# textFont: public function to change the text
#-------------------------------------------------------------------------	
    def textFont(  self, textFont = None):
        '''
	    set the text font of the colormap
	    Arguments:
		    textFont
	    Output:
        '''

        retVal	= self.txtFnt

        if textFont != None:
            self.txtFnt	= textFont
            self.fntObj.name.setValue( self.txtFnt	)
        return retVal
		
#-------------------------------------------------------------------------
# minVal: public function to change the text
#-------------------------------------------------------------------------	
    def minVal(  self, minVal = None):
        '''
	    set the minVal of the colormap
	    Arguments:
		    minVal
	    Output:
        '''

        retVal	= self.minV

        if minVal != None:
            self.minV	= minVal

            if self.nV > 1:
                for i in range(0, self.nV):
                    self.vals.insert(i, SbString(str(round(self.minV+i*(self.maxV-self.minV)/(self.nV-1), 2))))				
                    self.valsTxtObj[i].string.setValue( self.vals[i] )	
			
        return retVal

#-------------------------------------------------------------------------
# maxVal: public function to change the text
#-------------------------------------------------------------------------	
    def maxVal(  self, maxVal = None):
        '''
	    set the maxVal of the colormap
	    Arguments:
		    maxVal
	    Output:
        '''

        retVal	= self.maxV

        if maxVal != None:
            self.maxV	= maxVal

            if self.nV > 1:
                for i in range(0, self.nV):
                    self.vals.insert(i, SbString(str(round(self.minV+i*(self.maxV-self.minV)/(self.nV-1), 2))))				
                    self.valsTxtObj[i].string.setValue( self.vals[i] )	
			
        return retVal

#-------------------------------------------------------------------------
# nVals: public function to change the text
#-------------------------------------------------------------------------	
    def nVals(  self, nVals = None):
        '''
	    set the nVals of the colormap
	    Arguments:
		    nVals
	    Output:
        '''

        retVal	= self.nV

        if nVals != None:          
            self.vals = list()
            self.valsYPosition = list()
            self.valsSep = list()
            self.valsTrans = list()
            self.valsTxtObj = list()

            self.removeChild( self.valTextSep )
			
            self.nV	= nVals
            if self.nV > 1:
                for i in range(0, self.nV):
                    self.vals.insert(i, SbString(str(round(self.minV+i*(self.maxV-self.minV)/(self.nV-1), 2))))				
                    self.valsYPosition.insert(i, self.yP+i*self.ySz/(self.nV-1))
		
            self._addVals()
            self.viewer.redraw(	)
			
        return retVal

#-------------------------------------------------------------------------
# valFont: public function to change the text
#-------------------------------------------------------------------------	
    def valFont(  self, valFont = None):
        '''
	    set the text font of the colormap
	    Arguments:
		    valFont
	    Output:
        '''

        retVal	= self.valFnt

        if valFont != None:
            self.valFnt	= valFont
            self.fntObj.name.setValue( self.valFnt	)
        
        return retVal	

#-------------------------------------------------------------------------
# xpos: public function to change the text
#-------------------------------------------------------------------------	
    def xpos(  self, xpos = None):
        '''
	    set the text font of the colormap
	    Arguments:
		    xpos
	    Output:
        '''

        retVal	= self.xP

        if xpos != None:
            self.xP	= xpos
            self.transform.translation.setValue( [self.xP, self.yP, 0] )
            self.trans.translation.setValue( [self.xP, self.yP+self.ySz+0.02, 0] )
            for i in range(0, self.nV):
                self.valsTrans[i].translation.setValue( [self.xP-0.04, self.valsYPosition[i], 0] )
				
        return retVal	

#-------------------------------------------------------------------------
# ypos: public function to change the text
#-------------------------------------------------------------------------	
    def ypos(  self, ypos = None):
        '''
	    set the text font of the colormap
	    Arguments:
		    ypos
	    Output:
        '''

        retVal	= self.yP

        if ypos != None:
            self.yP	= ypos
            self.transform.translation.setValue( [self.xP, self.yP, 0] )
            self.trans.translation.setValue( [self.xP, self.yP+self.ySz+0.02, 0] )
            
            if self.nV > 1:
                for i in range(0, self.nV):		
                    self.valsYPosition.insert(i, self.yP+i*self.ySz/(self.nV-1))
                    self.valsTrans[i].translation.setValue( [self.xP-0.04, self.valsYPosition[i], 0] )
				
        return retVal	

#-------------------------------------------------------------------------
# xsize: public function to change the text
#-------------------------------------------------------------------------	
    def xsize(  self, xsize = None):
        '''
	    set the text font of the colormap
	    Arguments:
		    xsize
	    Output:
        '''

        retVal	= self.xSz

        if xsize != None:
            self.xSz = xsize
            screenVp = self.viewer.getViewportRegion()
            screenSize = screenVp.getViewportSizePixels()
            screenPixPerInch = screenVp.getPixelsPerInch()
            self.xSz = self.xSz*320/(screenPixPerInch*screenSize[0])
		       
            self.vertexPositions = list()		
            for i in range(0, 256):
                self.vertexPositions.insert(i, (0, i*self.ySz/256, 0))            	
            for j in range(0, 256):
                self.vertexPositions.insert(256+j, (self.xSz, j*self.ySz/256, 0)) 
			
            self._updateVertexPosition()
		
        return retVal		


#-------------------------------------------------------------------------
# ysize: public function to change the text
#-------------------------------------------------------------------------	
    def ysize(  self, ysize = None):
        '''
	    set the text font of the colormap
	    Arguments:
		    ysize
	    Output:
        '''

        retVal	= self.ySz

        if ysize != None:
            self.ySz = ysize
            screenVp = self.viewer.getViewportRegion()
            screenSize = screenVp.getViewportSizePixels()
            screenPixPerInch = screenVp.getPixelsPerInch()
            self.ySz = self.ySz*320/(screenPixPerInch*screenSize[1])
		       
            self.vertexPositions = list()		
            for i in range(0, 256):
                self.vertexPositions.insert(i, (0, i*self.ySz/256, 0))            	
            for j in range(0, 256):
                self.vertexPositions.insert(256+j, (self.xSz, j*self.ySz/256, 0)) 
			
            self._updateVertexPosition()
		
            self.trans.translation.setValue( [self.xP, self.yP+self.ySz+0.02, 0] )

	    if self.nV > 1:
                for i in range(0, self.nV):		
                    self.valsYPosition.insert(i, self.yP+i*self.ySz/(self.nV-1))
                    self.valsTrans[i].translation.setValue( [self.xP-0.04, self.valsYPosition[i], 0] )
		
        return retVal

#===========================================================================
#
# 
#
#===========================================================================

if __name__ == "__main__":
    
    myWindow = SoQt.init(sys.argv[0])
    if not myWindow:
        sys.exit(1)

    myRenderArea = SoQtExaminerViewer(myWindow)
    cmapLegend = AcuSgCmapLegend(   parent = myRenderArea,
                                    text        = "Pressure",
                                    textFont    = "Times-Roman",
                                    minVal      = 0,
                                    maxVal	= 2,
                                    nVals	= 4,
                                    valFont     = "Times-Roman",
                                    xpos        = 0.05,
                                    ypos        = 0.15,
                                    xsize       = 2,
                                    ysize       = 10    )   
    
    myRenderArea.setSceneGraph(cmapLegend)   
    myRenderArea.setTitle("Cmap Legend")
    myRenderArea.show()

    SoQt.show(myWindow)  
    writeAction = SoWriteAction()
    writeAction.getOutput().setBinary(False)
    writeAction.getOutput().openFile("CmapLegend.iv")
    writeAction.apply(cmapLegend)
    SoQt.mainLoop()
		
