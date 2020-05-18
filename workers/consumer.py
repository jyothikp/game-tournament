import json
import pika

from tournament.Interface import GameInterface


def main():
    connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq', connection_attempts=10,
                                      retry_delay=10))
    channel = connection.channel()

    channel.queue_declare(queue='game')

    def callback(ch, method, properties, body):
        try:
            data = json.loads(json.loads(body))
            print(data, type(data))
            GameInterface().save(data)
        except Exception as e:
            print(e)

    channel.basic_consume(
            queue='game', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
