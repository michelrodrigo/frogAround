import sys, subprocess

dependencies = ['arcade==1.3.7', 'pyglet==1.3.2']
subprocess.call([sys.executable, '-m', 'pip', 'install'] + dependencies)

    


