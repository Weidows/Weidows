/*
 * @Author: Weidows
 * @Date: 2020-09-25 19:40:22
 * @LastEditors: Weidows
 * @LastEditTime: 2020-12-31 19:20:51
 * @FilePath: \Weidows\C++\homework\ing\大二上\实验一\Data_Struct.cpp
 * @Description:main()里面一次性调用所有函数有点混乱,都给注释掉了,想用哪个消掉注释就好,函数间无干扰
 */

//!库
#include <math.h>
#include <stdio.h>
#include <stdlib.h> //*system,malloc...
#include <string.h>

//!函数 && struct && typedef
//2.里面的整数个数
#define SIZE 3

//3.里的结构体
typedef struct
{
  int year;
  int month;
  int day;
} Date;

//1.
char *str_combine(char *s1, const char *s2)
{
  char *s3 = (char *)malloc(strlen(s1) + strlen(s2) + 1);
  char *pointer = s3;
  while (*s1 != '\0')
    *pointer++ = *s1++;
  while (*s2 != '\0')
    *pointer++ = *s2++;
  *pointer = '\0'; // 字符串末尾截断
  return s3;       // 返回组合字符串
}

//2.
void swap(int *a, int *b)
{
  int t = *a;
  *a = *b;
  *b = t;
}

void sort(int *args)
{
  for (int i = 0; i < SIZE - 1; i++)
  {
    for (int j = i + 1; j < SIZE; j++)
    {
      if (args[i] > args[j])
        swap(&args[i], &args[j]);
    }
  }
}

//3.
int calculate_days(Date date)
{
  int ret = 0;
  int length_of_month[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

  for (int i = 0; i < date.month - 1; i++)
  { //累加计算天数
    ret += length_of_month[i];
  }
  ret += date.day; //加上当前月份的天数

  return (date.month > 2 && date.year % 4 == 0 && date.year % 100 == 0 && date.year % 400 == 0) ? ret++ : ret; // 是否是闰年,闰年再加一天
}

/**
 * 思考
 * 只有一个for循环,时间复杂度为 O(n)
 */
int calculate(int n)
{
  int ret = 0;
  for (int i = 1; i <= n; i++)
  {
    ret += i;
  }
  return ret;
}

//main
int main()
{
  // 1.自符串的连接
  // char *s1 = "Hello", *s2 = "World";
  // printf("%s\n", str_combine(s1, s2));

  // 2.三个整数，按由小到大的顺序输出
  // int args[SIZE];
  // printf("请输入%d个数字:", SIZE);
  // for (int i = 0; i < SIZE; i++)
  //   scanf("%d", &args[i]);
  // sort(args);
  // printf("排序完成后顺序:");
  // for (int i = 0; i < SIZE; i++)
  //   printf("%d\t", args[i]);

  //3.计算该日在本年中的第几天
  // Date date;
  // printf("按照格式输入: 年-月-日:");
  // scanf("%d-%d-%d", &date.year, &date.month, &date.day);
  // printf("第%d天", calculate_days(date));

  //思考.实现f（n）=1+2+3+…+n
  int n = 0;
  printf("输入n:");
  scanf("%d", &n);
  printf("f(n) = %d", calculate(n));

  return 0;
}
