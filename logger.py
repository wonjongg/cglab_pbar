from pip._vendor.rich.progress_bar import ProgressBar
from pip._vendor.rich.console import Console

import time
import termcolor

def toRed(content):
    return termcolor.colored(content,"red",attrs=["bold"])

def toGreen(content):
    return termcolor.colored(content,"green",attrs=["bold"])

def toBlue(content):
    return termcolor.colored(content,"blue",attrs=["bold"])

def toCyan(content):
    return termcolor.colored(content,"cyan",attrs=["bold"])

def toYellow(content):
    return termcolor.colored(content,"yellow",attrs=["bold"])

def toMagenta(content):
    return termcolor.colored(content,"magenta",attrs=["bold"])

def toGrey(content):
    return termcolor.colored(content,"grey",attrs=["bold"])

def toWhite(content):
    return termcolor.colored(content,"white",attrs=["bold"])

class Logger():
        """Renders a progress bar and training log.

        Args:
                max_epoch (int): Total number of training epoch
                max_iteration (int): Number of training iteration per epoch
                pbar_mode (string, optional): Enable pbar rendering. Determine which information will be rendered, 'iteration' or 'epoch'. Defaults to "iteration".
        """
        def __init__(self, max_epoch, max_iter, pbar_mode='iteration', exp_name=None):
            self.exp_name = exp_name
            self.max_epoch = max_epoch
            self.max_iter = max_iter
            self.start_time = time.time()
            self.pbar_mode = pbar_mode
            if self.pbar_mode == 'iteration':
                    self.pbar = ProgressBar(width=50, total=max_iter)
            elif self.pbar_mode == 'epoch':
                    self.pbar = ProgressBar(width=50, total=max_epoch)
            else:
                    self.pbar = None
            self.console = Console()
            self.console.show_cursor(False)
            self.console.file.write('\n')

        def print_log(self, cur_epoch, cur_iter, losses):
            CURSOR_UP_ONE = '\x1b[1A' 
            ERASE_LINE = '\x1b[2K'
            
            if self.pbar_mode == 'iteration':
                self.pbar.update(cur_iter)
            elif self.pbar_mode == 'epoch':
                self.pbar.update(cur_epoch)

            epoch_msg = f'{toWhite("Epoch")} [{toGreen(cur_epoch)}/{toGreen(self.max_epoch)}]: '
            time_msg = f"{time.strftime('%H:%M:%S', time.gmtime(time.time() - self.start_time))}"
            msg = f' [{toBlue(cur_iter)}/{toBlue(self.max_iter)}], {toWhite("Elapsed")}: {toCyan(time_msg)}\n'

            loss_string = ''
            for k, v in losses.items():
                if k == 'total':
                    loss_string = f'{toRed(k)}: {toRed(f"{v:0.4f}")}' + loss_string
                else:
                    loss_string += f', {toMagenta(k)}: {toMagenta(f"{v:0.4f}")}'
            loss_msg = toWhite('[Loss] ') + loss_string

            self.console.file.write(CURSOR_UP_ONE+ERASE_LINE)
            if self.exp_name is not None:
                exp_msg = f'{toYellow("[Experiment]:")} {toWhite(self.exp_name)}\n'
                self.console.file.write(CURSOR_UP_ONE+ERASE_LINE)
                self.console.file.write(exp_msg)
            self.console.file.write(epoch_msg)
            #self.console.file.write(f'{CURSOR_UP_ONE + ERASE_LINE}')
            if self.pbar is not None:
                self.console.print(self.pbar)

            self.console.file.write(msg)
            self.console.file.write(loss_msg)
            self.console.file.write('\r')

        def end(self):
            self.console.show_cursor(True)
            self.console.print()

if __name__ == '__main__':
        logger = Logger(50, 1000, 'iteration')
        loss = {}
        loss['total'] = 0.332323
        loss['mse'] = 0.232323
        loss['percept'] = 0.12312

        for n in range(0, 10):
                for i in range(0, 1000):
                    logger.print_log(n, i, loss)
                    time.sleep(0.5)
