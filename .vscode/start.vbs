'
' @?: *********************************************************************
' @Author: Weidows
' @Date: 2021-01-29 12:10:11
' @LastEditors: Weidows
' @LastEditTime: 2021-01-29 17:15:39
' @FilePath: \Weidows\.vscode\start.vbs
' @Description:
' @!: *********************************************************************
'

' 开机运行程序
CreateObject("WScript.Shell").Run "aria2c --conf-path=D:\Game\Scoop\persist\aria2\conf",0

CreateObject("WScript.Shell").Run "D:\Game\Scoop\apps\rainmeter\current\Rainmeter.exe",0

CreateObject("WScript.Shell").Run "D:\Software\Useful\PCMaster\MouseInc.exe",0
