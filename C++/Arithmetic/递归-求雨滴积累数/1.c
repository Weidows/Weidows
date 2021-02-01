/*
 * @Author: Weidows
 * @Date: 2020-06-19 20:52:43
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:16:31
 * @FilePath: \Weidows\C++\Arithmetic\递归-求雨滴积累数\1.c
 * 求雨滴存积数
 */
//库
#include <stdio.h>
#define length 12
//函数 && struct && typedef
    int deal(const int *s);
int main()
{
    int s[length]={0,1,0,2,1,0,1,3,2,1,2,1,};
    printf("%d", deal(s));  //调用并输出
    return 0;
}

int deal(const int *s){     //返回雨滴数
    static int height = 1, meter = 0;
    int log_array[length], log = 0;
    
    for (int i = 0; i < length;i++){    //记录同高度的黑块
        if(s[i]>=height){   //把同高度有黑块的那几列记录到数组log_array
            log_array[log] = i;
            log++;
        }
    }

    for(int i = 0; i < log; i++){       //记录量黑块间可容纳雨滴数
        // printf("%d\n", log_array[i]);    //测试,无误.
        if((log_array[i+1]-log_array[i])>1){    //至少空出一个空
            meter += log_array[i + 1] - log_array[i] - 1;
            // printf("%d\n", meter);   //测试
        }
    }

    if (log == 0) //如果这层高度无黑块(到头了)
        return meter;
    else{
        height++;
        meter = deal(s); //递归
    }
}