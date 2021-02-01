dim m,g,q,s'母鸡,公鸡,钱数,买法数
s=0
q=inputbox("q:","钱数","0")'钱数输入
for g=0 to (q/5)'循环公鸡
for m=0 to int((q-g*5)/3)'循环母鸡(嵌套)
s=s+1
next
next
msgbox s'输出