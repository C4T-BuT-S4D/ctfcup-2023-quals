# ppc | slons

## Information

> Арбалеты Сибири создали лотерею, где зарабатывают огомные деньги. Можно ли ее взломать ?
> 
> `http://slons-afb69872b377a978.ctfcup-2023.ru`

## Deploy

```sh
cd deploy
docker compose -p ella_enchanted up --build -d
```

## Public

No

## TLDR

Just bruteforce)

## Writeup (ru)

Декодируем сессию, и декодируем сообщение, после чего отправляем число.

## Writeup (en)

Decode the session, decode the message, then send the number

[Exploit](solve/solve.js)

## Domain

slons-afb69872b377a978.ctfcup-2023.ru

## Cloudflare

No

## Flag

ctfcup{a51c8cc4d131a6cbe54bfce654fa9c81}