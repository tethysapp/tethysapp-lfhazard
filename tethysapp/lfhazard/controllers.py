from django.shortcuts import render
from tethys_sdk.gizmos import TextInput
from tethys_sdk.gizmos import SelectInput
from django.http import JsonResponse

import json
import os
import math

from .app import LiquefactionHazardApp as App


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

    # Define Gizmo Options
    select_model = SelectInput(
        display_text='Model Type:',
        name='select_model',
        multiple=False,
        options=(('SPT (Standard Penetration Test)', 'spt'), ('CPT (Cone Penetration Test)', 'cpt')),
        initial=('SPT (Standard Penetration Test)', 'spt'),
    )
    select_year = SelectInput(
        display_text='Model Year:',
        name='select_year',
        multiple=False,
        options=[(2008, 2008), (2014, 2014)],
        initial=[(2008, 2008)]
    )
    select_return_period = SelectInput(
        display_text='Return Period:',
        name='select_return_period',
        multiple=False,
        options=[('475', 475), ('1033', 1033), ('2475', 2475)],
        initial=['475', 475]
    )
    select_state = SelectInput(
        display_text='State:',
        name='select_state',
        multiple=False,
        options=[
            ('Alaska', 'Alaska'),
            ('Connecticut', 'Connecticut'),
            ('Idaho', 'Idaho'),
            ('Montana', 'Montana'),
            ('Oregon', 'Oregon'),
            ('South Carolina', 'South_Carolina'),
            ('Utah', 'Utah'),
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

    context = {
        'select_model': select_model,
        'select_year': select_year,
        'select_return_period': select_return_period,
        'select_state': select_state,
        'text_input_lat': text_input_lat,
        'text_input_lon': text_input_lon,
    }

    return render(request, 'lfhazard/home.html', context)


def get_geojson(request):
    state = str(request.GET.get('state', 'utah')).lower().replace(' ', '')
    with open(os.path.join(App.get_app_workspace().path, 'state_geojson', f'{state}.geojson'), 'r') as gj:
        return JsonResponse(json.loads(gj.read()))


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
    # temp_numerator is a temporary variable for calculations
    temp_numerator = 1
    # point_value will contain the calculated variables that will be
    # brought to the js file.
    point_value = []
    try:
        lon = float(request.GET['lon'])
        lat = float(request.GET['lat'])
        year = request.GET['year']
        state = request.GET['state']
        returnPeriod = request.GET['returnPeriod']
        model = request.GET['model']

        csv_base_path = os.path.join(App.get_app_workspace().path, model)

        # path extentions
        LS_path = "LS-" + returnPeriod + '/LS-' + returnPeriod + '_' + state + '.csv'
        LT_path = "LT-" + returnPeriod + '/LT-' + returnPeriod + '_' + state + '.csv'
        SSD_path = "SSD-" + returnPeriod + '/SSD-' + returnPeriod + '_' + state + '.csv'
        path_extension = [LS_path, LT_path, SSD_path]

        print(csv_base_path)

        # This loops through the extensions, gets the right files and calculates.
        for extension in path_extension:
            csv_file_path = os.path.join(csv_base_path, year, extension)
            ext = str(extension)
            print(csv_file_path)
            # This checks if file exists
            if os.path.isfile(csv_file_path):
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
                            if temp_dist <= dist[0] and temp_dist <= dist[1]:
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
                            if temp_dist <= dist[2] and temp_dist <= dist[3]:
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
                            if temp_dist <= dist[4] and temp_dist <= dist[5]:
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
                            if temp_dist <= dist[6] and temp_dist <= dist[7]:
                                dist[7] = dist[6]
                                dist[6] = temp_dist
                                quad_line_tracker[7] = quad_line_tracker[6]
                                quad_line_tracker[6] = line

                    # This part calculates the values.
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
                                if year == "2014":
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
        result["point_value"] = point_value
    except Exception as e:
        print(e)
        result["status"] = "error"
    finally:
        return JsonResponse(result)
