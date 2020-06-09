# AvataService

1.install apache benchmark
sudo yum install httpd-tools

2.Start service

3.Run test
for python
ab -n 4000 -c 100 http://127.0.0.1:5000/-1

for nginx
ab -n 4000 -c 100 -H "Host: your_server_hostname" http://127.0.0.1:80/-1
