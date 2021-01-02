/*
 * @Author: Weidows
 * @Date: 2020-11-13 14:34:42
 * @LastEditors: Weidows
 * @LastEditTime: 2020-12-31 19:28:31
 * @FilePath: \Weidows\C++\homework\ing\大二上\实验二\c.cpp
 * @Description:实验二
 */

#include <stdio.h>
#include <stdlib.h>
typedef int Elemtype;

//全局变量
const Elemtype set1[] = {3, 8, 5, 11},
               set2[] = {22, 6, 8, 3, 15, 11, 20};
// 获取两组大小
const Elemtype size1 = sizeof(set1) / sizeof(set1[0]),
               size2 = sizeof(set2) / sizeof(set2[0]);

int main()
{
  Elemtype set3[size1 + size2], //并集
      set4[size1],              //交集
      size3 = 0,                //并集大小
      size4 = 0;                //交集大小

  //求交集,开始遍历
  for (Elemtype i = 0; i < size1; i++)
  {
    for (Elemtype j = 0; j < size2; j++)
    {
      if (set1[i] == set2[j])
      {
        set4[size4++] = set2[j];
      }
    }
  }

  /* 求并集 */
  for (Elemtype i = 0; i < size1; i++)
  { // 把set1遍历进set3
    set3[size3++] = set1[i];
  }
  for (Elemtype i = 0; i < size2; i++)
  { // 把set2遍历进set3
    set3[size3++] = set2[i];
  }

  for (Elemtype i = 0; i < size4; i++)
  { //把重复的变为'\n'
    for (Elemtype j = 0; j < size3; j++)
    {
      if (set3[j] == set4[i])
      {
        set3[j] = '\n';
        break;
      }
    }
  }

  //输出
  printf("交集:");
  for (Elemtype i = 0; i < size4; i++)
  {
    printf("%d ", set4[i]);
  }

  printf("\n并集:");
  for (Elemtype i = 0; i < size3; i++)
  {
    if (set3[i] != '\n')
      printf("%d ", set3[i]);
  }
}
