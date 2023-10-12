# pwn | ella_enchanted

## Information

> JavaScript teaches us to embrace mistakes and turn them into opportunities
> 
> `static-mistakes-4a27e2504ec596fe.ctfcup.ru`

## Deploy

```sh
cd deploy
docker compose -p mistakes up --build -d
```

## Public

Provide zip file: [public/task.zip](public/task.zip).

## TLDR

Prototype pollution via window name, bypass regex

## Writeup (ru)

1. Сайт взаимодействует с API через POST запросы без проверки origin. Это позволяет отправлять запросы с любого сайта через `postMessage`.

2. Заметим, что используется переменная `name` без предварительной инициализации:

    ```javascript
    if(!name) name = 'mainStorage'
    ```

   Поэтому будет использовано значение `window.name`, которое можно установить через `window.open`:

    ```javascript
    window.open(task, name_variable)
    ```

3. При установке `name` в `__proto__`, данные будут сохранены в `Object.prototype`:

    ```javascript
    storage = storage[name]
    ```

4. Затем, используя переданный JSON файл, можно провести атаку Prototype Pollution:

    ```javascript
    let instructionsJson = await fetch(debugUrl);
    instructionsJson = await instructionsJson.json();
    console.log(instructionsJson)
    for(let inst in instructionsJson){
        console.log(inst)
        storage[inst] = instructionsJson[inst].toLowerCase();
    }
    ```

   Но для этого необходимо обойти regex, что можно сделать, предоставив IPv6 url:

    ```
    http://[::-1]:#.task.ctfcup.ru
    ```

5. После этого находим chain для XSS в функции вставки элемента:

    ```javascript
    for(var param in params){
        if(param.startsWith("on"))
            node.setAttribute(param,"logEvent('debug',event)");
        else
            node.setAttribute(param, params[param])
    }
    ```

   Можно вставить любой атрибут, но не аттрибуты, начинающиеся с "on". Решение проблемы - переписать `srcdoc`, так как он имеет больший приоритет чем `src`, и при вставке `iframe` будет выполнен наш скрипт.

## Writeup (en)

# Website Security Analysis

1. The website communicates with the API via POST messages without checking the origin. This allows sending requests from any website using `postMessage`.

2. It is noticed that the variable `name` is used without prior initialization:

    ```javascript
    if (!name) name = 'mainStorage'
    ```

   Therefore, the value of `window.name` will be used, which can be set through `window.open`:

    ```javascript
    window.open(task, name_variable)
    ```

3. When `name` is set to `__proto__`, the data will be stored in `storage[Object.prototype]`:

    ```javascript
    storage = storage[name]
    ```

4. Next, by using the provided JSON file, it is possible to perform a Prototype Pollution attack:

    ```javascript
    let instructionsJson = await fetch(debugUrl);
    instructionsJson = await instructionsJson.json();
    console.log(instructionsJson)
    for (let inst in instructionsJson) {
        console.log(inst)
        storage[inst] = instructionsJson[inst].toLowerCase();
    }
    ```

   To do this, it is necessary to bypass regex, which can be done by providing an IPv6 URL:

    ```
    http://[::-1]:#.task.ctfcup.ru
    ```

5. Then, find a chain for XSS in the element insertion function:

    ```javascript
    for (var param in params) {
        if (param.startsWith("on"))
            node.setAttribute(param, "logEvent('debug',event)");
        else
            node.setAttribute(param, params[param])
    }
    ```

   It is possible to insert any attribute, but attributes starting with "on" cannot be inserted. The way to overcome this is to rewrite `srcdoc`, as it takes precedence over `src`, so when an `iframe` is inserted, our script will be executed.


[Exploit](solve/exploit.html)

## Domain

static-mistakes-4a27e2504ec596fe.ctfcup.ru
api-mistakes-4a27e2504ec596fe.ctfcup.ru


## Cloudflare

Yes

## Flag

ctfcup{380f99f77826f5fc0af980915f9c375d}