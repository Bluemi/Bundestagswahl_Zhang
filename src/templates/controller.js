(function () {
    var app = angular.module('app', []);
    var states;
    app.controller('main-controller', function ($scope, $http) {

        $http.get("http://localhost:5000/states")
            .then(function successCallback(response) {
                $scope.regions = response.data;
                console.log($scope.regions)
            }, function errorCallback(response) {
                console.log("http request error");
                console.log(response.error)
            });

        $scope.selectedRegion = -1;
        $scope.selectedConstituency = -1;

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
                    $scope.partys = response.data.filter(party => party.first_vote > 0 | party.second_vote > 0);
                    if (id === $scope.selectedConstituency)
                        $scope.selectedConstituency = -1;
                    else
                        $scope.selectedConstituency = id;
                    console.log($scope.partys)
                }, function errorCallback(response) {
                    console.log("open const error");
                    console.log(response.error)
                });
        };

    });

    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

}());