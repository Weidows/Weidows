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

void setup() {
  //初始化界面
  size(400, 400);

}

void draw() {
  //单流程控制
  calculator.control();

}

void mouseClicked( ){
  calculator.pressed();
}