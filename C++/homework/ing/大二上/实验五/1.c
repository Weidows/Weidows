/*
 * @Author: Weidows
 * @Date: 2020-11-27 15:27:06
 * @LastEditors: Weidows
 * @LastEditTime: 2020-12-04 15:01:15
 * @FilePath: \Weidows\C++\homework\ing\大二上\实验五\1.c
 * @Description:
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 32

int next[MAX] = {-999};                   //定义next数组
int BM_Index(char *S, char *T, int pos);  //普通算法
void get_next(char *T, int next[]);       //给next数组赋值
void print_index(int next[], int len);    //打印next数组
int KMP_index(char *S, char *T, int pos); //KMP算法
void get_nextval(char *T, int next[]);    //优化后的next数组求法

int BM_Index(char *S, char *T, int pos)
{
  int i = pos;
  int j = 0;
  while ((i < (int)strlen(S)) && (j < (int)strlen(T)))
  {
    if (S[i] == T[j])
    {
      ++i;
      ++j;
    }
    else
    {
      i = i - j + 1;
      j = 0;
    }
  }
  if (j == (int)strlen(T))
  {
    return i - j;
  }
  else
    return 0;
}

void get_next(char *T, int next[])
{

  int i, j;

  i = 0;
  j = -1;
  next[i] = j;
  while (i < (int)strlen(T))
  {
    if (j == -1 || T[i] == T[j])
    {
      ++i;
      ++j;
      next[i] = j;
    }
    else
    {
      j = next[j];
    }
  }
}

void get_nextval(char *T, int next[])
{
  int i, j;
  i = 0;
  j = -1;
  next[0] = -1;
  while (i < (int)strlen(T))
  {
    if (j == -1 || T[i] == T[j])
    {
      ++i;
      ++j;
      if (T[i] == T[j])
      {
        next[i] = next[j];
      }
      else
      {
        next[i] = j;
      }
    }
    else
    {
      j = next[j];
    }
  }
}

void print_index(int next[], int len)
{
  for (int i = 0; i < len; i++)
  {
    printf("next[%d] = %d\n", i, next[i]);
  }
}

int KMP_index(char *S, char *T, int pos)
{

  int i, j;
  i = pos;
  j = 0;
  while ((i < (int)strlen(S)) && (j < (int)strlen(T)))
  { //j < strlen(T)会出错，因为strlen返回是无符号数，j=-1时，退出了while循环。-1转换成无符号数是0xFFFFFFFF
    if (S[i] == T[j] || (j == -1))
    {
      i++;
      j++;
    }
    else
    {
      j = next[j];
    }
  }

  if (j == strlen(T))
  {

    return i - j;
  }
  else
    return 0;
}

int main()
{
  char *S = "aaabaaaab";
  char *T = "aaaab";
  int pos = 0;
  int index = 0;
  int len = strlen(T);

  printf("===============BM===============\n");
  index = BM_Index(S, T, pos);
  printf("index = %d\n", index);
  printf("===============KMP===============\n");
  get_next(T, next);
  // get_nextval(T, next);
  print_index(next, len);

  index = KMP_index(S, T, pos);
  printf("index = %d\n", index);
  return 0;
}
