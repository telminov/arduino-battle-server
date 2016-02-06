angular.module('arduinoBattle')
.controller 'MainCtrl', ($scope, $log, CarResource) ->
    $scope.cars = []

    cars = CarResource.query ->
        for car in cars
            $scope.cars.push(car)

