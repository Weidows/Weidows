/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:42:58
 * @LastEditors: Weidows
 * @LastEditTime: 2020-11-22 16:28:55
 * @FilePath: \Weidows\C++\Data_struct\LinkedList\1\链表.c
 * 1.链表(涉及插入(头插法) & 排序)
 */
//库
#include <stdio.h>
#include <stdlib.h>
//函数 && struct && typedef
//数据域修改
struct student
{
  char name[20];
  int num;
  int math;
} Class1; //(结构体声明或定义必须放在前面,不然编译无法识别)

typedef struct Node
{           //在结构体内部不能用NODE,只能用此处Node
  int data; //用下方外层构造结构方式修改简单快捷
  // struct student Class1;     //数据域，用来存放数据；
  struct Node *Next; //定义结构体指针，指向下一次个与当前节点数据类型相同的节点
} NODE;

NODE *createList();
NODE *createNode(int);
void printList(NODE *);
void insertNodeByHead(NODE *, int);
void deleteNodeByData(NODE *, int);
int length_List(NODE *);
void Sort_List(NODE *);
void Sort_List_2(NODE *);

//main
int main()
{
  NODE *list = createList();
  /*     {  //输入结构体测试
        struct student info;
        while(1){
            printf("请输入学生的姓名,学号,数学成绩:");
            scanf("%s%d%d", &info.name, &info.num, &info.math);
            insertNodeByHead(list,info);
            printf("continue(Y/N)?\n");
            setbuf(stdin, NULL);    //清空输入缓冲区
            int choice=getchar();
            if (choice=='N'|| choice=='n') break;
        }
    }
 */
  //插入
  insertNodeByHead(list, 1);
  insertNodeByHead(list, 2);
  insertNodeByHead(list, 3);
  insertNodeByHead(list, 4);
  insertNodeByHead(list, 5);
  //delete测试
  int num;
  scanf("%d", &num);
  deleteNodeByData(list, num);
  Sort_List(list);
  printf("节点个数:%d\n", length_List(list));
  printList(list);
  // system("pause");运行暂停
  return 0;
}

// 创建链表(头)
NODE *createList()
{
  NODE *headNode = (NODE *)malloc(sizeof(NODE));
  //结构体指针+malloc内存->结构体变量
  //表头data数据域为空
  headNode->Next = NULL;
  return headNode;
}

//创建节点
NODE *createNode(int data)
{
  NODE *newNode = (NODE *)malloc(sizeof(NODE));
  newNode->data = data;
  newNode->Next = NULL;
  return newNode;
}

//输出链表
void printList(NODE *list)
{
  NODE *pMove = list->Next; //创建一个移动指向结构体变量
  // printf("name\tnum\tmath\n");
  printf("已存链表中节点信息:");
  while (pMove)
  { //当下一个结构体非NULL
    // printf("%s\t%d\t%d\n", pMove->Class1.name,
    //     pMove->Class1.num,   pMove->Class1.math);
    printf("%d\t", pMove->data); //输出当前pMove代表的节点的data数据
    pMove = pMove->Next;         // #重要#移动向下一个节点
  }
}

//插入节点(头插法)
void insertNodeByHead(NODE *headNode, int data)
{
  //创建要插入的节点
  NODE *newNode = createNode(data);
  newNode->Next = headNode->Next;
  headNode->Next = newNode;
}

//删除链表
void deleteNodeByData(NODE *headNode, int delData)
{
  NODE *posNode = headNode->Next;
  NODE *posNodeFront = headNode; //定义两个指向指针

  while (posNode->data != delData && posNode != NULL)
  {
    posNodeFront = posNode;
    posNode = posNode->Next; //向后移动
    if (posNode == NULL)
    {
      printf("无法删除%d节点,不存在.\n", delData);
      return; //直接结束函数,不用向后判断了
    }
  }
  posNodeFront->Next = posNode->Next;
  free(posNode); //释放posNode所指节点的内存,也就是删除posNode节点
}

//链表中有效元素个数
int length_List(NODE *headNode)
{
  int len = 0;
  NODE *p = headNode->Next;
  while (p != NULL)
  {
    len++;
    p = p->Next;
  }
  return len;
}

//对链表中的元素进行排序
//(冒泡排序     ------直接交换数据)
void Sort_List(NODE *headNode)
{
  for (NODE *p = headNode->Next; p != NULL; p = p->Next)
  {
    for (NODE *q = p->Next; q != NULL; q = q->Next)
    { //两个移动指针
      if (p->data > q->data)
      {
        int temp = p->data;
        p->data = q->data;
        q->data = temp;
      }
    }
  }
}
//直接选择排序   ------直接交换数据
void Sort_List_2(NODE *headNode)
{
  for (NODE *p = headNode->Next; p != NULL; p = p->Next)
  {
    NODE *t = p;
    for (NODE *q = p->Next; q != NULL; q = q->Next)
    { //两个移动指针
      if (q->data > p->data)
        t = q;
    }
    if (t != p)
    {
      int temp = t->data;
      t->data = p->data;
      p->data = temp;
    }
  }
}
