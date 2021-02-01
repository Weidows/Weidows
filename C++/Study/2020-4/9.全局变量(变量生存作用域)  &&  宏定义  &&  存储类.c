/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:34:14
 * @LastEditors: Weidows
 * @LastEditTime: 2020-05-29 00:34:26
 * @FilePath: \demo\C\9.全局变量(变量生存作用域)  &&  宏定义  &&  存储类.c
 */ 
//19.全局变量(变量生存作用域)  &&  宏定义  &&  存储类
#include<stdio.h>
//宏定义
    #define PI 3.14
    #define Output int i1 = 0;\
                printf("i1=%d\n", i1)    //反斜杠'\'的作用是续行

    //没有赋值的define是用来条件判断的
        #define _DEBUG
    /*预定义的宏
        __LINE__ 显示行号
        __FILE__ 显示文件名
        __DATE__ 显示编译时的日期
        __TIME__ 显示编译时的时间
        __STDC__ 未知
    */

//在这里定义是全局变量,自动初始化为0/NULL,如果赋值不能赋变量和函数(报错)
    int i;//自动i=0,后续只能进行一次定义赋值给全局变量
    int *p;//p=NULL
    /* int i1 = i;这种就不对,除非i是const定义的全局变量
    全局变量被屏蔽时要使用需要加两个冒号"::",格式:   ::global   */

/*存储类 堆(静态存储 )  栈(动态存储)
    全局变量，静态局部变量，静态全局变量都在静态存储区分配空间，而局部变量在栈里分配空间
    auto (只能修饰局部变量,默认就是这个)
    register 定义存储在寄存器中而不是 RAM 中的局部变量,速度极快(只能修饰局部变量和形参)
    static
        (静态全局变量)修饰全局变量时会把全局变量局限在此编译单元里(此文件+头文件)
        (静态局部变量)修饰局部变量时会使程序在生命周期内保持局部变量的存在，而不需要在每次它进入和离开作用域时进行创建和销毁。(下有例子)
    extern(类似于.h头文件作用) 用于引用其他文件声明的#全局#变量/函数,本质上是声明,
        但是用extern声明时不能定义/赋值(报错).
        用extern声明XX后,XX对其后的#整个工程#可见,声明可以有多个,但定义只能有一个,extern就是在此文件声明有这么个东西,并去找整个工程有没有这个东西的全局定义(没有的话就报错)
        //main.c
            #include <stdio.h>
            
            int count ;
            extern void write_extern(); //声明此函数是全工程函数,也就是引入函数的定义
            
            int main()
            {
            count = 5;
            write_extern();
            }
        //support.c
            #include <stdio.h>
 
            extern int count;   //声明count,也就是引入main.c中全局变量count
            
            void write_extern(void)
            {
            printf("count is %d\n", count);
            }
    Tips:
        A.若全局变量仅在单个C文件中访问，则可以将这个变量修改为静态全局变量，以降低模块间的耦合度；
        B.若全局变量仅由单个函数访问，则可以将这个变量改为该函数的静态局部变量，以降低模块间的耦合度；
        C.设计和使用访问动态全局变量、静态全局变量、静态局部变量的函数时，需要考虑重入问题，因为他们都放在静态数据存储区，全局可见；
        D.如果我们需要一个可重入的函数，那么，我们一定要避免函数中使用static变量(这样的函数被称为：带"内部存储器"功能的的函数)
        E.函数中必须要使用static变量情况:比如当某函数的返回值为指针类型时，则必须是static的局部变量的地址作为返回值，若为auto类型，则返回为错指针。
*/

int main(){
    int i = 1;
    printf("函数名=%s  i=%d  p=%p\n", __func__,i,p);\
    //__func__输出本函数的名称(这里显示main)

    { //如果本地变量和全局变量重名,则在这个函数内那个全局变量被隐藏
        int i = 2;
        printf("i=%d %s\n", i,__func__);//这种内层的函数名也是main
        Output;
    }
    printf("文件名:%s  行号:%d\  ", __FILE__, __LINE__);
    printf("日期:%s  时间:%s\n", __DATE__, __TIME__);

    return 0;
}

void func_1(void){ 
//'thingy' 是局部变量,只初始化一次,每次调用函数 'func1' 'thingy' 值不会被重置。
    static int thingy=5;
    thingy++;
    printf("thingy为%d",thingy);
}
