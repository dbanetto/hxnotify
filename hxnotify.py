#!/usr/bin/env python3
__module_name__ = "hxnotify"
__module_version__ = "0.2"
__module_description__ = "Python module to display tray notifications"

import hexchat


def limit_msg(msg, length=50):
    if len(msg) > length:
        return msg[0:length - 3] + "..."
    else:
        return msg


def get_usrname(name):

    return name[1 if name[0] == ':' else 0:name.index('!')]


def friend_online(word, word_eol, userdata):
    for name in word[3][1:].split(','):
        hexchat.command("tray -b \"Friend Online\" \""
                        + get_usrname(name) + " is online\"")
    return None


def friend_offline(word, word_eol, userdata):
    for name in word[3].split(','):
        for i in hexchat.get_list("notify"):
            if name == i.nick and i.on != 0:
                hexchat.command("tray -b \"Friend Offline\" \""
                                + name
                                + " has gone offline\"")
    return None


def channel_msg(word, word_eol, userdata):
    if hexchat.get_info("win_status") == "active":
        return None

    for ch in hexchat.get_list("channels"):
        if word[2] == ch.channel and bool(ch.flags & 1 << 8):
            hexchat.command("tray -b \"Message in " + ch.channel + "\" \""
                            + get_usrname(word[0]) + ": "
                            + limit_msg(word_eol[3][2:])
                            + "\"")
            break
    return None


hexchat.hook_server("730", friend_online)
#hexchat.hook_server("731", friend_offline)
hexchat.hook_server("PRIVMSG", channel_msg)
print("Loaded " + __module_name__ + " v" + __module_version__)
