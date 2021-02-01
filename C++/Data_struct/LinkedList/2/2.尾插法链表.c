/*
 * @Author: Weidows
 * @Date: 2020-05-29 00:43:53
 * @LastEditors: Weidows
 * @LastEditTime: 2020-10-16 09:16:15
 * @FilePath: \Weidows\C++\Data_struct\LinkedList\2\2.尾插法链表.c
 */ 
//2.尾插法链表
//库
    #include <stdio.h>
    #include <stdlib.h>
    #include <time.h>
//定义全局变量MAX为14 
#define MAX 14

struct list    //描述节点 
{ 
	char string;
	struct list *next;
};
typedef struct list node;
typedef node* link;

char string[MAX]={'I',' ','l','o','v','e',' ','p','r','o','g','r','a','m'};//数据库 

link create_list(link head)   //尾插法建表
{
	link pointer,newpointer;
	int i;
	
	head=(link)malloc(sizeof(node));//动态分配内存 
	
	if(head==NULL)//判断是否分配成功 (防止内存泄露)
		printf("exit\n");
	
	else
	{
		head->string=string[0];
		head->next=NULL;
		pointer=head;
		
		for(i=1;i<MAX;i++)
		{
			newpointer=(link)malloc(sizeof(node));
			
			if(newpointer==NULL)
   				printf("exit\n");
	        else
			{
				newpointer->string=string[i];//尾插法的精髓 
				newpointer->next=NULL;
				
				pointer->next=newpointer;   //将倒数第二个节点的next指向新节点
				pointer=newpointer;     //然后再把pointer指向新节点
			}      
		}
	}  
	return head;
}

void printf_list(link head)  //定义打印列表函数 
{ 
    link temp;
    temp=head;
    
	while(temp!=NULL)
	{
		printf("%c",temp->string);
		temp=temp->next;
	}
} 


void free_list(link head)  //定义一个释放链表函数 
{
	link temp;

	while(head!=NULL)
	{
		temp=head;
		head=head->next;
		free(temp);
	}
}

int main()
{
    link head = create_list(head);
    if(head!=NULL)
	{
		printf_list(head);
		free_list(head);
	}
	
	return 0;
}
