#!/usr/bin/env python3
import hexchat

__module_name__ = "hxnotify"
__module_version__ = "0.3"
__module_description__ = "Python module to display tray notifications"


def limit_msg(msg, length=160):
    if len(msg) > length:
        return msg[0:length - 3] + "..."
    else:
        return msg


def get_usrname(name):
    return name[1 if name[0] == ':' else 0:name.index('!')]


def friend_online(word, word_eol, userdata):
    print("Online",word)
    for name in word[3][1:].split(','):
        hexchat.command("tray -b \"Friend Online\" \"" +
                        get_usrname(name) + " is online\"")
    return None


def friend_offline(word, word_eol, userdata):
    print('Offline', word)
    for i in hexchat.get_list("notify"):
        for name in word[3][1:].split(','):
            if name == i.nick:
                print(i.nick, i.on)
                if i.on != 0: # check if they have been online
                    hexchat.command("tray -b \"Friend Offline\" \"" +
                                    name +
                                    " has gone offline\"")
    return None


def channel_msg(word, word_eol, userdata):
    if hexchat.get_info("win_status") == "active":
        return None

    for ch in hexchat.get_list("channels"):
        # handle only channel
        if ch.type != 2:
            continue

        if word[2] == ch.channel:
            if bool(ch.flags & (1 << 10)): # blink task tray
                hexchat.command("tray -b \"Message in " + ch.channel + "\" \"" +
                                get_usrname(word[0]) + ": " +
                                limit_msg(word_eol[3][2:]) +
                                "\"")
            break

    return None


hexchat.hook_server("730", friend_online)
hexchat.hook_server("731", friend_offline)
hexchat.hook_server("PRIVMSG", channel_msg)
print("Loaded " + __module_name__ + " v" + __module_version__)
