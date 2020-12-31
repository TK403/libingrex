"""COMM monitor"""
import ingrex
import time


def main():
    """main function"""
    field = {
        "minLng": 116.298171,
        "minLat": 39.986831,
        "maxLng": 116.311303,
        "maxLat": 39.990941,
    }

    min_ts = -1

    while True:
        intel = ingrex.Intel(sessionid="")
        result = intel.fetch_msg(
            field["maxLat"], field["maxLng"], field["minLat"], field["minLng"], min_ts=min_ts,
        )
        if result:
            min_ts = int(result[0][1]) + 1
        for item in result[::-1]:
            message = ingrex.Message(item)
            print("{} {}".format(message.time, message.text))
        time.sleep(10)


if __name__ == "__main__":
    main()
