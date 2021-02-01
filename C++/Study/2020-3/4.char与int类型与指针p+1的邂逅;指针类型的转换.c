/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:12:20
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:12:23
 * @FilePath: \Weidows\C++\Study\2020-3\4.char与int类型与指针p+1的邂逅;指针类型的转换.c
 */
#include <stdio.h>
int main(void)
{
  char ac[] = {
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9,
  }; //char类型是小范围整数或单个字符
  int ab[] = {
      1,
      2,
      3,
      4,
  };
  char *p = ac;
  int *q = ab;
  printf("p地址=%p\n", p);
  printf("p+1地址=%p\n", p + 1); //*p+1=ac[1]
  printf("q地址=%p\n", q);
  printf("q+1地址=%p\n", q + 1); //*(q+1)=ab[1],而不是a[0]中的第二位
  //指针+1所代表的地址是加上那个类型的sizeof，char是+1，int是+4

  int *p1 = &ac;
  void *q1 = (void *)p1; /*void是未定类型的指针,不同类型的指针不能赋值，
    如*q1 = *p1;但是可以强制类型转换(参上)*/
  return 0;
}
