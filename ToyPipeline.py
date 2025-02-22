import time
from LoggerApp import visualize
import sys


@visualize(['epoch','loss','loss2','loss3','loss4','loss5'])
def main(logger=None):
    epoch = 1
    while epoch <= 50:
        loss = 100/epoch
        if logger:
            logger.logval('epoch',epoch,epoch)
            logger.logval('loss',epoch,loss)
            logger.logval('loss2',epoch,loss)
        time.sleep(1)
        epoch += 1

if __name__ == '__main__':
    main()
