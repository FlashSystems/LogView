# LogView
Logfile highlighter for Sublime Text 3.

![ScreenShot](https://raw.github.com/FlashSystems/LogView/master/README/LogViewScreen.png)

## Requirements
This plug-in requires at least Sublime Text 3 Build 3065. Please download the correct sublime text version before using this plug-in.

## Functionality
This Sublime Text 3 plug-in automates some common tasks when opening logfiles:
- Automatically makes the file read-only to prevent accidental changes.
- Search for common patterns and highlight them (see chapter "Automatic highlighting")
- Set bookmarks on the highlighted lines to speed up inspection of the matches.

## Supported file extensions
All files using the extension .log are automatically opened as logfiles. Any other file can be treated as a logfile by changing the syntax to "Logfile".

## Installation

This package should be installed using Package Control. Follow these steps to install LogView:
- Make sure you're using the correct Sublime Text 3 version (see Requirements).
- Install [Package Control](https://sublime.wbond.net/installation) if you don't already have it.
- [Use Package Control](https://sublime.wbond.net/docs/usage) to search for LogView and install the package.

## Editing the logfile
You have to switch to the "Plain Text" syntax in order to edit the opened logfile. As soon as you're done editing the file, you can switch back to the "Logfile" syntax. The file will automatically be parsed again and set to read-only.

## Automatic highlighting
The LogView plug-in distinguishes three types of log entries:
- errors
- warnings
- marks

Matching lines are marked with an icon within the gutter, too. If you only want the lines to have icons and no other hilighting should be performed set the `highlight_style` parameter within the config file to `none`.

It is possible to set a regular expression for detecting every type of log entry within the configuration file. If a file is loaded (or the file type is changed to "Logfile") it is automatically processed and all lines, that contain matches to the configured regular expressions are automatically highlighted and bookmarked. This way it is possible to analyse logfiles much faster and find the relevant portions with the "goto bookmark" (<kbd>F2</kbd>) functionality. The line highlighting feature shows the critical areas in the logfile via the Minimap. Portions of the logfile with a high density of red or yellow marks may hint at a problem.

If more than one regular expression matches for a given line of the logfile all matches are counted. For highlighting the line the error_filter takes precedence over the warning_filter and the warning_filter takes precedence over the mark_filter.

The "error_filter", "warning_filter" and "mark_filer" regular expressions contain sensible defaults. None the less you should tweak them to match the logfiles you're frequently dealing with.

# Configuration parameters
| Parameter              | Default                        | Description |
| :--------------------- | :----------------------------- | :---------- |
| error_filter           | `error\|fail\|exception`         | All lines containing a match for this regular expression are marked with the scope defined by the error_scope setting and bookmarked. |
| error_scope            | `markup.deleted`                      | Scope used for marking lines containing a match of the error_filter regular expression. |
| error_status_caption   | `Errors`                       | Prefix for the number of lines containing a match of the error_filter regular expression. This can be used for I18N. |
| warning_filter         | `warning\|not found\|[^\w]defer` | All lines containing a match for this regular expression are marked with the scope defined by the warning_scope setting and bookmarked. |
| warning_scope          | `markup.changed`               | Scope used for marking lines containing a match of the warning_filter regular expression. |
| warning_status_caption | `Warnings`                     | Prefix for the number of lines containing a match of the warning_filter regular expression. This can be used for I18N. |
| mark_filter            | `[^\w](start\|quit\|end\|shut(ing)* down)[^\w]` | All lines containing a match for this regular expression are marked with the scope defined by the mark_scope setting and bookmarked. |
| mark_scope             | `markup.inserted`                 | Scope used for marking lines containing a match of the mark_filter regular expression. |
| mark_status_caption    | `Marks`                           | Prefix for the number of lines containing a match of the mark_filter regular expression. This can be used for I18N. |
| auto_match_words       | `true`                       | 	If this config option is set to true the reguluar expression set via `error_filter`, `warning_filter` and `mark_filter` is automatically extended to only match whole words. If you want to use the regular expressions as they are specified, set this value to false. |
| highlight_style        | `underline`  | Configures the style for marking the lines selected by the filters. Available styles are: fill, outline, underline and none. See default config for details. |

All configuration parameters can be set via the Preferences menu. Just open Preferences > Package Settings > Log View > Settings - User. To have a look at the default settings use the "Settings - Default" menu option.
