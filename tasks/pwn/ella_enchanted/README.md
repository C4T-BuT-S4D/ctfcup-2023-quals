# pwn | ella_enchanted

## Information

> In the kingdom of Lamia, misguided fairy godmother Lucinda Perriweather bestows the "gift" of obedience on newborn Ella of Frell, causing her to instantly and literally obey any command she is given. Some years later, on her deathbed, Ella's mother warns her daughter not to tell anyone about the gift, for fear that someone might exploit her.
> 
> `nc ella-enchanted-afb698a2b374a968.ctfcup.ru 13000`

## Deploy

```sh
cd deploy
docker compose -p ella_enchanted up --build -d
```

## Public

Provide zip file: [public/ella_enchanted.zip](public/ella_enchanted.zip).

## TLDR

Arbitrary write to GOT and _fini_array sections.

## Writeup

We are given program with 3 options:
1) write any 8 bytes anywhere
2) read flag to buffer
3) write buffer contents to stdout.

We can only choose one option per program invocation.

As can be seen in Dockerfile the program doesn't have GOT table protection so we can write `main` function address to `puts@got` to loop our program.
After that we want to setup chain to read flag and output it. So we overwrite first entry in `_fini_array` to `ella_open` and `strchrnul@got` to `ella_print`. Finally we overwrite `puts@got` to `printf@plt` to exit the loop and execute chain `ella_open -> ella_print`.

[Exploit](solve/sploit.py)

## Domain

ella-enchanted-afb698a2b374a968.ctfcup.ru

## Cloudflare

No

## Flag

ctfcup{9b9a88751771e3b66c0f10e69cd5d6c8}
