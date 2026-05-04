# 文章自动发布 v1101.2 — mac/(占位,待汇总)

mac 三机已各自落 CDP nativeInputValueSetter 注入修法(2026-04-29 凌晨 air + neo 实战印证)。
代码各自维护在仓库 `air/自动文章/`、`neo/自动文章/`、(后续 mini / neo2 跟进)分目录下。

待 air + neo + mini + neo2 各 Claude 把桌面真版 push 进各自分目录后,
绣虎以小齐(neo)版本为 mac source 合并到本目录。

修法核心(JS 注入片段):
```js
var s = document.querySelector('input[placeholder*="账号"],input[placeholder*="手机"]');
var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
setter.call(s, '<账号名>');
s.dispatchEvent(new Event('input',  {bubbles:true}));
s.dispatchEvent(new Event('change', {bubbles:true}));
```
绕过键盘焦点 + 罐头前台依赖,React/Vue controlled input 认作用户输入。
