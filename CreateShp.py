import ogr
import os


# read txt and return a filename list
def readFile(filename):
    f = open(infile, 'r')
    lines = f.readlines()
    pointFilenameList = []

    for line in lines:
        pointFilenameList.append(line)

    return pointFilenameList


# input filename list and create point shape file
def createShp(pointFilenameList):
    # define list to restore x y coor and filename
    filename = []
    pointListX = []
    pointListY = []

    # register a driver
    driver = ogr.GetDriverByName('ESRI Shapefile')
    # outfile name
    outfile = 'point.shp'

    for line in pointFilenameList:
        sensor = line.split('.')[-3].split('-')[-1][0:-1]
        if sensor == 'MSS':
            y = line.split('_')[2][1:]
            x = line.split('_')[3][1:]

            pointListX.append(x)
            pointListY.append(y)
            filename.append(line)

    if os.path.exists(outfile):
        driver.DeleteDataSource(outfile)

    # create shape file
    outDS = driver.CreateDataSource(outfile)
    if outDS is None:
        print('Cannot open this file: ', outfile)

    # create layer
    outLayer = outDS.CreateLayer('point', geom_type=ogr.wkbPoint)

    # create fields
    fieldDefn1 = ogr.FieldDefn('filename', ogr.OFTString)
    fieldDefn1.SetWidth(60)
    outLayer.CreateField(fieldDefn1, 1)

    fieldDefn2 = ogr.FieldDefn('X', ogr.OFTString)
    fieldDefn2.SetWidth(4)
    outLayer.CreateField(fieldDefn2, 1)

    fieldDefn3 = ogr.FieldDefn('Y', ogr.OFTString)
    fieldDefn3.SetWidth(5)
    outLayer.CreateField(fieldDefn3, 1)

    # get feature defintion
    outFeatureDefn = outLayer.GetLayerDefn()

    # write every point to shape file
    for i in range(len(pointListX)):
        outFeature = ogr.Feature(outFeatureDefn)
        wkt = "POINT(%f %f)" % (float(pointListX[i]), float(pointListY[i]))
        point = ogr.CreateGeometryFromWkt(wkt)
        outFeature.SetGeometry(point)
        outFeature.SetField('filename', filename[i])
        outFeature.SetField('X', pointListX[i])
        outFeature.SetField('Y', pointListY[i])
        outLayer.CreateFeature(outFeature)
        outFeature.Destroy()

    outDS.Destroy()


if __name__ == '__main__':
    os.chdir('E:')
    infile = 'filelist.txt'
    namelist = readFile(infile)
    createShp(namelist)

    print('Success!')
