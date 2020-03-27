from queuingutils.subscriber import Subscriber

if __name__ == "__main__":
    project_id = 'pub-sub132608'
    subscription_name = 'sub_one'
    topic_name = 'hello-topic'

    subscriber = Subscriber(project_id, subscription_name, topic_name)

    subscriber.start_server()
