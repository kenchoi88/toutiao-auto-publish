import json, websocket, requests, os

port_file = os.path.expanduser("~/Library/Application Support/创作罐头/DevToolsActivePort")
PORT = int(open(port_file).readline().strip())

ts = requests.get(f"http://127.0.0.1:{PORT}/json", proxies={"http":"","https":""}).json()
main = next(t for t in ts if "czgts.cn" in t.get("url",""))
wtt  = next(t for t in ts if "weitoutiao/publish" in t.get("url",""))

print("MAIN:", main["url"])
print("WTT :", wtt["url"])

print("\n=== ALL targets ===")
for t in ts:
    print(f"  type={t.get('type'):10} title={(t.get('title') or '')[:25]:25}  url={t.get('url','')[:80]}")

def js(u, e):
    w = websocket.create_connection(u, suppress_origin=True)
    w.send(json.dumps({"id":1,"method":"Runtime.evaluate",
                       "params":{"expression":e,"returnByValue":True}}))
    r = json.loads(w.recv())
    w.close()
    return r["result"]["result"].get("value")

WV_PROBE = """
(function(){
  var wvs=document.querySelectorAll('webview');
  var a=[];
  for(var i=0;i<wvs.length;i++){
    var r=wvs[i].getBoundingClientRect();
    a.push({i:i,
            sx:Math.round(window.screenX+r.left),
            sy:Math.round(window.screenY+r.top),
            w:Math.round(r.width),
            h:Math.round(r.height)});
  }
  return JSON.stringify({sX:window.screenX,sY:window.screenY,list:a});
})()
"""

def cand_probe(kw):
    return """
(function(){
  var els=document.querySelectorAll('*');
  var a=[];
  for(var i=0;i<els.length;i++){
    var t=(els[i].textContent||"").trim();
    if(t==='""" + kw + """'){
      var r=els[i].getBoundingClientRect();
      a.push({tag:els[i].tagName,
              cls:String(els[i].className||""),
              id:els[i].id||"",
              kids:els[i].children.length,
              cx:Math.round(r.left+r.width/2),
              cy:Math.round(r.top+r.height/2),
              w:Math.round(r.width),
              h:Math.round(r.height)});
    }
  }
  return JSON.stringify(a);
})()
"""

print("\n=== main webviews ===")
print(js(main["webSocketDebuggerUrl"], WV_PROBE))

print("\n=== '文档导入' candidates (textContent === ) ===")
print(js(wtt["webSocketDebuggerUrl"], cand_probe("文档导入")))

print("\n=== '添加更多' candidates ===")
print(js(wtt["webSocketDebuggerUrl"], cand_probe("添加更多")))
