import sys
from PTTLibrary import PTT
import json
import numpy as np
import pandas as pd


print('import end')


#Initial Global Param
PTTBot=PTT.Library(kickOtherLogin=False)
pushBoundary=0
Board='Testtttt'
StartIndex=0
EndIndex=0
showPushTime=False
GapPrint=0
GapBoundary=0

Month={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}

#Read Setting
def readSettings():

    setting=[]
    st=pd.read_json('./settings.json')
    setting.append(st["ID"].values[0])
    setting.append(st["Password"].values[0])

    global pushBoundary,Board,StartIndex,EndIndex,showPushTime,GapPrint,GapBoundary
    pushBoundary=st["pushBoundary"].values[0]
    Board=st["Board"].values[0]
    StartIndex=st["StartIndex"].values[0]
    EndIndex=st["EndIndex"].values[0]
    showPushTime=st["showPushTime"].values[0]
    GapPrint=st["GapPrint"].values[0]
    GapBoundary=st["GapBoundary"].values[0]

    return setting    

#Calculate the time gap between post time and push time 
def TimeGap(postTime,pushTime):
    if pushTime==0:
        return 999999
    if showPushTime==True:
        print(pushTime,'push')

    try:
        HourGap=(int(pushTime.split(' ')[-1].split(':')[0])-int(postTime.split(' ')[-2].split(':')[0]))%24
        MinuteGap=(int(pushTime.split(' ')[-1].split(':')[1])-int(postTime.split(' ')[-2].split(':')[1]))%60
    except:
        print("Error when split the time/data")
        print(postTime,'post')
        print(pushTime,'push')
        return 999999

    #print(HourGap,MinuteGap,'Hour Min')

    Gap=HourGap*60+MinuteGap
    return Gap

#Analyse Bow Wen
def AnalyseBowWen(PIndex):
    ErrCode,Post=PTTBot.getPost(Board,PostIndex=PIndex)
    if ErrCode==0:
        PushCount=0
        BooCount=0
        ArrowCount=0
        time25=0
        time50=0
        time75=0
        timeTarget=0
        for Push in Post.getPushList():
            if Push.getType() == PTT.PushType.Push:
                PushCount+=1
                if PushCount==GapPrint:
                    timeTarget=Push.getTime()
                if PushCount==25:
                    time25=Push.getTime()
                if PushCount==50:
                    time50=Push.getTime()
                if PushCount==75:
                    time75=Push.getTime()
                    
            elif Push.getType() == PTT.PushType.Boo:
                BooCount+=1
            elif Push.getType() == PTT.PushType.Arrow:
                ArrowCount+=1

        if PushCount>pushBoundary:
            if showPushTime==True:
                print(Post.getDate(),'Post Time')
            gapTarget=TimeGap(Post.getDate(),timeTarget)
            gap1=TimeGap(Post.getDate(),time25)
            gap2=TimeGap(Post.getDate(),time50)
            gap3=TimeGap(Post.getDate(),time75)

            if GapPrint!=0:
                if gapTarget<GapBoundary:
                    print(PIndex,PushCount,BooCount,ArrowCount,'PIndex Push Boo Arrow')
                    print(Post.getTitle())
                    print(Post.getDate(),'post')
                    print('TargetGap:',gapTarget)
                    print('Gap25:',gap1)
                    print('Gap50:',gap2)
                    print('Gap75:',gap3)
            else:
                print(PIndex,PushCount,BooCount,ArrowCount,'PIndex Push Boo Arrow')
                print(Post.getTitle())
                #print(time50,'50 push Time')
                #print(Post.getDate(),'Post date')
                print(Post.getDate(),'post')
                print('Gap25:',gap1)
                print('Gap50:',gap2)
                print('Gap75:',gap3)





def main():
    setting=readSettings()

    #LOGIN
    
    ErrCode=PTTBot.login(str(setting[0]),str(setting[1]))
    if ErrCode != PTT.ErrorCode.Success:
        PTTBot.Log('Login Failed')
        sys.exit()

    #Show Params
    print('Analysis!')
    print('Target Board:',Board)
    print('Push over',pushBoundary,'will be analysis')
    print('Start Index:',StartIndex)
    print('End Index:',EndIndex)
    print('Total operate',EndIndex-StartIndex,'Times')
    print('The:',GapPrint,'-th push time gap lower than',GapBoundary,' will be print.')
    print('Show Push Time=',showPushTime)

    #Analyse
    for i in range(StartIndex,EndIndex):
        AnalyseBowWen(i)
    
    #Logout
    PTTBot.logout()



main()
