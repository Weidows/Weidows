/*
 * @Author: Weidows
 * @Date: 2020-11-04 18:46:27
 * @LastEditors: Weidows
 * @LastEditTime: 2020-11-04 18:51:16
 * @FilePath: \Weidows\Java\src\main\java\test\homework\ing\shape\Square.java
 * @Description:
 */
package test.homework.done.shape;

public class Square implements Shape {
  @Override
  public double area(double x) {
    return x * x;
  }
}
