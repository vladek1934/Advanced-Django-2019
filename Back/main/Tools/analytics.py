import matplotlib

matplotlib.use('Agg')
from shapely.geometry import Polygon as ShapePolygon, MultiPolygon
import numpy
import itertools
import json
from shapely.ops import cascaded_union, polygonize
from main.models import Image, User, Category, Label, Polygon
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf


def imageLabelMatrix(users, imagePolygons):
    matrix = []
    for user1 in users:
        row = []
        myPolygons = [a for a in imagePolygons if (a.created_by_id == user1.id)]
        if (len(myPolygons) == 0):
            for user2 in users:
                if (user1.id != user2.id):
                    row.append(0)
                else:
                    row.append(1)
            matrix.append(row)
            continue
        myShapePolygons = []
        for i in range(len(myPolygons)):
            newshape = ShapePolygon(json.loads(myPolygons[i].points))
            if (not newshape.is_valid):
                newshape = newshape.exterior
            myShapePolygons.append(newshape)
        for user2 in users:
            if (user1.id != user2.id):
                otherPolygons = [a for a in imagePolygons if (a.created_by_id == user2.id)]
                if (len(otherPolygons) == 0):
                    row.append(0)
                    continue
                otherShapePolygons = []
                for i in range(len(otherPolygons)):
                    newshape = ShapePolygon(json.loads(otherPolygons[i].points))
                    if (not newshape.is_valid):
                        newshape = newshape.exterior
                    otherShapePolygons.append(newshape)
                union = cascaded_union(myShapePolygons + otherShapePolygons)
                intersection = cascaded_union(
                    [
                        ShapePolygon(json.loads(a.points)).intersection(ShapePolygon(json.loads(b.points)))
                        for a, b in list(itertools.product(myPolygons, otherPolygons))
                    ]
                )
                if (union.area == 0 or intersection.area == 0):
                    row.append(0)
                else:
                    row.append(intersection.area / union.area)
            else:
                row.append(1)
        matrix.append(row)
    # print(list(users))
    # for r in matrix:
    #     print(r)
    # print('\n')
    return matrix


def labelMatrices(images, users, allPolygons):
    data3d = []

    for image in images:
        imagePolygons = [a for a in allPolygons if (a.image_id == image.id)]
        data3d.append(imageLabelMatrix(users, imagePolygons))
    # print(data3d)
    return data3d


def fullMactrix(categoryId):
    users = list(User.objects.all())
    category = Category.objects.get(id=categoryId)
    images = list(category.images.all())
    labels = list(Label.objects.all())
    polygons = list(Polygon.objects.filter(image__category=categoryId))
    print('started')
    data4d = []
    i = 0

    # Remove 'dead' users, images, labels
    usedLabels = labels.copy()
    for label in labels:
        allPolygons = [a for a in polygons if (a.label_id == label.id)]
        if (len(allPolygons) <= 0):
            usedLabels.remove(label)

    usedImages = images.copy()
    for image in images:
        imagePolygons = [a for a in polygons if (a.image_id == image.id)]
        if (len(imagePolygons) <= 0):
            usedImages.remove(image)

    usedUsers = users.copy()
    for user in users:
        userPolygons = [a for a in polygons if (a.created_by_id == user.id)]
        if (len(userPolygons) <= 0):
            usedUsers.remove(user)

    users = usedUsers.copy()
    images = usedImages.copy()
    labels = usedLabels.copy()

    for label in labels:
        allPolygons = [a for a in polygons if (a.label_id == label.id)]
        i += 1
        # print('label {}/{}'.format(i, len(labels)))
        labeledImages = list(set([p.image for p in allPolygons]))  # Check only images in which this label is
        data4d.append(labelMatrices(labeledImages, users, allPolygons))

    ans = {
        'labels': list(labels),
        'images': list(images),
        'users': list(users),
        'data4d': data4d
    }
    # print(ans)
    return ans


def compressMatrix(data3d):
    ans = numpy.subtract(data3d[0], data3d[0])
    for data2d in data3d:
        ans = numpy.add(ans, data2d)
    ans = numpy.divide(ans, len(data3d))
    # print(ans)
    return ans


def compressAll(categoryId):
    data = fullMactrix(categoryId)
    data4d = data['data4d']
    ans3d = []
    if len(data4d) <= 0:
        print('No data')
        return
    for data3d in data4d:
        ans3d.append(compressMatrix(data3d))
    # print(ans3d)

    ans2d = compressMatrix(ans3d)

    mat = numpy.ones(len(ans2d)) - numpy.array(ans2d)
    # print(mat)
    dists = squareform(mat.astype(numpy.float32))
    if len(dists) <= 0:
        print('Not enough data')
        return
    linkage_matrix = linkage(dists, "single")
    f = plt.figure()
    dendrogram(linkage_matrix, labels=numpy.array(data['users']))
    plt.title("Distance metrics, with HAC, category {}".format(Category.objects.get(id=categoryId).name))
    # f.savefig("media/reports/category{}_report_{}.pdf".format(categoryId, Category.objects.get(id=categoryId).name),
    #           # bbox_inches='tight')
    pdf = matplotlib.backends.backend_pdf.PdfPages(
        "media/reports/category{}_report_{}.pdf".format(categoryId, Category.objects.get(id=categoryId).name))
    pdf.savefig(f)
    i = 0
    labels = data['labels']

    for labelarray in ans3d:
        mat = numpy.ones(len(labelarray)) - numpy.array(labelarray)
        # print(labelarray)
        dists = squareform(mat.astype(numpy.float32))
        linkage_matrix = linkage(dists, "single")
        f = plt.figure()
        dendrogram(linkage_matrix, labels=numpy.array(data['users']))
        plt.title("Distance metrics, with HAC, label {}".format(labels[i].name))
        pdf.savefig(f)
        i += 1

    pdf.close()

    return "media/reports/category{}_report_{}.pdf".format(categoryId, Category.objects.get(
        id=categoryId).name)


def fullAnalytics(categoryId):
    labels = Label.objects.all()
    data = []
    for label in labels:
        data.append({
            'label': label.id,
            'data': labelAnalytics(label, categoryId)
        })
    return data


def labelAnalytics(label: Label, categoryId):
    images = Category.objects.get(id=categoryId).images.all()
    data = []
    for image in images:
        data.append({
            'image': image.id,
            'data': imageLabelAnalytics(image, label)
        })
    return data


def imageLabelAnalytics(image: Image, label: Label):
    users = User.objects.all()
    data = []
    for user in users:
        data.append({
            'user': user.username,
            'data': userImageLabelAnalytics(image, user, label)
        })
    return data


def userAnalytics(user: User, label: Label):
    images = Image.objects.all()
    data = []
    for image in images:
        data.append({
            'image': image.id,
            'analytics': userImageAnalytics(image, user, label)
        })
    return data


def userImageLabelAnalytics(image: Image, user1: User, label: Label):
    myPolygons = list(image.polygons.filter(created_by=user1, label=label))
    myShapePolygons = []
    for i in range(len(myPolygons)):
        myShapePolygons.append(ShapePolygon(json.loads(myPolygons[i].points)))
    users = User.objects.all()
    table = [[user.username for user in list(users)]]
    table[0].remove(user1.username)
    row = []
    for user2 in users:
        if (user1.id != user2.id):
            otherPolygons = list(image.polygons.filter(created_by=user2, label=label))
            otherShapePolygons = []
            for i in range(len(otherPolygons)):
                otherShapePolygons.append(ShapePolygon(json.loads(otherPolygons[i].points)))
            union = cascaded_union(myShapePolygons + otherShapePolygons)
            intersection = cascaded_union(
                [
                    ShapePolygon(json.loads(a.points)).intersection(ShapePolygon(json.loads(b.points)))
                    for a, b in list(itertools.product(myPolygons, otherPolygons))
                    # if a.name == b.name
                ]
            )
            if (union.area == 0 or intersection.area == 0):
                row.append(0)
            else:
                row.append(float("{0:.3f}".format(intersection.area / union.area)))
    table.append(row)
    return [{'user': table[0][i], 'accuracy': table[1][i]} for i in range(len(table[0]))]
