import pika

from tournament.Interface import GameInterface
import json

from functools import partial

# Standard library that includes the Unix environment.
import os

# AMQP client library.
import pika

#: Name of the RabbitMQ exchange.
EXCHANGE = 'exchange'
ROUTING_KEY = 'exchange.game'

#: Name of the RabbitMQ queue.
QUEUE = 'game'


def main2():
    """Main entry point to the program."""

    # Get the location of the AMQP broker (RabbitMQ server) from
    # an environment variable
    amqp_url = os.environ['AMQP_URL']
    print('URL: %s' % (amqp_url,))

    # Actually connect
    parameters = pika.URLParameters(amqp_url)
    connection = pika.SelectConnection(parameters, on_open_callback=on_open)

    # Main loop.  This will run forever, or until we get killed.
    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        connection.close()
        connection.ioloop.start()


def on_open(connection):
    """Callback when we have connected to the AMQP broker."""
    print('Connected')
    connection.channel(on_channel_open)


def on_channel_open(channel):
    """Callback when we have opened a channel on the connection."""
    print('Have channel')

    # We must declare the exchange before we can bind to it.  It
    # doesn't matter that both the publisher and consumer are
    # declaring the same exchange, except that they must both declare
    # it with the same parameters.
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct',
                             durable=True,
                             callback=partial(on_exchange, channel))

    # If we were brave we could also call queue_declare here, but
    # in the callback chain we'd have to wait to bind the queue to
    # the exchange until both had been declared.


def on_exchange(channel, frame):
    """Callback when we have successfully declared the exchange."""
    print('Have exchange')
    channel.queue_declare(queue=QUEUE, durable=True,
                          callback=partial(on_queue, channel))


def on_queue(channel, frame):
    """Callback when we have successfully declared the queue."""
    print('Have queue')

    # This call tells the server to send us 1 message in advance.
    # This helps overall throughput, but it does require us to deal
    # with the messages we have promptly.
    channel.basic_qos(prefetch_count=1, callback=partial(on_qos, channel))


def on_qos(channel, frame):
    """Callback when we have set the channel prefetch limit."""
    print('Set QoS')
    channel.queue_bind(queue=QUEUE, exchange=EXCHANGE,
                       callback=partial(on_bind, channel))


def on_bind(channel, frame):
    """Callback when we have successfully bound the queue to the exchange."""
    print('Bound')
    channel.basic_consume(queue=QUEUE, consumer_callback=on_message)


def on_message(channel, delivery, properties, body):
    """Callback when a message arrives.
    :param channel: the AMQP channel object.
    :type channel: :class:`pika.channel.Channel`
    :param delivery: the AMQP protocol-level delivery object,
      which includes a tag, the exchange name, and the routing key.
      All of this should be information the sender has as well.
    :type delivery: :class:`pika.spec.Deliver`
    :param properties: AMQP per-message metadata.  This includes
      things like the body's content type, the correlation ID and
      reply-to queue for RPC-style messaging, a message ID, and so
      on.  It also includes an additional table of structured
      caller-provided headers.  Again, all of this is information
      the sender provided as part of the message.
    :type properties: :class:`pika.spec.BasicProperties`
    :param str body: Byte string of the message body.
    """
    # Just dump out the information we think is interesting.
    print('Exchange: %s' % (delivery.exchange,))
    print('Routing key: %s' % (delivery.routing_key,))
    print('Content type: %s' % (properties.content_type,))
    print()
    print(body)
    print(json.loads(body))

    # Important!!! You MUST acknowledge the delivery.  If you don't,
    # then the broker will believe it is still outstanding, and
    # because we set the QoS limit above to 1 outstanding message,
    # we'll never get more.
    #
    # If something went wrong but retrying is a valid option, you
    # could also basic_reject() the message.
    channel.basic_ack(delivery.delivery_tag)

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
