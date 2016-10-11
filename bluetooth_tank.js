Serial3.setup(9600);
var status = {x: 0, y:0};
var key;
var value = '';
var collectingValue = false;

var Motor = require('@amperka/motor');
var mRight = Motor.connect(Motor.MotorShield.M1);
var mLeft = Motor.connect(Motor.MotorShield.M2);

breakId = undefined;

Serial3.on('data', function (data) {
  // таймер для остановки при потере сигнала
  if (breakId) {
    clearTimeout(breakId);
  }
  breakId = setTimeout(
    function() {
      status.x = 0;
      status.y = 0;
      move();
      breakId = undefined;
    },
    500
  );

  if (!key && (data == 'x' || data == 'y')) {
    setKey(data);
    return;
  }
  if (key && data == '=') {
    collectingValue = true;
    return;
  }
  if (key && data == '#') {
    setValue();
    return;
  }
  if (key && collectingValue) {
    addToValue(data);
    return;
  }

});

function addToValue(chank) {
  value += chank;
}

function setKey(k) {
  key = k;
  //print('set key', key);
}

function setValue() {
  newValue = Number(value);
  if (status[key] != newValue) {
    print(status);
    move();
  }
  
  status[key] = newValue;
  
  key = undefined;
  value = '';
  collectingValue = false;
}

function move () {
  var forward = mapRange(status.x, 6, -6, -1, 1);
  var side = mapRange(status.y, 6, -6, -1, 1);
  
  var v1 =forward + side*0.7;
  var v2 = forward - side*0.7;
    
  if (v1 < 0.1 && v1 > -0.1 ) {
    v1 = 0;
  }
  if (v2 < 0.1 && v2 > -0.1 ) {
    v2 = 0;
  }
  
  mRight.write(v1);
  mLeft.write(v2);
  
  //print(status, v1, v2);
}

function mapRange(value, low1, high1, low2, high2) {
    var v = low2 + (high2 - low2) * (value - low1) / (high1 - low1);
    v = E.clip(v, low2, high2);
    return v;
}
