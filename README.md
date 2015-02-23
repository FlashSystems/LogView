# LogView
Logfile viewer and highlighter for Sublime Text 3.

# Requirements
This plug-in requires at least Sublime Text 3 Build 3065. Please download the correct sublime text version before using this plug-in.

# Supported file extensions
All files using the extension .log are automatically opened as logfiles. Any other file can be treated as a logfile by changing the syntax to "Logfile".

# Functionality
This Sublime Text 3 plug-in automates some common tasks when opening logfiles:
- Automatically makes the file readonly to prevent accidental changes.
- Search for common patterns and highlight them.
- Set bookmarks on the highlighted lines to speed up inspection of the matches.

# Automatic highlighting
The LogView plug-in distinguishes three types of log entries:
- errors
- warnings
- marks

It is possible to set a regular expression for detecting every type of log entry via the config file. If a file is loaded (or the file type is changed to "Logfile") it is automatically processed and all lines, that contain matches to the configured regular expressions are automatically highlighted and bookmarked. This way it is possible to analyse logfiles much faster and find the relevant portions with the "goto bookmark" (F2) functionality. The line highlighting feature makes it possible to spot critical areas in the logfile via the Minimap. Areas with a high density of red or yellow marks may hint at a problem.

The "error_filter", "warning_filter" and "mark_filer" regular expressions contain sensible defaults. None the less you should tweak them according match the logfiles you're frequently dealing with.

# Configuration parameters
| Parameter              | Default                         | Description |
| :--------------------- | :------------------------------ | :---------- |
| error_filter           | error\|fail\|exception          | All lines containing a match for this regular expression are marked with the scope defined by the error_scope setting and bookmarked. |
| error_scope            | invalid                         | Scope used for marking lines containing a match of the error_filter regular expression. |
| error_status_caption   | Errors                          | Prefix for the number of lines containing a match of the error_filter regular expression. This can be used for I18N. |
| warning_filter         | warning\|not found\||[^\w]defer | All lines containing a match for this regular expression are marked with the scope defined by the warning_scope setting and bookmarked. |
| warning_scope          | markup.changed                  | Scope used for marking lines containing a match of the warning_filter regular expression. |
| warning_status_caption | Warnings                        | Prefix for the number of lines containing a match of the warning_filter regular expression. This can be used for I18N. |
| mark_filter            | [^\w](start\|quit\|end\|shut(ing)* down)[^\w] | All lines containing a match for this regular expression are marked with the scope defined by the mark_scope setting and bookmarked. |
| mark_scope             | markup.inserted                 | Scope used for marking lines containing a match of the mark_filter regular expression. |
| mark_status_caption    | Marks                           | Prefix for the number of lines containing a match of the mark_filter regular expression. This can be used for I18N. |

All configuration parameters can be set via the Preferences menu. Just open Preferences > Package Settings > Log View > Settings - User. To have a look at the default settings use the "Settings - Default" menu option.

# Editing the logfile
You have to switch to the "Plain Text" syntax in order to edit the opened logfile. As soon as you're done editing the file you can switch back to the "Logfile" syntax.