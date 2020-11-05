/*
 * @Author: Weidows
 * @Date: 2020-11-03 23:38:42
 * @LastEditors: Weidows
 * @LastEditTime: 2020-11-05 12:51:30
 * @FilePath: \Weidows\Java\src\main\java\twenty\november\thread\producer_and_customer\Test.java
 * @Description:生产者与消费者模型
 */
package twenty.november.thread.producer_and_customer;

public class Test {
  public static void main(String[] args) {
    Clerk clerk = new Clerk();

    new Thread(new Runnable() {
      @Override
      public void run() {
        synchronized (clerk) {
          while (true) { //一直生产
            if (clerk.productNumber == 0) {
              System.out.println("产品为0,开始生产");
              while (clerk.productNumber < 5) {
                System.out.println("库存: " + clerk.productNumber++);
              }
              clerk.notify();
            } else {
              try {
                clerk.wait();
              } catch (InterruptedException e) {
                e.printStackTrace();
              }
            }
          }
        }
      }
    }, "生产者").start();
    new Thread(new Runnable() {
      @Override
      public void run() {
        synchronized (clerk) {
          while (true) { //一直消费
            if (clerk.productNumber == 5) {
              System.out.println("产品为5,开始消费");
              while (clerk.productNumber > 0) {
                System.out.println("库存: " + clerk.productNumber--);
              }
              clerk.notify(); //唤醒生产者
            } else {
              try {
                clerk.wait(); //消费者等待
              } catch (InterruptedException e) {
                e.printStackTrace();
              }
            }
          }
        }
      }
    }, "消费者").start();
  }
}

class Clerk {
  public static int productNumber;
}
