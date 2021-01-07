/*
 * @Author: Weidows
 * @Date: 2020-11-04 18:47:05
 * @LastEditors: Weidows
 * @LastEditTime: 2020-11-04 19:28:25
 * @FilePath: \Weidows\Java\src\main\java\test\homework\done\shape\Circle.java
 * @Description:
 */
package test.homework.done.shape;

public class Circle implements Shape {
  @Override
  public double area(double r) {
    return 3.14 * r * r;
  }
}
