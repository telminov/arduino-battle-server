angular.module('arduinoBattle')

.factory 'CarResource', ($resource, config) ->
    url = "#{ config.serverAddress }/car/:id/"
    return $resource(url)
