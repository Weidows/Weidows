/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:18:56
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:13:22
 * @FilePath: \Weidows\C++\Study\2020-4\1.多维的指针和数组及其应用&switch语句大型实例.c
 */ 
#include<stdio.h>
#include<stdlib.h>//包含malloc函数的库
#include<string.h>//没用到,用于处理数组
int Test_point(int i){//指针,参数名字可以和外部的变量名相同
    int *p = &i;
    int **a = &p; //a是指针,指向另一个指针
    printf("%p\n", &i);
    printf("%p\n", p); //一二相同
    printf("%p\n", a); //**a的地址不同

    char b[10][10] = {
        //二维字符串数组
        "Hello", //相当于->char [10]
        "World", //共十个,不存在'\0'了
        "2",
        "3",
        "4   ", //引号内空格也算字符
        "....",
        "999999999",   //b[9],其中最多也是9个,不要强行占用第十位
    };                 //这种二维数组竖着写好看
    printf("%s\n", b); //输出二维的b->输出b[0]
}
int Month(int month){//输出英文月份的函数
    int ret = 0;//定义函数返回值(用于判断是否正常运行)
    switch (month){
    case 1:
        printf("January\n");//规整形式
        break;
    case 2:
        printf("February\n");
        break;
    case 3:printf("March\n");break;//单行形式,这种情况更好看
    case 4:printf("April\n");break;
    case 5:printf("May\n");break;
    case 6:printf("June\n");break;
    case 7:printf("July\n");break;
    case 8:printf("August\n");break;
    case 9:printf("September\n");break;
    case 10:printf("October\n");break;
    case 11:printf("November\n");break;
    case 12:printf("December\n");break;
    default://默认输出(没有case匹配时)
        ret = 1;    //ret=1时说明没有输入正确数
        printf("???\n");
        break;
    }
    return ret;//带回ret值可以用于条件判断
}
int Month2(int argc,char *argv[]){
    int ret = 0;
    while (argc > 12 || argc < 1){
        printf("请输入月份\n:");
        scanf("%2d", &argc);
    }/*while比do-while好用些
    与或非单目& | ~ 逻辑&& || !  */
    printf("%s\n", argv[argc - 1]);
    ret++;
    return ret;
}
int main(int argc,char const *argv[]){//main实际包含的参数
    int i = 0;
    int month = 0;
    Test_point(i);
    char *c[12] = {
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
    }; /*指针数组,每个元素是一个指针char *,这样
    同时能初始化(实际上只有c[0]=0,其余没赋值的默认为0,数组通用方法)*/

    //指针数组的特殊应用,month开始处
        label_1:{//跳转标记,使程序可读性降低,尽量避免使用
            printf("请输入月份\n");
            scanf("%2d", &month);//用户输入月份
            if(Month(month)){   //函数同时调用和作为if的判断条件
                goto label_1;
            }}//Month结束
    //month2开始
        if (Month2(month,c)){printf("Function runs successfully\n");}
    return 0;
}//正式结束!!!
