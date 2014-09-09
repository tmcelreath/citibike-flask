from . import main
from flask import render_template, g

@main.route('/', methods=['GET'])
def index():
    """
    GET: Home page
    """
    return render_template('index.html')


@main.route('/station/', methods=['GET'])
def station_all():
    """
    GET: Fetch all stations
    """
    stations = g.dao.find_all_stations()
    return render_template('stations.html', stations=stations)


@main.route('/station/<int:station_id>', methods=['GET'])
def station_view(station_id):
    """
    GET: Fetch a station by station_id
    """
    station = g.dao.find_station_by_id(int(station_id))
    record = create_station_record(station)
    return render_template('station.html', station=record)


def create_station_record(row):
    record = {
        'id': row['id'],
        'name': row['name'],
        'lat': row['loc']['coordinates'][1],
        'lon': row['loc']['coordinates'][0]
    }
    return record