# AvataService

# I tested using python and nginx: who is faster as an avatar server?

The test is conducted using `Apache Benchmark`, you can refer to these data

I use the `ab -n 4000 -c 100 http://127.0.0.1/avatar` command to test, the `apache benchmark` will make 4000 requests to the avatar server with 100 concurrent requests.

The avatar used in the test is this:
![avatar](https://github.com/kafuu-osu/AvataService/blob/master/target.jpg)

I placed the avatar picture in the avatars directory and named it `-1.png`, then used the test command to test.


# Test Result

**1.first, its python flask**

Flask comes with a server, you can see the speed is slow, the request took a total of 5 seconds

![flask_werkzeug](https://github.com/kafuu-osu/AvataService/blob/master/python_flask_werkzeug.png)

The code is in `flask.py`

---

**2.python flask with gunicorn**

Some slightly faster, 4 seconds

![flask_gunicorn](https://github.com/kafuu-osu/AvataService/blob/master/python_flask_gunicorn.png)

---

**3.The fastest python library: fastapi**

You can see that the speed comes directly to about 1.5 seconds, which is much faster than flask!

![python_fastapi](https://github.com/kafuu-osu/AvataService/blob/master/python_fastapi.png)

---

**4.python starlette, the underlying library of fastapi**

It contains some functions that I encapsulated myself, which is faster and came to about 1.2 seconds (in fact, the improvement is not as large as before, and it can only be optimized a little bit)

The code is in `starlette.py`

![python_starlette](https://github.com/kafuu-osu/AvataService/blob/master/python_starlette.png)

---

**5.Fastest, nginx**

The fastest server appeared, 4000 requests only took 0.45s! It is what we know as nginx!
I used a pseudo-static nginx configuration so that I can directly use the user id to access the avatar picture

like this: http://xxx/1000, http://xxx/-1

About pseudo static configuration reference, I put it in `nginx.conf`

![nginx](https://github.com/kafuu-osu/AvataService/blob/master/nginx.png)

---

**6.nginx with ssl**

However, under the blessing of ssl, even nginx became unable to run, which took 8 seconds.

![nginx_ssl](https://github.com/kafuu-osu/AvataService/blob/master/nginx_with_ssl.png)


---




# Test

**1.install apache benchmark**
sudo yum install httpd-tools

**2.Start service**

**3.Run test**
for python
`ab -n 4000 -c 100 http://127.0.0.1:5000/-1`

for nginx
`ab -n 4000 -c 100 -H "Host: your_server_hostname" http://127.0.0.1:80/-1`
