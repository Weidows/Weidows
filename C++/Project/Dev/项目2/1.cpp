//25.链表
//库
    #include<stdio.h>
    #include<stdlib.h>
//函数 && struct && typedef
    //数据结构体
    typedef struct Node{    //在结构体内部不能用NODE,只能用此处Node
        int data;           //数据域，用来存放数据域；
        struct Node *Next; //定义结构体指针，指向下一次个与当前节点数据类型相同的节点
    } NODE;

    // 创建链表
        NODE *createList(){ 
            NODE *headNode = (NODE *)malloc(sizeof(NODE));
            //结构体指针+malloc内存->结构体变量
            //表头data数据域
            headNode->Next = NULL;
            return headNode;
        }

    //创建节点
        NODE *createNode(int data){ 
            NODE *newNode = (NODE*)malloc(sizeof(NODE));
            newNode->data = data;
            newNode->Next = NULL;
            return newNode;
        }

    //输出链表
        void printList(NODE *list){
            NODE *pMove = list->Next;   //创建一个移动指向结构体变量
            while(pMove){       //当下一个结构体非空
                printf("%d", pMove->data);  //输出当前pMove代表的节点的data数据
                pMove = pMove->Next;    // #重要#移动向下一个节点
            }
        }

    //插入链表
        void insertNodeByHead(NODE *headNode,int data){
            //创建要插入的节点
            NODE *newNode = createNode(data);
            newNode->Next = headNode->Next;
            headNode->Next = newNode->Next;
        }

//main
int main()
{
    NODE *list = createList();
    insertNodeByHead(list, 1);
    insertNodeByHead(list, 2);
    insertNodeByHead(list, 3);
    printList(list);
    // system("pause");
    return 0;
}

