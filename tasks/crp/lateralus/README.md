# crp | lateralus

## Information

Black
Then
White are
All I see
In my infancy
Red and yellow then came to be
Reaching out to me
Lets me see

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
