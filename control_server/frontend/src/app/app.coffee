angular.module('arduinoBattle', [
    'ngResource'
    'ngSanitize'
    'ngRoute'
    'ngAnimate'

    'ui.bootstrap'

    'swUtils'
    'swWebSocket'
])


.config ($routeProvider) ->
    $routeProvider
        .when('/',
          templateUrl: 'controllers/main.html'
          controller: 'MainCtrl'
          label: ''
        )
        .when('/car/:id/',
          templateUrl: 'controllers/car.html'
          controller: 'CarCtrl'
          label: 'Car'
        )


.run ($location, $rootScope, swTitle) ->
    $rootScope.swTitle = swTitle
    $rootScope.$on '$routeChangeSuccess', (event, current, previous) ->
        baseTitle = current.$$route?.label or ''
        swTitle.setTitleBase(baseTitle)
        swTitle.setTitleStart('')
        swTitle.setTitleEnd('')


.config ($httpProvider) ->
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'