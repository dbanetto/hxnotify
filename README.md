# HXNotify

HexChat C & python plugin to push notifications to through libnotify

Currently pushes a notification for:

* when a friend is online
* when a channel marked with `alert_tray`, set via `/CHANOPT`

Planned notifications:

* name is said in a channel

## Requirements

* libnotify
* hexchat

## Note

The python is more stable than the C version.

The C version is prone to crash for unknown reasons, if you see anything wrong
PRs will be helpful.

## Build

For the C plugin run `make`

## Install

For the C plugin run `make install` to copy the plugin
or run `make install-link` to symlink the binary.

## How to use

Either load it manually in HexChat
or copy it to the add-on folder in :

* Windows `%appdata%\HexChat\Addons`
* Unix `~/.config/hexchat/addons`
