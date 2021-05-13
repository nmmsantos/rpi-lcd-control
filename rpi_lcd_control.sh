#!/bin/sh

dpkg -s python3-venv git tmux  >/dev/null

cd "$(dirname "$(readlink -f "$0")")"

test ! -d .venv && \
  python3 -m venv --system-site-packages .venv && \
  . .venv/bin/activate && \
  pip install -U pip && \
  pip install smbus2 git+https://github.com/pimoroni/VL53L0X-python.git || \
  . .venv/bin/activate

exec tmux new-session -d -s rpi_lcd_control 'exec python rpi_lcd_control.py >/dev/null 2>&1'
