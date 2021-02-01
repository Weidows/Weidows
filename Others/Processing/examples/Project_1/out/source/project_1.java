import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class project_1 extends PApplet {

public void setup(){
   //全屏显示
  
  print("helloworld"); //在setep里的print只会执行一次

  stroke( 255 ,0 ,255,155  );
  line(100,50,mouseX,mouseY);

  stroke( 0 ,255 ,255,155  ); //轮廓色
  fill(0xffFFF000,127);  //填充色(十六进制表示法),并且结合127/255透明度
  rect( 1000 ,200,500 ,250, 50); //矩形
  
}

public void draw(){
  spacing=spacing+random(-2,2);
  // print("helloworld");  这里的print连续执行(随着帧数刷新)
  background(255); //每次绘制会重绘背景,使上一帧的残影消失,如果背景放在最后会覆盖所有已绘制图案
  rectMode( CENTER);
  rect(mouseX,mouseY,100,50);

}

public void mousePressed(){ //鼠标按下

}

public void keyPressed(){ //按键

}
  public void settings() {  fullScreen( ); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "project_1" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
