import os
import sys
import time
import argparse
#*******************************配置部分***************************************#
parser = argparse.ArgumentParser()
parser.add_argument('--gpu_num', default=1, type=int,help='the number of your gpus GPU数量')
parser.add_argument('--cmd', default='python main.py', type=str,help='running command 运行命令')
parser.add_argument('--interval', default=0, type=float, help='interval seconds for every gpu memory search period 查询间隔(秒)')
parser.add_argument('--using_sc', default=False, type=bool, help='using serverchan?')
parser.add_argument('--SendKey', default='',type=str, help='ServerChan sendkey')
parser.add_argument('--less_than_memory', default=100,type=int, help='less than this number will execute the command 当GPU使用内存低于该数值时执行命令')
#*****************************************************************************#
args=parser.parse_args()


cmd1 = 'CUDA_VISIBLE_DEVICES='
cmd = args.cmd
gpu_num = args.gpu_num
interval = args.interval
SendKey = args.SendKey
using_sc = args.using_sc
less_than_memory = args.less_than_memory
def get_info():
    gpu_memory_list = []
    gpu_status = os.popen('nvidia-smi | grep %').readlines()
    for list_ in gpu_status:
        list_ = list_.split('|')
        gpu_memory = int(list_[2].split('/')[0].split('M')[0].strip())
        gpu_memory_list.append(gpu_memory)
    return gpu_memory_list


def server_jiang_push(SendKey):
    if SendKey == '':
        print("please set your sc-sendkey")
        return
    import requests
    requests.post('https://sctapi.ftqq.com/'+SendKey+'.send?title=%E5%BC%80%E5%A7%8B%E8%AE%AD%E7%BB%83%E5%95%A6%EF%BC%81')


def setup_python(interval=0):
    gpu_memory_list = get_info()
    i = 0
    gpu_memory_str = ""
    while (i != gpu_num):
        if gpu_memory_list[i] <= less_than_memory:  # 设置条件，满足则运行python程序
            break
        else:
            gpu_memory_str = gpu_memory_str + ' ' + str(i) + ' ' + 'gpu memory:%d MiB' % gpu_memory_list[i] + '||'
            i += 1
            if i % gpu_num == 0 and i != 0:  # 遍历一次GPU资源后重新查询
                i = 0
                gpu_memory_list = get_info()
                sys.stdout.write('\r' + gpu_memory_str)
                sys.stdout.flush()  # 输出并清空缓冲
                gpu_memory_str = ""
                if interval>0:
                    time.sleep(interval)
    if using_sc:
        server_jiang_push(SendKey)
    print('Executing command:\n')
    print(cmd1 + str(i) + cmd)
    os.system(cmd1 + str(i) + cmd)  # 运行python脚本


if __name__ == '__main__':
    try:
        setup_python(interval)
    except KeyboardInterrupt:
        print("\n See you ^_^ ")
        exit()
