/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:14:55
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:12:56
 * @FilePath: \Weidows\C++\Study\2020-3\9.字符串数组的两种定义方式以及注意事项及用途.c
 */ 
#include<stdio.h>
int main(){
    int i = 0;
    char *s = "Hello World";
    /*s[0] = 'B';//想把H换成B,报错,这样定义的字符串数组实际上
    是const char *s[],数组存放位置是只读性的,除非s="Bello World"*/
    char *s2 = "Hello World";
    //看似定义了两个字符串数组,实际上两个指针指向同一个位置
    char s3[] = "Hello World";
    //用指针方式存放的字符串不可修改,但用数组存放的可以修改
    s3[0] = 'B';
    printf("&i=%p\n", &i);
    printf("s=    %p\n", s);
    printf("&s2=%p\n", s2);
    printf("Here! s3[0]=\"%c\"\n", s3[0]);//s3[0]的 "H"->"B"
    /*在调试printf时可以用here来突出显示,反斜杠\加上字符可以
    让printf输出那个字符,比如这里表示双引号*/

    /*两种字符串
        1.数组(构造):作用域与变量相同,作为本地变量结束时空间被自动回收
        2.指针(处理):1.尚不知这字符串在哪里用
                            2.用于处理参数
                            3.动态分配空间
    字符串的输入:char string[8];
                        scanf("%s",string);注意没有取址符&*/
    return 0;
}
