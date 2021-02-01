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

public class calculator extends PApplet {

class Claculator {
  private String[][] text = new String[][]{{"%", "CE", "C", "<-X"}, {"1/x", "x^2", "x^1/2", "/"}, {"7", "8", "9", "*"}, {"4", "5", "6", "-"}, {"1", "2", "3", "+"}, {"+/-", "0", ".", "="}};
  private int x,y,turn=0;
  private double result;
  private String[] number = new String[]{"",""};
  private String symbol = "";

  private void button() {
    for (int x=0; x<width/100; x++) {
      for (int y=0; y<(height/50)-2; y++) {
        fill(1);
        strokeWeight(5);
        stroke(127);
        rect(x*100, (y+2)*50, 100, 50, 10);

        fill(255);
        textMode( MODEL );
        text( text[y][x] , x*100+50, (y+2)*50+25);
      }
    }
  }

  public void control(){
    background(255);
    button();
    output();
  }

  public void pressed() {
    if(mouseY < 100) return; //按的空白
    this.x = mouseX / 100 ;
    this.y = (mouseY - 100) / 50 ;

    if(x != 3 && y > 1)
      number[turn] += text[y][x];
    else {
      if(turn == 1 && x == 3 && y == 5) {
        //todo
        return;
      }
      symbol = text[y][x];
      turn = 1;
    }

  }
  
  private void output() {
    fill(0);
    text(number[0] + "   " + symbol + "   " + number[1] , 50 ,50);
  }

}



//实例化
Claculator calculator = new Claculator();

public void setup() {
  //初始化界面
  

}

public void draw() {
  //单流程控制
  calculator.control();

}

public void mouseClicked( ){
  calculator.pressed();
}
  public void settings() {  size(400, 400); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "calculator" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
