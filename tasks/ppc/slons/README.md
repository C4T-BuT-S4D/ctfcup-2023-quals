# ppc | slons

## Information

> Your task is to unveil the RSA secret and discover the number of elephants hidden within the heart of the Chess of Power. The hope of the great kingdom of Elephanta rests on you!
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

В задаче количестов слонов на доске может быть от 0 до 65, а ошибки нее учитываются, то есть достаточно просто перебрать.
## Writeup (en)

The task allows for the number of elephants on the board to range from 0 to 65, and errors are taken into account, so it's sufficient to simply iterate through them.


[Exploit](solve/solve.py)

## Domain

slons-afb69872b377a978.ctfcup-2023.ru

## Cloudflare

No

## Flag

ctfcup{a51c8cc4d131a6cbe54bfce654fa9c81}