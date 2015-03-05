var destFolder, sourceFolder, files, fileType, sourceDoc, targetFile, pngExportOpts;
// Select the source folder
sourceFolder = Folder.selectDialog( 'Select the folder with DXF files you want to convert to .eps', '~' );
// If a valid folder is selected
if ( sourceFolder != null )
{
    files = new Array();
    fileType = '*.dxf';

    var options = new EPSSaveOptions();
    options.embedLinkedFiles = false;
    options.embedAllFonts = false;
    options.includeDocumentThumbnails = true;
    options.saveMultipleArtboards = false;

    // Get all files matching the pattern
    files = sourceFolder.getFiles( fileType );
    if ( files.length > 0 )
    {

    // Get the destination to save the files
        destFolder = Folder.selectDialog( 'Select the folder where you want to save the converted EPS files, Be prepared to spam Enter.', '~' );
        for ( i = 0; i < files.length; i++ )
        {
            sourceDoc = app.open(files[i]); // returns the document object

            setArtBoardSize(790,384);

            // Call function getNewName to get the name and file to save the eps
            targetFile = getNewName();
            // Export as eps
            sourceDoc.saveAs( targetFile, options );
            sourceDoc.close(SaveOptions.DONOTSAVECHANGES);
        }
    }
    else
    {
        alert( 'No matching files found' );
    }
}


/*********************************************************
 setArtBoardSize: Function to set the size of the artboard to the default
**********************************************************/
function setArtBoardSize(width, height) {
    var idoc = app.activeDocument;  
    var newAB = idoc.artboards[0];

    var iartBounds = idoc.visibleBounds;  
    
    var ableft = iartBounds[0];  
    var abtop = iartBounds[1];  
    
    // Adobe only accepts width and height in points, so we multiply by a magic number to convert from mm to points:
    var newWidth = new UnitValue(width, "mm");
    var newHeight = new UnitValue(height, "mm");

    // for some reason, heights need to be negative
    newAB.artboardRect = [ableft, abtop, newWidth.as("px")+ableft, -newHeight.as("px")+abtop];
}

/*********************************************************
  getNewName: Function to get the new file name. The primary
  name is the same as the source file.
**********************************************************/
function getNewName()
{
    var ext, docName, newName, saveInFile, docName;
    docName = sourceDoc.name;
    ext = '.png'; // new extension for png file
    newName = "";
    for ( var i = 0 ; docName[i] != "." ; i++ )
    {
        newName += docName[i];
    }
    newName += ext; // full png name of the file
    // Create a file object to save the png
    saveInFile = new File( destFolder + '/' + newName );
    return saveInFile;
}
