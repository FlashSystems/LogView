import sublime, sublime_plugin
import threading
import unicodedata

class StatusAnimation:
	animation = [ "...  ", " ... ", "  ...", " ... "]

	animationPos = 0
	stopFlag = False
	view = None
	key = None
	updateLock = threading.RLock()

	def updateAnimation(self):
		if (self.stopFlag):
			self.view = None
			self.key = None
		else:
			with self.updateLock:
				if (self.stopFlag == False):
					self.view.set_status(self.key, self.prefix + self.animation[self.animationPos])
			self.animationPos += 1
			if (self.animationPos >= len(self.animation)): self.animationPos = 0
			sublime.set_timeout(self.updateAnimation, 500)

	def start(self, view, prefix, delay, key):
		# Show the first animation step and wait for the given time before starting the animation
		view.set_status(key, prefix + self.animation[0])

		self.animationPos = 1
		self.stopFlag = False
		self.view = view
		self.key = key
		self.prefix = prefix
		sublime.set_timeout(self.updateAnimation, delay)

	def stop(self):
		with self.updateLock:
			self.stopFlag = True
			self.view.erase_status(self.key)

class EventListener(sublime_plugin.EventListener):
	def highlight(self, view, regex, regionName, scope):
		if (regex == "") or (regex == None):
			return []

		foundRegions = view.find_all(regex, sublime.IGNORECASE, None, None)
		numFoundRegions = len(foundRegions)

		if (numFoundRegions > 0):
			# Expand all regions to match the whole line and mark the line with the given scpe
			for i in range(0, numFoundRegions):
				foundRegions[i] = view.expand_by_class(foundRegions[i], sublime.CLASS_LINE_START | sublime.CLASS_LINE_END)
			view.add_regions(regionName, foundRegions, scope, "", sublime.DRAW_NO_FILL);

		return foundRegions

	def markupView(self, view, statusAnimation):
		settings = sublime.load_settings("logview.sublime-settings")

		errorRegex = settings.get("error_filter", "error|fail|exception")
		errorScope = settings.get("error_scope", "invalid")
		errorStatusCaption = settings.get("error_status_caption", "Errors")
		warningRegex = settings.get("warning_filter", "warning|not found|[^\w]defer")
		warningScope = settings.get("warning_scope", "markup.changed")
		warningStatusCaption = settings.get("warning_status_caption", "Warnings")
		markRegex = settings.get("mark_filter", "[^\w](start|quit|end|shut(ing)* down)[^\w]")
		markScope = settings.get("mark_scope", "markup.inserted")
		markStatusCaption = settings.get("mark_status_caption", "Marks")

		foundRegions = self.highlight(view, errorRegex, "logfile.errors", errorScope)
		view.set_status("logview.0", errorStatusCaption + " " + str(len(foundRegions)))
		bookmarks = foundRegions
		foundRegions = self.highlight(view, warningRegex, "logfile.warnings", warningScope)
		view.set_status("logview.1", warningStatusCaption + " " + str(len(foundRegions)))
		bookmarks += foundRegions
		foundRegions = self.highlight(view, markRegex, "logfile.marks", markScope)
		view.set_status("logview.2", markStatusCaption + " " + str(len(foundRegions)))
		bookmarks += foundRegions
		del foundRegions

		# Set a bookmark for each region
		view.add_regions("bookmarks", bookmarks, "bookmarks", "bookmark", sublime.HIDDEN);
		del bookmarks

		# Stop the animation
		statusAnimation.stop()
		statusAnimation = None

		# Set the final message
		sublime.status_message("")

	# Called to prepare the view:
	# Makes it read only and applies the highlighting
	def prepareView(self, view):
		view.set_read_only(True)
		view.set_status("logview", "read-only")

		# Set a temporary message
		statusAnimation = StatusAnimation()
		statusAnimation.start(view, "Parsing", 2000, "0")
		#sublime.status_message("Processing log...")

		# Do the markup processing in its own thread.
		threading.Thread(target = self.markupView, daemon = True, args=[view, statusAnimation], kwargs={}).start()

	# Called to remove the preparations from the log file and turn it into a normal view.
	def unprepareView(self, view):
		view.set_read_only(False)
		view.erase_status("logview")
		view.erase_status("logview.0")
		view.erase_status("logview.1")
		view.erase_status("logview.2")
		view.erase_regions("logfile.errors")
		view.erase_regions("logfile.warnings")
		view.erase_regions("logfile.marks")
		view.erase_regions("bookmarks")

	# Called when a file is finished loading.
	def on_load(self, view):
		if (view.settings().get('syntax') == "Packages/LogView/logview.tmLanguage"):
			self.prepareView(view)

	# Called if a text command is executed on the buffer
	def on_text_command(self, view, command_name, args):
		if (command_name == "set_file_type"):
			currentSyntax = view.settings().get('syntax')
			newSyntax = args["syntax"]

			if (newSyntax != currentSyntax):
				if (newSyntax == "Packages/LogView/logview.tmLanguage"):
					# If the new syntax is logview then prepare the view.
					self.prepareView(view)
				else:
					# If the old syntax was logview then remove our preparations
					if (view.settings().get('syntax') == "Packages/LogView/logview.tmLanguage"):
						self.unprepareView(view)

		# Always run the command as is
		return None
