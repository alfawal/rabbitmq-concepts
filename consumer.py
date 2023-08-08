import pika
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    # consumer.py
    # -q/--queue
    parser.add_argument(
        "-q",
        "--queue",
        required=True,
        help="Queue name (routing key)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # if nothing is passed to the constructor, the default parameters are used
    # in the default situation, there is no need for pika.ConnectionParameters
    connection = pika.BlockingConnection()
    channel = connection.channel()

    try:
        # Declare a queue
        channel.queue_declare(queue=args.queue)

        # Consume a message
        def callback(ch, method, properties, body) -> None:
            print(f" [x] Received {body.decode()}")

        channel.basic_consume(
            queue=args.queue,
            on_message_callback=callback,
            auto_ack=True,
        )
        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()

    except KeyboardInterrupt:
        print("\nInterrupted by user, closing the connection and exiting...")
        connection.close()
        exit(0)
    except Exception as e:
        print(f"Failed to consume {args.message!r} from {args.queue!r}")
        print(e)

    connection.close()
