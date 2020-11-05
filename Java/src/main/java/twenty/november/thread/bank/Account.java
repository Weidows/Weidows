/*
 * @Author: Weidows
 * @Date: 2020-11-03 19:20:18
 * @LastEditors: Weidows
 * @LastEditTime: 2020-11-05 17:17:23
 * @FilePath: \Weidows\Java\src\main\java\twenty\november\thread\bank\Account.java
 * @Description:
 */
package twenty.november.thread.bank;

public class Account {
  private int money = 3000;
  // String name; //如果在这里直接获取线程名,那线程名都变成main,而且也不能让name在这里定义

  /**
   * 同步锁
   * <p>一个线程执行这个方法时锁住这个对象(account)
   * <p>所有其他涉及这个对象的线程等待这个方法执行完
   *!<p>锁的是对象,不是方法(weixin和zhifubao线程都用到account对象,于是在weixin.run().draw()运行时,zhifubao线程等待)
   * <p>不同的对象用不同的锁,但如果方法是static的,那此方法对于所有对象都锁住
   */
  public synchronized void draw(int money) {
    String name = Thread.currentThread().getName();
    this.threadConnect(name);
    System.out.println(name + "\t账户原有金额: " + this.money);
    System.out.println(name + "\t取款金额: " + money);
    if (this.money < money) {
      System.out.println(name + "\t账户余额不足");
    } else {
      this.money -= money;
      System.out.println(name + "\t取款后的余额" + this.money);
    }
    this.notify(); //唤醒这个对象所开的线程(也就是上面wait()的线程"微信")
  }

  private void test() {
    synchronized (this) { //对代码块进行同步锁,不同方法中的多个代码块共享同一个锁(一锁连着其他方法中的代码块也给锁住)
    }
  }

  /**
   * @description: 线程通信
   * @param {String} name
   * @return {*}
   * <p>判断线程是否是"微信",是的话让他wait(),让正在排队的线程执行
   */
  private void threadConnect(String name) {
    if (name.equals("微信")) {
      try {
        /**
         * 使当前线程进入等待状态,知道另一个线程对此对象发出.notify()为止
         * ! .wait() .notify() .notifyAll()这三个方法只能在有同步锁的方法或者代码块中执行
         */
        this.wait();
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
    }
  }
}
