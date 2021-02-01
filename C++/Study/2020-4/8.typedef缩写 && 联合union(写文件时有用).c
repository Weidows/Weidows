/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:33:41
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:14:19
 * @FilePath: \Weidows\C++\Study\2020-4\8.typedef缩写 && 联合union(写文件时有用).c
 */ 
//typedef缩写 && 联合union(写文件时有用)
#include <stdio.h>

typedef long int64_t;
typedef struct ADate{
    int year;
    int month;
    int day;
} Date;//Date类型就是Adate类型结构的缩写

typedef union {
    int i;
    char ch[sizeof(int)];
} CHI;//将一个联合类型命名为CHI


int main(){
    int64_t i1 = 1000000000;
    Date d = {2020, 4, 5};

    CHI chi;//定义联合chi
    chi.i = 1234;
    int i;
    for (i = 0; i < sizeof(int);i++){
        printf("%02hhX", chi.ch[i]);
    }//联合元素共用内存,这里就是以ch的方式读取i在内存中的存储格式

    return 0;
}
