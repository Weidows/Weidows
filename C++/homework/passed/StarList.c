//           Copyleft@Weidows   2020-5-21

#include <stdio.h>
#include<math.h>
#define star__max_num  7    //最长的行的星星数
#define line_differ (star__max_num + 1) / 2

int main()
{
    for (int line = 1; line <=star__max_num;line++){    //循环行

        for (int i = 0, space = abs(line_differ - line); i < space; i++){
            printf(" ");
        }   //循环空格

        for (int i = 0, star = 2 * (line_differ - abs(line_differ - line)) - 1; i < star; i++){
            printf("*");
        }   //循环星星

        printf("\n");   //换行
    }
    return 0;
}