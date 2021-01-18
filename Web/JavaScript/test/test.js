/*
 * @?: *********************************************************************
 * @Author: Weidows
 * @Date: 2021-01-07 16:58:40
 * @LastEditors: Weidows
 * @LastEditTime: 2021-01-19 02:00:30
 * @FilePath: \Weidows\Web\JavaScript\test\test.js
 * @Description:
 * @!: *********************************************************************
 */
"use strict";

for (var index_1 = 0; index_1 < 10; index_1++) {
  console.log(index_1);
}
for (let index_2 = 0; index_2 < 10; index_2++) {
  console.log(index_2);
}
console.log(index_1); // 10
console.log(index_2); // index_1 is not defined
