/*
 * @?: *********************************************************************
 * @Author: Weidows
 * @Date: 2021-02-21 23:34:01
 * @LastEditors: Weidows
 * @LastEditTime: 2021-02-21 23:43:12
 * @FilePath: \Weidows\Java\src\main\java\twenty_one\multi_thread\TestDaemon.java
 * @Description:
 * @!: *********************************************************************
 */
package twenty_one.multi_thread;

//上帝守护你
public class TestDaemon {
  public static void main(String[] args) {
    // ! 上帝
    Runnable god = () -> {
      while (true) {
        System.out.println("上帝保佑你");
      }
    };
    // ! 你
    Runnable you = () -> {
      for (int i = 0; i < 100; i++) {
        System.out.println("你一生都开心的活着");
      }
      System.out.println("GoodBye World");
    };

    Thread godThread = new Thread(god);
    godThread.setDaemon(true); //默认false表示是用户线程，正常的线程都是用户线程
    godThread.start();

    new Thread(you).start();
  }
}
