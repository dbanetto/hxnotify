#!/usr/bin/env python3
import hexchat

__module_name__ = "hxnotify"
__module_version__ = "0.5.1"
__module_description__ = "Python module to display tray notifications"

MESSAGE_LIMIT = 160

blink_tray = 1 << 9
blink_task_bar = 1 << 10


def get_usrname(name):
    return name[1 if name[0] == ':' else 0:name.index('!')]


def friend_online(word, word_eol, userdata):
    for name in word[3][1:].split(','):
        notification("Friend Online",
                     "{0} has is online".format(name))
    return None


def friend_offline(word, word_eol, userdata):
    names = word[3][1:].split(',')
    for i in hexchat.get_list("notify"):
        if i.nick in names and i.on != 0:
            notification("Friend Offline",
                         "{0} has gone offline".format(name))

    return None


def channel_msg(word, word_eol, userdata):
    # only show when not focused on hexchat
    # if hexchat.get_info("win_status") == "active":
    #     return None

    # get the channel info for where the message came from
    for ch in hexchat.get_list("channels"):
        # handle only channel
        if ch.type != 2:
            continue

        whitelist = hexchat.get_pluginpref('hxnotify_whitelist').split(',')

        # only show for whitelisted channels
        if word[2] in whitelist:

            # check if the chanopt is set
            if bool(ch.flags & blink_tray):
                my_nick = hexchat.get_info('nick')
                from_user = get_usrname(word[0])

                # fix getting notifcations from self when
                # a bouncer playback is running
                if hexchat.nickcmp(from_user, my_nick) != 0:
                    header = "Message ({0}/{1})".format(ch.network, ch.channel)
                    body = "{0}: {1}".format(from_user,
                                             hexchat.strip(word_eol[3][1:],
                                                           MESSAGE_LIMIT, 3))
                    # send the notification
                    notification(header, body)

            return None

    return None


def notification(header, body):
    hexchat.command('tray -b "{0}" {1}'.format(header, body))


HXNOTIFY_HELP = """/hxnotify - configuration control for hxnotify plugin
Commands
/hxnotify add (#channel) - adds channel(s) to whitelist of channels to notify on, defaults to current channel
/hxnotify rm (#channel)  - removes channel(s) from whitelist of channels to notify on, defaults to current channel
/hxnotify list - lists channels in whitelist
/hxnotify test - sends test notification
"""

def hxnotify_cb(word, word_eol, userdata):
    if len(word) < 2:
        print('No arguments passed')
        print(HXNOTIFY_HELP)

    cmd = word[1]

    if cmd == 'add':
        hxnotify_add(word)
    elif cmd == 'rm':
        hxnotify_rm(word)
    elif cmd == 'list':
        whitelist = get_whitelist()

        if len(whitelist) < 1:
            print("No channels whitelisted")
        else:
            print("whitelisted channels: {0}"
                  .format(str.join(', ', whitelist)))
    elif cmd == 'test':
        notification('Test', 'testing, 1, 2, 3')

    return hexchat.EAT_ALL


def hxnotify_add(word):
    if len(word) < 3:
        channels = [hexchat.get_info('channel')]
    else:
        channels = word[2:]

    whitelist = get_whitelist()

    for channel in channels:
        if channel in whitelist:
            print('{0} is already whitelisted'.format(channel))
            continue

        whitelist.append(channel)
        print('{0} has been added to the whitelisted'.format(channel))

    set_whitelist(whitelist)


def hxnotify_rm(word):
    if len(word) < 3:
        channels = [hexchat.get_info('channel')]
    else:
        channels = word[2:]

    for channel in channels:
        whitelist = get_whitelist()

        if channel not in whitelist:
            print('{0} is not whitelisted'.format(channel))
            continue

        whitelist.remove(channel)
        print('{0} has been removed from the whitelist'.format(channel))

    set_whitelist(whitelist)


def get_whitelist():
    whitelist = hexchat.get_pluginpref('hxnotify_whitelist')

    # ensure we got something back
    if whitelist is None:
        return []

    # remove blanks
    return [w for w in whitelist.split(',') if w.strip()]


def set_whitelist(whitelist):
    # remove blanks
    whitelist = [w for w in whitelist if w.strip()]
    hexchat.set_pluginpref('hxnotify_whitelist', str.join(',', whitelist))

hexchat.hook_command("hxnotify", hxnotify_cb, help=HXNOTIFY_HELP)
hexchat.hook_server("730", friend_online)
hexchat.hook_server("731", friend_offline)
hexchat.hook_server("PRIVMSG", channel_msg)
print("Loaded " + __module_name__ + " v" + __module_version__)
