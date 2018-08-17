# Importing all necessary packages.
import arcpy, configparser, os, sys, datetime

#_________________CONFIGPARSER_____________________________________________________
# The reason for the implementation of the configparser is to be able to change content of text elements in the map,
# without having to open the mxd and without having to mess around with the script.
# The desired text can simply be written into the configuration file.

# To execute the script, the program name must be always argument no. 1, at position 0.
programname = sys.argv [0]
# The program works only when at least two agruments were handed over (the python script and the configuration file).
# Else, an error message will be displayed and the program will be closed.
if len (sys.argv) < 2:
    # The error message:
    print ("Usage: " +programname+ " <config_file>")
    # Closing the program:
    raise SystemExit(1)

# The configuration file must be argument no. 2 at position 1.
configuration_file=sys.argv [1]

# Checks if the configuration file is in the right location. If not, an error message is displayed and the program is closed.
if os.path.isfile (configuration_file)==False:
    #The error message:
    print ("Error: Configuration file '"+configuration_file+"' not found.")
    # Closing the program:
    raise SystemExit(1)

config = configparser.RawConfigParser ()
# Opens and reads the configuration file.
config.readfp(open(configuration_file))

# Getting input from the configuration file and assigning it to variables.
conf_title=config.get("REFMAP","Title")
conf_desctext=config.get("REFMAP","DescText")
conf_mapname=config.get("REFMAP","MapName")
conf_version=config.get("LAYOUT","Version")
conf_vector=config.get("DATA","VectorData")
conf_projectpath=config.get("PATHS","Project")

#_________________MAP DOCUMENT & DATAFRAME_____________________________________________________

# Referencing the map document on which the program will act.
mxd=arcpy.mapping.MapDocument(conf_projectpath+"Project.mxd")

# Referencing the main dataframe and it's extent in the map document.
# Positions and extents are described in inches.
df=arcpy.mapping.ListDataFrames(mxd)[0]
df.elementHeight=11.7
df.elementWidth=10.96
df.elementPositionX=0.35
df.elementPositionY=3.7

# Referencing the overview dataframe and it's extent in the map document.
dfRef=arcpy.mapping.ListDataFrames(mxd)[1]
dfRef.elementHeight=2.25
dfRef.elementWidth=3.39
dfRef.elementPositionX=0.37
dfRef.elementPositionY=0.86


#_________________GRAPHIC ELEMENTS_____________________________________________________
# Graphic elements can't be created via arcpy.
# Therefore, two of the here referenced graphic elements (Header; LayotBar) were created within ArcMap.
# They can be addressed in the program by their name property which I gave them in ArcMap.
# The lower three elements are clones of the element "LayoutBar".

# Listing graphic elements.
graphElements=arcpy.mapping.ListLayoutElements(mxd,"GRAPHIC_ELEMENT")
# Looping through the list which holds the graphic elements.
for box in graphElements:

    if box.name=="Header":
        box.elementPositionX=-0.13
        box.elementPositionY=15.6
        headerHeight=box.elementHeight=0.6
        box.elementWidth=11.8

    if box.name=="LayoutBar":
        box.elementPositionX=0.36
        box.elementPositionY=3.25
        box.elementHeight=0.21
        box.elementWidth=3.42

        descrBox=box.clone("_Desc")
        descrBox.elementPositionX=3.95
        descrBox.elementPositionY=3.25

        dataBox=box.clone("_Data")
        dataBox.elementPositionX=3.95
        dataBox.elementPositionY=2.14

        legendBox=box.clone("_Legend")
        legendBox.elementPositionX=7.56
        legendBox.elementPositionY=3.25
        # I want this element to be a bit wider, so I set a different elementWidth.
        legendBox.elementWidth=3.76

#_________________TEXT ELEMENTS_____________________________________________________
# Like graphic elements, text elements can't be created via arcpy.
# But, an existing text element can be adressed by it's name property.
# This is useful, as text can be changed without opening the mxd and without having to know the exact wording of the text element.
# One way of changing text content via a python script would be to write the new text directly into the script,
# but in order to prevent the user from making unwanted changes, the configuration file can be opened and text content can be changed there.

# Listing text elements.
textElements=arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT")

# Looping through the list holding the text elements
for textbox in textElements:
    # The text in the text element named "Title" is exchanged with text from the configuration file by the variable conf_title.
    # It is not possible the change the font type of existing text elements via arcpy.
    # A workaround is to integrate some HTML code directly to the script, in order to change font types.
    if textbox.name=="Title":
        textbox.text='<FNT name="Calibri">'+conf_title+'</FNT>'
        textbox.fontSize=30.0
        textbox.elementPositionX=0.6
        textbox.elementPositionY=15.66

# The text displaying the production date is automatically updated to the present day when running the program.
    productionDate = datetime.date.today().strftime("PRODUCTION DATE: %d.%m.%Y")
    if textbox.name=='ProductionDate':
        textbox.text=productionDate
        textbox.fontSize=10
        textbox.elementPositionX=6.7
        textbox.elementPositionY=15.94

# Updating the mapname.
    if textbox.name=="MapName":
        textbox.text= '<FNT name="Calibri">'+"["+conf_mapname+"]"+'</FNT>'
        textbox.fontSize=25.0
        textbox.elementPositionX=2.85
        textbox.elementPositionY=15.7


# Updating the version number.
    if textbox.name=="Version":
        textbox.text='<FNT name="Calibri">'+conf_version+'</FNT>'
        textbox.fontSize=10
        textbox.elementPositionX=7.6
        textbox.elementPositionY=15.7

# Updating the description text.
    if textbox.name=="DescText":
        # Wrapping the description text in HTML to change the font type resulted in error messages.
        # This is because the description text includes line breaks.
        # Therefore, the font type of this element was set manually in ArcMap.
        textbox.text=conf_desctext
        textbox.elementPositionX=3.96
        textbox.elementPositionY=2.38
        textbox.elementHeight=0.84
        textbox.elementWidth=3.4

# Updating vector data sources.
    if textbox.name=="VectorData":
        # Same problem as with the description text - multiple lines wrapped in HTML result in errors.
        textbox.text=conf_vector
        textbox.fontSize=8
        textbox.elementPositionX=4.01
        textbox.elementPositionY=1.26
        textbox.elementHeight=0.83
        textbox.elementWidth=1.71

# Updating Service Layer Creadits.
    if textbox.name=="ServiceLayerCred":
        textbox.fontSize=7
        textbox.elementPositionX=5.70
        textbox.elementPositionY=1.12
        textbox.elementHeight=1.07
        textbox.elementWidth=1.53

# Updating CRS information
    if textbox.name=="CRS":
        textbox.elementPositionX=5.77
        textbox.elementPositionY=0.84
        textbox.elementHeight=0.40
        textbox.elementWidth=1.66

# Setting size and location of subheader "Location"
    if textbox.name=="Location":
        textbox.text='<FNT name="Calibri">'+"Loaction"+'</FNT>'
        textbox.fontSize=11
        textbox.elementPositionX=0.53
        textbox.elementPositionY=3.26

# Setting size and location of subheader "Description"
    if textbox.name=="Description":
        textbox.text='<FNT name="Calibri">'+"Description"+'</FNT>'
        textbox.fontSize=11
        textbox.elementPositionX=4.10
        textbox.elementPositionY=3.26

# Setting size and location of subheader "Legend"
    if textbox.name=="LegendHead":
        textbox.text='<FNT name="Calibri">'+"Legend"+'</FNT>'
        textbox.fontSize=11
        textbox.elementPositionX=7.71
        textbox.elementPositionY=3.26

# Setting size and location of subheader "Data"
    if textbox.name=="Data":
        textbox.text='<FNT name="Calibri">'+"Data"+'</FNT>'
        textbox.fontSize=11
        textbox.elementPositionX=4.13
        textbox.elementPositionY=2.16


#_________________PICTURE ELEMENTS_____________________________________________________

#Listing picture elements and setting it's size and location.
picElements=arcpy.mapping.ListLayoutElements(mxd,"PICTURE_ELEMENT")
for pic in picElements:
    if pic.name=="LogoSOS":
        pic.elementPositionX=8.98
        pic.elementPositionY=15.61
        pic.elementHeight=headerHeight
        pic.elementWidth=2.2
        pic.sourceImage= r"C:\Users\Linda\Desktop\Geoinformatik\Python\EOT\LogoSOS.JPG"

#_________________ADDING LAYERS_____________________________________________________

# Making a layer from a raster file.
popRaster = arcpy.MakeRasterLayer_management(conf_projectpath+"Data\\Worldpop_Uganda100mPopulation\\UGA_ppp_v2b_2015.tif")
popUganda = popRaster.getOutput(0)
arcpy.mapping.AddLayer(df, popUganda, "AUTO_ARRANGE")

# Listing layers.
lyr = arcpy.mapping.ListLayers(mxd, popUganda, df)[0]

# Loading the layer file which holds the symbology for the raster.
lyrPopRaster = arcpy.mapping.Layer(conf_projectpath+"Data\\UGA_ppp_v2b_2015.lyr")

# Updating the raster layer with the symbology from the layer file.
arcpy.mapping.UpdateLayer(df, lyr, lyrPopRaster, True)

# Checking the symbology type of the layer file.
if lyr.symbologyType == "RASTER_CLASSIFIED":
    # If it is the correct symbology type, the raster is reclassified.
    lyr.symbology.reclassify()

# Setting the value field text that is displayed in the legend.
lyr.symbology.valueField="Predicted no. of people per 100x100 grid cell"

# Setting the classbreak labels, which will later be displayed in the legend.
lyr.symbology.classBreakLabels = ["2 to 5", "6 to 10",
                                    "11 to 25", "Higher than 25"]

# Createing new layer objects from layer files.
adminUganda=arcpy.mapping.Layer(conf_projectpath+"Data\\g2008_1 selection.lyr")
lakes=arcpy.mapping.Layer(conf_projectpath+"Data\\ne_10m_lakes.lyr")
adminWorldBound=arcpy.mapping.Layer(conf_projectpath+"Data\\AdminBoundariesDissolvedBound.lyr")
adminWorld=arcpy.mapping.Layer(conf_projectpath+"Data\\AdminBoundariesDissolved.lyr")
basemap=arcpy.mapping.Layer(conf_projectpath+"Data\\basemap.lyr")
RefMapWorld=arcpy.mapping.Layer(conf_projectpath+"Data\\RefMapWorld.lyr")

# Updating the legend element which was created manually in ArcMap.
legend=arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", "Legend")[0]

# These layers will be added to the legend automatically.
legend.autoAdd = True
# Add the layer to the map at the top/bottom of the TOC in dataframe 0.
arcpy.mapping.AddLayer(df, adminUganda,"TOP")
arcpy.mapping.AddLayer(df, lakes,"BOTTOM")
arcpy.mapping.AddLayer(df, adminWorldBound,"BOTTOM")
arcpy.mapping.AddLayer(df, basemap,"BOTTOM")

# This layer I don't want in the legend, so autoAdd is set to False.
legend.autoAdd = False
arcpy.mapping.AddLayer(df, adminWorld,"BOTTOM")

# Adding a layer to the overview dataframe.
arcpy.mapping.AddLayer(dfRef, RefMapWorld,"AUTO_ARRANGE")


# Creating a list of all added layers, looping through them and assigning names which will later be displayed in the legend.
layers = arcpy.mapping.ListLayers(mxd)
for lyr in layers:
    if lyr.name == "AdminBoundariesDissolved":
        lyr.name = "Country Borders"

    if lyr.name == "ne_10m_lakes":
        lyr.name = "Lakes"

    if lyr.name == "g2008_1 selection":
        lyr.name = "Administrative Boundaries within Uganda"

    if lyr.name == "UGA_ppp_v2b_2015.tif":
        print lyr.name
        lyr.name = "Predicted no. of people per 100x100 grid cell"

#_________________LAYOUT ELEMENTS_____________________________________________________

# Repositioning the scalebar.
# The MapsurroundElement class does not offer to change many more properties of an element other than it's size, position or parent dataframe.
# Therefore, I designed a scalebar within ArcMap and named it "UgandaScaleBar", so it can be addressed in the script.
scaleBar = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "UgandaScaleBar")
for scale in scaleBar:
    scale.elementPositionX=4.0
    scale.elementPositionY=0.86
    scale.elementHeight=0.23
    scale.elementWidth=1.82
    scale.parentDataFrame=df

# Updating the legend.
# The legend items will be displayed in two rows.
legend.adjustColumnCount(2)
legend.elementPositionX=7.63
legend.elementPositionY=1.85
legend.elementHeight=1.3
legend.elementWidth=3.4
legend.title=" "
legend.parentDataFrame=df


#_________________SAVE COPY & EXPORT PDF_____________________________________________________
# All the changes made by the script will be saved as a copy of the original mxd.
copy=conf_projectpath+"ProjectCopy.mxd"
mxd.saveACopy(copy)
#arcpy.RefreshActiveView()

# A PDF of the copy will be created in the project folder.
# If a PDF with the same name already exists, it will be deleted and replaced by the new one.
pdfPath = conf_projectpath+"FinalMap.pdf"
if os.path.exists(pdfPath):
    os.remove(pdfPath)
arcpy.mapping.ExportToPDF(mxd, pdfPath)
print "done"

#_________________CLEAN UP_____________________________________________________
del df
del mxd