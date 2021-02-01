/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:38:16
 * @LastEditors: Weidows
 * @LastEditTime: 2020-05-29 00:38:30
 * @FilePath: \demo\C\2.位段.c
 */ 
//位段
//库
    #include<stdio.h>
//函数
    void Bin(unsigned int Num);
    typedef struct {    //3+1+1+27=32,这个位段结构占用一个int大小(数据先后不定但连续)
        unsigned int leading : 3;   //这种形式是leading占用多少位
        unsigned int Flag1 : 1;
        unsigned int Flag2 : 1;
        int trailing : 27;
    } U0;
//main
int main()
{
    U0 uu = {2, 0, 1, 0};   //typedef有集合赋值的优势
    printf("sizeof(uu)=%lu\n", sizeof(uu));
    Bin(*(int *)&uu);   //取uu结构地址强转成int*,再进行访问

    return 0;
}

void Bin(unsigned int Num){
    unsigned int mask = 1u << 31;   //无符号int型值1,左移31位,也就是最高位为1,其余为0
    for (; mask ; mask >>=1){   //不需要初始化计数器可空着,mask!=0为条件
        printf("%d", Num & mask ? 1 : 0);
    }
}
