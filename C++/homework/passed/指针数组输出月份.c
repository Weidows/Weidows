/*
 * @Author: Weidows
 * @Date: 2020-05-15 19:43:32
 * @LastEditors: Weidows
 * @LastEditTime: 2020-06-04 17:26:33
 * @FilePath: \demo\C_\homework\过去\指针数组输出月份.c
 */
//库
#include <stdio.h>
//函数 && struct && typedef

int main()
{
    char *month[12] = {
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    }; //定义指针数组存放月份(每个元素是一个指针,指向对应那个字符串数组)

    int month_num = 0;
    while (month_num < 1 || month_num > 12)
    { //保险循环
        printf("Input month number:");
        scanf("%d", &month_num);
    }

    printf("%dth month is %s", month_num, month[month_num - 1]);
    //printf中不用加*,他自动读址
    return 0;
}
