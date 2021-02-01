/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:07:40
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:11:53
 * @FilePath: \Weidows\C++\Study\2020-3\1.函数&指针.c
 * 
 * C语言中函数中多个参数一般用指针带回,而函数返回值习惯带回0/1,如果除法成功,返回1,否则返回0(可用于if条件判断)
 */
#include <stdio.h>
int divide(int a, int b, int *result);
int main(void)
{
  int a = 4;
  int b = 2;
  int result;

  if (divide(a, b, &result))
  { //这里函数的返回值可以用来作为if的判断条件
    printf("%d/%d=%d\n", a, b, result);
  }

  return 0;
}
int divide(int a, int b, int *result)
{
  int ret = 1;
  if (b == 0)
  {
    ret = 0;
  }
  else
  {
    *result = a / b;
  }
  return ret;
} //0和1分别对应错误和正常,作为函数返回值带回
