class Button{
  private int x,y;
  
  public Button(int x,int y) {

  }
  
  private void draw(){
    //画格子
    fill(1);
    strokeWeight(5);
    stroke(127);
    rect(x*100, (y+2)*50, 100, 50, 10);

    //文字
    fill(255);
    textMode( MODEL );
    text( text[y][x] , x*100+50, (y+2)*50+25);

  }
}
