/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:14:31
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:12:49
 * @FilePath: \Weidows\C++\Study\2020-3\8.初识字符串(数组),指针与元素位的三角恋.c
 */
#include <stdio.h>
#include <string.h> //字符串处理库头文件
int main()
{
    char a[5] = {'H', 'e', 'l', 'l', 'o', '\0'}; //末尾的\0可以不算做一位
    //标准格式,单引号不能少,否则是ASCII码值int类型
    printf("%s\n", a);    /*直接输出不带末尾\0的char类型数组也能
    出来一个hello,但是结尾有乱码,printf内的\n也无效*/
    printf("%d\n", a[0]); /*输出"H"的ASCII码值72,单元素在数组
    内部是字符%c形式存在,无法以%s字符串形式输出(报错)*/

    char *str = "Hello";     //以char类型指针在某地址下写入Hello(地址连续)
    char word[] = "Hello";   //另一种定义字符串数组的方法(同上)
    char line[5] = "Hello";  //这两个类似,建立char数组,依次写入
    printf("%d\n", str[0]);  //74
    printf("%d\n", word[0]); //74
    printf("%d\n", sizeof(word) / sizeof(word[0]));
    printf("%d\n", sizeof(line) / sizeof(line[0]));
    //由此看出'\0'确实需要占用一位元素,默认情况会自动写入(除非没位)
    return 0;
}
