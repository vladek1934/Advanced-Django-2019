# DRF-based markup system

This software is provided as is, under a License of its creators.

## Short description

The main parts of the project are:

1)Urls,py, which receives the calls and returns views, thus providing an API functionality
2)Serializers.py, which integrate the models into the django database manipulations
3)models.py, which contains all of the models. All of them are custom, even the User clss was extended to facilitate small changes and having a bigger control over the database tables
4)admin.py is just a file which allows us to change the database models display settings inside the Django admin panel.
For example, you can remove a few displayed fields if you deem that needed. The database will not be affected by that.

Views package:
Responsible for all of the functions/views which the urls.py uses. Importing is performed by using an init.py which initializes all the views. Has both of the Api views, and viewsets split for the better readability.

##Further help
Additional information can be acquired by running the server and opening a localhost:8000/api/help url in the browser. But before doing this, you have to login with a django superuser in the :8000/admin panel