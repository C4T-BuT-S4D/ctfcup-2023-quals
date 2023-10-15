# crp | geometry

## Information

In group theory, the symmetry group of a geometric object is the group of all transformations under which the object is invariant, endowed with the group operation of composition.

## Public

Provide zip file and traffic dump: [public/geometry.zip](public/geometry.zip) [public/geometry.pcapng](public/geometry.pcapng).

## TLDR

Diffie-Hellman on a symmetric group of a regular 1337-vertex polygon (with cardinality of 2 * 1337).

## Writeup (ru)

Нам дан сетевой дамп взаимодействия клиента и сервера с использованием протокола Диффи-Хеллмана над группой симметрий правильного 1337-угольника.

Поскольку мощность группы 2 ** 1337, мы можем просто перебрать все возможные степени генератора и расшифровать отправленное клиентом сообщение. 

## Writeup (en)

We are given an dump of a client server Diffie-Hellman exchange on a symmetric group of a regular 1337-vertex polygon.

Since the cardinality of the group is only 2 * 1337, we can just bruteforce all significant powers of the generator and decrypt the exchange.


[Exploit](solve/solve.py)

## Flag

ctfcup{4c38ecb373623fd0aba1b6bfb7f08be2}
