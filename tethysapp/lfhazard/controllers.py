from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .model import SessionMaker, StreamGage
from tethys_sdk.gizmos import MapView, MVLayer, MVView
from tethys_sdk.gizmos import TextInput
from tethys_sdk.gizmos import SelectInput
from django.http import JsonResponse

from pyproj import Proj, transform
import csv
import json
import os
import math

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    context = {}

    return render(request, 'lfhazard/home.html', context)


@login_required()
def map(request):
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
    select_state = SelectInput(display_text='State:',
                            name='select_state',
                            multiple=False,
                            options=[('Utah', 'Utah'), ('Alaska', 'Alaska'), ('Idaho', 'Idaho'), ('Montana', 'Montana'), ('Oregon', 'Oregon'), ('South Carolina', 'South_Carolina'), ('Connecticut', 'Connecticut'),],
                            initial=['Utah', 'Utah'])

    text_input_lat = TextInput(display_text='Longitude',
                                   name='lat-input')

    text_input_lon = TextInput(display_text='Latitude',
                                   name='lon-input')

    select_modelYear = SelectInput(display_text='Model Year:',
                            name='select_modelYear',
                            multiple=False,
                            options=[('2008', 2008), ('2014', 2014)],
                            initial=['2008', 2008])

    select_returnPeriod = SelectInput(display_text='Return Period:',
                            name='select_returnPeriod',
                            multiple=False,
                            options=[('475', 475), ('1033', 1033), ('2475', 2475)],
                            initial=['475', 475])

    # Check form data
    if request.POST and 'lat-input' and 'lon-input' in request.POST:
       lat = request.POST['lat-input']
       lon = request.POST['lon-input']


    if request.POST and 'select_state' and 'select_modelYear' and 'select_returnPeriod' in request.POST:
       state = request.POST['select_state']
       modelYear = request.POST['select_modelYear']
       returnPeriod = request.POST['select_returnPeriod']

    # Pass variables to the template via the context dictionary
    context = {'state': state,
               'lat': lat,
               'lon': lon,
               'modelYear': modelYear,
               'returnPeriod': returnPeriod,
               'select_state': select_state,
               'text_input_lat': text_input_lat,
               'text_input_lon': text_input_lon,
               'select_modelYear': select_modelYear,
               'select_returnPeriod': select_returnPeriod}

    return render(request, 'lfhazard/map.html', context)


@login_required
def documentation(request):

    # Create template context dictionary
    context = {}

    return render(request, 'lfhazard/documentation.html', context)


def query_csv(request):
  result = {}
  dist11 = 10000
  dist12 = 10000
  dist21 = 10000
  dist22 = 10000
  # dist will contain all the closests distances from the coordinate put in.
  # Quadrant 1: dist [0,1]
  # Quadrant 2: dist [2,3]
  # Quadrant 3: dist [4,5]
  # Quadrant 4: dist [6,7]
  dist = [10000,10000,10000,10000,10000,10000,10000,10000]
  # quad_line_tracker will contain the values of the point closest to the
  # cooridnates put in.
  quad_line_tracker=[0,0,0,0,0,0,0,0]
  # point_value will contain the calculated variables that will be 
  # brought to the js file.
  point_value = [100, 101, 102]
  try:
    if request.method == 'POST':
      request_dict = json.loads(request.body)

      # These are all the values from the javascript

      print request_dict 
      lon = float(request_dict['lon'])
      lat = float(request_dict['lat'])
      year = request_dict['year']
      state = request_dict['state']
      returnPeriod = request_dict['returnPeriod']
      
      # this finds the correct csv files given the parameters

      # path extentions
      LS_path = "LS-" + returnPeriod + '_States/LS-' + returnPeriod + '_' + state + '.csv'
      LT_path = "LT-" + returnPeriod + '_States/LT-' + returnPeriod + '_' + state + '.csv'
      SSD_path= "SSD-" + returnPeriod + '_States/SSD-' + returnPeriod + '_' + state + '.csv'
      
      csv_base_path = '/home/tethys/tethysdev/csv/'
      # "LS-475_States/LS-475_Alaska.csv"

      # LS path first
      csv_file_path = csv_base_path + LS_path
      
      with open(csv_file_path, 'r') as row:

        next(row) # this skips the first line
        for line in row:
          line = line.rstrip().split(',')

          # This sets up the lat and lon read from csv file
          temp_lon = float(line[0])
          temp_lat = float(line[1])
          
          # This tests for Quadrant one
          if temp_lon >= lon and temp_lat >= lat:
            
            # This calculates the distance between two points
            temp_dist = math.sqrt(math.pow(abs(lon-temp_lon),2)+math.pow(abs(lat-temp_lat),2))
            
            # This tests for the distance of point and sorts. 
            # This will store 2 points close to the coordinates.
            if temp_dist <= dist[1]:
              dist[1] = temp_dist
              quad_line_tracker[1] = line
            if (temp_dist <= dist[0] and temp_dist <= dist[1]):
              dist[1]= dist[0]
              dist[0] = temp_dist
              quad_line_tracker[1] = quad_line_tracker[0]
              quad_line_tracker[0] = line

          # This test for Quadrant two
          if temp_lon <= lon and temp_lat >= lat:
            
            # This calculates the distance between two points
            temp_dist = math.sqrt(math.pow(abs(lon-temp_lon),2)+math.pow(abs(lat-temp_lat),2))
            
            # This tests for the distance of point and sorts. 
            # This will store 2 points close to the coordinates.
            if temp_dist <= dist[3]:
              dist[3] = temp_dist
              quad_line_tracker[3] = line
            if (temp_dist <= dist[2] and temp_dist <= dist[3]):
              dist[3]= dist[2]
              dist[2] = temp_dist
              quad_line_tracker[3] = quad_line_tracker[2]
              quad_line_tracker[2] = line

          # This test for Quadrant three
          if temp_lon <= lon and temp_lat <= lat:
            
            # This calculates the distance between two points
            temp_dist = math.sqrt(math.pow(abs(lon-temp_lon),2)+math.pow(abs(lat-temp_lat),2))
            
            # This tests for the distance of point and sorts. 
            # This will store 2 points close to the coordinates.
            if temp_dist <= dist[5]:
              dist[5] = temp_dist
              quad_line_tracker[5] = line
            if (temp_dist <= dist[4] and temp_dist <= dist[5]):
              dist[5]= dist[4]
              dist[4] = temp_dist
              quad_line_tracker[5] = quad_line_tracker[4]
              quad_line_tracker[4] = line

              # This test for Quadrant four
          if temp_lon >= lon and temp_lat <= lat:
            
            # This calculates the distance between two points
            temp_dist = math.sqrt(math.pow(abs(lon-temp_lon),2)+math.pow(abs(lat-temp_lat),2))
            
            # This tests for the distance of point and sorts. 
            # This will store 2 points close to the coordinates.
            if temp_dist <= dist[7]:
              dist[7] = temp_dist
              quad_line_tracker[7] = line
            if (temp_dist <= dist[6] and temp_dist <= dist[7]):
              dist[7]= dist[6]
              dist[6] = temp_dist
              quad_line_tracker[7] = quad_line_tracker[6]
              quad_line_tracker[6] = line
          
        print "This is the 1st Quadrant"
        print " This is the 1st distance: "+str(dist[0])
        print " This is the 2nd distance: "+str(dist[1])
        print " This is the 1st line: "+str(quad_line_tracker[0])
        print " This is the 2nd line: "+str(quad_line_tracker[1])
        print "This is the 2nd Quadrant"
        print " This is the 1st distance: "+str(dist[2])
        print " This is the 2nd distance: "+str(dist[3])
        print " This is the 1st line: "+str(quad_line_tracker[2])
        print " This is the 2nd line: "+str(quad_line_tracker[3])
        print "This is the 3rd Quadrant"
        print " This is the 1st distance: "+str(dist[4])
        print " This is the 2nd distance: "+str(dist[5])
        print " This is the 1st line: "+str(quad_line_tracker[4])
        print " This is the 2nd line: "+str(quad_line_tracker[5])
        print "This is the 4th Quadrant"
        print " This is the 1st distance: "+str(dist[6])
        print " This is the 2nd distance: "+str(dist[7])
        print " This is the 1st line: "+str(quad_line_tracker[6])
        print " This is the 2nd line: "+str(quad_line_tracker[7])

        





      # write your logic here to get the value at lon, lat
      
      result["status"] = "success"
      result["point_value"] = point_value
    else:
      raise Exception('not a post request!')
  
  except Exception as e:
    print e.message
    result["status"] = "error"  
  finally:
    return JsonResponse(result)

  
  