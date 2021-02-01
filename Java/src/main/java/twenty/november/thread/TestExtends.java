/*
 * @Author: Weidows
 * @Date: 2020-11-03 10:57:22
 * @LastEditors: Weidows
 * @LastEditTime: 2020-12-13 21:15:57
 * @FilePath: \Weidows\Java\src\main\java\twenty\november\thread\TestExtends.java
 * @Description:线程类
 */
package twenty.november.thread;

public class TestExtends extends Thread {
  @Override
  public void run() {
    System.out.println("Running in TestThread.run()");
  }
}
