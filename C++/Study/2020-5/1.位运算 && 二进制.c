/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:36:55
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:14:40
 * @FilePath: \Weidows\C++\Study\2020-5\1.位运算 && 二进制.c
 */ 
//位运算 && 二进制
//库
    #include<stdio.h>
//函数
    void bit_and(); //按位与
    void bit_or();   //按位或
        //"^"单目按位异或
    void bit_Move();
    void Bin();

//main
int main()
{
    bit_and();
    bit_or();
    /*逻辑运算  &&  按位运算
        5&4->4     5&&4->1&&1->1
        5|4->5       5||4->1||1->1
        ~-4->3        !4->!1->0   (负数取反等于其绝对值-1)    */
    bit_Move();
    Bin();
    return 0;
}


void bit_and(){
    int a = 0x5A;                             //0101 1010
    int b = 0x8c;                             //1000 1100
    printf("一0x%d   ", a & b);  //0x08->0000 1000

//应用  1.通过与运算把特定位上的值置0
    int x1 = 0b11010010;  int x2=0b11111110;
    printf("二%i   ", x1 & x2);      //把x1的最后一位置0,其他位不变->210->1101 0010
//应用  2.通过与运算获取某段位上的值
    int x3 = 0b10101111;    //int是32位,没写的高位都是0
    int x4 = 0b0000000011110000;
    printf("三%i\n", (x3 & x4)>>4);    /*取x3十六进制倒数第二位也就是二进制倒数4~8位
    结果10->1010 (x3的4~8位)*/
}

void bit_or(){
//应用  1.通过与运算把特定位上的值置1
    int x1 = 0b11010010;  int x2=0b00000001;
    printf("四%i   ", x1 | x2);      //把x1的最后一位置1,其他位不变->211->1101 0011
//应用  2.原/反/补码运算
    char c = 0xAA; //注意char最多8位,高位补的都是F
    printf("五 c=%hhx  ", c);
    printf("-c=%hhx  ", -c);        //FF=AA+56
    printf("-c=%hhx  ", (char)-c);  //取负数
    printf("~c=%hhx\n", (char)~c);  //按位取反

}

void bit_Move(){
    //  a<<n 相当于 a*=2^n  (注意C语言没有幂符号)
    // a<<=n相当于a=a<<n,如果没有"="a的值不变
    int a = 0xC0000000;
    unsigned int b = 0x80000000;
    printf("六a=%d   ", a);
    printf("b=%u   ", b);    //unsigned按%d输出也是带符号的
    printf("a>>1=%d   ", a>>1); //C 1100 <-> 8  1000
    printf("b>>1=%u\n", b>>1); /*这里移位运算后是带符号的int类型,符号位1不会因为因为改变,于是1000>>1后变成1100  -->>  8 ->C   ,结果不带符号是因为%u输出*/
}

void Bin(){
    int Num;    scanf("%d", &Num);
    unsigned int mask = 1u << 31;   //无符号int型值1,左移31位,也就是最高位为1,其余为0
    for (; mask ; mask >>=1){   //不需要初始化计数器可空着,mask!=0为条件
        printf("%d", Num & mask ? 1 : 0);
    }
}
