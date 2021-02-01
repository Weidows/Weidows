/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:30:54
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:14:08
 * @FilePath: \Weidows\C++\Study\2020-4\6.枚举(弟)&结构(爷).c
 */ 
//枚举(弟)&结构(爷)  の  <<枚短结长>>
//库
    #include<stdio.h>
    #include<stdbool.h>
//枚举和结构
    enum color{RED,YELLOW,GREEN,NumColors};
    //从0->n的int型,枚举量当int用,反之不行(需要用数组),枚举相当于组合定义int

    struct point{
        /*定义了结构体同时定义p1,p2两个point类型的结构体
        p1,p2里面有x和y的值*/
        int x;
        char y;
    } p1, p2; //另外定义格式struct point p3;如无需额外定义可以去掉结构名

    struct date{
        int month;
        int day;
        int year;
    };

    bool isLeap(struct date d);//bool类型判断是否是闰年的函数
    int NumberOfDays(struct date d);

int main(int argc,const char *argv[]){
    //两种结构的定义和初始化方法
        struct date today1={07,31,2014};
        struct date thismonth={.month=7,.year=2014,};
        printf("today %d-%d-%d    ", today1.year, today1.month, today1.day);
        printf("thismonth %d-%d-%d    ", thismonth.year, thismonth.month, thismonth.day); //为定义的为0
        
        today1 = thismonth;//同是date类型结构体可以横向赋值
        printf("today %d-%d-%d\n", today1.year, today1.month, today1.day);

        struct point p3;//定义point类型的结构
        p3 = (struct point){1, 'y'};//区别于数组,结构体可以另行{}初始化
        printf("%d-%c\n", p3.x, p3.y);
        struct date *p = &today1;//结构体p内元素是指向today对应元素的指针
    //函数与数据结构结合实例
        struct date today, tomorrow;

        printf("Enter today's date(yyyy mm dd:");
        scanf("%d %d %d", &today.year, &today.month, &today.day);

        if(today.day!=NumberOfDays(today)){//today非月末
            tomorrow.day = today.day + 1;
            tomorrow.month = today.month;
            tomorrow.year = today.year;
        }else if(today.month==12){//today是月末且是12月
            tomorrow.day = 1;
            tomorrow.month = 1;
            tomorrow.year = today.year + 1;
        }else{//today是月末
            tomorrow.day = 1;
            tomorrow.month = today.month + 1;
            tomorrow.year = today.year;
        }
        printf("tomorrow's date is %d-%d-%d\n",
               tomorrow.year, tomorrow.month, tomorrow.day);
        
    return 0;
}

int NumberOfDays(struct date d){
    int days;

    const int daysPerMonth[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    if(d.month==2 && isLeap(d))
        days = 29; //注意if的简略写法,只能写一条语句,不带{}
    else
        days = daysPerMonth[d.month-1];

    return days;
}//判断每个月的月末是哪天

bool isLeap(struct date d){
    bool leap = false;//注意bool赋值格式,且需要有<stdbool.h>的头文件

    if((d.year %4 ==0  &&  d.year %100 !=0)||(d.year %400 == 0))
        leap = true;

    return leap;
}//bool类型函数,判断是否为闰年
