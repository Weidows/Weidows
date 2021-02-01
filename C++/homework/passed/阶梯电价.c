/*
 * @Author: Weidows
 * @Date: 2020-06-14 08:58:12
 * @LastEditors: Weidows
 * @LastEditTime: 2020-06-14 08:58:33
 * @FilePath: \demo\C_\homework\过去\阶梯电价.c
 */ 
//库
    #include <stdio.h>

int main()
{
    double Kwh, price;      //一定注意double的scanf是%lf,float是%f,写错会出错
    printf("Input Kwh:");
    scanf("%lf", &Kwh);
    if(Kwh<=150 && Kwh>0){
        price = Kwh * 0.52;
    }else if(Kwh>150 && Kwh<=280){
        price = 150 * 0.52 + (Kwh - 150) * 0.57;
    }else if(Kwh>280){
        price = 150 * 0.52 + 130 * 0.57 + (Kwh - 280) * 0.82;
    }
    printf("%.2f", price);
    return 0;
}
