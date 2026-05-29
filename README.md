# UMBC COMP 101 Discord Server Bot
## Overview
This is a custom Discord server admin bot using discord.py to automate a lot of the tasks needed for a new semester in the COMP 101 class discord. Some of the features includes
- Automation of wiping and resetting semester needed text channels
- Giving roles to new students joining the Discord server
- Moving students finished with the course to the Alumni role
- Bot logs on all actions taken by the bot to maintain non-repudiation
## Commands
!wipe <#channel>
- Clears a specified discord text channel. It does this by cloning it and deleting the old one, leaving a fresh channel with the same RBAC settings it had previously
- Logs changes to bot logs  
  
!wipehere
- Similar to the above, but it clears the channel of which the command is used in  
  
!wipegroups
- Clears all channels that begin with "group-". Used mainly to clear out the student group channels at the end of the semester
- Logs changes to bot logs  
  
!verify @user <Name_With_Underscores> <\Section>
Verifies the @user by:
- Giving them the Student role
- Giving them a section specific role
- Changing their server nickname to the one on the roster
- Logs changes to bot logs
Example:
```
!verify @Joeisjack John_Doe 21
```
Would give the discord user @Joeisjack the nickname "John Doe" the Student role and the Collaboration role (Section 21).  
  
!updatealumni
- Moves all users with the Student role to the Alumni role
In total, this command will go over everyone with the Student Role, remove all roles (including group, section, and student roles), and give them the Alumni role
  
!woof
- Used to ping bot
- Returns "Woof!"
