/*
 * @?: *********************************************************************
 * @Author: Weidows
 * @Date: 2020-12-31 21:05:58
 * @LastEditors: Weidows
 * @LastEditTime: 2020-12-31 22:10:48
 * @FilePath: \Weidows\C++\homework\ing\大二上\实验六源代码\二叉树.cpp
 * @Description:
 * @!: *********************************************************************
 */
#include <iostream>
using namespace std;

typedef struct Node //定义二叉树结构
{
  char data;
  struct Node *lchild, *rchild;
} * BiTree, BiTNode;

void CreateBiTree(BiTree &T) //先序创建二叉树
{
  char ch;
  cin >> ch;
  if (ch == '#')
    T = NULL;
  else
  {
    T = new BiTNode;
    T->data = ch;
    CreateBiTree(T->lchild);
    CreateBiTree(T->rchild);
  }
}

void InOrderTraverse(BiTree T) //中序遍历
{
  if (T)
  {
    InOrderTraverse(T->lchild);
    cout << T->data;
    InOrderTraverse(T->rchild);
  }
}

void PreOrderTraverse(BiTree T) //先序遍历
{
  if (T)
  {
    cout << T->data;
    PreOrderTraverse(T->lchild);
    PreOrderTraverse(T->rchild);
  }
}

void PostOrderTraverse(BiTree T) //后序遍历
{
  if (T)
  {
    PostOrderTraverse(T->lchild);
    PostOrderTraverse(T->rchild);
    cout << T->data;
  }
}

int main()
{
  BiTree T;
  cout << "先序遍历输入(以#结束):"; // AB#CD##E##F#GH###
  CreateBiTree(T);

  // 输出
  cout << "中序遍历输出:";
  InOrderTraverse(T);
  cout << endl
       << "先序遍历输出:";
  PreOrderTraverse(T);
  cout << endl
       << "后序遍历输出:";
  PostOrderTraverse(T);
  return 0;
}
