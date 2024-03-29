# 为了能在外部脚本中调用Django ORM模型，必须配置脚本环境变量，将脚本注册到Django的环境变量中
from email import message
import os, sys
import random
import time
import django
# 引入mqtt包
import paho.mqtt.client as mqtt
# 使用独立线程运行
from threading import Thread
import manage_system.gloabl_var as global_var


# 第一个参数固定，第二个参数是工程名称.settings
os.environ.setdefault('DJANGO_SETTING_MODULE', 'my_django.settings')
django.setup()


# 建立mqtt连接
def on_connect(client, userdata, flag, rc):
    print("Connect with the result code " + str(rc))
    client.subscribe('total_weight', qos=2)

# 接收、处理mqtt消息
def on_message(client, userdata, msg):
    out = str(msg.payload.decode('utf-8'))
    global_var.set_value("total_weight", out)
    global_var.set_value("status", "weight_ok")
    print(out)

def on_disconnect(client, userdata, rc):
    print("Disonnect with the result code " + str(rc))


# mqtt客户端启动函数
def mqttfunction():
    global client
    # 使用loop_start 可以避免阻塞Django进程，使用loop_forever()可能会阻塞系统进程
    #client.loop_start()
    # client.loop_forever() 有掉线重连功能
    client.loop_forever(retry_first_connection=True)


client = mqtt.Client(client_id=f'client-{random.randint(0, 1000)}', clean_session=False)


# 启动函数
def mqtt_run():
    # client = mqtt.Client(client_id=f'client-{random.randint(0, 1000)}', clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    # 绑定 MQTT 服务器地址
    # mqttBroker = '192.168.31.228'
    mqttBroker = "mqtt.eclipseprojects.io"
    # MQTT服务器的端口号
    client.connect(mqttBroker)
    # 启动
    #client.loop_start()
    mqttthread = Thread(target=mqttfunction)
    mqttthread.start()


# 启动 MQTT
# mqtt_run()

if __name__ == "__main__":
    mqtt_run()
