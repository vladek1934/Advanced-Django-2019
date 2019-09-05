from main.models import Image, Category, Folder
from main.Tools import dicomvert
import glob


# can be used to fix categories with some of the images missing. There has to be a category though.
def bulk_image():
    categories = Category.objects.all()
    for cat in categories:
        image_list = []
        selected_category = cat.id
        path = 'media/category_{0}/'.format(selected_category)
        for filename in glob.glob(path + '*.gif'):  # assuming gif
            filename = filename[len(path):]
            print(filename)
            image_list.append(filename)
        for filename in glob.glob(path + '*.png'):  # assuming png
            filename = filename[len(path):]
            print(filename)
            image_list.append(filename)
        for filename in glob.glob(path + '*.jpg'):  # assuming jpg
            filename = filename[len(path):]
            print(filename)
            image_list.append(filename)
        for filename in glob.glob(path + '*.jpeg'):  # assuming jpeg
            filename = filename[len(path):]
            print(filename)
            image_list.append(filename)
        for filename in glob.glob(path + '*.bmp'):  # assuming bmp
            filename = filename[len(path):]
            print(filename)
            image_list.append(filename)

        images = cat.images.all()
        imagesNames = []
        for i in images:
            imagesNames.append(i.file.name[len(path) - 6:])

        print(image_list)
        print(imagesNames)

        for i in imagesNames:
            image_list.remove(i)

        image_list.sort()
        for i in image_list:
            Image.objects.create(name='bulk_' + i, category=cat, file=path[6:] + i)

    return "done"


# file_edit.uploadDicoms("newcategory", r'C:\Users\Angi\Desktop\Summer\dicomms\1\NSCLC-RADIOMICS-INTEROBSERVER1\interobs05\02-18-2019-CT-90318\28629\\', "222")  - EXAMPLE

def uploadDicoms(categoryName, path, folderName):
    category = list(Category.objects.filter(name=categoryName))

    try:
        chosenfolder = Folder.objects.get(name=folderName)
        print('There is a folder with this name.')
    except:
        print('There is no folder with this name. Creating one')
        chosenfolder = Folder.objects.create(name=folderName,
                                             description="Standard blank description, you can change it later")

    if len(category) > 0:
        print('There is already category with this name.')
        return  

    category = Category.objects.create(name=categoryName, description=categoryName, folder=chosenfolder)

    output = 'media/category_{0}/'.format(category.id)
    dicomvert.convertDicoms(path, output)  # convert dicoms into jpg and place to media folder

    image_list = []
    for filename in glob.glob(output + '*.jpg'):  # assuming jpg
        filename = filename[len(output):]
        print(filename)
        image_list.append(filename)
    image_list.sort()
    for i in image_list:
        Image.objects.create(name=i, category=category, file=output[6:] + i)

    return "done"

# def uploadDicomsWin(categoryName, input):
#     category = list(Category.objects.filter(name=categoryName))
#     if (len(category) > 0):
#         print('There is already category with this name.')
#         return
#     category = Category.objects.create(name=categoryName, description=categoryName)
#
#     output = 'media\\category_{0}\\'.format(category.id)
#     dicomvert.convertDicoms(input, output)  # convert dicoms into jpg ang place to media folder
#
#     image_list = []
#     for filename in glob.glob(output + '*.jpg'):  # assuming jpg
#         filename = filename[len(output):]
#         print(filename)
#         image_list.append(filename)
#     image_list.sort()
#     for i in image_list:
#         Image.objects.create(name=i, category=category, file=output[6:] + i)
#
#     return "done"
