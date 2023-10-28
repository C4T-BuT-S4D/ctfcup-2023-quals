# web | waf

## Information

> В 2196 году ты не попадешь в кибервойска если не решишь вот эту задачу.  
>
> You won't get into cyberforce in 2196 if you don't solve this task.

## Deploy

Need whale deployment.

Image: `cr.yandex/crp56e8fvolm1rqugnkf/web-waf:latest`
Port: `80`

Compose(local) deploy:

```sh
cd deploy
docker compose -p web-scanner up --build -d
```

## Public

Provide zip file: [public/web-waf.zip](public/web-waf.zip).

## TLDR

WAF bypass by providing two "Content-Type" headers.

## Writeup (ru)

TODO 

[Эксплойт](solve/vzlom.py)

## Writeup (en)

TODO 

[Эксплойт](solve/vzlom.py)

## Domain

Should be auto-generated by Whale.

## Cloudflare

No

## Flag

Should be auto-generated by Whale.