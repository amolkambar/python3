# IO bound processes benefit from concurrency/multi-threading,
# CPU bound processes benefit from multiprocessing.

import time
import threading
import concurrent.futures
import requests

img_urls = [
    'https://images.unsplash.com/photo-1516117172878-fd2c41f4a759',
    'https://images.unsplash.com/photo-1532009324734-20a7a5813719',
    'https://images.unsplash.com/photo-1524429656589-6633a470097c',
    'https://images.unsplash.com/photo-1530224264768-7ff8c1789d79',
    'https://images.unsplash.com/photo-1564135624576-c5c88640f235',
    'https://images.unsplash.com/photo-1541698444083-023c97d3f4b6',
    'https://images.unsplash.com/photo-1522364723953-452d3431c267',
    'https://images.unsplash.com/photo-1513938709626-033611b8cc03',
    'https://images.unsplash.com/photo-1507143550189-fed454f93097',
    'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e',
    'https://images.unsplash.com/photo-1504198453319-5ce911bafcde',
    'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99',
    'https://images.unsplash.com/photo-1516972810927-80185027ca84',
    'https://images.unsplash.com/photo-1550439062-609e1531270e',
    'https://images.unsplash.com/photo-1549692520-acc6669e2f0c'
]

def do_something(seconds):
    print(f'Sleeping {seconds} second...')
    time.sleep(seconds)
    return f'Done Sleeping...{seconds}'

def var_time():

    start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        secs = [5, 4, 3, 2, 1]
        results = [executor.submit(do_something, sec) for sec in secs]

    # using the submit objects outside with
    # prints as tast completed order
    for f in concurrent.futures.as_completed(results): # iterable of type future
        print(f.result())

    print(f'Finished in {time.perf_counter() - start} second(s)')

def var_time_2():

    start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        secs = [5, 4, 3, 2, 1]
        results = [executor.submit(do_something, sec) for sec in secs]
        #using the submit objects inside pool executor
        for f in concurrent.futures.as_completed(results): # iterable of type future
            print(f.result())

    print(f'Finished in {time.perf_counter() - start} second(s)')
    #Finished in 5.019821000052616 second(s)

def exe_submit():
    start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(do_something, 2) # returns a future object
        f2 = executor.submit(do_something, 2)
        print(f1.result())
        print(f2.result())

    finish = time.perf_counter()

    print(f'Finished in {time.perf_counter()-start} second(s)')
    # Finished in 2.0157395999412984 second(s)

def sync_main():
    start_ts = time.perf_counter()

    # do_something(5) # finish print at 5 seconds

    t1 = threading.Thread(target=do_something, args=[2])
    t2 = threading.Thread(target=do_something, args=[2])
    t1.start()      # finish right after sleeping print ~ 0.008 seconds
    t1.join()       
    t2.start()     # join right after start is similar to synchronous exec
    t2.join()      # takes 10 secs for 2 threads
    
    print(f'finished in {time.perf_counter() - start_ts} seconds')
    # finished in 4.013705099932849 seconds

def concurr_main():
    start_ts = time.perf_counter()

    threads = []
    for _ in range(10):
        t = threading.Thread(target=do_something, args=[2])
        t.start()
        threads.append(t)
    
    for thread in threads:
        thread.join()
    
    print(f'finished in {time.perf_counter() - start_ts} seconds')
    # finished in 2.0268969999160618 seconds
    # Does not return anything

def download_image(img_url):
    img_bytes = requests.get(img_url).content
    img_name = img_url.split('/')[3]
    img_name = f'{img_name}.jpg'
    with open(img_name, 'wb') as img_file:
        img_file.write(img_bytes)
        print(f'{img_name} was downloaded...')

def download_sync():
    t1 = time.perf_counter()

    for url in img_urls:
        download_image(url)

    t2 = time.perf_counter()

    print(f'Finished in {t2-t1} seconds')
    # Finished in 15.382477200007997 seconds

def donwload_concurr():

    t1 = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, img_urls)
    
    t2 = time.perf_counter()

    print(f'Finished in {t2-t1} seconds')
    # Finished in 2.7116674999706447 seconds

# sync_main()

# concurr_main()

# exe_submit()

# var_time_2()

# download_sync()

donwload_concurr()