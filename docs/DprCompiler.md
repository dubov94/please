# Installing DelphiMini compiler under Windows #

1. Download DelphiMini.rar

2. Unrar it somewhere (path to the unpacked folder shouldn't contain spaces). It's recommended to unrar it into C:\DelphiMini and proceed to step 4.

3. If you've unrared it into `[DelphiMini_dir]`, that is not 'C:\DelphiMini' open `[DelphiMini_dir]`\dcc32.cfg and fix second line to the real path
`[DelphiMini_dir]`, where you've unrared DelphiMini.rar in step 2.

4. Add to the Path variable `[DelphiMini_dir]`: open command-line and enter 'set PATH=%PATH%;`[DelphiMini_dir]`'.

5. Check that everyting's ok entering dcc32 --version in command-line. If you've done well, it'll show you the version of installed compiler.