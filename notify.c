#include "hexchat-plugin.h"
#include <libnotify/notify.h>
#include <string.h>

#define PNAME "hxnotify"
#define PDESC "libnotify notifactions for Hexchat"
#define PVERSION "0.1"

// plugin handle
static hexchat_plugin *ph;

// util functions
static char*
get_username(char* str)
{
	char* ptr = strchr(str, '!');
	*ptr = '\0'; // ditry trick to use already allocated memory

	// Move past the ':' if it at the start of the name
	if (*str == ':')
	{
		str++;
	}

	return str;
}

// hook functions
static int
friend_joined_cb (char *word[], char *word_eol[], void *user_data)
{
	hexchat_printf(ph, "%s friend notify\n", word_eol[1]);

	NotifyNotification* Hello = notify_notification_new("Friend Online",
			get_username(word[4]),
			"hexchat");
	notify_notification_show(Hello, NULL);
	g_object_unref(G_OBJECT(Hello));

	return 1;
}

int hexchat_plugin_init(
		hexchat_plugin* plugin_handle,
		char** plugin_name,
		char** plugin_desc,
		char** plugin_version,
		char*  arg)
{
	// init libnotify
	notify_init ("hexchat");

	// we need to save this for use with any hexchat_* functions
	ph = plugin_handle;

	// tell HexChat our info
	*plugin_name = PNAME;
	*plugin_desc = PDESC;
	*plugin_version = PVERSION;
	hexchat_printf(ph, "%s plugin loaded successfully!\n", PNAME);

	// hooks
	hexchat_hook_server (ph, "730", HEXCHAT_PRI_NORM, friend_joined_cb, NULL);

	// 1 for success
	return 1;
}

int hexchat_plugin_deinit()
{
	// clean up libnotify
	notify_uninit();
	return 1;
}


