I want to build a tool to organise, tag and search for PDF files on disk.

The tool should have a GUI.

The tool should run locally on Linux and on Windows.

The tool should be packaged as an executable that is located in the same directory as the PDFs in question. PDFs outside this directory are out of scope.

The tool should allow me to link PDFs to it, by allowing me to browse through the device directory and select a file. When a file is selected, this should create a record of it in the tool's database. I should then be able to edit that database record to add tags, a description of the file, and so on. The database record should include a title field which should be taken from the filename of the PDF on disk.

The PDF itself should not be copied into the tool's database, but should remain on the device disk where it was originally. The tool's database should contain a link to the file's location, which will then allow a user to navigate to that file from the GUI when viewing that file's record in the GUI.

The tool should work such that if the entire directory which contains it, along with all the PDFs, is copied elsewhere on disk, everything still works.

If the tool has a record for a given PDF, but cannot then locate the PDF on disk, it should show an appropriate error.

I should be able to delete records of PDFs without deleting the file on disk.

I should be able to add and remove tags from each record of a PDF, and I should be able to add and remove tags from the list of tags.