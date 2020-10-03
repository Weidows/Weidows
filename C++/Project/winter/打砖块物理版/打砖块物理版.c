/*-----------------------------------
程序    ：   打砖块（物理版）
作者    ：   404name
完成时间：   2020.3.15
 
游戏默认地图均采用for循环+逻辑构建所以，并没有直接初始化地图

实现原理: autochange() 函数注释那里

bug： 1.目前对角相碰是进行的直接打破该方块，因为测试到进行正常的碰撞返回会重复之前的路。 （算是优化）
      2.未知的原因导致开局影子脱节，目前已经优化到后期几乎看不到脱节。

优化： 实现类似贪吃蛇玩法，制造跟随的移动轨迹，并且交叉的移动轨迹不会直接清除导致脱节。
       配色优化

---------------------------------*/
#include <conio.h> //用于getch（）
#include <math.h>
#include <stdio.h>
#include <stdlib.h> //用于rand
#include <string.h>
#include <windows.h>
#define pi 3.14
const double g = 10; //标准数越模糊，轨迹越连贯。

//----------------------------------------------------------------------------------------------------------------------------------
//	系统默认生成关卡地图，若想自己改造关卡请将1 设置为0并且再下方初始化地图（黏贴地图）
int auto_made_map = 1;
char man_made_map[1000][1000];
//---------------------------------------------------------------------------------------------------------------------------------
char map[1000][1000];
char End[200][800] = {
    {"##   ##   ##            ## #   "},
    {" ##   #   ##### ######  ## ##  "},
    {"   ##### ###### ######  ##  #  "},
    {"   #######          ##  ###### "},
    {"##  ##  # #####     ########## "},
    {" ## ####  #####  ## ######     "},
    {"    ####    ##   ## ##  ##  #  "},
    {"    ## # ######   ###   ## ##  "},
    {"  # ## # ######    ##   ## ##  "},
    {"  # ## #   ##     ####   ###   "},
    {" ## ## #   ##    ##  #   ##   #"},
    {" #  ## #   ##   ##      #### ##"},
    {"## ### #  ###   #     ###  ####"},
    {"## ## ##  ##          ##    ###"},
    {"                               "},
    {"  ##     ##            ##      "},
    {"  ##  ######### ###############"},
    {" ##   ######### ###############"},
    {"##  ##   ##            ##      "},
    {"###### #######    ############ "},
    {"  ##   #######    ############ "},
    {" ##               ##   ##   ## "},
    {"###### #######    ############ "},
    {"###### #######       #####     "},
    {"       ##   ##      ## ####    "},
    {"   ### ##   ##     ##  ## ##   "},
    {"###### #######   ###   ##  ### "},
    {"###    #######   ##    ##   ## "},
    {"       ##   ##         ##      "},
    {"                               "},
    {"     按 两 次 回 车 继 续      "},
};
char menu[40][40] = {
    {"      <--------------->      "},
    {"      <   打 砖 块    >      "},
    {"      <--------------->      "},
    {"                             "},
    {"      <1> 开始游戏  <$>      "},
    {"                             "},
    {"      <2> 贪吃蛇mod <$>      "},
    {"                             "},
    {"      <3> 编辑地图  <$>      "},
    {"                             "},
    {"      <4> 退出游戏  <$>      "},
    {"                             "}};

//全局变量区，在init里面改变
char wall, food, air, brick;
int width, length;
double X, Y, x, y, Vx, Vy, t, V; //默认向下向右为正
int old_x, old_y, head, tail, max, step, if_miss, food_num, goal, color;
int if_start, if_load_snake_mod, debug, life;    //debug模式调成1手动开启
int temp_x, temp_y, menu_x, menu_y, left, right; //临时坐标
double C[8] = {0, 10, 30, 70, 90};               //初始斜抛的角度，自右向上转角(目前已调整好最好的角度)

struct Step //轨迹
{
    int x;
    int y;
} s[1000];

void HideCursor() //光标隐藏
{
    CONSOLE_CURSOR_INFO cursor_info = {1, 0}; //后边的0代表光标不可见
    SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &cursor_info);
}

void gotoxy(int x, int y) //坐标函数
{
    HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
    COORD pos;
    pos.X = x;
    pos.Y = y;
    SetConsoleCursorPosition(handle, pos);
}

void init()
{
    int i, j, a, b;
    HideCursor();
    width = 40, length = 150;
    wall = '#', food = '*', air = ' ', brick = 'O';
    head = 0, tail = 0, max = 60, step = 0, if_miss = 0, food_num = 400, goal = 0, color = 0;
    debug = 0, life = 3;                                                    //debug模式调成1手动开启
    temp_x = 2, temp_y = 2, menu_x = 18, menu_y = 68, left = 4, right = 20; //临时坐标
    gotoxy(0, 0);

    //菜单模式
    if (if_start == 0)
    { //首页
        for (i = 0; i <= width; i++)
        { //生成地图模板
            for (j = 0; j <= length; j++)
            {
                if (i == 0 || i == width || j == 0 || j == length)
                    map[i][j] = wall;
                else if ((i == width / 3 || i == width * 2 / 3) && (j >= length * 2 / 5 && j <= length * 3 / 5))
                    map[i][j] = wall;
                else if ((i >= width / 3 && i <= width * 2 / 3) && (j == length * 2 / 5 || j == length * 3 / 5))
                    map[i][j] = wall;
                else
                    map[i][j] = air;
            }
        }
        while (food_num--)
        { //贪吃蛇生成食物
            int a = rand() % width;
            int b = rand() % length;
            if ((a >= width / 3 && a <= width * 2 / 3) && (b >= length * 2 / 5 && b <= length * 3 / 5) || a == 0 || b == 0)
                continue;
            map[a][b] = food;
        }
        for (i = 0; i <= width; i++)
        { //布置砖块brick
            for (j = 0; j <= length; j++)
            {
                if ((i == 15 || i == 20) && ((j >= 4 && j <= 50) || (j >= 100 && j <= 130)))
                    map[i][j] = brick;
            }
        }
    }
    //游戏模式
    else if (if_start == 1 || if_start == -1)
    {
        if (auto_made_map == 1)
        {
            for (i = 0; i <= width; i++)
            { //生成地图模板
                for (j = 0; j <= length; j++)
                {
                    if (i == 0 || i == width || j == 0 || j == length)
                        map[i][j] = wall;
                    else if ((i == width * 2 / 3) && (j >= length * 2 / 5 && j <= length * 3 / 5))
                        map[i][j] = wall;
                    else if (i == width - 1 && j >= left && j <= right)
                        map[i][j] = wall;
                    else
                        map[i][j] = air;
                }
            }
            if (if_load_snake_mod == 1)
            {
                food_num = 400;
                while (food_num--)
                { //贪吃蛇生成食物
                    a = rand() % width;
                    b = rand() % length;
                    if ((a >= width / 3 && a <= width * 2 / 3) && (b >= length * 2 / 5 && b <= length * 3 / 5) || a == 0 || b == 0)
                        continue;
                    map[a][b] = food;
                }
            }
            for (i = 0; i <= width; i++)
            { //布置砖块brick
                for (j = 0; j <= length; j++)
                {
                    if (((i >= 14 && i <= 15) && (j >= 1 && j <= 20)) || ((i >= 14 && i <= 15) && (j >= 130 && j <= 149)))
                        map[i][j] = brick;
                    if (((i >= 20 && i <= 22) && (j >= 10 && j <= 50)) || ((i >= 20 && i <= 22) && (j >= 100 && j <= 140)))
                        map[i][j] = brick;
                    if ((i == 10 || i == 11) && ((j >= 10 && j <= 50) || (j >= 100 && j <= 140)))
                        map[i][j] = brick;
                }
            }
        }
        else
        {
            for (i = 0; i <= width; i++)
            {
                strcpy(map[i], man_made_map[i]);
            }
            auto_made_map = 1;
        }
        gotoxy(2, width + 3);
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);
        printf("life:");
        for (i = 0; i < life; i++)
            printf("■");
    }
    gotoxy(0, 0);
    for (i = 0; i <= width; i++)
    { //打印地图
        for (j = 0; j <= length; j++)
        {
            if (if_start == 0 && i >= 14 && i <= 25 && j >= 61 && j <= 89)
                map[i][j] = menu[i - 14][j - 61];
            if (map[i][j] == wall && if_start != -1)
                SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 60);
            else if (map[i][j] == brick && if_start != -1)
                SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 80);
            else
                SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);
            if (i == width)
                printf("!");
            else
                printf("%c", map[i][j]);
        }
        printf("\n");
    }
    //构建初始位置以及速度和方向角度
    X = width - 5;
    Y = 4;
    old_x = (int)X;
    old_y = (int)Y;
    s[step].x = old_x;
    s[step].y = old_y;
    V = 26;
    Vx = -V * sin(C[3] * pi / 180.0); //速度向右向下为正方向
    Vy = V * cos(C[3] * pi / 180.0);
}

void gameover()
{
    int i, j;
    gotoxy(0, 0);
    for (i = 0; i <= width + 6; i++)
    {
        for (j = 0; j <= length; j++)
        {
            printf(" ");
        }
        Sleep(20);
    }
    gotoxy(0, 0);
    printf("即将退出游戏");
    Sleep(2000);
    exit(1);
}

void move(int *x, int *y, int limit_x1, int limit_x2, int limit_y1, int limit_y2, int xx, int yy, char ch)
{
    //主要函数 ：灵活的实现选择指针；
    //参数：开始坐标x y  限制活动空间 x上下  y左右 移动距离 xx yy
    char ch1, turn, temp;
    int tx = *x, ty = *y, i;
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 52);
    while (ch != 'b')
    {
        tx = *x, ty = *y, i;
        if (if_start == -1)
        {
            gotoxy(2, width + 4);
            printf("直接按下相应数字改变状态：|1墙体|2.砖块|3空气|4退出编译|");
        }
        gotoxy(*y, *x);
        temp = map[*x][*y];
        printf("$"); //可自定义1个字节的指针图标
        if (ch == -32)
        {
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
        case 'a':
            *y = *y - yy;
            break;
        case 'd':
            *y = *y + yy;
            break;
        case 'w':
            *x = *x - xx;
            break;
        case 's':
            *x = *x + xx;

            break;
        case ' ':
            break;
        }
        if (*x < limit_x1 || *x > limit_x2 || *y < limit_y1 || *y > limit_y2)
        {
            *x = tx;
            *y = ty;
        }
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 60);
        gotoxy(*y, *x);
        printf("$");
        gotoxy(12, width + 1);
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);
        printf("X:%3d Y:%3d", *x, *y);
        if (map[tx][ty] == wall && if_start != -1)
            SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 60);
        else
            SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);
        gotoxy(ty, tx);
        printf("%c", temp);
        if (ch == ' ' && if_start != -1) //进行功能处理
        {
            int flag = map[*x][*y] - '0';
            if (flag == 1)
            {
                if_start = 1;
                init();
                return;
            }
            else if (flag == 2)
            {
                if (if_load_snake_mod == 0)
                    if_load_snake_mod = 1;
                else if (if_load_snake_mod == 1)
                    if_load_snake_mod = 0;
                return;
            }
            else if (flag == 3)
            {
                if_start = -1;
                init();
                return;
            }
            else if (flag == 4)
            {
                gameover();
                return;
            }
        }
        if (ch >= '1' && ch <= '4' && if_start == -1)
        {
            turn = '?';
            switch (ch)
            {
            case '1':
                turn = wall;
                break;
            case '2':
                turn = brick;
                break;
            case '3':
                turn = air;
                break;
            case '4':
                ch = 'b';
                break;
            }
            if ((turn == wall || turn == brick || turn == air) && *x != width)
            {
                map[*x][*y] = turn;
                gotoxy(*y, *x);
                printf("%c", turn);
            }
            else
            {
                gotoxy(2, width + 4);
                printf("不规范的输入                                                      ");
            }
        }
        if (ch == 'b' && if_start == -1)
        {
            for (i = 0; i <= width; i++)
                strcpy(man_made_map[i], map[i]);
            gotoxy(2, width + 4);
            printf("                                                                        ");
            return;
        }
        if (if_start != -1)
            break;
        ch = getch();
    }
    if (ch == 'b' && if_start == -1)
    {
        for (i = 0; i <= width; i++)
            strcpy(man_made_map[i], map[i]);
        gotoxy(2, width + 4);
        printf("                                                                        ");
        return;
    }
    return;
}

void end()
{
    int i, j;
    int flag = max;
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);

    while (flag != 0)
    {
        if (step < 0)
            step += max;
        gotoxy(s[step].y, s[step].x);
        map[s[step].x][s[step].y]--;
        if (map[s[step].x][s[step].y] == air && !(s[step].x == 0 && s[step].y == 0)) //防止自己吃自己
            printf("%c", air);
        s[step].x = 0;
        s[step].y = 0;
        step--;
        flag--;
        Sleep(20);
        gotoxy(2, width + 1);
        printf("len:%5d", flag);
    }
    for (i = 0; i <= 30; i++)
    {
        gotoxy(60, 03 + i);
        printf("%s\n", End[i]);
        Sleep(100);
    }
    getchar();
    getchar();
    if_start = 0;
    init();
}

void manchange() //人为输入更新
{
    char ch, ch1, ch2;
    if (kbhit())
    {
        ch = getch(), ch1;
        if (ch != ' ' && ch != 'w' && ch != 's' && ch != 'a' && ch != 'd' && ch != -32 && ch != 'p' && ch != 'b')
            return;
        if (ch == -32)
        { //同时启用wasd  和上下左右键
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
        if (ch == 'a' || ch == 's' || ch == 'd' || ch == 'w' || ch == ' ' || ch == 'p' || ch == 'b')
        {
            if (if_start == 0)
                move(&menu_x, &menu_y, 18, 24, 68, 68, 2, 0, ch);
            else if (if_start == 1)
            {
                if (ch == 'a' && left > 1)
                {
                    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 60);
                    left--;
                    gotoxy(left, width - 1);
                    map[width - 1][left] = wall;
                    printf("%c", wall);
                    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);
                    gotoxy(right, width - 1);
                    map[width - 1][right] = air;
                    printf(" ");
                    right--;
                }
                else if (ch == 'd' && right < length - 1)
                {
                    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 60);
                    right++;
                    gotoxy(right, width - 1);
                    map[width - 1][right] = wall;
                    printf("%c", wall);
                    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);
                    gotoxy(left, width - 1);
                    map[width - 1][left] = air;
                    printf(" ");
                    left++;
                }
                else if (ch == 'p')
                {
                    gotoxy(2, width + 5);
                    printf("游戏暂停，按'p'继续游戏");
                    ch2 = getch();
                    while (ch2 != 'p')
                    {
                        ch2 = getch();
                    }
                    gotoxy(2, width + 5);
                    printf("                        ");
                }
                else if (ch == 'b')
                {

                    if_start = 0;
                    init();
                }
            }
        }
    }

    //function = move(&temp_x,&temp_y,0,width,0,length,1,1,ch);
    //function = move(&menu_x,&menu_y,18,24,68,68,2,0,ch);
}
void autochange() //自动更新
{
    int flag = 1, i;
    double t1, t2;
    double s1, s2;
    double temp;
    double x1_t1;
    double x2_t1;
    double x3_t1;
    double x4_t1;
    if (if_start == -1)
    {
        auto_made_map = 0;
        move(&temp_x, &temp_y, 0, width, 0, length, 1, 1, 'd');
        if_start = 0;
        init();
    }

    /*-------------------------------------------------------
    核心公式：   X = X0 + Vx*t + 1/2*VX*t*t;        
    		    Y = Y0 + Vy*t;
    核心思想：  如果选择时间作为移动参考，则每秒会出现点相差太远
                这里反过来，以连续为前提，尝试实现：

                分别算出 X 增加一个单位长度 应该增加的 Y 的距离 s1
                        Y 增加一个单位长度 应该增加的 X 的距离 s2
                        优先选择更短的作为下一次移动的基准。
                
                X Y 的增加都是1

                因为实体抛物线是连续的，每一段细微的位移理论上是连续的

                因此s1 和 s2 理论上只会是0和1以及少数出现2的跳节

                加入人为修正

                经测试小范围的数据能完美打印出物理抛物线
 ------------------------------------------------------------*/
    //X Y是double变量增加精准度，但坐标就需要强制转换

    //当X增加一个单位方向时
    //5*t*t + Vx t - 1= 0;解一元二次方程（这里判断  增加后减少仍然是1    可能会有4种情况）

    x1_t1 = (-Vx + sqrt(Vx * Vx + 20)) / 10;
    x2_t1 = (-Vx - sqrt(Vx * Vx + 20)) / 10;
    x3_t1 = (-Vx + sqrt(Vx * Vx - 20)) / 10;
    x4_t1 = (-Vx - sqrt(Vx * Vx - 20)) / 10;
    if (x1_t1 > 0 && x2_t1 > 0)
        t1 = x1_t1 < x2_t1 ? x1_t1 : x2_t1;
    else
        t1 = x1_t1 >= 0 ? x1_t1 : x2_t1;
    if (x3_t1 > 0 && x4_t1 > 0)
        temp = x3_t1 < x4_t1 ? x3_t1 : x4_t1;
    else if (x3_t1 * x4_t1 < 0)
        temp = x3_t1 >= 0 ? x3_t1 : x4_t1;
    else
        temp = 10;
    t1 = t1 < temp ? t1 : temp;
    s1 = t1 * Vy;
    //当Y增加一个单位方向时
    t2 = 1.0 / fabs(Vy);
    s2 = Vx * t2 + 0.5 * g * t2 * t2;
    if ((int)s1 == 0)
        flag = 1;
    else if ((int)s2 == 0)
        flag = 2;
    else
        flag = s1 < s2 ? 1 : 2;

    //选择最优进行处理
    if (flag == 1)
    {
        X = X + Vx * t1 + 5 * t1 * t1;
        Y = Y + s1;
        Vx = Vx + g * t1;
    }
    else if (flag == 2)
    {
        Y = Y + Vy * t2;
        X = X + s2;
        Vx = Vx + g * t2;
    }
    /*else{
			for(  i = 0; i < 4; i++)	
				放弃判断对角了选择其他方式解决（详细见开头注释） 
			} 
		} */
    //---------------------------------
    old_x = (int)X;
    old_y = (int)Y;

    //常规的判断碰撞
    if (map[old_x + 1][old_y] == wall && Vx >= 0)
    {
        color = (color + 1) % 5;
        Vx = -Vx;
    }
    else if (map[old_x - 1][old_y] == wall && Vx <= 0)
    {
        color = (color + 1) % 5;
        Vx = -Vx;
    }
    else if (map[old_x][old_y - 1] == wall && Vy <= 0)
    {
        color = (color + 1) % 5;
        Vy = -Vy;
    }
    else if (map[old_x][old_y + 1] == wall && Vy >= 0)
    {
        color = (color + 1) % 5;
        Vy = -Vy;
    }

    if (map[old_x + 1][old_y] == brick && Vx >= 0)
    {
        //color = (color + 1) % 5;
        Vx = -Vx;
        map[old_x + 1][old_y] = air;
        gotoxy(old_y, old_x + 1);
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);
        printf(" ");
        goal++;
        gotoxy(2, width + 2);
        printf("goal:%5d", goal);
    }
    else if (map[old_x - 1][old_y] == brick && Vx <= 0)
    {
        //color = (color + 1) % 5;
        Vx = -Vx;
        map[old_x - 1][old_y] = air;
        gotoxy(old_y, old_x - 1);
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);
        printf(" ");
        goal++;
        gotoxy(2, width + 2);
        printf("goal:%5d", goal);
    }
    else if (map[old_x][old_y + 1] == brick && Vy >= 0)
    {
        //color = (color + 1) % 5;
        Vy = -Vy;
        map[old_x][old_y + 1] = air;
        gotoxy(old_y + 1, old_x);
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);
        printf(" ");
        goal++;
        gotoxy(2, width + 2);
        printf("goal:%5d", goal);
    }
    else if (map[old_x][old_y - 1] == brick && Vy <= 0)
    {
        //color = (color + 1) % 5;
        Vy = -Vy;
        map[old_x][old_y - 1] = air;
        gotoxy(old_y - 1, old_x);
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);
        printf(" ");
        goal++;
        gotoxy(2, width + 2);
        printf("goal:%5d", goal);
    }
    if (if_miss == 1)
    {
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);
        gotoxy(s[step].y, s[step].x);
        map[s[step].x][s[step].y]--;
        if (map[s[step].x][s[step].y] == air && !(s[step].x == 0 && s[step].y == 0)) //防止自己吃自己
            printf("%c", air);
    }
    s[step].x = old_x;
    s[step].y = old_y;
    if (map[s[step].x][s[step].y] == food)
    {
        map[s[step].x][s[step].y] = air;
        max++;
        gotoxy(2, width + 1);
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);
        printf("len:%5d", max);
    }
    switch (color)
    {
    case 0:
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 60);
        break; //蓝色
    case 1:
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 70);
        break; //红色
    case 2:
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 40);
        break; //绿色
    case 3:
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 30);
        break; //深蓝色
    case 4:
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 128);
        break; //紫色
    }
    gotoxy(s[step].y, s[step].x);
    if (map[s[step].x][s[step].y] == brick)
    {
        map[s[step].x][s[step].y] = air;
        goal++;
        gotoxy(2, width + 2);
        printf("goal:%5d", goal);
    }
    map[s[step].x][s[step].y]++;
    if (debug == 0 && !(s[step].x == 0 && s[step].y == 0))
        printf("%c", air);
    else
        printf("%d", step % 10); //debug模式
    step++;
    if (step >= max)
    {
        if_miss = 1;
    }
    step = step % max;
    if (if_start == 0)
        Sleep(25);
    else
        Sleep(100 - 2 * old_x); //模拟下坠的时候速度加快--对应画面更新更快
    if (old_x == width - 1 && if_start != 0)
    {
        gotoxy(5 + 2 * life, width + 3);
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 07);
        printf("  ");
        life--;
        if (life == 0)
            end();
    }
}

int main()
{
    system("mode con cols=180 lines=60");
    if_start = 0, if_load_snake_mod = 0;
    system("color 07");
    printf("/*-----------------------------------------------------------------\n");
    printf("                                                                   \n");
    printf("                  ！！请先全屏防止乱码！！                          \n");
    printf("             如果乱码请右键窗口-属性-调小文字大小                   \n");
    printf("                        测试字号是18                               \n");
    printf("/*-----------------------------------------------------------------\n");
    printf("/*-----------------------------------------------------------------\n");
    printf("                    打砖块 -- 硬核物理版                           \n");
    printf("                                                                   \n");
    printf("                 内置软件在线地图编辑器（滑稽）                    \n");
    printf("                                                                   \n");
    printf("物理量：  g = 10| 水平分速Vy | 垂直分速Vx  | 水平坐标 Y| 垂直坐标 X\n");
    printf("                                                                   \n");
    printf("物理公式：X = X0 + Vx * t + 1/2 * g * t *t;                        \n");
    printf("		  Y = Y0 + Vy * t;                     					   \n");
    printf("/*-----------------------------------------------------------------\n");
    printf("基础操作:上下左右 + 空格     b~返回键    p~暂停键                  \n");
    printf("作者    ：404name                                                  \n");
    printf("/*-----------------------------------------------------------------\n");
    printf("                                                                   \n");
    printf("进入游戏：按两次回车进入菜单（！！请先全屏防止乱码！！）           \n");
    printf("                                                                   \n");
    printf("/*-----------------------------------------------------------------\n");
    getchar();
    getchar();
    init();
    while (1)
    {
        autochange();
        manchange();
    }
}
