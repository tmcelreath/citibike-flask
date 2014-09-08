angular.module('appMaps', ['google-maps'])
    .controller('mainCtrl', function($scope) {
        $scope.map = {control: {}, center: {latitude: 40.7284186, longitude: -73.98713956}, zoom: 13 };
        $scope.options = {scrollwheel: false};
        $scope.sites=[];
        var myLatlng = new google.maps.LatLng(40.7284186, -73.98713956);

        //var marker = new google.maps.Marker({
          //  position: myLatlng,
            //map: $scope.map.control.getGMap(),
            //title:"Hello World!"
        //});

        $scope.sites.push({latitude:52, longitude:0, options: { title: "Southerners" } });
        $scope.sites.push({latitude:52.5, longitude:1, options: { title: "Turkeys" } });

        alert("You have Map Instance of " + $scope.map.control);

        var onMarkerClicked = function (marker) {
                marker.showWindow = true;
                $scope.$apply();
        };

        _.each($scope.sites, function (site) {
                site.closeClick = function () {
                    site.showWindow = false;
                    $scope.$apply();
                };
                site.onClicked = function () {
                    onMarkerClicked(site);
                };
            });

    });