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
  number_line = 1
  dist1 = 1000
  quad1_line_tracker=[]
  try:
    if request.method == 'POST':
      request_dict = json.loads(request.body)

      # These are all the values from the javascript
      print "This is the Dist1: " + str(dist1)
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
          #Quadrant One
          # print "*********"
          # print "This is the Dist1: " + str(dist1)
          # print type(dist1)

          # print line

          temp_lon = float(line[0])
          temp_lat = float(line[1])
          # print "*********"

          # print type(lon)
          # print type(lat)
          # print type(temp_lon)
          # print type(temp_lat)
          # print line[0] + '>'+ lon +' '+ line[1] +'>'+ lat
          # print str(lon) + ' ' + str(lat)
          # print str(temp_lon) + ' ' + str(temp_lat)
          # print number_line
          # print abs(lon-temp_lon)
          # print abs(lat-temp_lat)
         
          if temp_lon > lon and temp_lat > lat:
            
            dist1 = math.sqrt(math.pow(abs(lon-temp_lon),2)+math.pow(abs(lat-temp_lat),2))
            # print "point 2 "
            # print dist1
            if dist1 < dist1:
              print "point 3"
              dist1 = dist1
              print "point 3"
              quad1_line_tracker.append(line[0])
              print "point 4"
      
          number_line += 1
        
        print "Number of lines: " + str(number_line)
        print "This is the distance: "+str(dist1)
        print "This is the line: "+str(quad1_line_tracker)






      # write your logic here to get the value at lon, lat
      point_value = [100, 101, 102]
      result["status"] = "success"
      result["point_value"] = point_value
    else:
      raise Exception('not a post request!')
  
  except Exception as e:
    print e.message
    result["status"] = "error"  
  finally:
    return JsonResponse(result)

  
  