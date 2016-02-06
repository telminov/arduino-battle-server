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

    $scope.moveStatus = {
        forward: false
        backward: false
        left: false
        right: false
    }

    carId = $routeParams.id
    CarResource.get {'id': carId}, (car) ->
        $scope.car = car


    $scope.commandLog = []
    $scope.carCommandHandler = (commandResponse) ->
        item = {
            response: JSON.parse(commandResponse)
            dt: new Date()
        }
        $scope.commandLog.unshift(item)

        if $scope.commandLog.length > 5
            $scope.commandLog.length = 5



    ws = _createWs($scope, swWebSocket, config, carId)
    $scope.move = (direction, state) ->
        oldState = $scope.moveStatus[direction]
        $scope.moveStatus[direction] = state
        if oldState != state
            sendMoveStatus(ws, $scope.moveStatus)


    $scope.keyDownHandler = (event) ->
        direction = _getDirection(event)
        if direction
            $scope.move(direction, true)

    $scope.keyUpHandler = (event) ->
        direction = _getDirection(event)
        if direction
            $scope.move(direction, false)


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


_createWs = ($scope, swWebSocket, config, carId) ->
    ws = new swWebSocket("#{ config.wsServerAddress }/car_command/#{ carId }")

    ws.onMessage($scope.carCommandHandler)

    durable = true
    ws.start(durable)

    $scope.$on('$destroy', -> ws.close())

    # initial msg
    sendMoveStatus(ws, $scope.moveStatus)

    return ws


sendMoveStatus = (ws, moveStatus) ->
    data = JSON.stringify(moveStatus)
    ws.send(data)
