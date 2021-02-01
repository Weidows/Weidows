/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:13:59
 * @LastEditors: Weidows
 * @LastEditTime: 2020-05-29 00:13:59
 * @FilePath: \demo\Notes\C\7.关于指针和数组的两种数位py用法解惑.c
 */
#include <stdio.h>
int main()
{
  int a[5] = {
      1,
      2,
      3,
      4,
      5,
  };
  int *p = a;     //p->a[0]
  int *q = &a[5]; /*妈的神秘用法,即使定义时没有这个位也能让
    指针指向这个位置*/
  printf("%d\n", (int)p);
  printf("%d\n", (int)q);
  printf("%d", q - p); /*又tm一个神秘用法,a[0]与a[5]明明差20
    位,指针相减结果是5(因为除去一个sizeof(int)4位)*/
  printf("%d", a);     //直接输出数组结果是a[0]的地址
  return 0;
}
