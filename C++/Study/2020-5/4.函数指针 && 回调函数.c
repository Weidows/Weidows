/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:40:17
 * @LastEditors: Weidows
 * @LastEditTime: 2020-05-29 00:40:17
 * @FilePath: \demo\C\5.函数指针 && 回调函数.c
 */ 
//函数指针 && 回调函数

#include <stdio.h>
#include<stdlib.h>

int max(int x,int y){
    return x > y ? x : y;
}

int getNextRandomValue(void){
    return rand();
}

void populate_array(int array[],size_t arraySize,int (*p)(void)){
    for (size_t i = 0; i < arraySize;i++){
        array[i] = p();
    }
}


int main()
{
    //函数指针
        // int (*p)(int, int) = &max;  //定义一个函数指针
        // int a, b, c, d;
        // printf("输入三个数:");
        // scanf("%d%d%d", &a, &b, &c);
        // d = p(p(a, b), c);
        // printf("最大数是:%d", d);
    //回调函数
        int myArray[10];
        populate_array(myArray, 10, getNextRandomValue);//get..不能带括号,那是调用
        for (int i = 0; i < 10; i++) {
            printf("%d\t", myArray[i]);
        }
    return 0;
}
