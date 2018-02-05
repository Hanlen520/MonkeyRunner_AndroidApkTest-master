#!/usr/bin/env monkeyrunner
# -*- coding: utf-8 -*-
"""
功能：执行货主端渠道包测试脚本
创建：张敏
"""
import time
import sys
import os
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
#设置应用包名和入口Activity名
pakageName = 'com.alog.owner'
componentName = 'com.alog.owner.moudles.guide.StartActivity'
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
dir = rootpath + "/apk/hz/"
screenPath = rootpath + "/screenShot/hz/"
duibiPath = rootpath + "/duibiPath/hz/"
logpath = rootpath + "/log/hz/"

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

    #启动页截图
    qdjt=device.takeSnapshot()
    print("Take ScreenShot qdjt...")

    #保存启动页截图
    qdjt.writeToFile(duibiPath + i + 'qdjt' +'.png','png')

    #滑动启动页
    for y in range(0, 4):
        device.drag((955, 537), (200, 537), 1, 5)
    device.touch(553, 1587, "DOWN_AND_UP")
    MonkeyRunner.sleep(2)
    device.touch(826, 1659, "DOWN_AND_UP")
    MonkeyRunner.sleep(1)
    device.touch(826, 1659, "DOWN_AND_UP")
    MonkeyRunner.sleep(3)

    # 用户登录
    device.touch(59, 161, "DOWN_AND_UP")
    MonkeyRunner.sleep(2)
    device.touch(1036, 156, "DOWN_AND_UP")
    MonkeyRunner.sleep(2)
    #登录页面截图
    dljt = device.takeSnapshot()
    print "Take ScreenShot dljt..."
    MonkeyRunner.sleep(1)
    #保存登录页图片
    dljt.writeToFile(duibiPath + i + 'dljt' +'.png','png')
    MonkeyRunner.sleep(2)
    device.touch(544, 757, "DOWN_AND_UP")
    MonkeyRunner.sleep(2)
    device.type("zm12345678")
    MonkeyRunner.sleep(2)
    device.touch(164, 637, "DOWN_AND_UP")
    MonkeyRunner.sleep(1)
    device.touch(285, 620, "DOWN_AND_UP")
    device.type("15088748900")
    MonkeyRunner.sleep(2)
    device.touch(1007, 1046, "DOWN_AND_UP")
    MonkeyRunner.sleep(2)
    device.touch(544, 1220, "DOWN_AND_UP")
    MonkeyRunner.sleep(2)
    device.touch(59, 161, "DOWN_AND_UP")
    MonkeyRunner.sleep(2)

    #保存登录后个人中心截图
    grzxjt = device.takeSnapshot()
    print "Take ScreenShot grzxjt..."

    grzxjt.writeToFile(duibiPath + i + 'grzxjt' + '.png', 'png')

    #进行图片比较
    qidongjietu=MonkeyRunner.loadImageFromFile(screenPath + r'HZQD.png')
    delujietu=MonkeyRunner.loadImageFromFile(screenPath + r'HZDL.png')
    gerenzhongxinjietu=MonkeyRunner.loadImageFromFile(screenPath + r'HZGRZX.png')

    print "Pic Comparing..."
    log.write("对比图片中...\n")
    if(qdjt.sameAs(qidongjietu,0.9)):
        print("%s 可以成功启动"%i)
        log.write("启动页比较通过！--%s--包启动成功！\n"%i)
        if (dljt.sameAs(delujietu,0.9)):
            print("%s 可以打开登录页面" % i)
            log.write("登录页比较通过！--%s--包登录页面正常！\n" % i)
            if (grzxjt.sameAs(gerenzhongxinjietu,0.9)):
                print("%s 登录成功，个人中心展示正常" % i)
                log.write("个人中心页比较通过！--%s--包个人中心页面正常！\n" % i)
                print('Removing...')
                log.write("初始化应用环境，移除中...\n")
                device.removePackage(pakageName)
                print ('Remove Successful!')
                log.write("==========移除完毕==========\n")
                countOK += 1
                MonkeyRunner.sleep(2)
            else:
                print("个人中心比对失败 %s!" % i)
                log.write("个人中心页比较失败！请检查安装包--%s--是否可用！\n" % i)
                uninstall()
                continue
        else:
            print("登录页比对失败 %s!" % i)
            log.write("登录页比较失败！请检查安装包--%s--是否可用！\n" % i)
            uninstall()
            continue
    else:
        print("False!Please check %s!"%i)
        log.write("启动页比较失败！请检查安装包--%s--是否可用！\n"%i)
        uninstall()
        continue

log.write("共测试 %s 个货主渠道包，%d 个通过。"%(countPak,countOK))
