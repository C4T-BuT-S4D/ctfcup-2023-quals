# crp | lateralus

## Information

С нами вошел в контакт один из ученых "Арбалетов Сибири", он утверждает, что не согласен с методами и корпорации, желает вам помочь и направляет вам секретный проэкт. Однако открыв его, единственное что вы обнаруживаете какие то бессмысленные заметки про числа Фибоначи и этот файл.

You were contacted by one of the scientists of "Arbalest of Siberia", he says he does not agree with the methods of the corporation, wants to help and forwards you some secret project. However having opened it, all you find is some incomprehensible ramblings about Fibonachi numbers and this file.

## Public

Provide python script file: [public/lateralus.py](public/lateralus.py).

## TLDR

Given nth fibonachi number modulo `p ^ 2` (where `p` is prime) find `n`.

## Writeup (ru)

Имея н-нное число фибоначи под модулю `p ^ 2` (где `p` - простое) найти `n`.

Имея формулу н-нного числа фибоначи через золотое сечение, поскольку, `(phi ^ n + psi ^ n) ^ 2 == phi ^ 2n + psi ^ 2n + 2`, получаем и решаем систему уравнений для `phi ^ n` и `psi ^ n`, потом находим дискретный логарифм по модулю `p` используя принцип криптосистемы Пэйе.

## Writeup (en)

Given nth fibonachi number modulo `p ^ 2` (where `p` is prime) find `n`.

Using the fibonachi number through golden rasio formula, since `(phi ^ n + psi ^ n) ^ 2 == phi ^ 2n + psi ^ 2n + 2`, we can get a system of equations for `phi ^ n` and `psi ^ n`, solve it, then find the discrete logarithm modulo `p` using the Paillier cryptosystem trick.

[Exploit](solve/solve.py)

## Flag

ctfcup{0v3rthInk1nG_ov3r4nal1ziNg}
