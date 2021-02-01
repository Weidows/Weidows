/*
 * @Author: Weidows
 * @Date: 2020-06-02 11:02:20
 * @LastEditors: Weidows
 * @LastEditTime: 2020-09-26 00:21:15
 * @FilePath: \Weidows\C++\homework\过去\围圈报数.c
 * 
 * n个人围成一圈,从1~3报数,报到3的退出,问最后剩下原来的第几号
 */
//库
#include <stdio.h>
//函数 && struct && typedef

int main()
{
    const int n;
    printf("Input n :");
    scanf("%d", &n);
    int people[n];
    for (int i = 0; i < n;i++){
        people[i] = 1;
    }
    while(1){
        static int num = 1, people_quit = 0;
        for (int i = 0; i < n; i++){
            if(people[i]==1){
                if(people_quit=n-1){
                    printf("第%d号",i+1);
                    return 0;
                }
                if(num%3==0){
                    people[i] = 0;
                    people_quit++;
                }       //喊到3的退出
                num++;
            }
        }           //一轮
    }       //多轮
}
