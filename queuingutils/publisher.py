from google.cloud import pubsub_v1


class Publisher:
    def __init__(self, project_id, topic_name):
        self._publisher_obj = pubsub_v1.PublisherClient()
        self.project = self.get_project(project_id)
        self.topic = self.get_topic(project_id, topic_name)

    def publish_message(self, subscriber, message, metadata):
        import json

        string_metadata = json.dumps(metadata)

        self._publisher_obj.publish(self.topic,
                                    message,
                                    subscription_name=subscriber,
                                    metadata=string_metadata)

    def create_topic(self, topic_name):
        response = self._publisher_obj.create_topic(topic_name)

        return response

    def delete_topic(self, topic_name):
        self._publisher_obj.delete_topic(topic_name)

    def get_topic(self, project_id, topic_name):
        topic = self._publisher_obj.topic_path(project_id,
                                               topic_name)
        return topic

    def get_project(self, project_id):
        return self._publisher_obj.project_path(project_id)
