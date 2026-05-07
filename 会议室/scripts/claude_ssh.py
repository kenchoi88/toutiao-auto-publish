#!/usr/bin/env python3
"""claude_ssh - 从台机 ssh 到 4 mac 调用 Claude CLI

设计要点:
- 密码通过 stdin (here-string <<<) 喂入 expect, 不在任何进程 argv
- ps aux 看不到 mac 登录密码
- 复用 macOS Keychain 中的 Claude Code-credentials (subscription token)

用法:
  CLAUDE_SSH_PWD=xxx python claude_ssh.py neo "你好"
  python claude_ssh.py neo "你好"  # 不带 env 时交互输入

机器代号(memory `reference_角色代号.md`):
  air  = 阿良 (kenair@100.126.82.58)
  mini = 东山 (kenchoimini@100.70.22.7)
  neo  = 小齐 (kenchoios@100.68.57.96)
  neo2 = 左右 (kenchoineo2@100.96.153.17)

memory 关联:
  reference_Tailscale网络.md     - 5 机 IP
  reference_SSH用户名规律.md      - 4 mac SSH user
  reference_统一密码.md           - 5 机统一登录密码 geng7997
  reference_4mac真版位置.md       - 4 mac 同款 ~/Desktop/<件>/
  feedback_跨机协同作战分工.md    - 绣虎指挥+现场实操
"""
import sys
import os
import subprocess
import getpass
import shlex

MACHINES = {
    'air':  ('kenair@100.126.82.58',      '阿良'),
    'mini': ('kenchoimini@100.70.22.7',   '东山'),
    'neo':  ('kenchoios@100.68.57.96',    '小齐'),
    'neo2': ('kenchoineo2@100.96.153.17', '左右'),
}
CLAUDE_BIN = '/opt/homebrew/bin/claude'
KEYCHAIN = '$HOME/Library/Keychains/login.keychain-db'
PROXY = 'http://127.0.0.1:1082'
SSH_TIMEOUT = 20


def call_claude(machine: str, prompt: str, pwd: str, stream: bool = False):
    """ssh 到指定 mac, unlock keychain, 调用 claude --print

    返回: (stdout, stderr, returncode)
    """
    if machine not in MACHINES:
        raise ValueError(f'未知机器: {machine}, 可选 {list(MACHINES)}')
    user_ip, alias = MACHINES[machine]

    # remote bash 命令(走 ssh argv,**不含密码**)
    # 密码通过 ssh 的 stdin 第一行喂入,bash read 拿到 → expect heredoc 引用 $pwd
    # expect 进程的 stdin 是 heredoc 内容(已替换 pwd),pwd 不出现在任何进程的 argv
    prompt_q = shlex.quote(prompt)
    remote = f"""\
read pwd
expect <<EOF_EXPECT >/dev/null 2>&1
spawn security unlock-keychain {KEYCHAIN}
expect "password to unlock"
send "$pwd\\r"
expect eof
EOF_EXPECT
unset pwd
export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH
export HTTPS_PROXY={PROXY} HTTP_PROXY={PROXY}
{CLAUDE_BIN} --print {prompt_q}
"""

    ssh_argv = [
        'ssh', '-o', f'ConnectTimeout={SSH_TIMEOUT}',
        '-o', 'BatchMode=yes',
        user_ip, 'bash', '-lc', remote,
    ]

    proc = subprocess.run(
        ssh_argv,
        input=pwd + '\n',
        capture_output=True,
        text=True,
        encoding='utf-8',
    )
    return proc.stdout, proc.stderr, proc.returncode


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    machine, prompt = sys.argv[1], sys.argv[2]

    pwd = os.environ.get('CLAUDE_SSH_PWD')
    if not pwd:
        pwd = getpass.getpass(f'mac 登录密码 ({machine}): ').strip()

    out, err, rc = call_claude(machine, prompt, pwd)
    sys.stdout.write(out)
    if err.strip():
        # 过滤 tailscale ssh banner 噪音
        clean_err = '\n'.join(
            l for l in err.splitlines()
            if 'Tailscale' not in l and 'Authentication' not in l and 'Time since' not in l
        )
        if clean_err.strip():
            sys.stderr.write('\n[STDERR]\n' + clean_err + '\n')
    sys.exit(rc)


if __name__ == '__main__':
    main()
