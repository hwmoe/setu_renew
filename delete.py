import os
import time
import hoshino

sv = hoshino.Service(
    name='色图清理',  # 功能名
    visible=False,  # False隐藏
    enable_on_default=True,  # 是否默认启用
)

path = os.path.join(hoshino.config.RES_DIR , 'img', 'setu_mix')
t = 24*3600*7 #过期时间容忍度

def delDir(dir,t=120):
    global n
    #获取文件夹下所有文件和文件夹
    files = os.listdir(dir)
    for file in files:
        filePath = os.path.join(dir, file)
        #判断是否是文件
        if os.path.isfile(filePath):
            #最后一次修改的时间
            last = int(os.stat(filePath).st_mtime)
            #上一次访问的时间
            #last = int(os.stat(filePath).st_atime)
            #当前时间
            now = int(time.time())
            #删除过期文件
            if (now - last >= t):
                os.remove(filePath)
                n += 1 
                #print(filePath + " was removed!")
        elif os.path.isdir(filePath):
            #如果是文件夹，继续遍历删除
            delDir(filePath,t)
            #如果是空文件夹，删除空文件夹
            if not os.listdir(filePath):
                os.rmdir(filePath)
                #print(filePath + " was removed!")

@sv.scheduled_job('cron', hour='5', minute='10', jitter=50)
async def auto_clean():
    delDir(path,t)

@sv.on_fullmatch('清理色图')
async def clean_setu(bot,ev):
    global n
    n = 0 #初始化
    delDir(path,t)
    await bot.send(ev, f'已经清理{n}张色图')