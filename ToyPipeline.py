import time
from LoggerApp import LoggerApp
import sys

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'tui':
        logger = LoggerApp(['epoch','loss'],train)
        logger.run(inline=False)
    else:
        train(TerminalLogger())

class TerminalLogger:
    def logval(self,key,x,y):
        print(key,y)

def train(logger):
    epoch = 1
    while epoch <= 50:
        loss = 100/epoch
        logger.logval('epoch',epoch,epoch)
        logger.logval('loss',epoch,loss)
        time.sleep(1)
        epoch += 1

if __name__ == '__main__':
    main()
