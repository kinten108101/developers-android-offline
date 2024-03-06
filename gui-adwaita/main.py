#!/usr/bin/env python

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("WebKit", "6.0")
from gi.repository import Gtk, Adw, Gio, WebKit

webview_settings = WebKit.Settings()
webview_settings.set_enable_write_console_messages_to_stdout(True)
webview_settings.set_allow_top_navigation_to_data_urls(False)
webview_settings.set_allow_universal_access_from_file_urls(False)
webview_settings.set_enable_back_forward_navigation_gestures(False)
# TODO(kinten): Disable this in production builds.
webview_settings.set_enable_developer_extras(True)
webview = WebKit.WebView(settings = webview_settings)
application = None


def load_style(path):
	global webview
	file = open(path, "r")
	content_str = file.read()
	stylesheet = WebKit.UserStyleSheet(
		content_str,
		WebKit.UserContentInjectedFrames.ALL_FRAMES,
	    WebKit.UserScriptInjectionTime.START,
	    None,
	    None
	)
	webview.get_user_content_manager().add_style_sheet(stylesheet)
	file.close()


def load_script(path):
	global webview
	file = open(path, "r")
	content_str = file.read()
	script = WebKit.UserScript(
		content_str,
		WebKit.UserContentInjectedFrames.ALL_FRAMES,
	    WebKit.UserScriptInjectionTime.START,
	    None,
	    None
	)
	webview.get_user_content_manager().add_script(script)
	file.close()


def on_window_close_request(obj):
	application.quit()
	return True


def on_application_run(obj):
	global webview
	
	window = Adw.ApplicationWindow()
	window.set_default_size(1500, 800)
	window.set_application(obj)
	window.set_hide_on_close(True)
	
	overlayer = Gtk.Overlay()
	view = Adw.ToolbarView()
	view.set_content(webview)
	overlayer.set_child(view)
	
	headerbar = Adw.HeaderBar()
	headerbar.set_valign(Gtk.Align.START)
	headerbar.set_halign(Gtk.Align.END)
	headerbar.set_size_request(300, -1)
	# Disable title text for now
	headerbar.set_title_widget(Gtk.Label())
	headerbar.add_css_class("flat")
	overlayer.add_overlay(headerbar)
	
	window.set_content(overlayer)
	window.connect("close-request", on_window_close_request)
	load_script("../left-side-menu.js")
	load_script("../toc.js")
	load_style("../main.css")
	load_style("./main.css")
	# TODO(kinten): Use archivebox api to retrieve latest snapshot for a URL
	webview.load_uri("file:///home/kinten/Web%20Archives/Android%20Developers/archive/1709582819.259706/singlefile.html")
	window.present()


def main():
	global application
	# FIXME(kinten): The website doesn't have a light theme except at code blocks. And flat headerbar title buttons f up in dark mode for some reasons. So we will disable dark mode entirely
	Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
	application = Adw.Application()
	application.connect("activate", on_application_run)
	return application.run()


if __name__ == "__main__":
    main()

