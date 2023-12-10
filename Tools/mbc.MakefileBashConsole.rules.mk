## ©️ 2023 Scale Invariant, Inc.  All rights reserved.
##      Reference: https://www.termsfeed.com/blog/sample-copyright-notices/
##
## Unauthorized copying of this file, via any medium is strictly prohibited
## Proprietary and confidential
##
## Written by Brad Hyslop <bhyslop@scaleinvariant.org> December 2023



MBC-T.MakefileBashConsole-Test.sh:
	$(MBC_SHOW_NORMAL) "Running a test at $(MBC_NOW)"
	$(MBC_PASS) this worked
	$(MBC_SHOW_NORMAL) "Expect fail chatter on next line and no stopping"
	false || $(MBC_FAIL) || echo ignoring error unix status and going on...
	$(MBC_SHOW_NORMAL) "Continuing..."
	$(MBC_PASS) No errors.


MBC-D.MakefileBashConsole-Demo.sh:
	$(MBC_SHOW_NORMAL) "Today is $(MBC_NOW)"
	$(MBC_SHOW_NORMAL) braddy
	$(MBC_SHOW_WHITE)  braddy
	$(MBC_SHOW_RED)    braddy
	$(MBC_SHOW_GREEN)  braddy
	$(MBC_SHOW_NORMAL) braddy divy
	$(MBC_SHOW_WHITE)  braddy divy
	$(MBC_SHOW_RED)    braddy divy
	$(MBC_SHOW_GREEN)  braddy divy
	$(MBC_SHOW_NORMAL) braddy divy asasr
	$(MBC_SHOW_WHITE)  braddy divy asasr
	$(MBC_SHOW_RED)    braddy divy asasr
	$(MBC_SHOW_GREEN)  braddy divy asasr
	@echo
	$(MBC_PASS) No errors.


# EOF
