class CitiBikeDAO:

    def __init__(self, mongo):
        self.db = mongo.db


    def find_all_stations(self):
        cursor = self.db.station.find({})
        return self.create_station_records(cursor)


    def find_station_by_id(self, station_id):
        station = self.db.station.find_one({'id': int(station_id)})
        return self.create_station_record(station)


    def find_stations_by_geo_location(self, lon, lat, radius, limit):
        cursor =  self.db.station.find({
            'loc':{
                '$near':{
                    '$geometry': {
                        'type': "Point",
                        'coordinates': [lon, lat]
                    },
                    '$maxDistance': radius
                }
            }
        }).limit(limit)
        return self.create_station_records(cursor)

    def get_station_averages(self, station_ids, hour, days):
        return self.db.status.aggregate(
            [
                {"$match": {"date.h": hour, "date.wk": {"$in": days}, "id": {"$in": station_ids}}},
                {"$group": {"_id": "$id", "avgBike": {"$avg": "$bike"}, "avgDock": {"$avg": "$dock"}}}
            ]
        )

    def get_rides_by_bike_id(self, bike_id, start_date, end_date):
        cursor = self.db.ride.find(
            {'bikeid': bike_id, 'start_time': {'$gte': start_date, '$lte': end_date}}
        );
        return self.create_ride_records(cursor)

    def get_rides_by_station_id(self, station_id, start_date, end_date):
        cursor = self.db.ride.find(
            {'start_station': station_id, 'start_time': {'$gte': start_date, '$lte': end_date}}
        )
        return self.create_ride_records(cursor)


    def get_station_status(self, station_id, start_date, end_date):
        cursor = self.db.status.find(
            {'id': station_id, 'date.dt': {'$gte': start_date}}
        )
        return self.create_station_status_records(cursor)


    def create_station_records(self, cursor):
        records = []
        for station in cursor:
            records.append(self.create_station_record(station))
        return records


    def create_station_record(self, row):
        record = {
            'id': row['id'],
            'name': row['name'],
            'lat': row['loc']['coordinates'][1],
            'lon': row['loc']['coordinates'][0]
        }
        return record


    def create_station_status_records(self, cursor):
        records = []
        for status in cursor:
            records.append(self.create_station_status_record(status))
        return records


    def create_station_status_record(self, row):
        record = {
            'stat': row['stat'],
            'dock': row['dock'],
            'bike': row['bike'],
            'date': row['date']['dt']
        }
        return record


    def create_ride_records(self, cursor):
        records = []
        for ride in cursor:
            records.append(self.create_ride_record(ride))
        return records


    def create_ride_record(self, row):
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
