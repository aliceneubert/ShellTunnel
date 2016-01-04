# ShellTunnel
Allows remote shell access to a computer without needing port forwards to it. Requires a computer somewhere with accessible inbound ports.

Purpose:
I have computers at my house I'd like to access. I do not have access to port forwarding with my current ISP. Therefore I must control these computers using only outbound connections, leading me to this solution.

# intel.py
To be run on the computer with accessible inbound ports. Takes commands from commander.py to send to solder.py. Will continue running until killed with ctrl+c, so I suggest running it like this:

python intel.py & disown

Which will run it and disown it from the shell. Remember to start it again the next time you boot.

PLEASE NOTE THAT THIS IS NOT GUARANTEED TO BE SECURE AND I HAVE NOT YET IMPLEMENTED ENCRYPTION. ANYONE LISTENING CAN SEE THE COMMANDS YOU SEND TO THE SOLDIER.

# soldier.py
Executes shell commands. Works exactly as a "sh" shell except for the cd command, which uses the os.chdir python command so that it can persist between commands.

# commander.py
A command-line style interface for passing shell commands to the soldier. There are a few dedicated commands for intel as well. Designed to be run on the same computer as intel.py, but can be used remotely with a port forward on intel and a line or two of changes.

list or queue
Returns the command queue stored by intel.
size
Returns the size of the command queue.
[0-99]
Returns the command in the queue at the given index.
