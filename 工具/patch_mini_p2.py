#!/usr/bin/env python3
"""
mini v1101.2 P2 兜底补丁 — 给 mini 三大件补上 find_or_reopen_webview L2 兜底

背景:
  v1101.2 仓库/neo/air mac 版本只移植了 P1 (scroll_find_account 内 CDP 注入),
  没移植 P2 (find_or_reopen_webview 关 tab 重建 partition L2 兜底)。
  mini 文章定时 04-29 时光浅巷 9 个小轮 X 找不到 webview 退出 → 缺哥手工救场。

修复:
  在 find_account_webview 函数体之后注入 _search_box_set / _locate_filtered_account /
  find_or_reopen_webview 三函数,并把业务调用 find_account_webview(main_ws, name)
  替换成 find_or_reopen_webview(main_ws, name)。

落地源: Win 台机桌面 gtg_batch.py:972-1071 (实战印证)
"""
import os, re, shutil, sys, time, ast

P2_BLOCK = '''

def _search_box_set(main_ws, value):
    """侧边栏搜索框设置值(空字符串=清空)。React-friendly: 用原型 setter 触发 input/change 事件。"""
    val_json = json.dumps(value)
    return js(main_ws, f"""
    (function(){{
        var inputs = document.querySelectorAll('input');
        for(var i=0;i<inputs.length;i++){{
            var ph = inputs[i].getAttribute('placeholder') || '';
            if(ph.indexOf('账号') !== -1 || ph.indexOf('手机号') !== -1){{
                var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                setter.call(inputs[i], '');
                inputs[i].dispatchEvent(new Event('input', {{bubbles:true}}));
                if({val_json}.length > 0){{
                    setter.call(inputs[i], {val_json});
                    inputs[i].dispatchEvent(new Event('input', {{bubbles:true}}));
                    inputs[i].dispatchEvent(new Event('change', {{bubbles:true}}));
                }}
                return 'ok';
            }}
        }}
        return 'no_input';
    }})()
    """, 50)


def _locate_filtered_account(main_ws, name):
    """搜索框过滤后,直接抓第一个匹配账号的中心坐标(viewport 相对)。"""
    name_json = json.dumps(name)
    pos = js(main_ws, f"""
    (function(){{
        var items = document.querySelectorAll('.{ACCOUNT_CLASS}');
        for(var i=0;i<items.length;i++){{
            var t = items[i].textContent.trim();
            if(t === {name_json} || t.startsWith({name_json})){{
                items[i].scrollIntoView({{block:'center', behavior:'instant'}});
                var r = items[i].getBoundingClientRect();
                if(r.width > 0)
                    return JSON.stringify({{x:Math.round(r.left+r.width/2), y:Math.round(r.top+r.height/2)}});
            }}
        }}
        return null;
    }})()
    """, 51)
    if not pos:
        return None
    return json.loads(pos)


def find_or_reopen_webview(main_ws, name, reopen_attempts=2):
    """虚拟滚动底部账号 webview partition 不渲染时,通过侧边栏搜索框定位账号让 webview 重建。

    流程:正常 find_account_webview 失败 → 关 tab → 搜索框输入账号名 → 等过滤 →
    抓过滤后的账号坐标 → click → 等更长时间 → 再尝试 find_account_webview。
    搜索框过滤后只剩匹配项渲染在 DOM 顶部,不再受虚拟滚动影响。
    """
    ws_url = find_account_webview(main_ws, name)
    if ws_url:
        return ws_url

    for attempt in range(reopen_attempts):
        log(f"  webview partition 失败,搜索框重建 {attempt+1}/{reopen_attempts}: 输入 \\"{name}\\"")
        try:
            close_current_tab(main_ws)
        except Exception as e:
            log(f"  关 tab 异常(忽略): {e}")
        time.sleep(1.0)

        # 用搜索框过滤
        rs = _search_box_set(main_ws, name)
        if rs != 'ok':
            log("  搜索框定位失败,降级用 scroll_find_account")
            pos = scroll_find_account(main_ws, name)
        else:
            time.sleep(1.5)  # 等过滤结果 React 渲染完
            pos = _locate_filtered_account(main_ws, name)
            if not pos:
                log("  搜索过滤后仍找不到,降级用 scroll_find_account")
                _search_box_set(main_ws, "")  # 清空恢复列表
                time.sleep(0.5)
                pos = scroll_find_account(main_ws, name)

        if not pos:
            log(f"  搜索/滚动都找不到 {name},重建中止")
            _search_box_set(main_ws, "")
            return None

        click(main_ws, pos["x"], pos["y"], 20)
        time.sleep(WAIT_LOAD + 2)  # 比首次多等 2 秒,给虚拟滚动 lazy render 留余地

        ws_url = find_account_webview(main_ws, name)

        # 不论成败,清空搜索框还原列表(避免影响后续账号)
        _search_box_set(main_ws, "")
        time.sleep(0.3)

        if ws_url:
            log(f"  webview 重建成功(尝试 {attempt+1})")
            return ws_url

    return None
'''


def patch_one(path):
    print(f"\n=== {path} ===")
    if not os.path.exists(path):
        print("  SKIP: file not found")
        return False

    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()

    if 'def find_or_reopen_webview' in src:
        print("  SKIP: already has find_or_reopen_webview")
        return False

    # 1. 备份
    ts = time.strftime('%Y%m%d_%H%M%S')
    bak = f"{path}.bak_pre_p2_{ts}"
    shutil.copy2(path, bak)
    print(f"  bak: {bak}")

    # 2. 先替换业务调用 (在原始 src 里改,这样不会误伤 P2 块本身的内部调用)
    pat = r'\bws_url\s*=\s*find_account_webview\(main_ws,\s*name\)'
    n_replaced = len(re.findall(pat, src))
    src2 = re.sub(pat, 'ws_url = find_or_reopen_webview(main_ws, name)', src)
    print(f"  replaced ws_url=find_account_webview → find_or_reopen_webview: {n_replaced} 处")

    # 3. 在 find_account_webview 函数体之后注入 P2 块
    #    定位:从 'def find_account_webview' 开始,找到下一个顶层 def 的开头,插在前面
    m = re.search(r'^def find_account_webview\(', src2, re.MULTILINE)
    if not m:
        print("  ERROR: find_account_webview not found")
        return False
    nxt = re.search(r'^def [A-Za-z_]', src2[m.end():], re.MULTILINE)
    if not nxt:
        print("  ERROR: cannot locate next top-level def after find_account_webview")
        return False
    insert_pos = m.end() + nxt.start()
    new_src = src2[:insert_pos] + P2_BLOCK.lstrip('\n') + '\n\n' + src2[insert_pos:]

    # 4. 语法校验
    try:
        ast.parse(new_src)
    except SyntaxError as e:
        print(f"  ERROR: syntax error after patch: {e}")
        # 不写回,留 bak
        return False

    # 5. 写回
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_src)

    # 6. 验证
    with open(path, 'r', encoding='utf-8') as f:
        chk = f.read()
    assert 'def find_or_reopen_webview' in chk
    assert 'def _search_box_set' in chk
    assert 'def _locate_filtered_account' in chk
    print(f"  OK lines={chk.count(chr(10))+1}")
    return True


if __name__ == '__main__':
    targets = [
        '/Users/kenchoimini/Desktop/微头条自动发布/gtg_batch.py',
        '/Users/kenchoimini/Desktop/文章自动发布/gtg_batch.py',
        '/Users/kenchoimini/Desktop/文章定时自动发布/gtg_timer.py',
    ]
    ok = sum(1 for t in targets if patch_one(t))
    print(f"\n=== 落地 {ok}/{len(targets)} ===")
