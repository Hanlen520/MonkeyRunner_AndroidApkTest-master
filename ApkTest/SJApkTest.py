#!/usr/bin/env monkeyrunner
# -*- coding: utf-8 -*-
"""
功能：执行司机端渠道包测试脚本
创建：张敏
"""
import time
import sys
import os
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
#设置应用包名和入口Activity名
pakageName = 'com.alog.driver'
componentName = 'com.kuaihuoyun.driver.KDLaunch'

#APP启动时等待时间(秒)
startTime = 5

#获取年月日时分秒
now = time.strftime("%Y-%m-%d-%H-%M")

#python中获取当前运行的文件的名字
name=sys.argv[0].split("\\")
filename=name[len(name)-1]

#MonkeyRunner下获取运行的文件所在的路径
rootpath  = os.path.split(os.path.realpath(sys.argv[0]))[0]
print(rootpath)


#指定位置
dir = rootpath + "/apk/sj/"
screenPath = rootpath + "/screenShot/sj/"
duibiPath = rootpath + "/duibiPath/sj/"
logpath = rootpath + "/log/sj/"

#获取待测APK个数
countPak = len(os.listdir(dir))

#新建一个Log文件
if not os.path.isdir(logpath):
    os.mkdir(logpath)
log = open( logpath + filename[0:-3] + "-log" +now + ".txt" , 'w')

#开始连接设备
print("Connecting...")
device = MonkeyRunner.waitForConnection()
log.write("连接设备...\n")

#卸载应用
def uninstall():
    print('Removing...')
    device.removePackage(pakageName)
    print ('Remove Successful!')
    MonkeyRunner.sleep(2)
    log.write("初始化应用环境...\n")
countOK = 0
countNO = 0


#安装目录下的apk
for i in os.listdir(dir):
    print('Installing...<%s>'%i)
    log.write("==========安装应用"+i+"==========\n")
    path = dir + '//' + i
    #安装应用
    device.installPackage(path)
    print('Install Successful!')

    #打开应用
    device.startActivity(component=pakageName+"/"+componentName)
    MonkeyRunner.sleep(startTime)
    log.write("启动App...\n")
    device.wake()
    # 登录页面截图保存
    dljt = device.takeSnapshot()
    print "Take ScreenShot dljt..."
    dljt.writeToFile(duibiPath + i + 'dljt' + '.png', 'png')
    # 用户手机号密码登录
    device.touch(524, 539, "DOWN_AND_UP")  # 手机号码
    MonkeyRunner.sleep(1)
    device.type("15088748900")
    MonkeyRunner.sleep(1)
    device.touch(524, 730, "DOWN_AND_UP")  # 密码
    MonkeyRunner.sleep(1)
    device.type("12345678")
    MonkeyRunner.sleep(1)
    device.touch(998, 1065, "DOWN_AND_UP")  # 收缩键盘弹框
    MonkeyRunner.sleep(1)
    device.touch(524, 1066, "DOWN_AND_UP")  # 开始使用按钮
    MonkeyRunner.sleep(1)
    # 完成登录
    device.touch(952, 1654, "DOWN_AND_UP")  # 点击公告确认按钮
    MonkeyRunner.sleep(2)
    # 装载状态浮窗截图
    # zzjt = device.takeSnapshot()
    # print "Take ScreenShot zzjt..."
    # zzjt.writeToFile(duibiPath + i + 'zzjt' + '.png', 'png')
    device.touch(986, 1468, "DOWN_AND_UP")  # 点击装载状态浮窗关闭按钮
    MonkeyRunner.sleep(1)

    # 个人中心
    device.touch(80, 183, "DOWN_AND_UP")  # 点击个人中心
    MonkeyRunner.sleep(2)
    # 个人中心截图
    grzxjt = device.takeSnapshot()
    print "Take ScreenShot grzxjt..."
    grzxjt.writeToFile(duibiPath + i + 'zzjt' + '.png', 'png')

    # 退出
    device.touch(277, 1048, "DOWN_AND_UP")  # 更多
    MonkeyRunner.sleep(1)
    device.touch(535, 1137,"DOWN_AND_UP")# 退出登录按钮
    MonkeyRunner.sleep(1)
    device.touch(782,1111,"DOWN_AND_UP")#确认退出



    #进行图片比较
    sijidenglujietu=MonkeyRunner.loadImageFromFile(screenPath + r'SJDL.png')
    gerenzhongxinjietu=MonkeyRunner.loadImageFromFile(screenPath + r'SJGRZX.png')

    print "Pic Comparing..."
    log.write("对比图片中...\n")
    if(dljt.sameAs(sijidenglujietu,0.9)):
        print("%s 可以成功启动"%i)
        log.write("启动页比较通过！--%s--包启动成功！\n"%i)
        if (grzxjt.sameAs(gerenzhongxinjietu,0.9)):
            print("%s 可以打开个人中心页面" % i)
            log.write("个人中心页比较通过！--%s--用户登录正常！\n" % i)
            print('Removing...')
            log.write("初始化应用环境，移除中...\n")
            device.removePackage(pakageName)
            print ('Remove Successful!')
            log.write("==========移除完毕==========\n")
            countOK += 1
            MonkeyRunner.sleep(2)
        else:
            print("个人中心页比对失败 %s!" % i)
            log.write("个人中心页比较失败！请检查安装包--%s--是否可用！\n" % i)
            uninstall()
            continue
    else:
        print("False!Please check %s!"%i)
        log.write("启动页比较失败！请检查安装包--%s--是否可用！\n"%i)
        uninstall()
        continue

log.write("共测试 %s 个货主渠道包，%d 个通过。"%(countPak,countOK))
