###Georadar Diffraction Picking - GDPy

from tkinter import *
from tkinter import filedialog, messagebox
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
import os                                                                              
import numpy as np
import sys
import warnings
import platform
import siina

root = Tk()

class GeoRad(Frame):
    
    def __init__(self, master):
        
        #Variáveis
        self.files = None
        self.frames = []
        self.figs = []
        self.figs_trs = []
        self.axs = []
        self.axs_trs = []
        self.canvas = []
        self.toolbars = []
        self.arts = []
        self.arts_trs = []
        self.trs_connects = []
        self.plots_trs = []
        self.cbars = []
        
        #Frame principal
        Frame.__init__(self, master)
        self.grid(row = 0, column = 0, sticky = NSEW)
        
        #Configuração da janela
        root.config(background='#F3F3F3')
        root.title('GeoRad - v0.0.1')
        root.wm_state('zoomed')
        root.bind('<Alt-s>', lambda x: self.quit())
        root.bind('<Control-a>', lambda x: self.open())
        root.bind('<Left>', lambda x: self.backPage())
        root.bind('<Right>', lambda x: self.nextPage())
        
        #Menus
        menuBar = Menu(root)
        #Menu arquivo
        fileMenu = Menu(menuBar)
        menuBar.add_cascade(label = 'Arquivo', menu = fileMenu)
        fileMenu.add_command(label='Abrir (Ctrl+A)',
                             command=self.open)
        fileMenu.add_separator()
        fileMenu.add_command(label='Sair (Alt+S)',
                             command=self.quit)
        #Menu editor
        procMenu = Menu(menuBar)
        menuBar.add_cascade(label='Processamento',menu=procMenu)
        procMenu.add_command(label='Ganho (Ctrl + ->)',
                             command=self.nextPage)#aqui
        #Menu visualização
        viewMenu = Menu(menuBar)
        menuBar.add_cascade(label='Visualizaçao',menu=viewMenu)
        viewMenu.add_command(label='Proximo (->)',
                             command=self.nextPage)#aqui
        viewMenu.add_command(label='Anterior (<-)',
                             command=self.backPage)#aqui
        viewMenu.add_separator()
        viewMenu.add_command(label='Picking (on/off)',
                             command = self.picking)
        viewMenu.add_separator()
        viewMenu.add_command(label='Mapa de cores: Greys',
                             command = self.cMap1)

        viewMenu.add_command(label='Mapa de cores: Summer',
                             command = self.cMap2)
        viewMenu.add_command(label='Mapa de cores: Cool',
                             command = self.cMap3)
        viewMenu.add_command(label='Mapa de cores: PiYG',
                             command = self.cMap4)
        viewMenu.add_command(label='Mapa de cores: bwr_r',
                             command = self.cMap5)
        viewMenu.add_command(label='Mapa de cores: PRGn',
                             command = self.cMap6)
        viewMenu.add_command(label='Mapa de cores: PuOr',
                             command = self.cMap7)
        
        viewMenu.add_separator()
        viewMenu.add_command(label='Traços (Ctrl+T)',
                             command=self.view_traces)#aqui
        #Menu ajuda
        helpMenu = Menu(menuBar)
        menuBar.add_cascade(label='Ajuda',menu=helpMenu)
        helpMenu.add_command(label='Atalhos de teclado',command = lambda: print(''))
        #Ativar menus na janela
        root.configure(menu=menuBar)

        #Imagens
        self.img_open = PhotoImage(file="%s/images/img_open.gif"%os.getcwd())
        self.img_back = PhotoImage(file="%s/images/img_back.gif"%os.getcwd())
        self.img_next = PhotoImage(file="%s/images/img_next.gif"%os.getcwd())
        self.img_cmap1 = PhotoImage(file="%s/images/img_cmap1.gif"%os.getcwd())
        self.img_cmap2 = PhotoImage(file="%s/images/img_cmap2.gif"%os.getcwd())
        self.img_cmap3 = PhotoImage(file="%s/images/img_cmap3.gif"%os.getcwd())
        self.img_cmap4 = PhotoImage(file="%s/images/img_cmap4.gif"%os.getcwd())
        self.img_cmap5 = PhotoImage(file="%s/images/img_cmap5.gif"%os.getcwd())
        self.img_cmap6 = PhotoImage(file="%s/images/img_cmap6.gif"%os.getcwd())
        self.img_cmap7 = PhotoImage(file="%s/images/img_cmap7.gif"%os.getcwd())
        self.img_picking = PhotoImage(file="%s/images/img_crosshair.gif"%os.getcwd())

        #Botões
        bt_open = Button(self, command = self.open)
        bt_open.config(image = self.img_open)
        bt_open.grid(row=0,column=0,sticky=W)
        bt_back = Button(self, command = self.backPage)
        bt_back.config(image=self.img_back)
        bt_back.grid(row=0,column=2,sticky=W)
        bt_next = Button(self, command = self.nextPage)
        bt_next.config(image=self.img_next)
        bt_next.grid(row=0,column=3,sticky=W)
        bt_cmap1 = Button(self, command = self.cMap1)
        bt_cmap1.config(image=self.img_cmap1)
        bt_cmap1.grid(row=0,column=4,sticky=W)
        bt_cmap2 = Button(self, command = self.cMap2)
        bt_cmap2.config(image=self.img_cmap2)
        bt_cmap2.grid(row=0,column=5,sticky=W)
        bt_cmap3 = Button(self, command = self.cMap3)
        bt_cmap3.config(image=self.img_cmap3)
        bt_cmap3.grid(row=0,column=6,sticky=W)
        bt_cmap4 = Button(self, command = self.cMap4)
        bt_cmap4.config(image=self.img_cmap4)
        bt_cmap4.grid(row=0,column=7,sticky=W)
        bt_cmap5 = Button(self, command = self.cMap5)
        bt_cmap5.config(image=self.img_cmap5)
        bt_cmap5.grid(row=0,column=8,sticky=W)
        bt_cmap6 = Button(self, command = self.cMap6)
        bt_cmap6.config(image=self.img_cmap6)
        bt_cmap6.grid(row=0,column=9,sticky=W)
        bt_cmap7 = Button(self, command = self.cMap7)
        bt_cmap7.config(image=self.img_cmap7)
        bt_cmap7.grid(row=0,column=10,sticky=W)
        bt_crosshair = Button(self, command = self.picking)
        bt_crosshair.config(image=self.img_crosshair)
        bt_crosshair.grid(row=0,column=11,sticky=W)
        
        #Configuração atalhos matplotlib
        plt.rcParams['keymap.zoom'] = 'z,Z'
        plt.rcParams['keymap.back'] = 'b,B'
        plt.rcParams['keymap.home'] = 'ctrl+z,ctrl+Z'
        plt.rcParams['keymap.save'] = 'ctrl+i,ctrl+I'
        plt.rcParams['keymap.pan'] = 'm,M'

    def quit(self):
        self.destroy()
        root.destroy()
        sys.exit()
        
    def open(self):
        if self.files == None:
            self.files = sorted(filedialog.askopenfilenames(title='Abrir',
                               filetypes=[('GSSI','*.dzt')]))
            if len(self.files) > 0:
                
                for i in range(len(self.files)):
                    radFile = siina.Radar()
                    radFile.read_file(self.files[i])
                    if radFile.header.get('frequency', None) is None:
                        radFile.header['frequency'] = 1e9 # 1 GHz
                    print("points in samples={}, samples={}, channels={}".format(radFile.nrows,
                        radFile.ncols, radFile.nchan))
                    print(radFile.header)
                    radFile.read_markers()
                    #radFile.func_dc(start=500)
                    frame = Frame(root,bg='#F3F3F3')
                    frame.grid(row=1, column=0, sticky = NSEW)
                    self.frames.append(frame)
                    fig = plt.figure(i,figsize=(14,6.2),facecolor='#F3F3F3')
                    self.figs.append(fig)
                    ax = plt.subplot(1,1,1)
                    self.axs.append(ax)
                    img = ax.imshow(radFile.data, aspect='auto', cmap = "Greys", interpolation="nearest")
                    self.arts.append(img)
                    cb = fig.colorbar(img, orientation='vertical', aspect = 50, shrink = .5)
                    self.cbars.append(cb)
                    plt.title('%s'%(os.path.basename(self.files[i])))     
                    plt.xlabel('Distância (m)')
                    plt.ylabel('Tempo (ns)')
                    #plt.xlim((0,float(radFile.ncols)/float(radFile.header['spm'])))
                    #plt.ylim((0,radFile.header['range']))
                    tela = FigureCanvasTkAgg(self.figs[i], self.frames[i])
                    self.canvas.append(tela)
                    self.canvas[i].draw()
                    self.canvas[i].get_tk_widget().pack(fill='both', expand=True)
                    toolbar = NavigationToolbar2Tk(self.canvas[i], self.frames[i])
                    self.toolbars.append(toolbar)
                    self.toolbars[i].update()
                    self.canvas[i]._tkcanvas.pack(fill='both', expand=True)
                    
                self.frames[0].tkraise()
                self.page = 0
                plt.figure(self.page)
                self.plot = True
                

                def do(event):
                    key_press_handler(event, self.canvas[self.page], self.toolbars[self.page])

                self.figs[-1].canvas.mpl_connect('key_press_event', do)

    def ampUp(self):
        if self.plot == True:
            self.arts[self.page].set_array(self.arts[self.page].get_array()*2)
            self.figs[self.page].canvas.draw()

    def picking(self):
        
        def onclick(event):
            try:
                print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                event.x, event.y, event.xdata, event.ydata))
            except:
                pass

        if self.crosshair == False:
            for i in range(len(self.files)):
                cid = self.figs[i].canvas.mpl_connect('button_press_event', onclick)
                self.trs_connects.append(cid)
            self.crosshair = True
            
        else:
            for i in range(len(self.files)):
                self.figs[i].canvas.mpl_disconnect(self.trs_connects[i])
            del self.trs_connects[:]
            self.crosshair = False
        cid = self.figs[i].canvas.mpl_connect('button_press_event', onclick)
    
    def nextPage(self):
        if self.plot == True and self.page < len(self.files)-1:
            frame = self.frames[self.page+1]
            frame.tkraise()
            self.page += 1
            self.canvas[self.page].draw()
            
    def backPage(self):
        if self.plot == True and self.page != 0:
            frame = self.frames[self.page-1]
            frame.tkraise()
            self.page -= 1
            self.canvas[self.page].draw()

    def cMap1(self):    
        if self.plot == True:
            for i in range(len(self.files)):
                self.arts[i].set_cmap("Greys")
                self.figs[i].canvas.draw()

    def cMap2(self):    
        if self.plot == True:
            for i in range(len(self.files)):
                self.arts[i].set_cmap("summer")
                self.figs[i].canvas.draw()

    def cMap3(self):    
        if self.plot == True:
            for i in range(len(self.files)):
                self.arts[i].set_cmap("cool")
                self.figs[i].canvas.draw()

    def cMap4(self):    
        if self.plot == True:
            for i in range(len(self.files)):
                self.arts[i].set_cmap("PiYG")
                self.figs[i].canvas.draw()

    def cMap5(self):    
        if self.plot == True:
            for i in range(len(self.files)):
                self.arts[i].set_cmap("bwr_r")
                self.figs[i].canvas.draw()

    def cMap6(self):    
        if self.plot == True:
            for i in range(len(self.files)):
                self.arts[i].set_cmap("PRGn")
                self.figs[i].canvas.draw()

    def cMap7(self):    
        if self.plot == True:
            for i in range(len(self.files)):
                self.arts[i].set_cmap("PuOr")
                self.figs[i].canvas.draw()
            
    def view_traces(self):
        if self.plot == True:
            self.axs[self.page].cla()
            #plt.xlim(0,len(self.arts[self.page].get_array()[0]))
            k = 40000
            plt.xlim(0,len(self.arts[self.page].get_array()[0]))
            self.cbars[self.page].remove()
            for i in range(len(self.arts[self.page].get_array())):
                self.axs[self.page].plot([j for j in range(len(self.arts[self.page].get_array()[i]))],
                                         [j+k*i*-1 for j in self.arts[self.page].get_array()[i]], c = "black", lw = .3)
                 
            
                #plt.gca().invert_yaxis()
            self.figs[self.page].canvas.draw()
            #self.plots_trs[self.page] = True
            
        elif self.plot == True:
            img = self.axs[self.page].imshow(self.arts[self.page].get_array(), aspect='auto', cmap = "Greys",
                                             interpolation="nearest")
            self.arts[self.page] = img
            
            cb = self.figs[self.page].colorbar(img, orientation='vertical', aspect = 50, shrink = .5)
            
            self.cbars[self.page] = cb
            #self.figs[self.page].colorbar(img, orientation='vertical', aspect = 50, shrink = .5)
            plt.title('%s'%(os.path.basename(self.files[self.page])))     
            plt.xlabel('Número no traço')
            plt.ylabel('Número da amostra')
            self.figs[self.page].canvas.draw()
            #self.plots_trs[self.page] = False
            

warnings.filterwarnings('ignore')
GeoRad(root)
root.mainloop()

















    

