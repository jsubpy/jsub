## Version 0.3
 * Simpler jsubrc file for user.
 * Reworked juno package.
 * On dirac backend, job group reflect user name to avoid conflict.
 * Changed the folder structure of jsub dirs. Now the top layer is <task-id>, and there are logfiles/runtime/taskInfo in the 2nd layer.
 * Changed the behavior of `jsub getlog` command. Now it dump results to <jsub-dir>/<task-id>/logfiles.
