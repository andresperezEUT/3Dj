//// TODO: maybe send acceleration and gravity in a bundle, since they are acquired always together

import oscP5.*;
import netP5.*;
import android.view.MotionEvent;

AccelerometerManager accel;

float azimuth, elevation, roll;
float lastAzimuth, lastElevation, lastRoll;
float dOrientation = 0.05; // in degrees--> in order to not send all the time and avoid collapsing the net
float[] acceleration = new float[3];
float[] lastAcceleration = new float[3];
float dAcceleration = 0.005; // newtons
float[] gravity = new float[3];
float[] lastGravity = new float[3];
float dGravity = 0.005; //newtons

int lastSensor;
public static final int ACCELERATION = 0;
public static final int ORIENTATION = 1;
public static final int GRAVITY = 2;

NetAddress myRemoteLocation;
OscP5 oscP5;
OscMessage myMessage;


float x,y;


void setup() {
  accel = new AccelerometerManager(this);
  orientation(PORTRAIT);
  
  background(0);
  fill(255);
  textSize(40);
  textAlign(CENTER, CENTER);
  text("*****",
       0, 0, width, height);
       
  
  
  oscP5 = new OscP5(this, 12000);
  myRemoteLocation = new NetAddress("255.255.255.255", 57120); // local broadcast
  
  noLoop();
}


void draw() {
//  background(0);
//  fill(255);
//  textSize(40);
//  textAlign(CENTER, CENTER);
//  text("azi: " + nf(ax, 1, 2) + "\n" + 
//       "ele: " + nf(ay, 1, 2) + "\n",
//       0, 0, width, height);

  //sendOrientation("orientation",azimuth,elevation);
       
  //println(lastSensor);
  sendMessage(lastSensor);
  
}

public void resume() {
  if (accel != null) {
    accel.resume();
  }
}

    
public void pause() {
  if (accel != null) {
    accel.pause();
  }
}


public void shakeEvent(float force) {
  println("shake : " + force);
}


public void orientationEvent(float x, float y, float z) {
  boolean update = false;
  //println("orientation: " + azimuth + ", " + elevation);
  
  lastAzimuth = azimuth;
  lastElevation = elevation;
  lastRoll = roll;
  
  azimuth = x;
  elevation = y;
  roll = z;
  

  if (abs(lastAzimuth-azimuth) > dOrientation) {update=true;};
  if (abs(lastElevation-elevation) > dOrientation) {update=true;};
  if (abs(lastRoll-roll) > dOrientation) {update=true;};
  
  if (update) {  
    lastSensor = ORIENTATION;
    redraw();
  }
}

public void accelerationEvent(float x, float y, float z) {
  boolean update = false;
  //println("acceleration: " + x + ", " + y + ", " + z);
  
  
  // arrayCopy(source,destination)
  arrayCopy(acceleration,lastAcceleration);
  
  acceleration[0] = x;
  acceleration[1] = y;
  acceleration[2] = z;
  
  if (abs(acceleration[0]-lastAcceleration[0]) > dAcceleration) {update=true;};
  if (abs(acceleration[1]-lastAcceleration[1]) > dAcceleration) {update=true;};
  if (abs(acceleration[2]-lastAcceleration[2]) > dAcceleration) {update=true;};
  
  if (update) {
    lastSensor = ACCELERATION;
    redraw();
  }
}

public void gravityEvent(float x, float y, float z) {
  boolean update = false;
  
  //println("gravity: " + x + ", " + y + ", " + z);
    
  // arrayCopy(source,destination)
  arrayCopy(gravity,lastGravity);
  
  gravity[0] = x;
  gravity[1] = y;
  gravity[2] = z;
  
  if (abs(gravity[0]-lastGravity[0]) > dGravity) {update=true;};
  if (abs(gravity[1]-lastGravity[1]) > dGravity) {update=true;};
  if (abs(gravity[2]-lastGravity[2]) > dGravity) {update=true;};
  
  lastSensor = GRAVITY;
  redraw();
}

public void sendMessage (int sensor) {
//    sendOrientation();
//    sendAcceleration();
//    sendGravity();
  switch (sensor) {
   case ORIENTATION:
   // since orientation is slower than the others, send all sensors when orientation is ready
     sendOrientation();
     //sendAcceleration();
     //sendGravity();
     break;
   case ACCELERATION:
   // acceleration and gravity are in the same rate, so send the two
     sendAcceleration();
     sendGravity();
     break;
   case GRAVITY:
     sendAcceleration();
     sendGravity();
     break;
  } 
}

public void sendOrientation() {
  //println("sendOrientation");
  myMessage = new OscMessage("/orientationController/"+"orientation");
  myMessage.add(azimuth);
  myMessage.add(elevation);
  myMessage.add(roll);
  oscP5.send(myMessage, myRemoteLocation);
}


public void sendAcceleration() {
    //println("sendAcceleration");
  myMessage = new OscMessage("/orientationController/"+"acceleration");
  myMessage.add(acceleration);
  oscP5.send(myMessage, myRemoteLocation);
}

public void sendGravity() {
  //println("sendGravity");
  myMessage = new OscMessage("/orientationController/"+"gravity");
  myMessage.add(gravity);
  oscP5.send(myMessage, myRemoteLocation);
}

//////////////////////////////////////

public void sendDown() {
  //println("sendGravity");
  myMessage = new OscMessage("/orientationController/"+"down");
  oscP5.send(myMessage, myRemoteLocation);
}

public void sendUp() {
  //println("sendGravity");
  myMessage = new OscMessage("/orientationController/"+"up");
  oscP5.send(myMessage, myRemoteLocation);
}

@Override
public boolean dispatchTouchEvent(MotionEvent event) {

  //x = event.getX(); // get x/y coords of touch event
  //y = event.getY();
  
  
  int action = event.getActionMasked(); // get code for action
//  pressure = event.getPressure(); // get pressure and size
//  pointerSize = event.getSize();
//
  switch (action) { // let us know which action code shows up
  case MotionEvent.ACTION_DOWN:
    
    background(255,0,0);
    sendDown();
    break;
  case MotionEvent.ACTION_UP:
 
    background(0);
    sendUp();
    break;
//  case MotionEvent.ACTION_MOVE:
//    touchEvent = "MOVE";
//    break;
//  default:
//    touchEvent = "OTHER (CODE " + action + ")"; // default text on other event
  }

  return super.dispatchTouchEvent(event); // pass data along when done!
}
