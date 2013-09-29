DIM objShell
set objShell=wscript.createObject("wscript.shell")
iReturn=objShell.Run("Check4SeafileUpdate.exe", 0, FALSE)
