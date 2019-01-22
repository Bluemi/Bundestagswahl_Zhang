(function () {
    var app = angular.module('app', []);
    var states;
    app.controller('main-controller', function ( $scope, $http ) {
        $scope.openConstituency = function (id){
            console.log(id)
            $http.get("http://localhost:5000/constituencies/" + id )
            .then(function successCallback(response) {
                $scope.constituency = response.data;
                $scope.selectedRegion = id;
                console.log($scope.constituency)
            }, function errorCallback(response) {
                console.log("open const error");
                console.log(response.error)
        });
        }
        $http.get("http://localhost:5000/states")
            .then(function successCallback(response) {
                $scope.region = response.data;
                console.log($scope.region)
            }, function errorCallback(response) {
                console.log("http request error");
                console.log(response.error)
        });
    });
}());