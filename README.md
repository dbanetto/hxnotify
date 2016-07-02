# hxnotify

A python 3 plugin to control OS notification on message in a channel and
to notification when users you have `/notify`'d login in or off.

## Install

Either load it manually in HexChat
or copy it to the add-on folder in :

* Windows `%appdata%\HexChat\Addons`
* Unix `~/.config/hexchat/addons`

## How to use

The plugin exposes a command `/hxnotify` which has 3 commands for the white list
of channels that the notification should be for.

* `add` - which adds the listed channels after it, or your current channel if none are provided
* `rm` - which removes the listed channels after it, or your current channel if none are provided
* `list` - lists all the channels that are white listed

```
/hxnotify - configuration control for hxnotify plugin
/hxnotify add (#channel) - adds channel(s) to whitelist of channels to notify on, defaults to current channel
/hxnotify rm (#channel)  - removes channel(s) from whitelist of channels to notify on, defaults to current channel
/hxnotify list - lists channels in whitelist
/hxnotify test - sends test notification
```

## Limitations

The whitelist is global and is applied to all networks, so if you have 
one channel named the same on two networks and only want one of them to be
whitelisted, this is not supported yet.

This was developed using the Python 3 plugin for HexChat 2.12 on Linux,
testing on other platforms or earlier versions of python or hexchat are supported

### License

MIT see LICENSE.md for more
