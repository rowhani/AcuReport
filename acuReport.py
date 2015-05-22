#---------------------------------------------------------------------------
#Import required modules
#---------------------------------------------------------------------------

import  time
import  os.path
import  types
import  re
import  shutil
import  math

from    PIL             import  Image

import  acuConvertU3D
import  acuLogo

#---------------------------------------------------------------------------
# _normalizeHtml: scale figures, remove extra lines and tth credit
#---------------------------------------------------------------------------

def _normalizeHtml(input, output, basePath, credit = False):

    """This module sets scale attributes for the images in the
    html file according to the scale information in tex file.
    """

    '''
    _normalizeHtml(input, output)

    Argument:
        input  - the tex file
        output - the html file
        credit - tth credit
    '''

    tex = open(                         input, "rt"                     )
    html = open(                        output, "rt"                    )

    tempFile = os.getenv(                   "TEMP", ""                  )
    if tempFile == "":
        tempFile = os.path.basename(html.name) + "t"
    else:
        tempFile += "/" + os.path.basename(       html.name             )
    temp = open(tempFile, "wt")

    texline = tex.readline(                                             )
    while texline != "":
        if texline.find("includegraphics") != -1:
            htmlline = ""
            htmlline = html.readline(                                   )
            while htmlline != "":
                htmlline = htmlline.replace("@Entry[1]", ""             )

                img = re.compile(       r"<\s*img\s*", re.IGNORECASE    )
                if img.search(htmlline) != None:
                    mat = img.search(htmlline).group(                   )
                    index = htmlline.find(mat) + len(       mat         )

                    img = re.compile(
                                 r"\[\s*scale\s*=\s*\d*[.]{0,1}\d+\s*\]"
                                                        , re.IGNORECASE )
                    if img.search(texline) != None:
                        img = re.compile(r"\d*[.]{0,1}\d+",
                                                        re.IGNORECASE   )
                        scale = img.search(texline).group(              )
                        scale = float(scale) * 1.33

                        src = re.compile(r"src\s*=\s*", re.IGNORECASE   )
                        name = src.search(htmlline).group(              )
                        nix = htmlline.find(name) + len(name) + 1
                        endIndex = nix + htmlline[nix:].find(r'"'       )
                        name = htmlline[nix:endIndex]

                        pimg = Image.open( name )
                        width = str(int(math.ceil(pimg.size[0]*scale)   ))
                        height = str(int(math.ceil(pimg.size[1]*scale)  ))

                        if name.startswith(basePath):
                            name = "." + name[len(basePath):]

                        htmlline = htmlline[:index] + \
                                   " width=\"" + width + "\" " + \
                                   " height=\"" + height + "\" " + \
                                   r'src="' + name + r'"' + \
                                   htmlline[endIndex:]

                    temp.write(                 htmlline                )
                    break

                else:
                    temp.write(                 htmlline                )

                htmlline = html.readline(                               )
        texline = tex.readline(                                         )
    end = html.read(                                                    )
    if end and end != "":
        end = str(end                                                   )
        if not credit:
            startIndex = end.find("<br /><br /><hr /><small>File translated from")
            endIndex = end.find("</html>"                               )
            if startIndex != -1 and endIndex != -1:
                end = end.replace(end[startIndex:endIndex], ""          )

        temp.write(                         end                         )

    tex.close(                                                          )
    html.close(                                                         )
    temp.close(                                                         )
    shutil.copyfile(                    tempFile, output                )
    os.remove(                          tempFile                        )

#---------------------------------------------------------------------------
# _canonicalFileName: Create a file name with .tex extention
#---------------------------------------------------------------------------

def _canonicalFileName(fileName):

    """
    canonicalFileName(fileName) -> string

        Returns:
            a file name with .tex extention

    """

    rawPath = os.path.split(fileName)[0]
    basePath = rawPath.replace("\\", "/"                                )
    if basePath == "":
        basePath = "."

    if rawPath == "":
        tmp = basePath + "/" + fileName
    else:
        if not os.path.exists(rawPath):
            os.makedirs(rawPath                                         )
        tmp = fileName
    tmp = tmp.replace(                      "\\", "/"                   )
    if(not tmp.lower().endswith(".tex")):
        tmp = tmp + ".tex"

    return (basePath, tmp)

#---------------------------------------------------------------------------
# _isImageValid: Specify whether image is valid
#---------------------------------------------------------------------------

def _isImageValid(basePath, fileName):

    """
    isImageValid(fileName) -> string

        Argument:
            fileName: image file Name

        Return:
            error or None message to indicate whether the image
            is valid or not.

    """

    tmp = fileName
    if os.path.splitdrive(fileName)[0] == "":
        tmp = basePath + "/" + fileName

    if not os.path.exists(fileName) and not os.path.exists(tmp):
        return "Error: Image file is not exising"

    if (os.path.splitext(fileName)[1].lower()
        not in [".ps", ".png", ".gif", ".jpg",
               ".jpeg", ".pdf"]):
        return "Error: Image format not supported."

    return None

#---------------------------------------------------------------------------
# AcuReport: Main functions of AcuReport module
#---------------------------------------------------------------------------

class AcuReport:

    """The class containing all the required operations to
    create output formats from input file."""

    itemsStack = 0
    bulletsStack = 0

#---------------------------------------------------------------------------
# "__init__": Create a new LaTeX file object
#---------------------------------------------------------------------------

    def __init__( self,     fileName,
                            packages    = (),
                            docClass    = 'article',
                            docClassOpt = 'letterpaper,12pt',
                            fullPage    = True,
                            verbose     = 2                      ):

        '''Create a new LaTeX file object.
        Argument:
            fileName    - File name (eg., "report.tex")
            packages    - (opt) List of document packages (default=())
            docClass    - (opt) Document class (default='article')
            docClassOpt - (opt) Document class options
                                (default='psfig,12pt')
            fullPage    - Set margin to full page
            verbose     - Verbosity level
        Return:
            report      - report object
        '''

	self.verbose = verbose

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------
        if type(fileName) != types.StringType:
            raise AcuReportError, "Invalid fileName " + str(  fileName  )
        if type(docClass) != types.StringType:
            raise AcuReportError, "Invalid docClass " + str(  docClass  )
        if type(docClassOpt) != types.StringType:
            raise AcuReportError, "Invalid docClassOpt " \
                                   + str(       docClassOpt             )

        #----Make the file path ready for use and then create the file

        (basePath, fileName) = _canonicalFileName(          fileName    )
        self.basePath = basePath
        self.fileName = fileName
        self.baseName = os.path.basename(self.fileName)\
                        [:os.path.basename(self.fileName).rfind(".")]
        self.file = open(                       fileName, "wt"          )
        self.file.write(        "% FileName: " + fileName + "\n"        )

        #----Add default headers to tex file

        self.file.write(            "% Generated by: AcuReport\n"       )
        Now = time.strftime("%a %b %d %I:%M:%S %z %Y",
                            time.localtime(time.time())                 )
        self.file.write(                "% Date: " + Now + "\n"         )

        #----Add package headers
        self.file.write(            "\\documentclass[" + docClassOpt
                                    + "]{" + docClass + "}\n"           )
        #----Add Default Packages
        self.file.write("\\usepackage{graphicx}\n"                      )
        self.file.write("\\usepackage{hyperref}\n"                      )
        self.file.write("\\usepackage{cooltooltips}\n"                  )
        self.file.write("\\usepackage[3D]{movie15}\n"                   )        

        if len(packages) != 0 and \
           type(packages) != types.TupleType and \
           type(packages) != types.ListType:
            packages = (packages, )

        if len(packages) != 0:
            for package in packages:
                if type(package) != types.StringType:
                    raise AcuReportError, "Invalid package " \
                          + repr(               package                 )
                self.file.write("\\usepackage"                          )
                optPack = package.split(":"                             )
                if len(optPack) >= 2:
                    self.file.write("[" + optPack[1] + "]"              )
                self.file.write("{" + optPack[0] + "}\n"                )

        if fullPage:
            self.file.write( "\\addtolength{\\oddsidemargin}{-.875in}\n" )
            self.file.write( "\\addtolength{\\evensidemargin}{-.875in}\n" )
            self.file.write( "\\addtolength{\\textwidth}{1.75in}\n" )
            self.file.write( "\\addtolength{\\topmargin}{-.875in}\n" )
            self.file.write( "\\addtolength{\\textheight}{1.75in}\n" )

        self.file.write(            "\\begin{document}\n"               )

        #----------------------------------------------------------------
        # Set required variables for conversion functions (eg WritePdf())
        # REPORT_BIN refers to the
        # base path of the bin directory containing the converters
        #----------------------------------------------------------------

        self.ACUSIM_ROOT = os.path.join( os.getenv( "ACUSIM_HOME", "" ),
                                         os.getenv( "ACUSIM_MACHINE", "" ),
                                         os.getenv( "ACUSIM_VERSION", "" ) )
  
        self.REPORT_BIN = os.path.join( self.ACUSIM_ROOT, "base", "bin" )     

        self.pdfw = 0
        self.rtfw = 0
        self.htmlw = 0
        self.closed = False

        self.isWin = ( os.name == 'nt' )

        #---- Default Package Setting
        
        self.modifyPackageOptions("hypersetup",
                                  optionMap={"pdfborder":"{0 0 0}"}     )

#---------------------------------------------------------------------------
# "close": Close the report and file
#---------------------------------------------------------------------------

    def close(self):
        '''Close the report and file.
        '''

        self.file.write(                    "\\end{document}\n"         )
        self.file.flush(                                                )
        self.file.close(                                                )
        self.closed = True

#---------------------------------------------------------------------------
# "addDate": Add date to the report
#---------------------------------------------------------------------------

    def addDate(self, date = None):

        '''Add date to the report.
        Argument:
            date - Date (eg., "09/17/2008")
        '''

	if date == None:
	    date = time.ctime(time.time())	

	#--------------------------------------------------------------------
        # Check for error
        #--------------------------------------------------------------------

        if type(date) != types.StringType:
            raise AcuReportError, "Invalid date " + repr(       date    )

        '''self.file.write(            "\\date{" + date + "}\n"            )'''

        self.addText( date, justify="center"                            )
        self.addSpace( )

#---------------------------------------------------------------------------
# "addTitle": Add the title of the document
#---------------------------------------------------------------------------

    def addTitle(self, title):

        '''Add title to the report.
        Argument:
            title - Title of the document (str)
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------

        if type(title) != types.StringType:
            raise AcuReportError, "Invalid title " + repr(      title   )

        '''self.file.write(        "\\title{" + title + "}\n"              )
        self.file.write(            "\\maketitle\n\\vfill\n"            )'''

        self.addText( title, justify="center", size="Large"             )
        self.addSpace( )

#---------------------------------------------------------------------------
# "addSpace": Add vertical space to the report
#---------------------------------------------------------------------------

    def addSpace(self, spaceSize = 1.0, unit = "mm" ):

        '''Add vertical space to the report.
        Argument:
            spaceSize - (opt) Space Size (default = 1.0 )
            unit - (opt) Unit of the size (default='mm' i.e. milimeter)
                    valid: cm, mm, in
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------
        if type(unit) != types.StringType:
            raise AcuReportError, "Invalid unit for \\\\[] space " \
                  + repr(                   unit                        )

        space = "\\vspace*{%.2f%s}\\hspace*{\\fill}\\\\\n" \
                % ( spaceSize, unit )

        self.file.write(    space                                       )

#---------------------------------------------------------------------------
# "addAuthors": Add a set of authors to the report
#---------------------------------------------------------------------------

    def addAuthors(self, *args):

        '''Add a set of authors to the report.
        Argument:
            *args - Name of authors (str)
        '''

        '''self.file.write(                    "\\author{"                 )'''
        authors = ''
        for author in args:

            #------------------------------------------------------------
            # Check for error
            #------------------------------------------------------------

            if type(author) != types.StringType:
                raise AcuReportError, "Invalid author " + repr( author  )

            authors += author + ", "

        if(authors.endswith(", ")):
            authors = authors[:authors.rindex(", ")]

        '''self.file.write(                    authors                     )
        self.file.write(                    "}\n"                       )'''

        self.addText( authors, justify="center" , size="large"          )
        self.addSpace( )

#---------------------------------------------------------------------------
# "newPage": Start a new page
#---------------------------------------------------------------------------

    def newPage(self):

        '''Start a new page.
        '''

        self.file.write(                    "\\vfill\n"                 )
        self.file.write(                    "\\newpage\n"               )
        self.file.write(                    "\\clearpage\n"             )

#---------------------------------------------------------------------------
# "fillVSpace": Push text to the end
#---------------------------------------------------------------------------

    def fillVSpace(self):

        '''Push text to the end.
        '''

        self.file.write(                    "\\vfill\n"                 )

#---------------------------------------------------------------------------
# "addSection": Add a section to the report
#---------------------------------------------------------------------------

    def addSection(self, title):

        '''Add a section to the report.
        Argument:
            title - Title of the section (str)
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------
        if type(title) != types.StringType:
                raise AcuReportError, "Invalid section title " \
                      + repr(               title                       )

        self.file.write(            "\\section{" + title + "}\n"        )

#---------------------------------------------------------------------------
# "addSubSection": Add a sub-section to the report
#---------------------------------------------------------------------------

    def addSubSection(self, title):

        '''Add a sub-section to the report.
        Argument:
            title - Title of the sub-section (str)
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------

        if type(title) != types.StringType:
                raise AcuReportError, "Invalid subsection title " \
                      + repr(               title                       )
        self.file.write(            "\\subsection{" + title + "}\n"     )

#---------------------------------------------------------------------------
# "addSubSubSection": Add a sub-sub-section to the report
#---------------------------------------------------------------------------

    def addSubSubSection(self, title, number = True):

        '''Add a sub-sub-section to the report.
        Argument:
            title - Title of the sub-sub-section (str)
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------

        if type(title) != types.StringType:
                raise AcuReportError, "Invalid subsubsection title " \
                      + repr(                   title                   )

        self.file.write(       "\\subsubsection{" + title + "}\n"       )

#---------------------------------------------------------------------------
# "addText": Add a text to the report
#---------------------------------------------------------------------------

    def addText(self, text, justify="flushleft", newLine=True, style=None,
                size=None):

        '''Add a text to the report.
        Argument:
            text    - Text to be added to the document (str)
            justify - (opt) Justify (default="flushleft")
                       valid: flushleft, flushright, center
            newLine - (opt) Add a new line after the text
                            if set as True (default=True)
            style   - Style of the text
                      valid: emph, textrm, textsf, texttt, textup, textit,
                      textsl, textsc, textbf, textmd, uline, uwave, sout
            size    - (opt) Text size (default=None)
                      valid: HUGE, Huge, LARGE, Large, large, small, tiny
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------

        if type(text) != types.StringType:
                raise AcuReportError, "Invalid text " + repr(   text    )
        if type(justify) != types.StringType:
                raise AcuReportError, "Invalid justify for text" \
                      + repr(               justify                     )
        if style and type(style) != types.StringType:
                raise AcuReportError, "Invalid style for text" \
                      + repr(                   style                   )

        if justify != "flushleft":
            self.file.write(            "\\begin{" + justify + "}\n"    )
        if style:
            self.file.write(            "\\" + style + "{ "             )
        if size:
             self.file.write("\\" + size + "{ \\textsc{ " + text + " }}")
        else:
            self.file.write(                    text                    )
        if style:
            self.file.write(                        " }"                )
        if(newLine == True):
            self.file.write(                        "\\\\\n"            )
        else:
            self.file.write(                        "\n"                )
        if justify != "flushleft":
            self.file.write(            "\\end{" + justify + "}\n"      )

#---------------------------------------------------------------------------
# "addImage": Add an image to the report
#---------------------------------------------------------------------------

    def addImage(self,   fileName,
                         justify    = 'center',
                         scale      = 1,
                         hasCaption = False ):

        '''Add an image to the report.
        Argument:
            fileName    - Image file name (str)
            justify     - (opt) Justify (default="center")
                          valid: flushleft, flushright, center
            scale       - (opt) Specify the image scale (default=1)
            hasCaption  - (opt) Leave the Justify block open if set as true
                           for adding the caption (default=False)
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------

        if type(fileName) != types.StringType:
                raise AcuReportError, "Invalid image fileName " \
                      + repr(               fileName                    )
        if justify != None and type(justify) != types.StringType:
                raise AcuReportError, "Invalid justify for image" \
                      + repr(               text                        )

        if justify != None:
            self.file.write(            "\\begin{" + justify + "}\n"    )

        result = _isImageValid( self.basePath,        fileName          )
        fileName = fileName.replace( "\\", "/"                          )

        # pdflatex and latex2rtf multiply scale by 1.33 by default and
        # it should be neutralized with the following statement
        scale = float(scale) / 1.33

        if(result == None):
            self.file.write(                "\\includegraphics"         )
            self.file.write(        "[scale=" + str(scale) + "]"        )
            self.file.write(            "{" + fileName + "}\n"          )
        else:
            self.addText(                   result                      )

        if(justify != None and not hasCaption):
            self.file.write(         "\\end{" + justify + "}\n"         )

#---------------------------------------------------------------------------
# "addFigure": Add a figure to the report
#---------------------------------------------------------------------------

    def addFigure( self, fileName,
                         justify    = 'center',
                         caption    = None,
                         scale      = 1,
                         ref        = None,
                         placement  = "default" ):

        '''Add a figure to the report.
        Argument:
            fileName - Image file name (str)
            justify - (opt) Justify (default="center")
                       valid: flushleft, flushright, center
            caption - (opt) Caption of the figure (default=None)
            scale - (opt) Specify the image scale (default=1)
            ref - (opt) Label of the figure for reference (default=None)
            placement - (opt) Specify the placement of the image (default = 'default' )
                        valid: here, force_here, top, force_top, bottom, force_bottom,
                        separate_page, force_separate_page
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------

        if type(fileName) != types.StringType:
                raise AcuReportError, "Invalid figure fileName "\
                      + repr(               fileName                    )

        if placement != None and type(placement) != types.StringType:
                raise AcuReportError, "Invalid placement for image" \
                      + repr(               text                        )

        if placement == 'here':
            placeText = 'h'
        elif placement == 'force_here':
            placeText = '!h'
        elif placement == 'top':
            placeText = 't'
        elif placement == 'force_top':
            placeText = '!t'
        elif placement == 'bottom':
            placeText = 'b'
        elif placement == 'force_bottom':
            placeText = '!b'
        elif placement == 'separate_page':
            placeText = 'p'
        elif placement == 'force_separate_page':
            placeText = '!p'
        else:
            placeText = '!h!tbp'

        self.file.write(        "\\begin{figure}[" + placeText + "]\n"  )
        self.addImage(      fileName, justify, scale, True              )
        self.file.write(                "\\caption{"                    )
        if(ref != None):
            self.file.write(            "\\label{" + ref + "}"          )
        if(caption != None):
            self.file.write(                    caption                 )
        self.file.write(                        "}\n"                   )

        if justify != None:
            self.file.write(                "\\end{" + justify + "}\n"  )

        self.file.write(                "\\end{figure}\n"               )

#---------------------------------------------------------------------------
# "addTabular": Add a tabular to the report
#---------------------------------------------------------------------------

    def addTabular( self, table,
                          justify       = 'center',                        
                          colsWidths    = None,
                          border        = True,
                          colHzJustify  = None,
                          colVtJustify  = None,
                          hasCaption    = False     ):

        '''Add a tabular to the report.
        Argument:
            table - A two dimensional list containing the table
                    rows and columns contents           
            justify - (opt) Justify (default="center")
                       valid: flushleft, flushright, center            
            colsWidths - (opt) List of column widths
                            in centimeter (default=None)
            border - (opt) Draw table borders if true (default=True)
            colHzJustify - (opt) The horizontal justification of columns(default = center)
                        valid: left, right, center
            colVtJustify - (opt) The vertical justification of columns(default = middle)
                        valid: top, bottom, middle
            hasCaption  - (opt) Leave the Justify block open if set as true
                           for adding the caption (default=False)
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------

        if justify != None and type(justify) != types.StringType:
                raise AcuReportError, "Invalid justify for image" \
                      + repr(               text                        )

        if justify != None:
            self.file.write(            "\\begin{" + justify + "}\n"    )

        if colHzJustify == 'center':
            colHzMarker = 'c'
        elif colHzJustify == 'left':
            colHzMarker = 'l'
        elif colHzJustify == 'right':
            colHzMarker = 'r'
        else:
            colHzMarker = 'l'

        if colVtJustify == 'middle':
            colVtMarker = 'm'
        elif colVtJustify == 'top':
            colVtMarker = 'p'
        elif colVtJustify == 'bottom':
            colVtMarker = 'b'
        else:
            colVtMarker = 'p'            

        self.file.write(                "\\begin{tabular}"              )

        if border:
            self.file.write(                    "{| "                   )
        else:
            self.file.write(                    "{ "                    )
        for i in range(len(table[0])):
            #---- width 0 means normal
            if colsWidths and i < len(colsWidths) and colsWidths[i]!= 0:
                self.file.write( colVtMarker + "{"
                                 + str(colsWidths[i]) + "cm} "          )        
            else:
                self.file.write(            colHzMarker + " "           )
            if border:
                self.file.write(                    "| "                )
        self.file.write(                            "}\n"               )
        if border:
            self.file.write(                    "\\hline\n"             )
        for row in table:
            for cell in row:
                if type(cell) != types.StringType:
                    self.file.write(            repr(cell)              )
                else:
                    self.file.write(                cell                )
                if cell != row[-1]:
                    self.file.write(" & ")
            self.file.write(                    " \\\\\n"               )
            if border:
                self.file.write(                    "\\hline\n"         )

        self.file.write(                    "\\end{tabular}\n"          )
        
        if(justify != None and not hasCaption):
            self.file.write(         "\\end{" + justify + "}\n"         )

#---------------------------------------------------------------------------
# "addTable": Add a table to the report
#---------------------------------------------------------------------------

    def addTable( self,	table,
    			caption         = None,
			justify         = 'center',                       
		      	ref             = None,
			colsWidths      = None,
			border          = True,
			placement       = "default",
                        colHzJustify    = None,
                        colVtJustify    = None      ):

        '''Add a table to the report.
        Argument:
            table - A two dimensional list containing the table
                    rows and columns contents
            caption - (opt) Caption of the table (default=None)
            justify - (opt) Justify (default="flushleft")
                       valid: flushleft, flushright, center      
            ref - (opt) Label of the table for reference (default=None)
            colsWidths - (opt) List of column widths
                            in centimeter (default=None)
            border - (opt) Draw table borders if true (default=True)
            placement - (opt) Specify the placement of the image (default = "default" )
                        valid: here, force_here, top, force_top, bottom, force_bottom,
                        separate_page, force_separate_page
            colHzJustify - (opt) The horizontal justification of columns(default = center)
                        valid: left, right, center
            colVtJustify - (opt) The vertical justification of columns(default = middle)
                        valid: top, bottom, middle
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------

        if type(caption) != types.StringType:
                raise AcuReportError, "Invalid table caption " \
                      + repr(                 caption                   )

        if placement != None and type(placement) != types.StringType:
                raise AcuReportError, "Invalid placement for image" \
                      + repr(               text                        )

        if placement == 'here':
            placeText = 'h'
        elif placement == 'force_here':
            placeText = '!h'
        elif placement == 'top':
            placeText = 't'
        elif placement == 'force_top':
            placeText = '!t'
        elif placement == 'bottom':
            placeText = 'b'
        elif placement == 'force_bottom':
            placeText = '!b'
        elif placement == 'separate_page':
            placeText = 'p'
        elif placement == 'force_separate_page':
            placeText = '!p'
        else:
            placeText = '!h!tbp'

        self.file.write(    "\\begin{table}[" + placeText + "]\n"       )
        
        self.addTabular( table, justify, colsWidths, border,
                         colHzJustify, colVtJustify, True               )
        
        self.file.write(                "\\caption{"                    )
        if(ref != None):
            self.file.write(          "\\label{" + ref + "}\n"          )
        if(caption != None):
            self.file.write(                    caption                 )
        self.file.write(                        "}\n"                   )

        if(justify != None):
            self.file.write(            "\\end{" + justify + "}\n"      )
            
        self.file.write(                "\\end{table}\n"                )

#---------------------------------------------------------------------------
# "addFigures": Add a table of figures to the report
#---------------------------------------------------------------------------

    def addFigures(	self,
    			table,
			justify = 'center',
			caption = None,
			scale = 1,
			ref = None,
			colsWidths = None,
			border = True,
			placement = "default" ):

        '''Add a table of figures to the report.
        Argument:
            table - The file names and labels of images (str)
            justify - (opt) Table justification (default="flushleft")
                       valid: flushleft, flushright, center
            caption - (opt) Caption of the figure (default=None)
            scale - (opt) Specify the image scale (default=1)
            ref - (opt) Label of the figure for reference (default=None)
            colsWidths - (opt) List of column widths
                            in centimeter (default=None)
            border - (opt) Draw table borders if true (default=True)
            placement - (opt) Specify the placement of the image (default = "default" )
                        valid: here, force_here, top, force_top, bottom, force_bottom,
                        separate_page, force_separate_page
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------

        if type(caption) != types.StringType:
                raise AcuReportError, "Invalid figure table caption " \
                      + repr(                 caption                   )

        if placement != None and type(placement) != types.StringType:
                raise AcuReportError, "Invalid placement for image" \
                      + repr(               text                        )

        if placement == 'here':
            placeText = 'h'
        elif placement == 'force_here':
            placeText = '!h'
        elif placement == 'top':
            placeText = 't'
        elif placement == 'force_top':
            placeText = '!t'
        elif placement == 'bottom':
            placeText = 'b'
        elif placement == 'force_bottom':
            placeText = '!b'
        elif placement == 'separate_page':
            placeText = 'p'
        elif placement == 'force_separate_page':
            placeText = '!p'
        else:
            placeText = '!h!tbp'

        self.file.write(    "\\begin{figure}[" + placeText + "]\n"      )
        if(justify != None):
            self.file.write(          "\\begin{" + justify + "}\n"      )

        self.file.write(                "\\begin{tabular}"              )

        if border:
            self.file.write(                    "{| "                   )
        else:
            self.file.write(                    "{ "                    )

        for i in range(len(table[0])):

            #---- width 0 means normal

            if colsWidths and i < len(colsWidths) and colsWidths[i]!= 0:
                self.file.write( "p{" + str(colsWidths[i]) + "cm} "     )
            else:
                self.file.write(                    "c "                )
            if border:
                self.file.write(                    "| "                )
        self.file.write(                            "}\n"               )
        if border:
            self.file.write(                    "\\hline\n"             )

        max = len(table[0])
        for row in table:
            if len(row) > max:
                max = len(row)

        for row in table:
            caps = " \\\\ "

            for cell in row:
                #---- Add figure
                self.addImage(  cell[0], None, scale, True              )
                if cell[1] != None:
                    caps =  caps + cell[1]

                if cell != row[-1]:
                    self.file.write(" & "                               )
                    caps =  caps + " & "

            for i in range(max - len(row)):
                    self.file.write(" & "                               )
                    caps =  caps + " & "

            self.file.write(             caps +        " \\\\\n"        )
            if border:
                self.file.write(                    "\\hline\n"         )

        self.file.write(                    "\\end{tabular}\n"          )

        self.file.write(                "\\caption{"                    )
        if(ref != None):
            self.file.write(          "\\label{" + ref + "}\n"          )
        if(caption != None):
            self.file.write(                    caption                 )
        self.file.write(                        "}\n"                   )

        if(justify != None):
            self.file.write(            "\\end{" + justify + "}\n"      )
        self.file.write(                "\\end{figure}\n"               )

#---------------------------------------------------------------------------
# "addEquation": Add a formal equation to the report
#---------------------------------------------------------------------------

    def addEquation(self, equation, ref = None):

        '''Add a formal equation to the report.
        Argument:
            equation - The equation in latex format
            ref - (opt) Label of the equation for reference (default=None)
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------

        if type(equation) != types.StringType:
                raise AcuReportError, "Invalid equation " \
                      + repr(               equation                    )

        self.file.write(                "\\begin{equation}\n"           )
        if(ref != None):
            self.file.write(                "\\label{" + ref + "}\n"    )
        self.file.write(                equation + "\n"                 )
        self.file.write(                "\\end{equation}\n"             )

#---------------------------------------------------------------------------
# "addInlineEquation": Add an inline equation to the report
#---------------------------------------------------------------------------

    def addInlineEquation(self, equation):

        '''Add an inline equation to the report.
        Argument:
            equation - The equation in latex format
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------
        if type(equation) != types.StringType:
                raise AcuReportError, "Invalid inline equation " \
                      + repr(               equation                    )

        self.file.write(            "$" + equation + "$\n"              )

#---------------------------------------------------------------------------
# "addTableOfContent": Add table of contents to the report
#---------------------------------------------------------------------------

    def addTableOfContent(self):

        '''Add table of contents to the report.
        '''

        self.file.write(                "\\tableofcontents\n"           )

#---------------------------------------------------------------------------
# "addBibliography": Add bibliography to the report
#---------------------------------------------------------------------------

    def addBibliography(self, title):

        '''Add bibliography to the report.
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------
        if type(title) != types.StringType:
                raise AcuReportError, "Invalid biblography title " \
                      + repr(                    title                  )

        self.file.write(        "\\bibliography{" + title + "}\n"       )

#---------------------------------------------------------------------------
# "beginBullet": Start a new bullet block in the report
#---------------------------------------------------------------------------

    def beginBullet(self):

        '''Start a new bullet block in the report.
        '''

        self.bulletsStack += 1
        self.file.write(                "\\begin{itemize}\n"            )

#---------------------------------------------------------------------------
# "endBullet": Close a bullet block in the report
#---------------------------------------------------------------------------

    def endBullet(self):

        '''Close a bullet block in the report.
        '''

        self.bulletsStack -= 1
        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------

        if(self.bulletsStack < 0):
            raise AcuReportError, "Several unmatched" \
                  + " bullets are existing in the document."
        else:
            self.file.write(                "\\end{itemize}\n"          )

#---------------------------------------------------------------------------
# "beginItemize": Start a new numbered block in the report
#---------------------------------------------------------------------------

    def beginItemize(self, indexType=""):

        '''Start a new numbered block in the report.
        Argument:
            indexType - (opt) Type of index (default="")
                        valid: arabic, alph, Alph, roman, Roman, fnsymbol
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------

        if type(indexType) != types.StringType:
                raise AcuReportError, "Invalid indexType " \
                      + repr(               indexType                   )

        self.itemsStack += 1
        if indexType != "":
            #----making the enumeration index as indexType
            self.file.write("\\renewcommand{\\theenumi}{\\"
                             + indexType + "{enumi}}\n"                 )
            self.file.write("\\renewcommand{\\labelenumi}{\\theenumi}\n")

        self.file.write(            "\\begin{enumerate}\n"              )

#---------------------------------------------------------------------------
# "endItemize": Close a numbered block in the report
#---------------------------------------------------------------------------

    def endItemize(self):

        '''Close a numbered block in the report.
        '''

        self.itemsStack -= 1
        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------

        if(self.itemsStack < 0):
            raise AcuReportError, "Several unmatched itemizes" \
                  + " are existing in the document."
        else:
            self.file.write("\\end{enumerate}\n")

        #----return to notmal index type

        self.file.write("\\renewcommand{\\theenumi}{\\arabic{enumi}}\n" )
        self.file.write("\\renewcommand{\\labelenumi}{\\theenumi}\n"    )

#---------------------------------------------------------------------------
# "addItem": Add an item to a bullet or numbered block in the report
#---------------------------------------------------------------------------

    def addItem(self, text, name = None):

        '''Add an item to a bullet or numbered block in the report.
        Argument:
            text - The item body content (str)
            name - (opt) The Item name or title next to bullet or number
                   (default=None)
        '''

        #----------------------------------------------------------------
        # Check for error
        #----------------------------------------------------------------
        if type(text) != types.StringType:
                raise AcuReportError, "Invalid item " + repr(   text    )
        if(self.itemsStack + self.bulletsStack <= 0):
            raise AcuReportError, "No itemize or enumerate" \
                  + " list has been opened."
        else:
             self.file.write("\\item{\\emph{" + str(name)
                              + "}}\n" + text + "\n"                    )

#---------------------------------------------------------------------------
# "modifyPackageOptions": Modify predefined package options
#---------------------------------------------------------------------------

    def modifyPackageOptions(self, package, optionMap):

        '''Modify predefined package options
        Argument:
            package - Package name (e.g., "hypersetup")
            optionMap - Key-value pairs of options
        '''

        self.file.write(            "\\" + package + "{"                )
        for opt in optionMap.keys():
            self.file.write(    opt + "=" + optionMap[opt] + " "        )
        self.file.write(                        "}\n"                   )

#---------------------------------------------------------------------------
# "rawLaTeX": Add an unformatted latex text to the report
#---------------------------------------------------------------------------

    def rawLaTeX(self, text):

        '''Add an unformatted latex text to the report.
        '''

        self.file.write(                    text + "\n"                 )

#---------------------------------------------------------------------------
# "_addLogo": Create and add a logo
#---------------------------------------------------------------------------

    def _addLogo( self,     logoKey,
                            logoName,
                            justify = 'center',
                            length  = 600,
                            dir     = 'Figures' ):

        if dir != "." and not dir.startswith( self.basePath ):
            imageName = self.basePath + "/" + dir + "/" + logoName
        else:
            imageName = dir + "/" + logoName

        format = os.path.splitext( imageName )[1][1:].upper(            )

        imageLength = acuLogo.getLogo( logoKey, imageName, format       )

        if imageLength == 0:
            raise AcuReportError, "Logo is corrupted."

        scale = float( length ) / imageLength

        self.addImage( imageName, justify, scale                        )

        return imageName
    
#---------------------------------------------------------------------------
# "addAcusimLogo": Add the Acusim Logo to the report
#---------------------------------------------------------------------------

    def addAcusimLogo( self,    justify = 'center',
                                length  = 400,
                                dir     = 'Figures' ):

        '''Add the Acusim Logo to the report.
        Argument:
            justify - logo justification
            length  - logo length
            dir     - image directory
        '''

        return self._addLogo( "acusim", "AcusimLogo.png",
                              justify, length, dir                      )

#---------------------------------------------------------------------------
# "addCFDCalcLogo": Add the CFDCalc Logo to the report
#---------------------------------------------------------------------------

    def addCFDCalcLogo( self,   justify = 'center',
                                length  = 400,
                                dir     = 'Figures' ): 

        '''Add the CFDCalc Logo to the report.
        Argument:
            justify - logo justification
            length  - logo length
            dir     - image directory
        '''

        return self._addLogo( "cfdcalc", "CFDCalcLogo.png",
                              justify, length, dir                      )

#---------------------------------------------------------------------------
# "convertUnit": Convert physical units
#---------------------------------------------------------------------------

    def convertUnit(self, quantity, fromUnit, toUnit):

        '''Convert physical units.
        Argument:
            quantity - physical quantity
            fromUnit - source unit
            toUnit   - destination unit
        '''

        if fromUnit == "rad/sec" and toUnit == "RMP":
            return quantity * 60 / ( 2 * math.pi )
        return quantity

#---------------------------------------------------------------------------
# "_getLatexPath": Set and Return the path to lalex
#---------------------------------------------------------------------------

    def _getLatexPath( self ):

        if self.isWin:
            cmd = os.path.join( self.REPORT_BIN, "miktex", "init.bat"   )
            if self.verbose > 1: print "Executing: " + cmd + "\n"
	    os.system( cmd )

	    path = os.path.join( self.REPORT_BIN,
                                 "miktex",
                                 "texmf",
                                 "miktex",
                                 "bin"                                  )
	    opt = "--silent"
	
	else:
            path = self.REPORT_BIN
            opt = "-interaction=batchmode -file-line-error"
	
        os.environ["PATH"] = os.environ["PATH"] + ";" + path

        return ( path, opt )

#---------------------------------------------------------------------------
# "writePdf": Convert the report to PDF format
#---------------------------------------------------------------------------

    def writePdf( self ):

        '''Convert the report to PDF format.
        '''

        if self.pdfw:
            return

        if not self.closed:
            self.close(                                                 )

        path, opt = self._getLatexPath(                                 )

        latexCmd = os.path.join( path, "latex" ) + \
                      ' %s -output-directory="%s" "%s" > "%s.con"' \
                      % ( opt, self.basePath, self.fileName, \
                          os.path.splitext(self.fileName)[0] )

        pdflatexCmd = os.path.join( path, "pdflatex" ) + \
                      ' %s -output-directory="%s" "%s"' \
                      % ( opt, self.basePath, self.fileName )              

        if self.verbose > 0: print "Converting to PDF using pdflatex..."

        if self.verbose > 1: print "Executing: " + latexCmd
        os.system( latexCmd                                             )

        if self.verbose > 1: print "Executing: " + pdflatexCmd
        os.system( pdflatexCmd                                          )   

        if self.verbose > 0: print "Convert to PDF done.\n"

        #----pdfw shows that the pdf is created once

        self.pdfw = 1

#---------------------------------------------------------------------------
# "writeHtml": Convert the report to HTML format
#---------------------------------------------------------------------------

    def writeHtml(self, credit = False):

        '''Convert the report to HTML format.
        Argument:
            credit    - (opt) Specify whether tth credit is to be existing
                        in html output or not (default=False)
        '''

        if self.htmlw:
            return

        if not self.closed:
            self.close(                                                 )

        self._getLatexPath(                                             )
        cmd = os.path.join( self.REPORT_BIN, "tth", "tth" ) + \
              ' -w0 -a -e2 "%s"' % self.fileName

        if self.verbose > 0: print "Converting to HTML using tth..."
        if self.verbose > 1: print "Executing: " + cmd
        os.popen( cmd ).close(                                          )
        _normalizeHtml( self.fileName,
                        os.path.splitext(self.fileName)[0] + ".html",
                        self.basePath,
                        credit                                          )
        if self.verbose > 0: print "Convert to HTML done.\n"

        #----htmlw shows that the html is created once

        self.htmlw = 1

#---------------------------------------------------------------------------
# "writeRtf": Convert the report to RTF format
#---------------------------------------------------------------------------

    def writeRtf(self):

        '''Convert the report to RTF format.
        '''

        if self.rtfw:
            return

        if not self.closed:
            self.close(                                                 )

        self._getLatexPath(                                             )

        cmd = os.path.join( self.REPORT_BIN, "latex2rtf" , "latex2rtf" ) + \
                            ' -d0 %s' % self.fileName

        if self.verbose > 0: print "Converting to RTF using latex2rtf..."
        if self.verbose > 1: print "Executing: " + cmd
        os.environ["RTFPATH"] = os.path.join( self.REPORT_BIN, "latex2rtf", "cfg" )
        os.popen( cmd ).close(                                          )
        if self.verbose > 0: print "Convert to RTF done.\n"

        #---rtfw shows that the rtf is created once

        self.rtfw = 1

#---------------------------------------------------------------------------
# "createAnimation": Create an animation from a set of images
#---------------------------------------------------------------------------

    def createAnimation(self,   type = "dir",
                                output = 'Figures/animation.gif',
                                delay = 10,
                                loop = 0,
                                images = list(),
                                dir = "Figures",
                                prefix = "*"):

        bin = os.path.join( self.ACUSIM_ROOT, "base", "ImageMagick", "convert" )

        bin += " -delay " + str(delay)
        bin += " -loop " + str(loop)

        if type == "dir":
            bin += " " + dir + "/*.*"
        elif type == "prefix":
            bin += " " + prefix
        elif type == "images":
            for img in images:
                bin += " " + img
        else:
            raise AcuReportError, "Invalid input type " + repr(   type  )

        bin += " " + output

        if self.verbose > 0: print 'Creating animation "%s"...' % output
        os.popen( bin )
        if self.verbose > 0: print 'Creating animation done.\n'

#---------------------------------------------------------------------------
# "addVideo": Add a video to the report
#---------------------------------------------------------------------------

    def addVideo(self,   video,
                         width      = "\\linewidth",
                         height     = "0.67\\linewidth",
                         justify    = "center"              ):
        
        video = video.replace(          "\\", "/"                       )

        if justify != None:
            self.file.write(            "\\begin{" + justify + "}\n"    )

        if width != "\\linewidth" and type( width ) != types.StringType:
            width = str( width / 1.33 ) + "pt"
        if height != "\\linewidth" and type( height ) != types.StringType:
            height = str( height / 1.33 ) + "pt"

        videoName = os.path.basename( video )

        self.file.write( "\\includemovie[\n" + \
                         "\tposter,\n" + \
                         "\ttoolbar, %same as `controls\n" + \
                         "\trepeat,\n" + \
                         "\tmouse,\n" + \
                         "\tlabel=" + videoName + ",\n" + \
                         "\ttext={\\small(Loading " + videoName + ")},\n" + \
                         "]{" + width + "}{" + height + "}" + \
                         "{" + video + "}\n"                            )

        if justify != None:
            self.file.write(            "\\end{" + justify + "}\n"      )


#---------------------------------------------------------------------------
# "_u3dCreator": Create a u3d model
#---------------------------------------------------------------------------

    def _u3dCreator( self,  sceneGraphs,
                            u3dFileName,
                            width,
                            height,
                            justify,
                            bgColor,
                            renderMode,
                            mergeMeshGroups         = True,
                            mergeMeshSets           = True,
                            regroupNodes            = True,
                            flattenDataTree         = True,
                            reduceMeshSets          = True,
                            addAnimationScripts     = False,
                            playMS                  = 500,
                            delayMS                 = 100,
                            speedFactor             = 1.2,
                            loopAnimation           = True,
                            animationControlList    = None,
                            displayTimeStepNum      = True,
                            displayGuideFootnote    = True,
                            createDisplayControl    = True,
                            fct                     = None  ):

        if u3dFileName == None:
            baseName =  os.path.splitext( os.path.basename( self.fileName ) )[0]
                        
            fileCont = 1
            newName = baseName
            while True:
                u3dFileName = os.path.join( "Figures", newName + '.u3d' )
                if not os.path.exists( u3dFileName ):
                    break
                newName = baseName + str( fileCont )
                fileCont += 1

        u3dFileName = u3dFileName.replace( "\\", "/"                    )

        converterObj = acuConvertU3D.saveAsU3d( sceneGraphs         = sceneGraphs,
                                                ivFileNames         = None,
                                                outputIdtfFileName  = None,
                                                outputU3dFileName   = u3dFileName,
                                                removeIdtf          = True,
                                                verbose             = self.verbose,
                                                mergeMeshGroups     = mergeMeshGroups,
                                                mergeMeshSets       = mergeMeshSets,
                                                regroupNodes        = regroupNodes,
                                                flattenDataTree     = flattenDataTree,
                                                reduceMeshSets      = reduceMeshSets,
                                                createDisplayControl= createDisplayControl,
                                                fct                 = fct )

        texString = acuConvertU3D.getTexString( converterObj        = converterObj,
                                                u3dFileName         = u3dFileName,
                                                width               = width,
                                                height              = height,
                                                justify             = justify,
                                                bgColor             = bgColor,
                                                renderMode          = renderMode,
                                                standAlone          = False,
                                                simple              = True,
                                                useBaseName         = False,
                                                addAnimationScripts = addAnimationScripts,
                                                playMS              = playMS,
                                                delayMS             = delayMS,
                                                speedFactor         = speedFactor,
                                                loopAnimation       = loopAnimation,
                                                animationControlList= animationControlList,
                                                displayTimeStepNum  = displayTimeStepNum,
                                                displayGuideFootnote= displayGuideFootnote,
                                                createDisplayControl= createDisplayControl )
        
        self.file.write( texString                                      )

#---------------------------------------------------------------------------
# "addU3DModel": Add a u3d model to the report
#---------------------------------------------------------------------------

    def addU3DModel( self, sceneGraph,
                           u3dFileName          = None,
                           width                = None,
                           height               = None,
                           justify              = None,
                           bgColor              = None,
                           renderMode           = None,
                           mergeMeshGroups      = True,
                           mergeMeshSets        = True,
                           regroupNodes         = True,
                           flattenDataTree      = True,
                           reduceMeshSets       = True,
                           displayGuideFootnote = True,
                           createDisplayControl = True,
                           fct                  = None  ):

        '''
            Add a u3d model to the report

            Arguments:
                sceneGraph	    - An instance of iv scene graph
                u3dFileName         - The u3d model file name
                width	            - The width of u3d model
                height	            - The height of u3d model
                justify	            - The justification of u3d model
                bgColor             - The background color of u3d model
                renderMode          - Render mode of the u3d model;
                                      Valid: outline, solid_outline,
                                             wireframe, solid_wire, point
                mergeMeshGroups     - Flag to merge group of mesh sets under
                                      a single group to a single mesh set
                mergeMeshSets       - Flag to merge mesh sets under
                                      a single group to a single mesh set
                regroupNodes        - Flag to put the nodes with the
                                      same name under a single group                                
                flattenDataTree     - Flag to flatten the data tree
                reduceMeshSets      - Flag to reduce the coordinate
                                      vectors of the of mesh sets
                displayGuideFootnote- Flag to specify whether the control's guide should be
                                      added as a footnote or not
                createDisplayControl- Create the display control node
                fct                 - Decimation level [default=None or 1.0 : no decimation]
        
            Output:
                None
        '''

        self._u3dCreator( sceneGraphs             = sceneGraph,
                          u3dFileName             = u3dFileName,
                          width                   = width,
                          height                  = height,
                          justify                 = justify,
                          bgColor                 = bgColor,
                          renderMode              = renderMode,
                          mergeMeshGroups         = mergeMeshGroups,
                          mergeMeshSets           = mergeMeshSets,
                          regroupNodes            = regroupNodes,
                          flattenDataTree         = flattenDataTree,
                          reduceMeshSets          = reduceMeshSets,
                          displayGuideFootnote    = displayGuideFootnote,
                          createDisplayControl    = createDisplayControl,
                          fct                     = fct )

#---------------------------------------------------------------------------
# "addU3DAnimation": Add a u3d animation to the report
#---------------------------------------------------------------------------

    def addU3DAnimation( self,  sceneGraphList,
                                u3dFileName         = None,
                                width               = None,
                                height              = None,
                                justify             = None,
                                bgColor             = None,
                                renderMode          = None,
                                mergeMeshGroups     = True,
                                mergeMeshSets       = True,
                                regroupNodes        = True,
                                flattenDataTree     = True,
                                reduceMeshSets      = True,                                
                                playMS              = 500,
                                delayMS             = 100,
                                speedFactor         = 1.2,
                                loopAnimation       = True,
                                animationControlList= None,
                                displayTimeStepNum  = True,
                                displayGuideFootnote= True,
                                createDisplayControl= True,
                                fct                 = None  ):

        '''
            Add a u3d animation to the report

            Arguments:
                sceneGraphList      - The list of iv scene graphs
                u3dFileName         - The u3d model file name
                width	        - The width of u3d model
                height	        - The height of u3d model
                justify	        - The justification of u3d model
                bgColor             - The background color of u3d model
                renderMode          - Render mode of the u3d model;
                                      Valid: outline, solid_outline,
                                             wireframe, solid_wire, point
                mergeMeshGroups     - Flag to merge group of mesh sets under
                                          a single group to a single mesh set
                mergeMeshSets       - Flag to merge mesh sets under
                                          a single group to a single mesh set
                regroupNodes        - Flag to put the nodes with the
                                          same name under a single group                                
                flattenDataTree     - Flag to flatten the data tree
                reduceMeshSets      - Flag to reduce the coordinate
                                          vectors of the of mesh sets          
                playMS              - Play interval per time-step in ms                
                delayMS             - Delay after each time-step in ms
                speedFactor         - Speed factor for faster and slower modes
                loopAnimation       - Flag to indicate whether the animation should loop or not
                animationControlList- The ordered list of animation controls;
                                      Valid keys in the list: "FirstStep", "StepBackward",
                                                              "PlayBackward", "Stop", "Pause",
                                                              "Play", "StepForward",
                                                              "LastStep", "Slower", "Faster"
                displayTimeStepNum  - Flag to specify whether the time-step number
                                      should be displayed or not
                displayGuideFootnote- Flag to specify whether the control's guide should be
                                      added as a footnote or not
                createDisplayControl- Create the display control node
                fct                 - Decimation level [default=None or 1.0 : no decimation]
                                      
            Output:
                None
       '''

        self._u3dCreator( sceneGraphs             = sceneGraphList,
                          u3dFileName             = u3dFileName,
                          width                   = width,
                          height                  = height,
                          justify                 = justify,
                          bgColor                 = bgColor,
                          renderMode              = renderMode,
                          mergeMeshGroups         = mergeMeshGroups,
                          mergeMeshSets           = mergeMeshSets,
                          regroupNodes            = regroupNodes,
                          flattenDataTree         = flattenDataTree,
                          reduceMeshSets          = reduceMeshSets,
                          addAnimationScripts     = True,
                          playMS                  = playMS,
                          delayMS                 = delayMS,
                          speedFactor             = speedFactor,
                          loopAnimation           = loopAnimation,
                          animationControlList    = animationControlList,
                          displayTimeStepNum      = displayTimeStepNum,
                          displayGuideFootnote    = displayGuideFootnote,
                          createDisplayControl    = createDisplayControl,
                          fct                     = fct )

#===========================================================================
# The class for AcuRepor exceptions
#===========================================================================

class AcuReportError( Exception ):

    """The class which handles acuReport exceptions.
    """

    def __init__( self, value ):
        self.value = "Error from AcuReport module: <%s> " % value

    def __str__( self ):
        return repr(                    self.value                      )

#===========================================================================
# Test the code
#===========================================================================

if __name__ == '__main__':
    tmpApp  = QApplication( sys.argv                                    )

    fileName = "report"
    doc = AcuReport(                        fileName                    )
    doc.addText(r'''
                You can put a long multi-line
                sentence here. '''                                      )
    doc.addImage(       'logo.jpg', justify='center', scale = 1         )
    doc.addFigure('flower.gif', caption = 'Image of a flower',
                   scale = 0.5, ref = 'fig:flower'                      )
    doc.addTable( (('City','Number of Cars'),('New York',5),('London',12)),
                  caption = 'number of cars cars available to us',
                  justify= 'center', ref = 'table:numcars'              )
    doc.addEquation( r'\rho u_{i,t} + \rho u_j u_{i,j}'
                    + r' = -p_{,i} + \tau_{ij,j} + \rho b_i',
                    ref='eqn:continuity'                                )
    doc.addBibliography(                    "reference"                 )
    doc.beginBullet(                                                    )
    doc.addItem(                        "A bullet"                      )
    doc.endBullet(                                                      )
    doc.beginItemize(                                                   )
    doc.addItem(                            "one"                       )
    doc.addItem(                            "two"                       )
    doc.endItemize(                                                     )
    doc.close(                                                          )
    doc.writePdf(                                                       )
