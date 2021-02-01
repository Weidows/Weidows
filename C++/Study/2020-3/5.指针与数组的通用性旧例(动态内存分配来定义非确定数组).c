/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:12:57
 * @LastEditors: Weidows
 * @LastEditTime: 2020-09-26 23:27:14
 * @FilePath: \Weidows\C++\Study\2020-3\5.指针与数组的通用性旧例(动态内存分配来定义非确定数组).c
 */
#include <stdio.h>
#include <stdlib.h>
int main()
{
  int num, i;
  printf("输入数量:");
  scanf("%d", &num);

  int *a; //指针和数组同类可以把*a用作为数组
  a = (int *)malloc(num * sizeof(int));
  /**
   * 定义指针内存占用大小,malloc返回的结果是void*,需要转换成需要的类型
   */

  for (i = 0; i < num; i++)
  {
    scanf("%d", &a[i]);
  } //以数组看待指针并正序输入元素
  for (i = num - 1; i >= 0; i--)
  {                                //正序时i<num,倒序时i>= 0
    printf("a[%d]=%d\n", i, a[i]); //解释性数组元素输出
  }
  free(a); //释放a占用的内存
  return 0;
}
