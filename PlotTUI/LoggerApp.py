import threading
from textual.app import App
from textual.widgets import Footer, Header
from textual_plotext import PlotextPlot
from textual.containers import VerticalScroll
import numpy as np

def visualize(keys,daemon=True):
    def wrapper(func):
        def run():
            LoggerApp(keys,func,daemon).run()
        return run
    return wrapper 

class LoggerApp(App):
    CSS = """
    VerticalScroll {
        scrollbar-color: cyan;
    } 

    UpdatingPlot {
        height: 40;
    }

    ImgQueue {
        height: 30;
        width: 60;
    }
    """


    def __init__(self,keys,func,daemon=True):
        super().__init__()
        self.title = 'PlotTUI'
        self.t = threading.Thread(target=func, kwargs={'logger':self}, daemon=daemon)
        self.keys = keys

    def compose(self):
        yield Header()
        yield VerticalScroll(*tuple([self.get_plot(key) for key in self.keys]))
        yield Footer()

    def get_plot(self,key):
        if type(key) == tuple:
            if key[1] in (float,int):
                return UpdatingPlot(key[0])
            elif key[1] == 'img':
                return ImgQueue(key[0])
            else:
                pass
        else:
            return UpdatingPlot(key)
    
    def on_ready(self):
        self.t.start()
    
    def logval(self,key,x,y):
        try:
            self.query_one('#'+key,UpdatingPlot).update(x,y) 
        except:
            #wandb.log({key,x}) 
            pass 

    def logimg(self,key,img): 
        try:
            self.query_one('#'+key,ImgQueue).update(img) 
        except:
            #wandb.log({key,x}) 
            pass 

    def on_exit():
        try:
            self.t.join()
        except:
            pass

class UpdatingPlot(PlotextPlot):
    def __init__(self,title):
        super().__init__()
        self.id = title
        self._title = title
        self._x = []
        self._y = []

    def on_mount(self):
        self.plt.title(self._title)
        self.plt.axis_margins = 4

    def update(self,x,y):
        self._x.append(x)
        self._y.append(y)
        self.plt.xticks([min(self._x),max(self._x)])
        self.plt.yticks([min(self._y),max(self._y)])
        self.plt.clear_data()
        self.plt.plot(self._x,self._y,marker='dot')
        self.refresh()

class ImgQueue(PlotextPlot):
    def __init__(self,title):
        super().__init__()
        self.id = title
        self._title = title
        self.imgs = []

    def on_mount(self):
        self.plt.title(self._title)
        self.plt.plot_size(10,20)

    def update(self,img_path): 
        self.plt.image_plot(img_path,fast=True)
