from . import main
from flask import render_template, jsonify, g
from bson.json_util import dumps

@main.route('/', methods=['GET'])
def index():
    """ GET: Home page """
    return render_template('index.html')


@main.route('/station/', methods=['GET'])
def station_all():
    """ GET: Fetch all stations """
    stations_cursor = g.mongo.citibike.stations.find({})
    stations = []
    for station in stations_cursor:
        stations.append(create_station_record(station))
    return render_template('stations.html', stations=stations)


@main.route('/station/<int:station_id>', methods=['GET'])
def station_view(station_id):
    """ GET: Fetch a station by station_id """
    station = g.mongo.citibike.stations.find_one({'id': int(station_id)})
    record = create_station_record(station)
    return render_template('station.html', station=record)

@main.route('/api/station/<int:station_id>', methods=['GET'])
def api_station_view(station_id):
    """ GET: Fetch a station by station_id """
    station = g.mongo.citibike.stations.find_one({'id': int(station_id)})
    g.logging.debug('Station #{}, {}'.format(station_id, station))
    record = create_station_record(station)
    return jsonify({
        'payload': record,
        'prev': '',
        'next': '',
        'status': 200
    })

@main.route('/api/station/', methods=['GET'])
def api_station_all():
    stations_cursor = g.mongo.citibike.stations.find({})
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

def create_station_record(row):
    record = {
        'id': row['id'],
        'name': row['stationName'],
        'lat': row['latitude'],
        'lon': row['longitude']
    }
    return record