from google.cloud import pubsub_v1
import time


class Subscriber:
    def __init__(self, project_id, subscriber, topic_name):
        self._subscriber_obj = pubsub_v1.SubscriberClient()
        self.project_id = project_id
        self.subscriber_name = subscriber
        self.topic_name = topic_name
        self.project = self.get_project(project_id)
        self.subscriber = self.get_subscriber(project_id, subscriber)

    def get_project(self, project_id):
        """

        This function returns the entire project path by using the project id

        :param project_id: project identifier corresponding to the project
        containing the desired subscriber
        :return:
        """
        return self._subscriber_obj.project_path(project_id)

    def get_subscriber(self, project_id, subscriber):
        """

        This function returns the entire subscriber path by using the
        project id and subscriber name

        :param project_id: project identifier corresponding to the project
        containing the desired subscriber
        :param subscriber: name of the subscriber that you want to pull
        messages from
        :return:
        """
        return self._subscriber_obj.subscription_path(
                project_id, subscriber
            )

    def create_subscriber(self, name):
        subscriber_path = self._subscriber_obj.subscription_path(
            self.project_id, name
        )
        topic_path = self._subscriber_obj.topic_path(
            self.project_id, self.topic_name
        )

        self._subscriber_obj.create_subscriber(subscriber_path, topic_path)

    @staticmethod
    def callback(message):
        """

        This function will be called every time a new message is pulled from
        the queue.

        :param message: object containing information about the incoming
        message
        :return:
        """
        print(f"Received message: {message.data}")
        metadata_dict = message.attributes
        print(f"Message metadata: {metadata_dict}")
        message.ack()

    def start_server(self):
        """

        This function will indefinitely pull messages from the queue sent to
        the previously selected subscriber.

        :return:
        """
        print(f"Listening for messages on {self.subscriber}")
        print("...")
        while True:
            streaming_pull_future = self._subscriber_obj.subscribe(
                self.subscriber, callback=Subscriber.callback
            )

            try:
                streaming_pull_future.result(timeout=4)
            except KeyboardInterrupt:
                streaming_pull_future.cancel()
                print("Exiting Gracefully")
                break
            except:
                # print(f"Exception: {e}")
                streaming_pull_future.cancel()

            time.sleep(5)
