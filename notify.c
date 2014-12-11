#include "hexchat-plugin.h"
#include <libnotify/notify.h>

#include <stdlib.h>
#include <string.h>

#define PNAME "hxnotify"
#define PDESC "libnotify notifications for Hexchat"
#define PVERSION "0.1"

//TODO: Support multiple "friends" coming online at once (e.g on-start up)
//TODO: support channel specific notifications of messages

// plugin handle
static hexchat_plugin *ph;

// util functions
//Assumes src is pointing at the start of the name
int get_username_length(char* src)
{
	int len;
	char* itr;

	len = 0;
	itr = src;

	while (*itr != '!' && *itr != '\0') {
		len++;
		itr++;
	}
	return len;
}

// hook functions
	static int
friend_online_cb (char* word[], char* word_eol[], void *user_data)
{
	char* friend = strtok(++(word[4]), ","); // pass starting ':'
	while (friend != NULL) {
		// TODO: have multiple friends in one message?
		int nameln = get_username_length(friend);
		char* msg;
		size_t msg_len = (nameln + 11) * sizeof(char);
		msg = malloc(msg_len);
		memset(msg, '\0', msg_len); //Clean memory

		strncat(msg, friend, nameln);
		strncat(msg, " is online\0", 11);

		NotifyNotification* notify = notify_notification_new("Friend Online"
				,msg
				,"hexchat");

		// FREEDOM!
		notify_notification_show(notify, NULL);
		g_object_unref(G_OBJECT(notify));
		free(msg);

		friend = strtok(NULL, ",");
	}
	return HEXCHAT_EAT_NONE;
}

// TODO: Only show notifications if the friend was already online
	static int
friend_offline_cb (char* word[], char* word_eol[], void* user_data)
{
	char* friend = strtok(word[4], ",");
	while (friend != NULL) {
		int nameln = get_username_length(friend);
		char* msg;
		size_t msg_len = (nameln + 11) * sizeof(char);
		msg = malloc(msg_len);
		memset(msg, '\0', msg_len); //Clean memory

		strncat(msg, friend, nameln);
		strcat(msg, " is offline.\0");

		NotifyNotification* notify = notify_notification_new("Friend Offline"
				,msg
				,"hexchat");

		notify_notification_show(notify, NULL);
		g_object_unref(G_OBJECT(notify));
		free(msg);

		friend = strtok(NULL, ",");
	}

	return HEXCHAT_EAT_NONE;
}

	static int
notifcation_test(char* word[], char* word_eol[], void* user_data)
{
	hexchat_printf(ph, "Start of Test\n");
	char* friend = "friend"; // strtok(word[0], ","); // pass starting ':'
	hexchat_printf(ph, "Post strtok\n");
	// TODO: have multiple friends in one message?

	int nameln = get_username_length(friend);
	hexchat_printf(ph, "Post get_username_length\n");

	char* msg;
	size_t msg_len = (nameln + 11) * sizeof(char);
	msg = malloc(msg_len);
	memset(msg, '\0', msg_len); //Clean memory

	hexchat_printf(ph, "Post malloc\n");

	strcat(msg, friend);
	hexchat_printf(ph, "msg: %s\n", msg);

	strncat(msg, " is online\0", 11);
	hexchat_printf(ph, "msg: %s\n", msg);

	NotifyNotification* notify = notify_notification_new("Friend Online"
			,msg
			,"hexchat");

	// FREEDOM!
	notify_notification_show(notify, NULL);
	g_object_unref(G_OBJECT(notify));
	free(msg);

	return HEXCHAT_EAT_ALL;
}

	int
hexchat_plugin_init(
		hexchat_plugin* plugin_handle,
		char** plugin_name,
		char** plugin_desc,
		char** plugin_version,
		char*  arg)
{
	// init libnotify
	notify_init("hexchat");

	// we need to save this for use with any hexchat_* functions
	ph = plugin_handle;

	// tell HexChat our info
	*plugin_name = PNAME;
	*plugin_desc = PDESC;
	*plugin_version = PVERSION;
	hexchat_printf(ph, "%s plugin loaded\n", PNAME);

	// hooks
	hexchat_hook_server (ph, "730", HEXCHAT_PRI_NORM, friend_online_cb, NULL);
	//hexchat_hook_server (ph, "731", HEXCHAT_PRI_NORM, friend_offline_cb, NULL);

	//commands
	hexchat_hook_command(ph, "NotifyTest", HEXCHAT_PRI_NORM, notifcation_test, "", 0);
	// 1 for success
	return 1;
}

	int
hexchat_plugin_deinit()
{
	// clean up libnotify
	notify_uninit();
	return 1;
}
