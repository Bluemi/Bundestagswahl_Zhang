(function () {
    var app = angular.module('app', ["chart.js"])

    var parties_data;

    app.controller("PieCtrl", function ($scope) {
        $scope.labels = [];
        $scope.data_1 = [];
        $scope.data_2 = [];
        $scope.updateCharts = function () {
            parties_data.forEach(function (obj) {
                $scope.labels.push(obj.party);
                $scope.data_1.push(obj.first_vote);
                $scope.data_2.push(obj.second_vote);
            });
        }
        $scope.$emit('onUpdate', $scope.updateCharts());
    });

    app.controller('main-controller', function ($scope, $http) {

        $scope.selectedRegion = -1;
        $scope.selectedConstituency = -1;


        $http.get("http://localhost:5000/states")
            .then(function successCallback(response) {
                $scope.regions = response.data;
                console.log($scope.regions);
            }, function errorCallback(response) {
                console.log("http request error");
                console.log(response.error);
            });

        $scope.openConstituency = function (id) {
            console.log(id)
            $http.get("http://localhost:5000/constituencies/" + id)
                .then(function successCallback(response) {
                    $scope.constituencies = response.data;
                    if (id === $scope.selectedRegion)
                        $scope.selectedRegion = -1;
                    else
                        $scope.selectedRegion = id;
                    console.log($scope.constituencies)

                }, function errorCallback(response) {
                    console.log("open const error");
                    console.log(response.error)
                });
        };

        $scope.openDetails = function (id) {
            console.log(id)
            $http.get("http://localhost:5000/votes/" + id)
                .then(function successCallback(response) {
                    //$scope.partys = response.data.filter(party => party.first_vote > 0 | party.second_vote > 0);
                    $scope.partys = response.data
                    parties_data = response.data;

                    if (id === $scope.selectedConstituency)
                        $scope.selectedConstituency = -1;
                    else
                        $scope.selectedConstituency = id;
                    console.log($scope.partys)
                }, function errorCallback(response) {
                    console.log("open details error");
                    console.log(response.error)
                });
        };

        $scope.searchFor = function () {
            console.log($scope.regions);
            let wasFound = false;

            for (let region of $scope.regions){
                $http.get("http://localhost:5000/constituencies/" + region.id)
                .then(function successCallback(response) {
                    response.data.forEach(function (elem) {
                        if (elem.name.toLowerCase().includes($scope.search.toLowerCase())) {
                            wasFound = true;
                            $scope.selectedRegion=region.id;
                            $scope.openDetails(elem.id);
                            $scope.constituencies = response.data;
                            console.log(region.id + " " + elem.id);
                        }
                    })
                }, function errorCallback(response) {
                    console.log("searchError");
                    console.log(response.error)
                });

            }

            if (!wasFound){
                $scope.selectedRegion = -1;
                $scope.selectedConstituency = -1;
            }

        };

    });

}());