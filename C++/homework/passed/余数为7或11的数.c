/*
 * @Author: Weidows
 * @Date: 2020-06-02 11:18:16
 * @LastEditors: Weidows
 * @LastEditTime: 2020-06-02 11:18:54
 * @FilePath: \demo\C_\homework\过去\余数为7或11的数.c
 */ 
//库
#include <stdio.h>
//函数 && struct && typedef
void fun(int m);

int main()
{
    int m = 0;
    printf("Please input 'm':");
    scanf("%d", &m);
    fun(m);
    return 0;
}
void fun(int m)
{
    for (int i = 1; i <= m; i++)
    {
        if (i % 7 == 0 || i % 11 == 0)
            printf("%d\t", i);
    }
}