/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:11:24
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:12:12
 * @FilePath: \Weidows\C++\Study\2020-3\3数组元素个数与地址,函数限制性传入参数.c
 */
#include <stdio.h>
int main()
{
  int i = 5;
  int a[i]; //数组定义时大小不可为空,但是可以用另外变量改变
  printf("数组起始地址=0x%d\n数组元素个数=%d", a, sizeof(a) / sizeof(a[0]));
  //求数组元素个数通式:数组大小/数组某个元素占用大小(一般用第一个a[0])
  const int b[5] = {1, 2, 3, 4, 5};
  /**
   * const定义数组只能一开始进行集合初始化
   * 数组内元素个数和值之后都不可以改变,b[5]中的5也不可以用变量代替
   */
  return 0;
}

void sum(const int a[], int length)
{
  /**
   * 为了保护数组值(数组本身也是指针,进入函数是可能会被改变)
   * 可以在声明函数原型时把参数加上const,不会改变原数组类型
   * 只是在函数内部把数组看做const使用
   */
  return 0; //函数是无返回值的,写返回0会警告
}
