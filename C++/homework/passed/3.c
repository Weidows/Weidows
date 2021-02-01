/*请编写程序将 “ShiYanLou” 译成密码，用原来的字母后面第一个字母替代原来的字母。
例如 A 后面的第二个字母是 B，因此 “ShiYanLou” 应该译成 “TijZboMpv”。
请大家编写一个程序，用赋初值的方法使 c1，c2，c3，c4，c5，c6，c7，c8，c9 
这 9 个变量值分为 'S'，'h'，'i，'，'Y'，'a'，'n'，'L'，'o'，'u'，经过这 9 个变量分别变为'T'， 'i'，'j'，'Z'，'b'，'o'，'M'，'p'，'v'。分别用 putchar 函数和 printf 函数输出这 9 个字符。*/

// “ShiYanLou” 译成密码
//库
    #include<stdio.h>
    #define Str_len 9 
//函数 && struct && typedef

//main
int main()
{
    char encryption[Str_len+1] = "ShiYanLou";   //初始化
    printf("putchar输出:");
    for (int i = 0; i < Str_len;i++){           //加密转化和putchar输出
        encryption[i] = (char)((int)encryption[i] + 1);
        putchar(encryption[i]);
    }
    printf("\n");   //换行
    printf("printf输出:%s\n", encryption);  //printf输出
    return 0;
}
