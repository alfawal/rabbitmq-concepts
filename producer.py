import pika
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    # producer.py
    # -q/--queue
    parser.add_argument(
        "-q",
        "--queue",
        required=True,
        help="Queue name (routing key)",
    )

    # -m/--message
    parser.add_argument(
        "-m",
        "--message",
        required=True,
        help="Message to send",
    )

    # -e/--exchange (optional)
    parser.add_argument(
        "-e",
        "--exchange",
        help="Exchange name",
        default="",
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

        # Send a message
        channel.basic_publish(
            exchange=args.exchange,
            routing_key=args.queue,
            body=args.message,
        )

        print(f" [x] Sent {args.message} to {args.queue}")
    except Exception as e:
        print(f"Failed to send {args.message!r} to {args.queue!r}")
        print(e)

    connection.close()
