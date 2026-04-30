import json, websocket, requests, os

port_file = os.path.expanduser("~/Library/Application Support/创作罐头/DevToolsActivePort")
PORT = int(open(port_file).readline().strip())

ts = requests.get(f"http://127.0.0.1:{PORT}/json", proxies={"http":"","https":""}).json()
# 文章 publish 页 url 通常是 graphic/publish 或 publish/...
candidates = [t for t in ts if "mp.toutiao.com" in t.get("url","") and "publish" in t.get("url","")]
print("=== publish targets ===")
for t in candidates:
    print("  ", t.get("url",""))
print()

if not candidates:
    print("no publish target")
    exit()

target = candidates[0]
print("PROBE:", target["url"])

def js(u, e):
    w = websocket.create_connection(u, suppress_origin=True)
    w.send(json.dumps({"id":1,"method":"Runtime.evaluate",
                       "params":{"expression":e,"returnByValue":True}}))
    r = json.loads(w.recv())
    w.close()
    return r["result"]["result"].get("value")

PROBE = """
(function(){
  var els = document.querySelectorAll('.ProseMirror');
  var arr = [];
  for(var i=0;i<els.length;i++){
    var t = els[i].textContent || "";
    var p = els[i].getAttribute('placeholder') || "";
    var aria = els[i].getAttribute('aria-label') || "";
    var cls = String(els[i].className||"");
    var r = els[i].getBoundingClientRect();
    arr.push({i:i, len:t.length, head:t.slice(0,40), placeholder:p, aria:aria, cls:cls.slice(0,80), w:Math.round(r.width), h:Math.round(r.height)});
  }
  // 全局也找 textarea / contenteditable
  var ces = document.querySelectorAll('[contenteditable=true]');
  var cearr = [];
  for(var i=0;i<ces.length;i++){
    var t = ces[i].textContent || "";
    cearr.push({i:i, tag:ces[i].tagName, len:t.length, head:t.slice(0,40), cls:String(ces[i].className||"").slice(0,60)});
  }
  return JSON.stringify({pms:arr, contentEditables:cearr, url:location.href});
})()
"""

print(json.dumps(json.loads(js(target["webSocketDebuggerUrl"], PROBE)), indent=2, ensure_ascii=False))
