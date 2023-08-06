import requests
import tqdm

if __name__ == '__main__':
    requests.put('http://127.0.0.1:8081/v1/arizon/force?flag=true')
    try:
        with tqdm.tqdm() as pbar:
            while True:
                resp = requests.get('http://127.0.0.1:8081/v1/arizon/force')
                data = resp.json()['data']
                if len(data) > 0:
                    pbar.set_description("Force: {}, Timestamp: {}".format(data[-1]['f'], data[-1]['ts'] ))
                    pbar.update(len(data))
                    # Force: 0.0, Timestamp: 1675831264.3972561: : 5817it [00:15, 368.32it/s]  
    except KeyboardInterrupt as e:
        requests.put('http://127.0.0.1:8081/v1/arizon/force?flag=false')