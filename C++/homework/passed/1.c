//
//库
    #include<stdio.h>
//函数

//main
int main()
{
    printf("请输入单个字符:");
    char input = getchar();

    int line = 0;
    printf("请输入三角形列数:");
    scanf("%d:", &line);

    int x;
    int y;
    for (y=0; y < line ; y++){
        for (x=0; x <= y ; x++){
            printf("*");
        }
        printf("\n");
    }
    return 0;
}
