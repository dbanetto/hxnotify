#!/usr/bin/env python3
import hexchat

__module_name__ = "hxnotify"
__module_version__ = "0.5"
__module_description__ = "Python module to display tray notifications"


def limit_msg(msg, length=160):
    # fixes issue with quotes cannot be esacped in hexchat commands
    msg = msg.replace('"', "'")
    if len(msg) > length:
        return msg[0:length - 3] + "..."
    else:
        return msg


def get_usrname(name):
    return name[1 if name[0] == ':' else 0:name.index('!')]


def friend_online(word, word_eol, userdata):
    for name in word[3][1:].split(','):
        hexchat.command("tray -b \"Friend Online\" \"" +
                        get_usrname(name) +
                        " is online\"")
    return None


def friend_offline(word, word_eol, userdata):
    for i in hexchat.get_list("notify"):
        for name in word[3][1:].split(','):
            if name == i.nick:
                if i.on != 0:  # check if they have been online
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
            if bool(ch.flags & (1 << 10) != 0):  # blink task tray
                from_user = get_usrname(word[0])
                # fix getting notifcations from self when a bouncer playback is running
                if hexchat.get_info('nick').strip() != from_user.strip():
                    hexchat.command("tray -b \"Message in " + ch.channel +
                                    "\" \"" + from_user + ": " +
                                    limit_msg(word_eol[3]) +
                                    "\"")
            break

    return None


hexchat.hook_server("730", friend_online)
hexchat.hook_server("731", friend_offline)
hexchat.hook_server("PRIVMSG", channel_msg)
print("Loaded " + __module_name__ + " v" + __module_version__)
