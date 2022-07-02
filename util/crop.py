# import pakages
from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import tqdm 
import pandas as pd
import cv2
import glob

# def crop_by_coords
def crop_by_coords(tif, lat, lon, scale):
    return gdal.Translate('new.tif', tif, projWin = [lon-scale, lat+scale, lon+scale, lat-scale])

def crop_korea(tif):
    return gdal.Translate('new.tif', tif, projWin = [125, 40, 131, 32])


    



if __name__ == "__main__":
    # /https://www.geeksforgeeks.org/visualizing-tiff-file-using-matplotlib-and-gdal-using-python/
    dataset = gdal.Open(r'EOGimages/SVDNB_npp_d20220622.rade9d.tif')
    #https://gis.stackexchange.com/questions/203664/clipping-tiff-raster-image-using-bounding-box-with-gdal-in-python

    ds = gdal.Translate('new.tif', dataset, projWin = [125, 40, 131, 32])
    # print(dataset.RasterCount)

    band1 = ds.GetRasterBand(1)

    b1 = band1.ReadAsArray()

    upper = 50
    lower = 0

    b1 = np.where(b1>upper ,upper,b1)
    b1 = np.where(b1<lower, lower, b1)

    b1 = b1/(upper-lower)

    f = plt.figure()  
    plt.imshow(b1)
    plt.show()

    # plt.hist(b1, bins=upper, range = [lower, upper])

    print(b1)

    # hist = cv2.calcHist([b1*upper], [0], None, [upper], [lower, upper])
    # print(hist)
    # plt.plot(hist)
    # plt.show()

