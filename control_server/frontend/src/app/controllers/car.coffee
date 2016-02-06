SPACE_KEY_CODE = 32

FORWARD_KEY_CODE = 38
BACKWARD_KEY_CODE = 40
LEFT_KEY_CODE = 37
RIGHT_KEY_CODE = 39

BTN_DIRECTIONS = {
    forwardBtn: 'forward'
    backwardBtn: 'backward'
    leftBtn: 'left'
    rightBtn: 'right'
}

angular.module('arduinoBattle')
.controller 'CarCtrl', ($scope, $routeParams, $log, $interval, config, CarResource, swWebSocket) ->
    ws = _createWs($scope, swWebSocket, config)

    $scope.moveStatus = {
        forward: false
        backward: false
        left: false
        right: false
    }

    carId = $routeParams.id
    CarResource.get {'id': carId}, (car) ->
        $scope.car = car


    $scope.move = (direction, state) ->
        $scope.moveStatus[direction] = state
        sendMoveStatus(ws, $scope.moveStatus)

    $scope.keyDownHandler = (event) ->
        direction = _getDirection(event)
        if direction
            $scope.move(direction, true)

    $scope.keyUpHandler = (event) ->
        direction = _getDirection(event)
        if direction
            $scope.move(direction, false)


#    sendPromise = $interval(
#        -> sendStatus(ws, $scope.moveStatus)
#        100
#    )
#    $scope.$on('$destroy', -> $interval.cancel(sendPromise))


_getDirection = (event) ->
    if event.keyCode == SPACE_KEY_CODE and event.target.type == 'button'
        direction = BTN_DIRECTIONS[event.target.id]
        return direction

    if event.keyCode == FORWARD_KEY_CODE
        return 'forward'

    if event.keyCode == BACKWARD_KEY_CODE
        return 'backward'

    if event.keyCode == LEFT_KEY_CODE
        return 'left'

    if event.keyCode == RIGHT_KEY_CODE
        return 'right'

    return undefined


_createWs = ($scope, swWebSocket, config) ->
    ws = new swWebSocket("#{ config.wsServerAddress }/car_command")

    durable = true
    ws.start(durable)

    $scope.$on('$destroy', -> ws.close())

    return ws


sendMoveStatus = (ws, moveStatus) ->
#    haveActionStatus = false
#    for direction of moveStatus
#        if moveStatus.hasOwnProperty(direction) and moveStatus[direction]
#            haveActionStatus = true
#            break
#
#    if haveActionStatus
        data = JSON.stringify(moveStatus)
        ws.send(data)
