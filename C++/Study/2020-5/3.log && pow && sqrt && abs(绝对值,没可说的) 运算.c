/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:38:50
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:14:50
 * @FilePath: \Weidows\C++\Study\2020-5\3.log && pow && sqrt && abs(绝对值,没可说的) 运算.c
 */
// log && pow && sqrt && abs(绝对值,没可说的) 运算
//库
#include <math.h>
#include <stdio.h>
//main
int main()
{
    //换底公式 log a B = log c B / log c A
    printf("一%f\n", log10(8) / log10(2)); //相当于log2 (8)
    printf("%f\n", log(8) / log(2));       //不写底数默认以e为底

    //开方和乘方
    printf("二%f\n", pow(10, 8));
    printf("%d\n", pow(10, 8)); //pow()返回值是浮点数,如果用%d输出,结果不对
    printf("%d\n", (int)pow(10, 8));
    //特殊:乘方0.5时就是开方sqrt
    printf("三%f\n", pow(100, 0.5));
    printf("%f\n", sqrt(100));
    return 0;
}
