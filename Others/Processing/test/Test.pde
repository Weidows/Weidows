//实例化
Claculator calculator = new Claculator();

void setep(){
  //初始化界面
  size(400, 400);

}

void draw(){
  //单流程控制
  calculator.control();
}

void mouseClicked( ){
  calculator.pressed();
}
