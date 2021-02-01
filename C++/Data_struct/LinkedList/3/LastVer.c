/*
 * @Author: Weidows
 * @Date: 2020-05-03 01:18:32
 * @LastEditors: Weidows
 * @LastEditTime: 2020-11-22 16:32:23
 * @FilePath: \Weidows\C++\Data_struct\LinkedList\3\LastVer.c
 * 3.终极优化版单向链表
 */

//库
#include <stdio.h>
#include <stdlib.h> //malloc申请内存,system函数调用
#include <string.h> //strcmp用到
#define LengthOfName 10

//函数 && struct && typedef
typedef struct stu
{
  long long int id;        //链表数据域-学号
  char name[LengthOfName]; //链表数据域-姓名
  struct stu *next;        //链表指针域,指向下一个节点
} NODE;                    //把struct stu命名为NODE

NODE *create_list(int);               //初始化链表并录入第一批int n个节点
void print(NODE *);                   //对传入的链表输出
void insert_change_Node(NODE *, int); //对传入的链表的第int n个节点处插入或修改
void *list_reversed(NODE *);          //对传入的链表倒置
void Delete_node(NODE *);             //对传入的链表以序号、id、name三种方式筛查删除
int Node_length(NODE *);              //对传入的链表统计节点个数并返回节点数
void Sort_List(NODE *);               //对传入的链表进行冒泡排序

int main()
{
  //创建初始化
  char *Choice_menu[5] = {
      //指针数组,作为函数选择菜单
      "\n************************************************************",
      "\n0: 输出链表/退出.\t1:插入/修改节点.\t2: 倒置链表.",
      "\n3: 删除节点\t\t4:统计节点数.\t\t5.按ID排序",
      "\n************************************************************\n",
      "\n                   单向链表数据管理系统\n", //后加的,懒的改顺序了
  };
  int n = 0, choice_num = -1; //初始化时链表节点数n,指令数choice_num
  system("cls");
  printf("欢迎使用!\n%s%s", Choice_menu[4], Choice_menu[3]);
  do
  { //保险循环,确保n>0
    printf("输入链表初始化要创建的节点个数: ");
    scanf("%d", &n);
  } while (n < 0);
  NODE *Linked_list = create_list(n); //此处创建并录入第一批数据,链表成型

  //功能函数调用
  while (choice_num != 0)
  { //初始化时定义了choice_num
    system("cls");
    printf("%s %s %s %s %s请输入想实现的功能序号:", Choice_menu[4], Choice_menu[0], Choice_menu[1], Choice_menu[2], Choice_menu[3]);
    scanf("%d", &choice_num);
    switch (choice_num)
    {
    case 0:
    {
      printf("按任意键输出链表 或者输入'Q'退出程序,请输入:");
      setbuf(stdin, NULL); //清空缓冲区
      char choice = getchar();
      if (choice == 'q' || choice == 'Q') //输入e或E退出所有
        printf("谢谢使用!\t");
      else
      {
        print(Linked_list);
        choice_num = 1; //置于非0状态,循环程序继续
      }
      break;
    }
    case 1:
    {
      printf("请输入对第几(N)号节点操作:");
      int n = 0;
      scanf("%d", &n);
      insert_change_Node(Linked_list, n);
      break;
    }
    case 2:
    {
      list_reversed(Linked_list);
      break;
    }
    case 3:
    {
      Delete_node(Linked_list);
      break;
    }
    case 4:
    {
      printf("总计节点数为 %d 个.\n", Node_length(Linked_list));
      break;
    }
    case 5:
    {
      Sort_List(Linked_list);
      break;
    }
    default:
    {
      printf("输入错误,请重试.\n");
      continue;
    }
    }
    system("pause"); //暂停,用于确认信息
    system("cls");   //清屏
  }
  return 0; //保险起见把终止放在外面
}

//尾插法创建链表(返回头 || 尾)
NODE *create_list(int n)
{
  NODE *head, *node, *end;
  head = (NODE *)malloc(sizeof(NODE));
  end = head;
  for (int i = 0; i < n; i++)
  {
    node = (NODE *)malloc(sizeof(NODE));
    printf("分别输入第%d个ID,name : ", i + 1);
    scanf("%lld %s", &node->id, &node->name);
    end->next = node; //end是上个节点,令其指向当前节点
    end = node;       //让end指向当前节点
  }
  end->next = NULL;
  //选择返回指针
  printf("press any key return head\tor press 'e' to return end:");
  setbuf(stdin, NULL);
  char choice = getchar();
  if (choice == 'e' || choice == 'E')
    return end;
  else
    return head;
}

//输出链表
void print(NODE *head)
{
  NODE *p = head->next; //for初始条件域内无法同时定义多个不同类型的变量
  for (int i = 1; p != NULL; i++, p = p->next)
  {
    printf("第%d个节点:%lld \t %s \n", i, p->id, p->name);
  }
}

//插入(后插) && 修改链表
void insert_change_Node(NODE *headList, int n)
{
  NODE *p = headList; //创建NODE类型的移动指针p
  for (int i = 0; i < n; i++, p = p->next)
  {
    if (p->next == NULL)
    {
      printf("%dth node hasn't found!\t Input N again or press nothing  to exit :", n);
      scanf("%d", &n); //重置n
      i = 0;
      p = headList; //都重置
    }
  } //判断是否存在并把p指向第n节点
  while (1)
  {
    printf("insert or change node? input 'i' or 'c':");
    setbuf(stdin, NULL);
    char choice = getchar();
    if (choice == 'i' || choice == 'I')
    { //插入
      NODE *insertNode = (NODE *)malloc(sizeof(NODE));
      printf("input id: ID & name :");
      scanf("%lld %s", &insertNode->id, &insertNode->name);
      insertNode->next = p->next;
      p->next = insertNode;
      break;
    }
    else if (choice == 'c' || choice == 'C')
    { //修改
      printf("请输入修改后的数据:");
      scanf("%lld %s", &p->id, &p->name);
      break;
    }
    else
    {
      printf("输入错误.请重试.\n");
      continue;
    }
  }
}

//倒置链表
void *list_reversed(NODE *List)
{
  if (List == NULL || List->next == NULL)
  { //保证链表非空
    printf("链表过小,无法倒置.\n");
    return List;
  }
  else
  {
    NODE *backward = List->next,
         *temp = (List->next)->next,
         *forward = (List->next)->next;
    while (forward != NULL)
    {
      forward = forward->next; //forward前进
      temp->next = backward;   //指针反转
      backward = temp;         //backward前进
      temp = forward;          //temp前进
    }
    (List->next)->next = NULL; //原第二个节点指向NULL
    List->next = backward;
  }
}

//删除节点
void Delete_node(NODE *List)
{
  NODE *pointer = List->next, *pointer_back = List; //创建移动指针
  long long int Del_num = 0, Del_id = 0;
  char *Del_name = "", choice = 0;
  while (choice == 0)
  {
    printf("A: 节点序号\tB: id\tC: name 请输入筛查类型:");
    setbuf(stdin, NULL);
    switch (choice = getchar())
    {
    case 'a':
    case 'A':
    {
      printf("输入要删除的节点序号:");
      scanf("%lld", &Del_num);
      break;
    }
    case 'b':
    case 'B':
    {
      printf("输入要删除节点的id:");
      scanf("%lld", &Del_id);
      break;
    }
    case 'c':
    case 'C':
    {
      printf("输入要删除节点的name:");
      scanf("%s", &Del_name);
      break;
    }
    default:
    {
      printf("输入错误,请重试.\n");
      choice = 0;
      continue;
    }
    }
  }
  for (int i = 1; pointer != NULL; i++,
           pointer_back = pointer, pointer = pointer->next)
  { //一直向后计数移动
    if (i == Del_num || pointer->id == Del_id ||
        strcmp(Del_name, pointer->name) == 0)
    {
      printf("Press any key to confirm deleting\t%dth node: %lld %s,\tor press 'E' to stop:", i, pointer->id, pointer->name);
      setbuf(stdin, NULL);
      choice = getchar();
      if (choice == 'e' || choice == 'E')
      {
        return;
      }
      else
      {
        pointer_back->next = pointer->next;
        free(pointer);
        return;
      }
    }
  }
  printf("Appointed id not found!\n");
}

//统计节点个数
int Node_length(NODE *Linked_list)
{
  int cnt = 0;
  while (Linked_list->next != NULL)
  {
    Linked_list = Linked_list->next;
    cnt++;
  }
  return cnt;
}

//对链表中的元素进行排序--冒泡排序
void Sort_List(NODE *Linked_list)
{
  for (NODE *p = Linked_list->next; p != NULL; p = p->next)
  {
    for (NODE *q = p->next; q != NULL; q = q->next)
    {
      if (p->id > q->id)
      {
        int temp_id = p->id;
        p->id = q->id;
        q->id = temp_id;
        char temp_name[LengthOfName] = "";
        strcpy(temp_name, p->name); //strcpy中不要用*s表示字符串数组
        strcpy(p->name, q->name);
        strcpy(q->name, temp_name);

        /*错误交换节点  */
        // NODE *temp_1 = q;
        // NODE *temp_2 = q_former;
        // q_former->next = p_former->next;
        // q->next = p->next;
        // p->next = temp_1->next;
        // p_former->next = temp_2->next;

        /*二维指针容易出错(如下) */
        // char **str_1 = (char *)&p->name, **str_2 = (char *)&q->name, **str_temp = (char *)&p->name;
        // str_1 = str_2;
        // str_2 = str_temp;
      }
    }
  }
}
