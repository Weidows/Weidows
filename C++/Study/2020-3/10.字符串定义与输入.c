/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:15:18
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-07 23:43:04
 * @FilePath: \Github\Weidows\C++\Study\2020-3\10.字符串定义与输入.c
 */
#include <stdio.h>
int main()
{
  char string[8];
  scanf("%7s", string);
  /**
   * scanf读到空格/Tab/回车时结束,%7s表示最多读取7位字符,7+'\0'=8(数组大小),不到7个没事,超过的字符不读取,如果下一句也是scanf,则传给它
  */
  printf("%s\n", string);

  //#常见错误#
  char *string2;
  /*1.定义指针没初始化=0;
    2.这种形式的指针没有指向内存地址,不能代表是数组*/
  scanf("%s", string2);

  char buffer[100] = ""; //空字符串,[]内不能为空,否则是真空字符串
  //这样定义buffer[0] == '\0';

  return 0;
}
