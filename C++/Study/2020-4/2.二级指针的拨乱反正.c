/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:20:02
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:13:31
 * @FilePath: \Weidows\C++\Study\2020-4\2.二级指针的拨乱反正.c
 */
/*
int main()
{
    char **s = "hello world"; //这样是错误的，
    // 因为 s 的类型是 char **而 "hello world "的类型是 char *
    // 虽然都是地址， 但是指向的类型不一样，因此，不能这样用
    // 从其本质来分析， "hello world",
    // 代表一个地址，比如0x003001, 这个地址中的内容是 'h' 
    // 为 char 型，而 s 也保存一个地址 ，这个地址中的内容(*s) 
    // 是char *,所以两者类型是不一样的
    char **s;                 //如果是这样呢？
    *s = "hello world";
    //貌似是合理的，编译也没有问题，但是 printf("%s", *s), 就会崩溃
    //咱来慢慢推敲一下。。
    printf("%s", *s);
    首先得有s 保存的地址，再在这个地址中找到 char *的地址，即 *s;

    举例：

    s = 0x1000;

    在0x1000所在的内存单元中保存了 "hello world"的地址 0x003001 ， *s = 0x003001;

    这样printf("%s", *s);

    这样会先找到 0x1000, 然后找到0x003001;

    如果直接 char **s;

    *s = "hello world";

    s 变量中保存的是一个无效随机不可用的地址， 谁也不知道它指向哪里。。。。， *s 操作会崩溃。。

        所以用 char **s 时，要给它分配一个内存地址。

        char **s;

    s = (char **)malloc(sizeof(char **));

    *s = "hello world";

    这样 s 给分配了了一个可用的地址，比如 s = 0x412f;

    然后在 0x412f所在的内存中的位置，保存 "hello world"的值。。

        再如：

#include <stdio.h>

        void
        buf(char **s)

    {

        *s = "message";
    }

    int main()

    {

        char *s;

        buf(&s);

        printf("%s\n", s);
    }

    二级指针的简单用法。。。。，说白了，二级指针保存的是一级指针的地址，它的类型是指针变量，而一级指针保存的是指向数据所在的内存单元的地址，虽然都是地址，但是类型是不一样的。。。
}
*/