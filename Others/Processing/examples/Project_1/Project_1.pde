void setup(){
  fullScreen( ); //全屏显示
  
  print("helloworld"); //在setep里的print只会执行一次

  stroke( 255 ,0 ,255,155  );
  line(100,50,mouseX,mouseY);

  stroke( 0 ,255 ,255,155  ); //轮廓色
  fill(#FFF000,127);  //填充色(十六进制表示法),并且结合127/255透明度
  rect( 1000 ,200,500 ,250, 50); //矩形
  
}

void draw(){
  // print("helloworld");  这里的print连续执行(随着帧数刷新)
  background(255); //每次绘制会重绘背景,使上一帧的残影消失,如果背景放在最后会覆盖所有已绘制图案
  rectMode( CENTER);
  rect(mouseX,mouseY,100,50);

}

void mousePressed(){ //鼠标按下

}

void keyPressed(){ //按键

}