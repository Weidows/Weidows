/*
 * @Author: Weidows
 * @Date: 2020-11-04 18:47:31
 * @LastEditors: Weidows
 * @LastEditTime: 2020-11-04 18:56:30
 * @FilePath: \Weidows\Java\src\main\java\test\homework\ing\shape\Test.java
 * @Description:测试类
 */
package test.homework.done.shape;

import java.util.Scanner;

public class Test {
  public static void main(String[] args) {
    Scanner in = new Scanner(System.in);
    Shape square = new Square();
    Shape circle = new Circle();
    System.out.print("Input square 边长: ");
    System.out.println("square area is: " + square.area(in.nextDouble()));
    System.out.print("Input circle 半径: ");
    System.out.println("circle area is: " + circle.area(in.nextDouble()));

    in.close();
  }
}
