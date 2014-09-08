from . import api
from flask import jsonify, g, request


@api.route('/station/', methods=['GET'])
def api_station_all():
    stations_cursor = g.dao.find_all_stations()
    stations = []
    for station in stations_cursor:
        stations.append(create_station_record(station))
        g.logging.debug(station)
    return jsonify({
        'payload': stations,
        'prev': '',
        'next': '',
        'status': 200
    })


@api.route('/station/<int:station_id>', methods=['GET'])
def api_station_view(station_id):
    """ GET: Fetch a station by station_id """
    station = g.dao.find_station_by_id(int(station_id))
    g.logging.debug('Station #{}, {}'.format(station_id, station))
    record = create_station_record(station)
    return jsonify({
        'payload': record,
        'prev': '',
        'next': '',
        'status': 200
    })


@api.route('/station/geosearch/', methods=['GET'])
def api_station_geo_search():
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
    return jsonify({
        'payload': stations,
        'prev': '',
        'next': '',
        'status': 200
    })

@api.route('/station/<int:station_id>/avg')
def api_get_station_averages(station_id):
    hour = int(request.args.get('hour'))
    day = int(request.args.get('day'))
    weekend = True if day in (6, 7) else False
    stations = get_station_average([station_id], hour, weekend)
    return jsonify({
        'payload': stations,
        'prev': '',
        'next': '',
        'status': 200
    })


def create_station_record(row):
    record = {
        'id': row['id'],
        'name': row['name'],
        'loc': row['loc']
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
