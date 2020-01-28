from django.shortcuts import render
from tethys_sdk.gizmos import TextInput
from tethys_sdk.gizmos import SelectInput
from django.http import JsonResponse

from pyproj import Proj, transform
import csv
import json
import os
import math


def home(request):
    """
    Controller for map page.
    """

    # Default value for name
    state = ''
    lat = ''
    lon = ''
    modelYear = ''
    returnPeriod = ''
    features = []

    # Define Gizmo Options
    select_state = SelectInput(
        display_text='State:',
        name='select_state',
        multiple=False,
        options=[
            ('Utah', 'Utah'),
            ('Alaska', 'Alaska'),
            ('Idaho', 'Idaho'),
            ('Montana', 'Montana'),
            ('South Carolina', 'South_Carolina'),
            ('Connecticut', 'Connecticut'),
        ],
        initial=['Utah', 'Utah']
    )

    text_input_lat = TextInput(
        display_text='Longitude',
        name='lat-input'
    )

    text_input_lon = TextInput(
        display_text='Latitude',
        name='lon-input'
    )

    select_modelYear = SelectInput(
        display_text='Model Year:',
        name='select_modelYear',
        multiple=False,
        options=[('2008', 2008), ('2014', 2014)],
        initial=['2008', 2008]
    )

    select_returnPeriod = SelectInput(
        display_text='Return Period:',
        name='select_returnPeriod',
        multiple=False,
        options=[('475', 475), ('1033', 1033), ('2475', 2475)],
        initial=['475', 475]
    )

    # Check form data
    if request.POST and 'lat-input' and 'lon-input' in request.POST:
        lat = request.POST['lat-input']
        lon = request.POST['lon-input']

    if request.POST and 'select_state' and 'select_modelYear' and 'select_returnPeriod' in request.POST:
        state = request.POST['select_state']
        modelYear = request.POST['select_modelYear']
        returnPeriod = request.POST['select_returnPeriod']

    # Pass variables to the template via the context dictionary
    context = {
        'state': state,
        'lat': lat,
        'lon': lon,
        'modelYear': modelYear,
        'returnPeriod': returnPeriod,
        'select_state': select_state,
        'text_input_lat': text_input_lat,
        'text_input_lon': text_input_lon,
        'select_modelYear': select_modelYear,
        'select_returnPeriod': select_returnPeriod
    }

    return render(request, 'lfhazard/map.html', context)


def documentation(request):
    return render(request, 'lfhazard/documentation.html', {})


def query_csv(request):
    """
    From the lon and lat interpolates from 4 of the closests points from a csv files,
    the LD, LS and SSD values.
    """

    result = {}
    dist11 = 10000
    dist12 = 10000
    dist21 = 10000
    dist22 = 10000
    # dist will contain the 2 closests distances from the coordinate put in.
    # LS files
    # Quadrant 1: dist [0,1]
    # Quadrant 2: dist [2,3]
    # Quadrant 3: dist [4,5]
    # Quadrant 4: dist [6,7]
    dist = [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]
    # quad_line_tracker will contain the values of the point closest to the
    # cooridnates put in.
    quad_line_tracker = [0, 0, 0, 0, 0, 0, 0, 0]
    # temp_numerator is a temporary variable for calcuations
    temp_numerator = 1
    # point_value will contain the calculated variables that will be
    # brought to the js file.
    point_value = []
    try:
        if request.method == 'POST':
            request_dict = json.loads(request.body)

            # These are all the values from the javascript

            print(request_dict)
            lon = float(request_dict['lon'])
            lat = float(request_dict['lat'])
            year = request_dict['year']
            state = request_dict['state']
            returnPeriod = request_dict['returnPeriod']

            # this finds the correct csv files given the parameters

            # path extentions
            LS_path = "LS-" + returnPeriod + '_States/LS-' + returnPeriod + '_' + state + '.csv'
            LT_path = "LT-" + returnPeriod + '_States/LT-' + returnPeriod + '_' + state + '.csv'
            SSD_path = "SSD-" + returnPeriod + '_States/SSD-' + returnPeriod + '_' + state + '.csv'
            path_extension = [LS_path, LT_path, SSD_path]

            # checks if path to the files is right
            temp_path = '/home/student/tethysdev/lf_hazard/' + year + '/'  # Local path
            print(temp_path + LS_path)
            if os.path.isfile(temp_path + LS_path) == True:
                csv_base_path = temp_path
                # print "local path: " + csv_base_path
            else:
                csv_base_path = '/lf_hazard/' + year + '/'  # Server
                # print "server path: " + csv_base_path

            # This part helps with telling if you are working on the local or serverpath
            print("Current Path: " + os.getcwd())
            if csv_base_path[:2] == "/h":
                print("Connected to Local path")
            elif csv_base_path[:2] == "/l":
                print("Connected to Server path")

            # This loops through the extensions, gets the right files and calculates.
            for extension in path_extension:
                csv_file_path = csv_base_path + extension
                ext = str(extension)
                print(csv_file_path)
                # This checks if file exists
                if os.path.isfile(csv_file_path) == True:
                    print("Is a file")
                    print("Now working on: " + csv_file_path)

                    with open(csv_file_path, 'r') as row:
                        next(row)  # this skips the first line
                        for line in row:
                            # print line
                            line = line.rstrip().split(',')
                            # This sets up the lat and lon read from csv file
                            temp_lon = float(line[0])
                            temp_lat = float(line[1])

                            # This tests for Quadrant one
                            if temp_lon >= lon and temp_lat >= lat:

                                # This calculates the distance between two points
                                temp_dist = math.sqrt(
                                    math.pow(abs(lon - temp_lon), 2) + math.pow(abs(lat - temp_lat), 2))

                                # This tests for the distance of point and sorts.
                                # This will store 2 points close to the coordinates.
                                if temp_dist <= dist[1]:
                                    dist[1] = temp_dist
                                    quad_line_tracker[1] = line
                                if (temp_dist <= dist[0] and temp_dist <= dist[1]):
                                    dist[1] = dist[0]
                                    dist[0] = temp_dist
                                    quad_line_tracker[1] = quad_line_tracker[0]
                                    quad_line_tracker[0] = line

                            # This test for Quadrant two
                            if temp_lon <= lon and temp_lat >= lat:

                                # This calculates the distance between two points
                                temp_dist = math.sqrt(
                                    math.pow(abs(lon - temp_lon), 2) + math.pow(abs(lat - temp_lat), 2))

                                # This tests for the distance of point and sorts.
                                # This will store 2 points close to the coordinates.
                                if temp_dist <= dist[3]:
                                    dist[3] = temp_dist
                                    quad_line_tracker[3] = line
                                if (temp_dist <= dist[2] and temp_dist <= dist[3]):
                                    dist[3] = dist[2]
                                    dist[2] = temp_dist
                                    quad_line_tracker[3] = quad_line_tracker[2]
                                    quad_line_tracker[2] = line

                            # This test for Quadrant three
                            if temp_lon <= lon and temp_lat <= lat:

                                # This calculates the distance between two points
                                temp_dist = math.sqrt(
                                    math.pow(abs(lon - temp_lon), 2) + math.pow(abs(lat - temp_lat), 2))

                                # This tests for the distance of point and sorts.
                                # This will store 2 points close to the coordinates.
                                if temp_dist <= dist[5]:
                                    dist[5] = temp_dist
                                    quad_line_tracker[5] = line
                                if (temp_dist <= dist[4] and temp_dist <= dist[5]):
                                    dist[5] = dist[4]
                                    dist[4] = temp_dist
                                    quad_line_tracker[5] = quad_line_tracker[4]
                                    quad_line_tracker[4] = line

                                    # This test for Quadrant four
                            if temp_lon >= lon and temp_lat <= lat:

                                # This calculates the distance between two points
                                temp_dist = math.sqrt(
                                    math.pow(abs(lon - temp_lon), 2) + math.pow(abs(lat - temp_lat), 2))

                                # This tests for the distance of point and sorts.
                                # This will store 2 points close to the coordinates.
                                if temp_dist <= dist[7]:
                                    dist[7] = temp_dist
                                    quad_line_tracker[7] = line
                                if (temp_dist <= dist[6] and temp_dist <= dist[7]):
                                    dist[7] = dist[6]
                                    dist[6] = temp_dist
                                    quad_line_tracker[7] = quad_line_tracker[6]
                                    quad_line_tracker[6] = line

                        # This part calculates the values.
                        print("***********")
                        if ext[:2] == "LS":
                            print("Working on LS file")

                            i = 0
                            temp_numerator = 0
                            temp_denominator = 0
                            LS_Dm_IDW = 0

                            # This loop sums up all the values and the distances for the IDW
                            # equation.
                            for i in range(8):
                                if dist[i] == 10000:
                                    continue
                                    # if((state == "Connecticut" and year == "2014") or (state == "connecticut" and year == "2014")):
                                    if ((year == "2014")):
                                        temp_numerator_add = float(quad_line_tracker[i][3]) / float(
                                            math.pow(dist[i], 2))
                                        temp_numerator = temp_numerator + temp_numerator_add
                                        temp_denominator_add = 1 / float(math.pow(dist[i], 2))
                                        temp_denominator = temp_denominator + temp_denominator_add
                                        LS_Dm_IDW = temp_numerator / temp_denominator
                                else:
                                    temp_numerator_add = float(quad_line_tracker[i][2]) / float(math.pow(dist[i], 2))
                                    temp_numerator = temp_numerator + temp_numerator_add
                                    temp_denominator_add = 1 / float(math.pow(dist[i], 2))
                                    temp_denominator = temp_denominator + temp_denominator_add
                                    try:
                                        LS_Dm_IDW = math.log(temp_numerator / temp_denominator, 10)
                                    except:
                                        LS_Dm_IDW = temp_numerator / temp_denominator
                                    print("LS_Dm_IDW: " + str(LS_Dm_IDW))
                            # This part appends the LS value to the point_value being sent
                            # to the Javascript.
                            point_value.append(LS_Dm_IDW)  # D value
                            # print "This is the LS Dm IDW: "+str(LS_Dm_IDW)

                        elif ext[:2] == "LT":
                            print("Working on LT file")
                            # i, place and v are values to help keep track in loop.
                            i = 0
                            place = 0
                            v = [2, 3]
                            # temp_numerator and temp_denominator are numerator and denominator
                            # of the IDW equation.
                            # LT_IDW[0]=Cetin value, LT_IDW[1]=CSR value.
                            LT_IDW = [0, 0]

                            for j in v:
                                temp_numerator = 0
                                temp_denominator = 0
                                for i in range(8):
                                    if dist[i] == 10000:
                                        continue
                                    temp_numerator_add = float(quad_line_tracker[i][j]) / float(math.pow(dist[i], 2))
                                    temp_numerator = temp_numerator + temp_numerator_add
                                    temp_denominator_add = 1 / float(math.pow(dist[i], 2))
                                    temp_denominator = temp_denominator + temp_denominator_add
                                LT_IDW[place] = temp_numerator / temp_denominator
                                place += 1

                            point_value.append(LT_IDW[0])  # Cetin value
                            point_value.append(LT_IDW[1])  # CSR value

                        elif ext[:2] == "SS":
                            print("Working on SSD file")

                            print("####################")
                            print("This is the 1st Quadrant")
                            print(" This is the 1st distance: " + str(dist[0]))
                            print(" This is the 2nd distance: " + str(dist[1]))
                            print(" This is the 1st line: " + str(quad_line_tracker[0]))
                            print(" This is the 2nd line: " + str(quad_line_tracker[1]))
                            print("This is the 2nd Quadrant")
                            print(" This is the 1st distance: " + str(dist[2]))
                            print(" This is the 2nd distance: " + str(dist[3]))
                            print(" This is the 1st line: " + str(quad_line_tracker[2]))
                            print(" This is the 2nd line: " + str(quad_line_tracker[3]))
                            print("This is the 3rd Quadrant")
                            print(" This is the 1st distance: " + str(dist[4]))
                            print(" This is the 2nd distance: " + str(dist[5]))
                            print(" This is the 1st line: " + str(quad_line_tracker[4]))
                            print(" This is the 2nd line: " + str(quad_line_tracker[5]))
                            print("This is the 4th Quadrant")
                            print(" This is the 1st distance: " + str(dist[6]))
                            print(" This is the 2nd distance: " + str(dist[7]))
                            print(" This is the 1st line: " + str(quad_line_tracker[6]))
                            print(" This is the 2nd line: " + str(quad_line_tracker[7]))
                            # i, place and v are values to help keep track in loop.
                            i = 0
                            place = 0
                            v = [2, 3, 4, 5]
                            # temp_numerator and temp_denominator are numerator and denominator
                            # of the IDW equation.
                            # SSD_IDW[0]=Cetin percent, SSD_IDW[1]=I&Y percent,
                            # SSD_IDW[2]=PBR&S, SSD_IDW[3]=PBR&T.
                            SSD_IDW = [0, 0, 0, 0]

                            for j in v:
                                temp_numerator = 0
                                temp_denominator = 0
                                for i in range(8):
                                    if dist[i] == 10000:
                                        continue
                                    temp_numerator_add = float(quad_line_tracker[i][j]) / float(math.pow(dist[i], 2))
                                    temp_numerator = temp_numerator + temp_numerator_add
                                    temp_denominator_add = 1 / float(math.pow(dist[i], 2))
                                    temp_denominator = temp_denominator + temp_denominator_add
                                if (temp_numerator == 0 and temp_denominator == 0):
                                    SSD_IDW[place] = 0
                                else:
                                    SSD_IDW[place] = temp_numerator / temp_denominator
                                place += 1

                            point_value.append(SSD_IDW[0])  # Cetin percent
                            point_value.append(SSD_IDW[1])  # I&Y percent
                            point_value.append(SSD_IDW[2])  # R&S
                            point_value.append(SSD_IDW[3])  # B&T

                        # Resets the variables dist and quad_line_tracker
                        dist = [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]
                        quad_line_tracker = [0, 0, 0, 0, 0, 0, 0, 0]
                        print("The end of the Line")
                else:
                    print("Is not a file")
                    if ext[:2] == "LS":
                        point_value.append("No Answer Yet")
                    elif ext[:2] == "LT":
                        point_value.append("No Answer Yet")
                        point_value.append("No Answer Yet")
                    elif ext[:2] == "SS":
                        point_value.append("No Answer Yet")
                        point_value.append("No Answer Yet")
                        point_value.append("No Answer Yet")
                        point_value.append("No Answer Yet")

            result["status"] = "success"
            print("These are the point_values")
            print(point_value)
            result["point_value"] = point_value
        else:
            raise Exception('not a post request!')

    except Exception as e:
        print(e.message)
        result["status"] = "error"
    finally:
        return JsonResponse(result)
