import subprocess, os, time, socket, sys

# 先关掉已有的罐头（Windows 语法，不能用 /dev/null）
subprocess.run(['taskkill', '/f', '/im', '创作罐头.exe'],
               capture_output=True, text=True)
time.sleep(2)

exe = r'C:\Program Files (x86)\Muse\创作罐头\1.7.11\创作罐头.exe'
if not os.path.exists(exe):
    print(f'X 找不到罐头可执行文件: {exe}')
    input('按回车退出...')
    sys.exit(1)

# DETACHED_PROCESS + CREATE_NEW_PROCESS_GROUP：让罐头脱离本脚本独立运行
DETACHED = 0x00000008
NEW_GROUP = 0x00000200
subprocess.Popen([exe, '--remote-debugging-port=9223'],
                 creationflags=DETACHED | NEW_GROUP,
                 close_fds=True)

print('罐头启动中，等待 CDP 端口 9223 就绪...')
ready = False
for i in range(30):
    time.sleep(1)
    try:
        s = socket.create_connection(('127.0.0.1', 9223), timeout=1)
        s.close()
        print(f'★ CDP 9223 已就绪（耗时 {i+1}s），现在可以点 GO')
        ready = True
        break
    except Exception:
        pass

if not ready:
    print('X CDP 9223 30 秒内未就绪，请检查罐头是否闪退')

input('按回车关闭此窗口（罐头会继续运行）...')
