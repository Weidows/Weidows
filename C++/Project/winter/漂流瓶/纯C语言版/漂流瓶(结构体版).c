/*--------------------------------------------------------------------
���� C���� Ư��ƿ
���ߣ� 404name | ����N
˵��:  ����Ԥ���� | ���Զ�������
�Զ��巽����
    ���������ݣ�
        ���ṹ��18�нṹ����������ͬ������ݼ���
        ֮��ϵͳ���Զ��������ݴ���ҳ�棬�����з�ҳ��
        ������и������
    �����Ľ��棺
        �Լ������߼���������Ӧ�����Լ���
    �����Խ��ܣ�
        User ����10�������ַ�(5������/10Ӣ���ַ�)
        Datetime 2020-03-05 04:11:12���ڵĳ���
                 ����C���԰汾��֧���Զ�����ʱ��
                 �����������Լ����ú�������
        Message  108�����ֵ��������ݣ�������Χϵͳ��Ĭ���ں������ʡ�Ժ�
�汾��ʱ�䣺 ver 1.0.0  2020-06-10 20:20:12
--------------------------------------------------------------------*/
#include <conio.h> //����getch����
#include <stdio.h>
#include <stdlib.h> //����rand
#include <string.h>
#include <windows.h>
#define width 64
#define height 22
#define page_include 6
const char block1[3] = "��";
const char block2[3] = "��";
const char point[4][3] = {{"/"}, {"��"}, {" "}, {"  "}};

struct bottle
{
    char User[11];
    char Datetime[30];
    char Message[500];
} bottles[200] = {
    {"����������", "2020-06-08 17:39:43", "���ţ�����ѡ��һ����ȥ����;��"},
    {"����Ů��", "2020-05-31 02:32:56", "����15�ˣ������кܶ��´ﲻ�����������졢�����Ǹ�������¸ҡ�����Ŭ�������������Ա�"},
    {"��Ƥũ��", "2020-05-20 19:53:16", "����ѧ��Ӣ������ȥ��һ��������ȥ���������ǲ�������д���ã����ж�󣿹����ǲ����������ô���Ĵ��ԭ�������ǲ���������Ӱ����������һ��һ�����׵�С�����Լ��ͣ�ϣ���߰������һ��ڹ��ⷢһ�����ӣ��������������ͣ�Ϊ���Լ���Ը����Ϊ����ô���ķ羰��Ϊ����ϲ�������Ӱ�Ӽ����ǣ�������-�ձ��뿭��-��˹���أ���"},
    {"�ݼ�", "2020-05-06 01:32:07", "��Ϊ�����������������˸����Ʒ�����վ�ֻ�����Ʒ��û�пɱ��ԣ����Ǿ����ϵļ��к�ο�����������ã���ĺ�����Ҳ�ܼ尾����"},
    {"�϶�", "2020-04-13 14:26:05", "������һ�������ѵ��¡�"},
    {"�϶�", "2020-04-13 14:27:05", "��ϲ���㡭"},
    {"�����úõ�", "2020-04-14 15:24:05", "ϣ����Ҷ��ܺúõĻ��ߣ��Ͼ������������ã�����ɳ�� ˯�ۻ軨 ����ͷ���������Ӱ����һ������"},
    {"88888", "2020-04-15 14:27:05", "2020-04-15 14:27:05"},
    {"10086", "2020-05-15 12:27:05", "�𾴵Ŀͻ�������,5���˵��Ѿ�������,�뼰ʱ�ɷ��"},
    {"�羺ʳ��", "2020-02-15 15:27:03", "ÿһ�ſ��ƣ����Ƕ����һ��˼��Ҷ�Ӯ�����У�ȴӮ������İ�"},
    {"������־", "2020-03-15 14:27:05", "����������֮�䡣 �ҵĽ���ԸΪ��Ч�͡� "},
    {"˼��", "2020-02-25 02:24:25", "������ҹ�����ŵ��̻� ��ȼÿһ��ʢ�� ������Ī���˸� ʱ������һ�� ���ĵ���ʧ���� ����ӳ��ϼ Ϧ������� ��ǣ���� ������Ϥ�Ľ��� ֱ����ͷ ��������ؽ�����ӵ ���������������� Ĩ��ȥ��˼�� б�����΢Ц ���н�Զ ���µ�΢�紵ɢ������ ����������ļ� ������ȴ �������������ŵ��΢Ц���� "},
    {"�Һ�����", "2020-01-03 05:21:05", "������5���׼䣬���Ƿ����˱˴ˡ�Ҳ������5����֮�䣬���Ǵ���˱˴ˡ�"},
    {"111dw11", "2020-03-05 04:11:12", "ϣ��������"},
    {"��������", "2020-06-09 23:51:12", "��Ϊһ��ɽ���ˣ����ر�����ɽ���Ĺ������硣��ѧ��ҵ�������ɽ����ũ����Ǯ����������������ߵ�¥����������������С�Ӵ��Ļ���ɲ�����ʵ�µ��١�ɽ�������ڿ����������ľ��ǳ������˰ɣ�û�ж������壬�����Ժ�Ҳ���ٻ�ȥ�ˡ����ż��˺úõ��ڱ�����ɡ� "},
    {"ʱ��", "2020-06-09 20:02:25", "�˼��̻���ʲô���أ� �м���С���ʳ.....��������տ��������̣���Ƥ���棬±ζ"},
    {"14449", "2020-06-08 16:00:11", "����úõػ���ȥ����Ϊ�����ڹ��ò��ã������������ȥ�������������ú�һ�㣬ֻ��һ��ͺá� "},
    {"С����", "2020-06-08 14:05:21", "Ҳ�������������"},
    {"һλ����", "2012-01-22 23:41:48", "�������ĵĳ�����ҹ�� �ؼ���Ϊһ�����ݵİ���绰 ���ﳳ������ һ����վ����̨�ϱ߿��̻��ߵ��� �䵽���� ��󱻰�Ӳ���ط� �����ڻ���ͣ�Ĳ� ��˵ 2012���������� �ܲ���һ�춼��Ҫ�� "},
    {"��������", "2012-01-22 22:21:45", "����Ĳ���ϲ����һ���еģ������ص������õ���Ҳ���еĺ��������¶�����Ľ�����Ҫ���˺�ô���Ը�Ҳ�ܺã�����ʦ����Ц���š�����Ҳ�ܺ��������ʲô�ĸ��޻���˵���������ˡ� "},
    {"????", "2015-03-25 22:20:15", "ʲô�п���?���������Լ��ı��˶�ÿ����΢Ц"},
    {"��������", "2010-04-21 21:21:10", "����gg����mm��"},
    {"¬��ΰ", "2019-02-15 20:05:05", "�ң�¬��ΰ��û�п���!"},
    {"����N", "2020-06-10 18:57:21", "�����������ۻ��ˣ������������ѽ~~~"},
    {"Ư��ƿ", "2017-02-15 14:05:05", "��л���յ������Ư��ƿ�����ڴ󲿷��˶�������Ư��ƿ�ˣ�����Ļǰ���㻹�ڿ����������������Ϣ���ǳ���л��...ϣ�����Ư��ƿ�ܳ����Ź�ȥ������һֱƯ����"},
    {"С����", "2018-01-10 12:04:05", "�����ϲ���㣬����֪�����䲻�ϣ�������Զȥ���ֺ����ᣬ��ģ�����ġ�����������������������������"},
    {"�߿�����", "2020-06-08 14:50:21", "��Ҫȥ��Ĵ�ѧ��������������������"},
    {"ʱ��", "2017-05-07 12:35:21", "˭�ּǵ������������أ������Ư��ƿ��Ц����������������Ͳ����ˣ�Ҫ˭ȥ�����أ�"},
    {"Java", "2018-06-05 13:25:51", "������������õ����ԣ�"},
    {"awsl", "2019-06-08 21:25:51", "ʱ�䲻������ǳ嵭���������"},
    {"����", "2017-11-18 01:25:05", "�ҿ�����Զȥ��������Ϊʲô��Ҫȥ��ңԶ��δ���أ�"},
    {"ɳ��", "2014-10-24 12:24:05", "����sb������sb������sb��������sb������sb������sb������sb������sb������sb������sb������sb������sb������sb��"},
    {"����", "2020-05-01 15:20:51", "�������������ܲ����ˣ��������Σ�ѧ����ȥ��"},
    {"��������", "2020-06-10 14:22:20", "�ɱ�"},
    {"��������", "2020-06-01 12:00:21", "��ͯ�ڿ���ѽ"},
}; //����׷�����ݼ���

char keymap[10][7] = { //��Ӧ���ȥȥ��
    {"xxxxxx"},
    {"x0000x"},
    {"x1111x"},
    {"x2222x"},
    {"x3333x"},
    {"x4444x"},
    {"x5555x"},
    {"x6789x"},
    {"xxxxxx"}};
int keymap_to_map0[10][2] = { //keymapӳ��·��    +3��Ӧ������ֵĵط�
    {14, 5},                  //0
    {14, 7},
    {14, 9}, //2
    {14, 11},
    {14, 13}, //4
    {14, 15},
    {8, 19}, //6
    {20, 19},
    {34, 19}, //8
    {47, 19}};
int tx, ty, now_x, now_y, function, point_flag;
int page, All_messages, All_pages;
int menu_flag;                // 0���ض����� 1���˵�  2�������  3�������鿴��Ϣ   ���ؼ����λ���
const char mapMaker[8][3] = { //��������߼����������ǲ��� Ҳ�ܸ��ƽ�����������Ŵ�ӡ
    {"/"},                    //0
    {"��"},                    //1
    {"��"},                    //2
    {"��"},                    //3
    {"\\"},                   //4
    {"�x"}};                   //5
const char title[10][50] = {  //ż�����˵���������ҳ��
    {"|��Ϣ|User:            Datetime:           "},
    {"|ƿ��|404name          Datetime:           "},
    {"      ������ҳ�~ ��ӭ���ʹ��             "},
    {"                                           "},
    {"      Ư��ƿ  ver 1.0.0                    "},
    {"                                           "},
    {"      ����C���Դ                        "},
    {"                                           "},
    {"      ��ӭ���ʹ��                         "}};
const char menu[8][12] = { //ż�����˵���������ҳ��
    {"��===="},
    {"������"},
    {"����һ��"},
    {"����һҳ"},
    {"�����̿�"},
    {"����һҳ"},
    {"���ҵ�ƿ��"},
    {"��ҳ�룺01"}};
void HideCursor(int x) //�������
{
    CONSOLE_CURSOR_INFO cursor_info = {1, x}; //��ߵ�0�����겻�ɼ�
    SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &cursor_info);
}

void gotoxy(int x, int y) //���꺯��
{
    HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
    COORD pos;
    pos.X = x;
    pos.Y = y;
    SetConsoleCursorPosition(handle, pos);
}

void change_menu(int turn) //���Ĳ˵��Ĺ��ܰ�ť��ʾ  ���벻ͬҳ����ʾ��ͬ����
{
    int flag = 0, i;
    if (turn == 1)
        flag = 0;
    else
        flag = 1;
    for (i = 0; i < 8; i++)
    {
        if (i == 0)
        {
            gotoxy(11, 2);
            printf("%s", title[i]);
        }
        else
        {
            if (i > 1)
                SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 5);
            gotoxy(11, 1 + 2 * i);
            printf("%s", title[i]);
        }
    }
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 0);
    for (i = 6; i <= 9; i++)
    {
        tx = keymap_to_map0[i][0];
        ty = keymap_to_map0[i][1];
        gotoxy(tx, ty - 1);
        printf("%s", menu[(i - 6) * 2 + flag]);
    }
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 1);
}

void init() //��init
{
    //��ʼ����Ϣ��Ŀ��ҳ������
    int i, j;
    for (i = 0;; i++)
    {
        if (strlen(bottles[i].Datetime) == 0)
            break;
    }
    All_messages = i;
    page = 0;
    All_pages = (All_messages % page_include == 0 ? All_messages / page_include : All_messages / page_include + 1);
    //��������ʾ
    HideCursor(0);
    point_flag = 0; //�����̬
    now_x = 7, now_y = 1;
    //HideCursor(); //���ع��
    menu_flag = 1;
    //�߼�������ͼ    Ҳ���Ը����������ַ���ȥ��ӡ����Ҫ��for�������ϵ��ٸ���ҳ��
    for (i = 0; i < height; i++)
    {
        for (j = 0; j <= width; j++)
        {
            if ((i > 0 && i < height - 1 && (j == 0 || j == width)) || (i > 1 && i < height - 2 && (j == 2 || j == width - 2)))
            {
                gotoxy(j, i);
                printf("%s", mapMaker[2]);
            }
            if ((i == 0 && j == 0) || (i == 1 && j == 2) || (i == height - 1 && j == width - 1) || (i == height - 2 && j == width - 3))
            {
                gotoxy(j, i);
                printf("%s", mapMaker[0]);
            }
            if ((i == 0 && j == width - 1) || (i == 1 && j == width - 3) || (i == height - 1 && j == 0) || (i == height - 2 && j == 2))
            {
                gotoxy(j, i);
                printf("%s", mapMaker[4]);
            }
            if ((i == 0 && j < width - 1 && j % 2 == 1) || (i == 1 && j >= 3 && j < width - 3 && j % 2 == 1))
            {
                gotoxy(j, i);
                printf("%s", mapMaker[1]);
            }
            else if ((i == height - 1 && j < width - 1 && j % 2 == 1) || (i == height - 2 && j >= 3 && j < width - 3 && j % 2 == 1))
            {
                gotoxy(j, i);
                printf("%s", mapMaker[5]);
            }
            else if (i >= 2 && i <= 16)
            {
                if (j == 8 || j == width - 9)
                {
                    gotoxy(j, i);
                    printf("%s", mapMaker[3]);
                }
                else if (i > 2 && i % 2 == 0 && j >= 16 && j <= width - 12 && j % 2 == 1)
                {
                    gotoxy(j, i);
                    printf("%s", mapMaker[1]);
                }
            }
        }
        Sleep(50);
    }
    gotoxy(4, height - 3);
    printf("      ����        ������        ������       ��������    ");
    //������ͼ������

    //��ʾ��ʼ�Ľ���ѡ��3����
    change_menu(menu_flag);

    //��λ��ʼ���ָ��
    function = keymap[now_x][now_y] - '0';
    tx = keymap_to_map0[function][0];
    ty = keymap_to_map0[function][1];
    gotoxy(tx, ty);
    printf("%s", point[point_flag]);
    function = 0;
}

int move(int x, int y, int limit_x1, int limit_x2, int limit_y1, int limit_y2, int xx, int yy)
{
    //��������ʼ����x y  ���ƻ�ռ� x����  y���� �ƶ����� x y
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 0);
    int last_x = x, last_y = y;
    function = keymap[x][y] - '0';
    ;
    tx = keymap_to_map0[function][0];
    ty = keymap_to_map0[function][1];
    gotoxy(tx, ty);
    //printf("%s",point);
    printf("%s", point[point_flag]);
    char ch = '\0', ch1;
    char res[20];
    while (ch != ' ')
    {
        ch = getch();
        gotoxy(tx, ty);
        printf("%s", point[point_flag + 2]); //����ո�����
        if (ch == -32)
        { //ͬʱ����wasd  ���������Ҽ�   //�����ȡ����һ����-32��ô ������ȡһ���ַ�
            ch1 = getch();
            switch (ch1)
            {
            case 72:
                ch = 'w';
                break;
            case 75:
                ch = 'a';
                break;
            case 80:
                ch = 's';
                break;
            case 77:
                ch = 'd';
                break;
            }
        }
        switch (ch)
        {
        case 'w':
            x = x - xx;
            break;
        case 's':
            x = x + xx;
            break;
        case 'a':
            y = y - yy;
            break;
        case 'd':
            y = y + yy;
            break;
        case ' ':
            break;
        }
        if (x < limit_x1 || x > limit_x2 || y < limit_y1 || y > limit_y2 || (menu_flag != 2 && (ch == 'w' || ch == 's')))
        {
            x = last_x;
            y = last_y;
        }
        last_y = y, last_x = x;
        if (x == 7) //��x == 7��ʱ������ʾ == /
            point_flag = 0;
        else // ��Ȼ��x < 7��ʱ������ O
            point_flag = 1;
        function = keymap[x][y] - '0';
        tx = keymap_to_map0[function][0];
        ty = keymap_to_map0[function][1];
        gotoxy(tx, ty);
        printf("%s", point[point_flag]);
    }
    if (x < 7)
        x = 7, y = 1;
    now_x = x, now_y = y; //����x y
    gotoxy(tx, ty);
    printf("%s", point[point_flag + 2]); //����ո�����
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 1);
    return function;
}

void show_message(int id) //��ʾ��id����Ϣ   ������ʾ����Ĵ���
{
    int i;
    gotoxy(17, 3);
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 4);
    printf("%-17s%s", bottles[id].User, bottles[id].Datetime);
    int index = 0;
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 5);
    for (i = 0; i <= 5; i++)
    {
        tx = keymap_to_map0[i][0];
        ty = keymap_to_map0[i][1];
        gotoxy(tx + 3, ty);
        printf("                                     ");
    }
    if (id == -1) //��װû�̵�
    {
        int flag = rand() % 4;
        gotoxy(17, 3);
        if (flag == 0)
            printf("�ۣ��ô�һֻ�з������ �� �����̿�  ");
        else if (flag == 1)
            printf("���ˮ���Σ���ȥ�����ơ������̿�    ");
        else if (flag == 2)
            printf("�̵������ӡ����� �� �����̿�        ");
        else if (flag == 3)
            printf("�̵�һ����ƿ�ӣ�����ʲô��û�С�    ");
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 1);
        return;
    }
    for (i = 0; i <= 5; i++)
    {
        tx = keymap_to_map0[i][0];
        ty = keymap_to_map0[i][1];
        gotoxy(tx + 3, ty);
        int cnt = 18 * 2;
        while (cnt-- && bottles[id].Message[index] != '\0')
        {
            if (i == 5 && cnt == 1)
            {
                printf("��");
                cnt--;
                break;
            }
            printf("%c", bottles[id].Message[index]);
            index++;
        }
        if (bottles[id].Message[index] == '\0' && cnt)
        {
            while (cnt--)
            {
                printf(" ");
            }
        }
    }
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 1);
}

void show_page(int page) //��ʾ�ڼ���ҳ��
{
    int start = (page - 1) * page_include;
    int end = page * page_include;
    int i;
    if (end > All_messages)
        end = All_messages;
    int index = 0;
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 5);
    for (i = 0; i <= 5, start < page * page_include; i++, start++)
    {
        tx = keymap_to_map0[i][0];
        ty = keymap_to_map0[i][1];
        gotoxy(tx + 3, ty);
        if (start < end)
            printf("%-17s%s", bottles[start].User, bottles[start].Datetime);
        else
            printf("                                     ");
    }
    tx = keymap_to_map0[9][0];
    ty = keymap_to_map0[9][1];
    gotoxy(tx + 8, ty - 1);
    printf("%02d", page);
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 1);
}

void throw_bottle() //��Ư��ƿ   == ���ӹ���   �������ڴ�������
{
    int i;
    HideCursor(1);
    for (i = 0; i <= 5; i++)
    {
        tx = keymap_to_map0[i][0];
        ty = keymap_to_map0[i][1];
        gotoxy(tx + 3, ty);
        printf("                                     ");
    }
    gotoxy(17, 3);
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 4);
    printf("          ||�ڴ����벻Խ�ߵ��û���  ");
    char username[100];
    gotoxy(17, 3);
    scanf("%s", username);
    if (strlen(username) > 10)
    {
        gotoxy(17, 2);
        printf("�û�������,�������룬���س��˻�       ");
        getchar();
        getchar();
        change_menu(menu_flag);
        return;
    }
    else
    {
        gotoxy(17, 2);
        printf("�ɹ�����,%10s|                 ", username);
        gotoxy(17, 3);
        printf("�������������а��س�����             ");
    }
    int index = 0;
    char res[500] = "\0";
    char temp[50];
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 5);
    for (i = 0; i <= 5; i++)
    {
        getchar();
        tx = keymap_to_map0[i][0];
        ty = keymap_to_map0[i][1];
        gotoxy(tx + 3, ty);
        scanf("%[^\n]", &temp);
        strcat(res, temp);
    }
    strcpy(bottles[All_messages].User, username);
    strcpy(bottles[All_messages].Message, res);
    strcpy(bottles[All_messages].Datetime, "2020-06-08 17:39:43 ");
    All_messages++;
    All_pages = (All_messages % page_include == 0 ? All_messages / page_include : All_messages / page_include + 1);
    gotoxy(17, 2);
    printf("Ư��ƿ������󺣣��س�����");
    getchar();
    getchar();
    menu_flag = 1;
    change_menu(menu_flag);
    HideCursor(0);
}

void manchange() //��Ϊ�������
{
    char ch, ch1;
    if (kbhit())
    {
        function = move(now_x, now_y, 1, 7, 1, 4, 1, 1);

        if (function >= 0 && function <= 5) //�鿴��������mҳ�ĵ�n+1��
        {
            menu_flag++;
            show_message((page - 1) * page_include + function); //ȡ���ݿ�ڼ���
        }
        if (function == 6) //����
        {
            if (menu_flag <= 2)
            { //�鿴�������Է��ز˵�
                menu_flag = 1;
                change_menu(menu_flag);
            }
            if (menu_flag == 3)
            { //�������Բ鿴��ϸ  ���� ����
                menu_flag--;
                show_page(page);
            }
        }
        else if (function == 7)
        {
            if (menu_flag == 1)
            { //��һ��
                throw_bottle();
            }
            else
            { //��һҳ
                if (page > 1)
                {
                    menu_flag = 2;
                    show_page(--page);
                }
            }
        }
        else if (function == 8)
        {
            if (menu_flag == 1) //���̿�
            {
                if (rand() % 3 == 1)
                    show_message(-1); //û�̵�
                else
                    show_message(rand() % All_messages); //�����
            }
            else
            { //��һҳ
                if (page < All_pages)
                {
                    menu_flag = 2;
                    show_page(++page);
                }
            }
        }
        else if (function == 9)
        {
            if (menu_flag == 1)
            {
                menu_flag++;
                change_menu(menu_flag);
                page = 1;
                show_page(1);
            }
        }
        function = keymap[now_x][now_y] - '0';
        tx = keymap_to_map0[function][0];
        ty = keymap_to_map0[function][1];
        gotoxy(tx, ty);
        printf("%s", point[point_flag]);
    }
}
void autochange() //�Զ�����
{
    //��
}
int main()
{
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10 | 1);
    //SetConsoleTextAttribute
    //���ÿ���̨����������ɫ�ͱ���ɫ��
    init();
    while (1)
    {
        autochange();
        manchange();
    }
}

