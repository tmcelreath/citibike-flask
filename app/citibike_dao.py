class CitiBikeDAO:

    def __init__(self, mongo):
        self.db = mongo.db

    def find_station_by_id(self, station_id):
        return self.db.station.find_one({'id': int(station_id)})

    def find_all_stations(self):
        return self.db.station.find({})

    def find_stations_by_geo_location(self, lon, lat, radius, limit):
        return self.db.station.find({
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

    def get_station_averages(self, station_ids, hour, days):
        return self.db.status.aggregate(
            [
                {"$match": {"date.h": hour, "date.wk": {"$in": days}, "id": {"$in": station_ids}}},
                {"$group": {"_id": "$id", "avgBike": {"$avg": "$bike"}, "avgDock": {"$avg": "$dock"}}}
            ]
        )