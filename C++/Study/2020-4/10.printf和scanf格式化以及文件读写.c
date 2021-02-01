/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:34:52
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:14:28
 * @FilePath: \Weidows\C++\Study\2020-4\10.printf和scanf格式化以及文件读写.c
 */ 
// printf和scanf格式化以及文件读写
#include<stdio.h>

int main(){
// printf & scanf 格式化
    /*printf  %[flags][width][.prec][hlL]type
       scanf  %[flags]type    */

    //[flags]:"-"左对齐  "+"在前面放正负号   "space"正数留空   "0"用0填充空
        printf("%+09d\n", -123);
        printf("%-+09d\n", 123);

    //[width][.prec]: "num"输出占几位    ".num"小数点后占几位  "*"和".*"代替量
        printf("%+9.2f\n", 123.0);//符号也占位
        int i = 5;         //i用来代替*的位置
        int i1 = 5;       //i1用来代替.*的位置
        printf("%*.*f\n", i, i1,123.4);//".*"可超越"*"的约束字符数,此处输出9位>i=5

    //[hlL]: "h"short   "l"long  "ll"long long  "L"long double
    
    //type %i是十进制,可根据输入进制转换,如
        printf("%i-%i-%i\n", 1234, 056, 0x78);
    
    //scanf格式控制   "*"忽略此项     "[^,]"到","之前的所有
        scanf("%*[^,],%i", &i);       //例如输入GPRMC,4319
        printf("%i\n", i);                       //输出          i=4319 

    //printf和scanf都有返回值,分别是输出的字符数,读入的项目数
        int a = printf("%d\n", 123);   //此处a应为4,123后有个\n占一位
        printf("%d\n", a);

        a = scanf("%d", &a);                //此处a应为1
        printf("%d\n", a);

/*文件输入输出用<和>做重定向 ,打开文件的标准形式如下,其实FILE是用typedef定义的
结构关键字,fopen就是那个结构类型的名字
    FILE *fp = fopen("filename", "mode");      //本质是定义了个指针类型的结构
    if(fp){
        // fscanf(fp, ...);
        // fprintf(fp, ...);
        fclose(fp); //打开对应关闭
    }else{
        // ...
    } */

    /*mode类型
        r       打开只读
        r+      打开读写,从文件头开始
        w       打开只读,如不存在则新建,如存在则清空
        w+     打开读写,如不存在则新建,如存在则清空 
        a         打开追加,如不存在则新建,如存在则从文件尾开始
        ..x(后缀)只新建,如存在则不能打开*/ 

    FILE *fp = fopen("123.c", "r");
    if(fp){
        int num = 0;
        fscanf(fp, "%d", &num);
        printf("%d\n", num);
        fclose(fp);
    }else{
        printf("无法打开文件\n");
    }

return 0;
}
