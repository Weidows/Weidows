/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:13:27
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:12:37
 * @FilePath: \Weidows\C++\Study\2020-3\6.传址在条件判定时的微小应用&malloc函数申请内存地址.c
 */
#include <stdio.h>
#include <stdlib.h>
int main()
{
  void *p = 0, *q = 0; //用作接受malloc地址,习惯性的在定义指针时初始为0
  int cnt = 0;         //计数变量
  while ((p = malloc(100 * 1024 * 1024)))
  {        //申请内存地址,内存不足时返回0/NULL
    cnt++; //malloc返回的是地址而非值,只能用指针(*p)来接
  }
  printf("分配了%d00MB的空间", cnt);

  q = malloc(100 * 1024 * 1024); //申请100MB的内存地址给q
  free(q);                       /*与malloc配对,用完之后释放内存,但如果指针q有任何修改
    或者指针q的地址不是malloc申请来的,那么无法free内存*/
  free(NULL);                    //等同于free(0);特殊,不会报错.照顾指针初始化为0后未用的情况
  return 0;
}