import cv2
import os
import pydicom


# base = 'C:\\Users\\Angi\\Desktop\\Summer\\dicomms\\1\\NSCLC-RADIOMICS-INTEROBSERVER1\\'
# inputdir = base + 'interobs34\\02-18-2019-CT-58112\\33129\\'
# outdir = inputdir + '..\\processed\\'


# EXAMPLE USE :
# dicomvert.run(r'C:\Users\Angi\Desktop\Summer\dicomms\1\NSCLC-RADIOMICS-INTEROBSERVER1\interobs05\02-18-2019-CT-90318\28629')

def sortDicoms(dicoms):
    n = len(dicoms)

    for i in range(n):
        for j in range(0, n - i - 1):
            if dicoms[j].data_element('InstanceNumber').value > dicoms[j + 1].data_element('InstanceNumber').value:
                dicoms[j], dicoms[j + 1] = dicoms[j + 1], dicoms[j]
    return dicoms


def convertDicoms(input, output):
    inputdir = str(input)
    outdir = str(output)
    test_list = [f for f in os.listdir(inputdir)]
    test_list.sort()
    os.mkdir(outdir)

    dicoms = []
    for f in test_list:  # remove "[:10]" to convert all images
        ds = pydicom.dcmread(inputdir + f)  # read dicom image
        dicoms.append(ds)

    dicoms = sortDicoms(dicoms)

    for i in range(len(dicoms)):
        img = dicoms[i].pixel_array * 0.125  # get image array
        cv2.imwrite(outdir + test_list[i].replace('.dcm', '.jpg'), img)  # write png image
