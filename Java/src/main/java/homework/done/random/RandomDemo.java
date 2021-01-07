/*
 * @Author: Weidows
 * @Date: 2020-12-02 18:44:00
 * @LastEditors: Weidows
 * @LastEditTime: 2020-12-02 19:02:45
 * @FilePath: \Weidows\Java\src\main\java\test\homework\ing\random\RandomDemo.java
 * @Description:
 */
package test.homework.ing.random;

import java.util.Random;

public class RandomDemo {
  public static void main(String[] args) {
    final int m = 20, n = 30;

    for (int i = 0; i < 5; i++) {
      int number = m + new Random().nextInt(n - m + 1);
      System.out.print(number + "\t");
    }

    System.out.println();
    for (int i = 0; i < 5; i++) {
      System.out.print(m + (int) ((n - m + 1) * Math.random()) + "\t");
    }
  }
}
