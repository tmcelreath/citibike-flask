from . import api
from flask import jsonify, g, request
from .. import date_utils

@api.route('/station/', methods=['GET'])
def api_station_all():
    """
    GET: Fetch all station records
    """
    stations_cursor = g.dao.find_all_stations()
    stations = []
    for station in stations_cursor:
        stations.append(create_station_record(station))
        g.logging.debug(station)
    return create_response(stations)


@api.route('/station/<int:station_id>', methods=['GET'])
def api_station_view(station_id):
    """
    GET: Fetch a station by station_id
    Parameters:
        - station_id
    """
    station = g.dao.find_station_by_id(int(station_id))
    g.logging.debug('Station #{}, {}'.format(station_id, station))
    record = create_station_record(station)
    return create_response(record)


@api.route('/station/geosearch/', methods=['GET'])
def api_station_geo_search():
    """
    GET: Fetch stations within a radius of a geo location, ordered by distance.
    Parameters:
        - lat: latitude
        - lon: longitude
        - radius: distance from lat/lon in meters (default=500)
        - limit: max records to be returned (default=10)
    """
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    radius = request.args.get('radius')
    limit = request.args.get('limit')
    if radius:
        radius = int(radius)
    else:
        radius = 500
    if limit:
        limit = int(limit)
    else:
        limit = 10
    stations_cursor = g.dao.find_stations_by_geo_location(lon, lat, radius, limit)
    stations = []
    for station in stations_cursor:
        stations.append(create_station_record(station))
    return create_response(stations)


@api.route('/station/<int:station_id>/avg')
def api_get_station_averages(station_id):
    """
    GET: Find average bike/dock count for a station at a time of day. This will average out the
     count of bikes and docks over the entire hour of the time specified on a day type (weekend/weekday).
     For example, if the hour is 10 and the day is 3 (Wed), the result will be the average for weekdays between
     10:00 and 11:00. If the day were 7 (Sun), the result would be for weekends during the same time period.
    Parameters:
        - hour: hour of the date (24H)
        - day: day of the week (1-7 = MON-SUN)
    """
    hour = int(request.args.get('hour'))
    day = int(request.args.get('day'))
    weekend = True if day in (6, 7) else False
    averages = get_station_average([station_id], hour, weekend)
    return create_response(averages)


@api.route('/station/<int:station_id>/status', methods=['GET'])
def api_get_station_status(station_id):
    """
    GET: Get the list of station status records for a particular station between two times:
        - start_date: formatted as 'YYYYMMDD', default = CURRENT DATE
        - end_date: formatted as 'YYYYMMDD', default = start_date + 1 day
    """
    g.logging.debug("API: Get Station Status")
    start_date = date_utils.convert_string_date(request.args.get('start_date'))
    end_date = date_utils.convert_string_date(request.args.get('end_date'))
    if(not start_date):
        start_date = date_utils.get_current_date()
    if(not end_date):
        end_date = start_date
    end_date = date_utils.get_next_day(end_date)
    g.logging.debug('station_id: {}, start_date: {}, end_date: {}'.format(station_id, start_date, end_date))
    status_cursor = g.dao.get_station_status(start_date, start_date, end_date)
    statuses = []
    for status in status_cursor:
        row = {'stat': status['stat'], 'dock': status['dock'], 'bike': status['bike'], 'date': status['date']['dt']}
        statuses.append(row)
    return create_response(statuses)


@api.route('/station/<int:station_id>/rides', methods=['GET'])
def api_get_rides_by_station(station_id):
    """
    GET: Get the list of rides originating from a particular station between two times:
        - start_date: formatted as 'YYYYMMDD', default = CURRENT DATE
        - end_date: formatted as 'YYYYMMDD', default = start_date + 1 day
    """
    g.logging.debug("API: Get Rides by Station ID")
    start_date = date_utils.convert_string_date(request.args.get('start_date'))
    end_date = date_utils.convert_string_date(request.args.get('end_date'))
    if(not start_date):
        start_date = date_utils.get_current_date()
    if(not end_date):
        end_date = start_date
    end_date = date_utils.get_next_day(end_date)
    #g.logging.debug('start date: {}'.format(start_date))
    #g.logging.debug('end date: {}'.format(end_date))
    rides_cursor = g.dao.get_rides_by_station_id(station_id, start_date, end_date)
    rides = []
    for ride in rides_cursor:
        ride_record = create_ride_record(ride)
        rides.append(ride_record)
        #app.logger.debug(ride_record)
    return create_response(rides)


@api.route('/bike/<int:bike_id>/rides', methods=['GET'])
def api_get_rides_by_bike(bike_id):
    """
    GET: Get the list of rides for a particular bike between two times:
        - start_date: formatted as 'YYYYMMDD', default = CURRENT DATE
        - end_date: formatted as 'YYYYMMDD', default = start_date + 1 day
    """
    g.logging.debug("API: Get Rides by Bike ID")
    start_date = date_utils.convert_string_date(request.args.get('start_date'))
    end_date = date_utils.convert_string_date(request.args.get('end_date'))
    if(not start_date):
        start_date = date_utils.get_current_date()
    if(not end_date):
        end_date = start_date
    end_date = date_utils.get_next_day(end_date)
    g.logging.debug('start date: {}'.format(start_date))
    g.logging.debug('end date: {}'.format(end_date))
    rides_cursor = g.dao.get_rides_by_bike_id(bike_id, start_date, end_date)
    rides = []
    for ride in rides_cursor:
        ride_record = create_ride_record(ride)
        rides.append(ride_record)
        #app.logger.debug(ride_record)
    return create_response(rides)


def create_station_record(row):
    record = {
        'id': row['id'],
        'name': row['name'],
        'lat': row['loc']['coordinates'][1],
        'lon': row['loc']['coordinates'][0]
    }
    return record

def create_ride_record(row):
    record = {
        'bikeid': row['bikeid'],
        'duration': row['duration'],
        'start_time': row['start_time'],
        'start_station': row['start_station'],
        'end_time': row['end_time'],
        'end_station': row['end_station'],
        'user_type': row['user_type'],
        'gender': row['gender'],
        'birth_year': row['birth_year']
    }
    return record

def get_station_average(station_ids, hour, weekend):
    print(station_ids, hour, weekend)
    weekday_days = (0, 1, 2, 3, 4, 5)
    weekend_days = (6, 7)
    days = weekend_days if weekend else weekday_days
    station_cursor = g.dao.get_station_averages(station_ids, hour, days)
    stations = []
    for station in station_cursor['result']:
        stations.append(station)
    return stations

def create_response(payload, status=200, prev=None, next=None):
    response = { 'result': payload, 'status': status }
    if(prev):
        response['pev'] = prev
    if next:
        response['next'] = next
    return jsonify(response)