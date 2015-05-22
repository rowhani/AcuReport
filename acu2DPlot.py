#------------------------------------------------------------------------
# Get the modules
#------------------------------------------------------------------------

import  math
import  types
import  os

import  numarray
import  pylab

#========================================================================
#
# Useful defines
#
#========================================================================

TRUE    = 1
True    = 1
FALSE   = 0
False   = 0

_lineType                   = {}
_lineType["solid"]          = "-"
_lineType["dashed"]         = "--"
_lineType["dash-dot"]       = "-."
_lineType["dotted"]         = ":"

_symbols                    = {}
_symbols["points"]          = "."
_symbols["pixels"]          = ","
_symbols["circle"]          = "o"
_symbols["triangleUp"]      = "^"
_symbols["triangleDown"]    = "v"
_symbols["triangleLeft"]    = "<"
_symbols["triangleRight"]   = ">"
_symbols["square"]          = "s"
_symbols["plus"]            = "+"
_symbols["cross"]           = "x"
_symbols["diamond"]         = "D"
_symbols["thinDiamond"]     = "d"
_symbols["tripodDown"]      = "1"
_symbols["tripodUp"]        = "2"
_symbols["tripodLeft"]      = "3"
_symbols["tripodRight"]     = "4"
_symbols["hexagon"]         = "h"
_symbols["rotatedHexagon"]  = "H"
_symbols["pentagon"]        = "p"
_symbols["verticalLine"]    = "|"
_symbols["horizontalLine"]  = "_"

_colors                     = {}
_colors["b"]                = "blue"
_colors["g"]                = "green"
_colors["r"]                = "red"
_colors["c"]                = "cyan"
_colors["m"]                = "magenta"
_colors["y"]                = "yellow"
_colors["k"]                = "black"
_colors["w"]                = "white"
_colors["auto"]             = "auto"

#========================================================================
# Errors
#========================================================================

acu2DPlotError  = "ERROR from acu2DPlot module"

#========================================================================
#
# "curve"
#
#========================================================================

def curve(  x,                      y,
            name        = None,     lineType    = "solid",
            lineWidth   = 1,        symbol      = None,
            symbolSize  = 1,        color       = "blue"    ):

    """
        Create a curve with the styles provided.

        Argument:
            x            - The value of the X data of the curve.
            y            - The value of the Y data of the curve.
            name         - The curve's name.
            lineType     - The curve's line types.
                           valid: solid(-), dashed(--), dash-dot(-.), dotted(:)
            lineWidth    - The curve's line width.
            symbol       - The curve's symbol.
            symbolSize   - The curve's symbol size.
            color        - The curve's color string.
                           valid: blue(b), green(g), red(r),
                           cyan(c), magenta(m), yellow(y), black(k), white(w)

        Output:
            The created curve.
    """

    lineType            = lineType.lower(                               )
    if lineType in _lineType:
        lineType        = _lineType[lineType]
    elif lineType not in _lineType.values( ):
        raise acu2DPlotError, \
             'The "%s" line type is invalid.' %lineType

    color               = color.lower(                                  )
    if color in _colors:
        color           = _colors[color]
    elif color not in _colors.values( ):
        raise acu2DPlotError, \
             'The "%s" color is invalid.' %color
    
    marker              = 'None'
    markerfacecolor     = color
    markersize          = symbolSize
    if symbol:
        symbol          = symbol.lower(                                 )
        marker          = symbol
        if symbol in _symbols:
            marker      = _symbols[symbol]
        elif symbol not in _symbols.values( ):
            raise acu2DPlotError, \
                 'The "%s" symbol is invalid.' %symbol

    if not name:
        name            = "Curve_(" + color + ")_(" + lineType + ")"
    
    if isinstance( x, numarray.NumArray ) and len( x.shape ) != 1:
        x.ravel(                                                        )
    if isinstance( y, numarray.NumArray ) and len( y.shape ) != 1:
        y.ravel(                                                        )
    
    return  { "x"               : x,          "y"         :   y,
              "name"            : name,       "type"      :   lineType,
              "width"           : lineWidth,  "marker"    :   marker,
              "markersize"      : markersize, "color"     :   color,
              "markerfacecolor" : markerfacecolor                       }

#========================================================================
#
# "plot"
#
#========================================================================

def plot(   curves,
            title       = "",           legend      = True,
            legendPos   = "auto",       xLabel      = "X",
            xLog        = False,        xRange      = "auto",
            yLabel      = "Y",          yLog        = False,
            yRange      = "auto",       width       = 600,
            height      = 400,          fileName    = None,
            fileType    = "png",        dirName     = "Figures",
            fontSize    = 14,           fontScale   = 1.0,
            resolution  = 80,           resScale    = 1.0,
            tickSize    = 12,           tickScale   = 1.0           ):

    """
        Creates an x-y plot from a set of curves.

        Argument:
            curves      - list of lists, each child list is a curve.
            title       - plot title.
            legend      - True/False;
                          create a legend for the lines in in the plot.
            legendPos   - legend position in the plot.
                          valid: best(0), upper right (1), upper left(2),
                          lower left(3), lower right(4), right(5),
                          center left(6), center right(7), lower center(8),
                          upper center(9), center(10)
            xLabel      - The X-axis label
            xLog        - The X-axis scale Linear/Log.
            xRange      - can be either "auto" or [min,max]
                          (or (min,max)) values
            yLabel      - The Y-axis label
            yLog        - The Y-axis scale Linear/Log.
            yRange      - can be either "auto" or [min,max]
                          (or (min,max)) values
            width       - plot width
            height      - plot height
            fileName    - The name of file to be saved
            fileType    - Type of the image file to be saved
            dirName     - Directory of output file
            fontSize    - Font Size
            fontScale   - Font Scale
            resolution  - Resolution in dpi
            resScale    - Resolution Scale
            tickSize    - Size of x and y axes ticks
            tickScale   - Scale of x and y axes ticks

        Output:
            Name of the saved file.
    """

    fontSize    = fontSize * fontScale
    tickSize    = tickSize * tickScale
  
    if type( curves ) != types.TupleType and \
       type( curves ) != types.ListType:
        curves = (curves, )

    curveClrs   = []   
   
    #----- Clear a figure window
    
    pylab.clf(                                                          )
    
    for curve in curves:
        curveClrs.append(           curve["color"]                      )
        
    for curve in curves:
        color = curve["color"]
        if color  == "auto":
            for clr in _colors.values( ):
                if clr not in curveClrs:
                    color   = clr
                    curveClrs.append(               clr                 )
                    break
            
        pylab.plot( curve["x"],
                    curve["y"],
                    label           = curve["name"],
                    linestyle       = curve["type"],
                    linewidth       = curve["width"],
                    color           = color,
                    marker          = curve.get( "marker" ),
                    markerfacecolor = curve.get( "markerfacecolor" ),
                    markersize      = curve.get( "markersize" )         )

    pylab.title(                        title, fontsize = fontSize      )

    if legend:
        if legendPos == "auto":
            pylab.legend(                                               )            
        else:
            try:
                pylab.legend(           loc = legendPos                 )
            except:
                raise acu2DPlotError, "legend position is not correct."

    pylab.xlabel(                       xLabel, fontsize = fontSize     )
    pylab.ylabel(                       yLabel, fontsize = fontSize     )

    pylab.xticks(                       size = tickSize                 )
    pylab.yticks(                       size = tickSize                 )

    if xLog:
        pylab.semilogx(                                                 )
    elif xRange != 'auto':
        pylab.xlim(     xRange[0], xRange[1]                            )
      
    if yLog:
        pylab.semilogy(                                                 )
    elif yRange != 'auto':
        pylab.ylim(     yRange[0], yRange[1]                            )   
    
    if not os.path.exists( dirName ):
        os.makedirs(                       dirName                      )

    if fileType.lower( ) not in [ "ps", "eps", "svg", "png" ]:
        raise acu2DPlotError, "File type not suppoerted."

    if fileName:
        fullName = fileName
        if not fullName.endswith( "." + fileType ):
            fullName += "." + fileType
    else:
        counter = 1
        while True:
            name = "plot_" + str( counter ) + "." + fileType
            fullName = os.path.join(        dirName, name               )
            if not os.path.exists( fullName ):              
                break
            counter += 1

    #----- save the file
            
    resolution = resolution * resScale
    pylab.gcf( ).set_size_inches(    ( width / resolution,
                                       height / resolution )            )
    pylab.savefig(      fullName, dpi = resolution                      )  
    
    #-------------------------------------------------------------------
    # return the name of saved file
    #-------------------------------------------------------------------

    return fullName

#========================================================================
#
# Test
#
#========================================================================

if __name__ == '__main__':

    presx   = [ 1, 2, 3, 4, 5, 6 ]
    presy   = [ 10, 20, 30, 40, 50, 60 ]
    velx    = [ 1.5, 2.5, 3.5 ]
    vely    = [ 4.5, 5.5, 6.5 ]

    curve1    = curve(  x = presx, y = presy, name = "Pressure",
                        lineType = "solid", color = "Red",
                        symbol = "square", symbolSize = 5               )

    curve2    = curve(  x = velx, y = vely, name = "Velocity",
                        lineType = "--", color = "g"                    )
    
    image = plot(   curve1,
                    title       = "Test",
                    legend      = True,
                    legendPos   = "upper left",
                    xLabel      = "Time (sec)",
                    xRange      = (0,10),
                    yLog        = True,
                    yLabel      = "Residual Ratio",
                    fileType    = "png"
                                                                        )
    print "Output File saved as:", image    

    image = plot(   curve2,
                    title       = "Test",
                    legend      = True,
                    legendPos   = "upper left",
                    xLabel      = "Time (sec)",
                    xRange      = (0,10),
                    yLog        = True,
                    yLabel      = "Residual Ratio",
                    fileType    = "png"
                                                                        )

    print "Output File saved as:", image

    image = plot(   ( curve1, curve2 ),
                    title       = "Test",
                    legend      = True,
                    legendPos   = "upper left",
                    xLabel      = "Time (sec)",
                    xRange      = (0,10),
                    yLog        = True,
                    yLabel      = "Residual Ratio",
                    fileType    = "png"
                                                                        )

    print "Output File saved as:", image
    
