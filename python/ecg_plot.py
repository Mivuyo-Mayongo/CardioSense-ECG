"""Real-time ECG visualization for CardioSense.

Receives ADC readings from an ESP32 over USB Serial and displays
the most recent samples on a continuously updating graph.
"""

import argparse
from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Display ECG samples received from an ESP32."
    )
    parser.add_argument(
        "--port",
        default="COM4",
        help="Serial port connected to the ESP32 (default: COM4)",
    )
    parser.add_argument(
        "--baud",
        type=int,
        default=115200,
        help="Serial baud rate (default: 115200)",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=600,
        help="Number of samples displayed on the graph (default: 600)",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    ecg_values = deque([0] * args.samples, maxlen=args.samples)
    serial_connection = serial.Serial(
        args.port,
        args.baud,
        timeout=1,
    )
    serial_connection.reset_input_buffer()

    figure, axis = plt.subplots()
    line, = axis.plot(range(args.samples), ecg_values, color="teal")

    axis.set_title("CardioSense Live ECG Signal")
    axis.set_xlabel("Samples")
    axis.set_ylabel("ESP32 ADC Value")
    axis.set_xlim(0, args.samples - 1)
    axis.set_ylim(0, 4095)
    axis.grid(True, alpha=0.3)

    def update(_frame):
        while serial_connection.in_waiting:
            raw_value = serial_connection.readline().decode(
                "utf-8", errors="ignore"
            ).strip()

            try:
                ecg_value = int(raw_value)
            except ValueError:
                # Ignore status messages such as "Leads Off".
                continue

            ecg_values.append(ecg_value)

        line.set_ydata(ecg_values)
        return (line,)

    def close_serial(_event):
        if serial_connection.is_open:
            serial_connection.close()

    figure.canvas.mpl_connect("close_event", close_serial)

    animation.FuncAnimation(
        figure,
        update,
        interval=20,
        blit=True,
        cache_frame_data=False,
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
