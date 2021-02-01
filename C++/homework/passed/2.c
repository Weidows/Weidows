//
//库
    #include<stdio.h>
//函数

//main
int main()
{
    char ch1, ch2, ch;
    unsigned char c;
    int a;

    ch1 = 80;
    ch2 = 60;
    ch = ch1 + ch2;
    c = ch1 + ch2;
    a = ch1 + ch2;

    printf("ch1+ch2=%d\n", ch1 + ch2);      //ch1+ch2=140
    printf("ch=%d\n", ch);                //ch=-116  原因:char(-128~127)越界
    printf("c=%d\n", c);                    //c=140    无符号char未越界
    printf("a=%d\n", a);                    //a=140   int型范围大多了,不会越界

    //修改:第二个输出改为 printf("ch=%d\n", 256+ch);
    return 0;
}
