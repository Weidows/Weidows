/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:26:45
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:13:48
 * @FilePath: \Weidows\C++\Study\2020-4\4.实现在test函数中改变str的指针指向地址.c
 */
#include <stdio.h>
char *test(char *string)
{ //方法1.返回值带回
    string = "hello world";
    /*易错,结果str不是hello world,仍是null,原因:test不是改变指针
的目标null,而是让指针指向另一个目标hello world,所指地址改变
但test没有返回结果,加上return string;就ok了*/
    return string;
}
void test2(char **string)
{ //方法2.用二维指针,但此方法不适用于函数中二维指针数组修改
// 修改一维指针数组, 只能用for单个遍历*string = "hello world"
}
int main()
{
    char *str = NULL;
    char *str2 = NULL;
    str = test(str); //返回值是让函数整体带有某个参数的值,需赋值
    test2(&str2);
    printf("str=%s\n", str);
    printf("str=%s\n", str2);
    return 0;
}
