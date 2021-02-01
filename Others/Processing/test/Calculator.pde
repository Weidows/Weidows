class Claculator {
  private String[][] text = new String[][]{{"%", "CE", "C", "<-X"}, {"1/x", "x^2", "x^1/2", "/"}, {"7", "8", "9", "*"}, {"4", "5", "6", "-"}, {"1", "2", "3", "+"}, {"+/-", "0", ".", "="}};
  // private int x,y,turn=0;
  private double result;
  private String[] number = new String[]{"",""};
  private String symbol = "";

  // private void button() {
  //   for (int x=0; x<width/100; x++) {
  //     for (int y=0; y<(height/50)-2; y++) {

  //     }
  //   }
  // }

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
