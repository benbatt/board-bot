#!/bin/sh

mkdir -p ~/.config/systemd/user
cp board-bot.service board-bot.timer ~/.config/systemd/user
systemctl --user enable --now board-bot.timer
systemctl --user daemon-reload

echo "Remember to add BOARD_BOT_TOKEN=<your whapi token> to ~/board-bot/systemd/environment"
