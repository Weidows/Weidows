/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:32:37
 * @LastEditors: Weidows
 * @LastEditTime: 2020-05-29 00:33:14
 * @FilePath: \demo\C\2_2020-4\7.两种指针结构与函数抽插结合の轮舞.c
 */
//两种 ->结构与函数抽插结合の轮舞
#include <stdio.h>

struct point{
    int x;
    int y;//注意结构单元用分号隔开不是逗号
} getStruct_1(), *getStruct_2(), a[10]; //函数&数组也可以是某结构类型

//一
    struct point getStruct_1(void){
        struct point p;
        scanf("%d %d", &p.x, &p.y);
        return p;
    }//getStruct这个函数是point结构类型

//二
    struct point *getStruct_2(struct point *p){//这里指针类型的函数没必要
        scanf("%d %d", &p->x, &p->y);//p->x等同于(*p).x,指针专用
        return p;//没必要的返回,只是为了展示效果
    }

void output(struct point p){//结构传入函数是传值(函数需要内构结构,效率低下)
    printf("x=%d y=%d\n", p.x, p.y);
}

int main(int argc,char const *argv[]){
    //函数返回结构:一    另造结构return
        struct point  y_1 = {0, 0};
        y_1 = getStruct_1();
        //无法通过return带回结构内值的变化,但是可以带出整个结构给另一个结构
        output(y_1);
    
    //函数返回结构:二   指针(更加高效好用)
        struct point y_2 = {0, 0};
        getStruct_2(&y_2);
        output(y_2);
        output(*getStruct_2(&y_2));//先执行getStruct_2,后执行output
    
    //结构类型数组&&结构类型结构(嵌套结构)
        struct point a[3]={{1,2},{3,4},{5,6},};//数组元素是结构

        struct DateAndTime{
            struct Date{
                int year;
                int month;
                int day;
            };
            struct Time{
                int hour;
                int minute;
                int second;
            };
        };//像是DAT[]这种现用现定义,最好不要提前声明(可能报错)

        struct DateAndTime DAT[2] = {
            {{2020,4,5}, {10,38,01}},//DAT[0]
            {{2020,4,5}, {10,38,01}},//DAT[1]
        };

    return 0;
}
