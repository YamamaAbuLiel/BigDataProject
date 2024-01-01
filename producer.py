#!/usr/bin/env python
# coding: utf-8

# In[11]:


import time
import json
from kafka import KafkaProducer
import random
from time import sleep

# Kafka producer configuration
bootstrap_servers = 'localhost:9092' 
topic_name = "tweets"
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,value_serializer=lambda v: json.dumps(v).encode('utf-8'))

i = 1

with open(r'C:\Users\Yamama Abu Liel\Desktop\Big Data Project\training.csv', 'rt') as f:
    # Rest of your code
    for line in f:
        if i % 1000 != 0:
            line = line.replace("\'", "\"")
            attribute_details = line.split(',')
            tweet = {
                "id": attribute_details[1],
                "date": int(time.time() * 1000),
                "user": attribute_details[4],
                "text": attribute_details[5],
                "retweets": int(random.random() * 10)
            }

            # Publish the tweet to Kafka
            producer.send(topic_name, value=tweet)
        else:
            sleep(1)

        i = i + 1

# Close the Kafka producer
producer.close()


# In[ ]:





# In[ ]:




