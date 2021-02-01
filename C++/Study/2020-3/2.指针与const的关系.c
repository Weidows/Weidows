/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:09:40
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:12:03
 * @FilePath: \Weidows\C++\Study\2020-3\2.指针与const的关系.c
 */
#include <stdio.h>
int main()
{
  int a = 0;
  int *p1;
  p1 = &a;                             //不能写成*p1=&a;
  *p1 += 1;                            //a+1，另一种写法(*p)++;
  *p1++;                               //*(p1指针的地址+1),++比*运算优先级高
  printf("a=%d\np1地址=0x%d", a, *p1); //printf函数中输出指针*p1或p1都是地址

  /* int i = 0; //判断哪个被const了的标志是const在*前还是后
    const int *p2 = &i;
    *p2 += 1;
    printf("一,i=%d", i);
    int const *p3 = &i;     //前两种相同,是指针所指的实数不能改变
    *p3 += 1;
    printf("二,i=%d", i);
    int *const p3 = &i;     //这种是指针本身(这个地址)不能改变
    *p4 += 1;
    printf("三,i=%d", i); */
  //报错,原因:定义*p2时同是令i成为const,后续因此不能修改而报错
  return 0;
}
