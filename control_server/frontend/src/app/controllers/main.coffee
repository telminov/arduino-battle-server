angular.module('arduinoBattle')
.controller 'MainCtrl', ($scope, $log, CarResource) ->
    $log.info('Start!')

    cars = CarResource.query ->
        for car in cars
            $log.info(car)

