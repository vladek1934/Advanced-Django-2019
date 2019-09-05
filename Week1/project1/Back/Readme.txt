This txt file is a small manual for the administrator of this software.
This software is provided as is, under a License of its creators.

The main parts of the project are:

1)Urls,py, which receives the calls and returns views, thus providing an API functionality
2)Serializers.py, which integrate the models into the django database manipulations
3)models.py, which contains all of the models. All of them are custom, except for the User class which was built-in into the Django already
4)admin.py is just a file which allows us to change the database models display settings inside the Django admin panel.
For example, you can remove a few displayed fields if you deem that needed. The database will not be affected by that.

Basic structure of the database -  Folders have categories, which in turn have photos attached to them. The Categories have permissions.
Photos have 2 basic subdivisions - comments section and the polygons section. For more information, check out the models.py in the 'main' folder.

Views package:
Responsible for all of the functions/views which the urls.py uses. Importing is performed by using an init.py which initializes all the views.

    Analytics.py:
    A view which is  linked to the serializer, which then calls to the analytics.py of the TOOLS package.
    Auth.py:
    Handles authentication (login, logout) using a system of token saving
    Generic.py:
    All of the other accessing methods to the listing of models, with filters and permissions. Basically all of the daily database queries.

Tools package:
A package which contains all of the administrative commands which have to be imported to your python command line to function.
Example: 'python3 manage.py shell' -> 'from main.Tools import analytics' (used to generate pdf report on the particular category.)
                                        ->'analytics.compressAll(1)' - creates a report on the category 1.
                                        It (category) has to exist and also there has to be more than 1 person
                                        who created a polygon in this category. If there are none/only 1 person who performed
                                        marking in this category, the pdf does not generate and the front side gives out an error.

                                   -> 'from main.Tools import file_edit'
                                        ->file_edit.uploadDicoms(categoryName, pathToDicoms, folderName)
                                            categoryName - String. Name of the category, that will be created to store this images.
                                                           You cannot use existing categories
                                            pathToDicoms - String. Path to dicom files (careful with formatting)
                                            folderName - String. Name of the folder where category should be.
                                                         You can use existing folder or create a new one

                                            #This command will create new category in given folder,
                                             convert all dicoms in the given path into .jpg format
                                              and upload them to this category.#

                                            EXAMPLE:
                                                file_edit.uploadDicoms("Patient_Ivan", "C:\\dicomms\\", "Lungs")

                                   ->file_edit.bulk_image()
                                         #This command will simply parse through all of the categories, and append each
                                         of the images which are situated in the respected folders#

                                         Example - you have many simple jpg pictures which need to be uploaded as a category.
                                         Steps:1)create a category inside the database via the Djnago admin panel.
                                         2)create a folder with the same id as the newly created category (or upload 1 image there so that the
                                         folder is created automatically)
                                         3)Put all of your images inside the folder.
                                         4)Run the file_edit.bulk_image() command to automatically bind the images to the categories.

                                         DONE! Good job!