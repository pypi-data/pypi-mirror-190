import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class FHcolors:
    def __init__(self):
        self.green1=np.array([23,156,125,255])/255
        self.green2=np.array([178,210,53,255])/255
        self.orange1=np.array([245,130,32,255])/255
        self.blue1=np.array([0,91,127,255])/255
        self.blue2=np.array([0,133,152,255])/255
        self.blue3=np.array([57,193,205,255])/255
        self.blue4=np.array([28,63,82,255])/255
        self.blue5=np.array([229,238,242,255])/255
        self.grey1=np.array([166,187,200,255])/255

class FHcmap:
    def __init__(self):
        self.BlackToGreen = self.create_cmap([[0,0,0,1],colors.green1])
        self.BlackToBlue = self.create_cmap([[0,0,0,1],colors.blue1])
        self.WhiteToGreen = self.create_cmap([[1,1,1,1],colors.green1])
        self.BlueToWhite = self.create_cmap([colors.blue1,[1,1,1,1]])
        self.GreenToWhite = self.create_cmap([colors.green1,[1,1,1,1]])
        self.OrangeToGreen = self.create_cmap([colors.orange1,colors.green1])
        self.GreenToOrange = self.create_cmap([colors.green1, colors.orange1])
        self.BlueToGreen = self.create_cmap([colors.blue1, colors.green1])
        self.BlueToBlue = self.create_cmap([colors.blue1, colors.blue3])
        self.BlueToBlue_dark = self.create_cmap([self.BlackToBlue(100),colors.blue1, colors.blue3],[0,100,255])
        self.BlueToBlueToBlue = self.create_cmap([colors.blue4, colors.blue1, colors.blue3,colors.blue5],[0,25,135,255])
        self.BlueToBlueToBlue_dark = self.create_cmap([self.BlackToBlue(100), colors.blue1, colors.blue3,colors.blue5],[0,60,155,255])
        self.BlackToGreenToOrangeToWhite = self.create_cmap([[0,0,0,1],colors.green1,colors.orange1,[1,1,1,1]])
        self.BlackToGreenToWhite = self.create_cmap([[0,0,0,1],colors.green1,[1,1,1,1]],[0,100,255])
        self.BlackToGreenToWhite_short = self.create_cmap([self.BlackToGreenToWhite(50),colors.green1,self.BlackToGreenToWhite(200)],[0,85,255])
        self.colors=ListedColormap(np.vstack([colors.green1,colors.blue1,colors.grey1,colors.blue2,colors.blue3,colors.green2]),N=255)

        
        self.BlackToGreen_r = ListedColormap(self.BlackToGreen.colors[::-1])
        self.BlackToBlue_r = ListedColormap(self.BlackToBlue.colors[::-1])
        self.WhiteToGreen_r = ListedColormap(self.WhiteToGreen.colors[::-1])
        self.BlueToWhite_r = ListedColormap(self.BlueToWhite.colors[::-1])
        self.GreenToWhite_r = ListedColormap(self.GreenToWhite.colors[::-1])
        self.OrangeToGreen_r = ListedColormap(self.OrangeToGreen.colors[::-1])
        self.GreenToOrange_r = ListedColormap(self.GreenToOrange.colors[::-1])
        self.BlueToGreen_r = ListedColormap(self.BlueToGreen.colors[::-1])
        self.BlueToBlue_r = ListedColormap(self.BlueToBlue.colors[::-1])
        self.BlueToBlue_dark_r = ListedColormap(self.BlueToBlue_dark.colors[::-1])
        self.BlueToBlueToBlue_r = ListedColormap(self.BlueToBlueToBlue.colors[::-1])
        self.BlueToBlueToBlue_dark_r = ListedColormap(self.BlueToBlueToBlue_dark.colors[::-1])
        self.BlackToGreenToOrangeToWhite_r = ListedColormap(self.BlackToGreenToOrangeToWhite.colors[::-1])
        self.BlackToGreenToWhite_r = ListedColormap(self.BlackToGreenToWhite.colors[::-1])
        self.BlackToGreenToWhite_short_r = ListedColormap(self.BlackToGreenToWhite_short.colors[::-1])
        self.colors_r = ListedColormap(self.colors.colors[::-1])

    def startstoparray(self,start,stop,length=256):
        r=np.interp(np.linspace(0,1,length),[0,1],[start[0],stop[0]])
        g=np.interp(np.linspace(0,1,length),[0,1],[start[1],stop[1]])
        b=np.interp(np.linspace(0,1,length),[0,1],[start[2],stop[2]])
        a=np.interp(np.linspace(0,1,length),[0,1],[1,1])
        rgba=np.vstack((r,g,b,a)).T
        return rgba
        
    def create_cmap(self,tup,poss=False):
        if not poss:
            poss=np.linspace(0,255,len(tup))
        a=np.empty((0,4))
        for i in range(len(tup)-1):
            start=tup[i]
            stop =tup[i+1]
            b=self.startstoparray(start,stop,int(poss[i+1]-poss[i]))
            a=np.vstack((a,b))
        return ListedColormap(a)
        

colors=FHcolors()
maps=FHcmap()

if __name__ == "__main__":
    maps=[
        maps.BlackToGreen,maps.GreenToWhite,
        maps.GreenToOrange,
        maps.BlackToGreenToOrangeToWhite,
        maps.BlackToGreenToWhite,
        maps.BlackToGreenToWhite_short,
        maps.BlueToGreen,
        maps.BlueToBlue,
        maps.BlueToBlue_dark,
        maps.BlueToWhite,
        maps.BlueToBlueToBlue,
        maps.BlueToBlueToBlue_dark,
        maps.BlackToBlue,
        maps.colors]
    mapnames=[
        'maps.BlackToGreen',
        'maps.GreenToWhite',
        'maps.GreenToOrange',
        'maps.BlackToGreenToOrangeToWhite',
        'maps.BlackToGreenToWhite',
        'maps.BlackToGreenToWhite_short',
        'maps.BlueToGreen',
        'maps.BlueToBlue',
        'maps.BlueToBlue_dark',
        'maps.BlueToWhite',
        'maps.BlueToBlueToBlue',
        'maps.BlueToBlueToBlue_dark',
        'maps.BlackToBlue',
        'maps.colors']
    fig,axes=plt.subplots(nrows=np.round(len(maps)/2).astype(int), ncols=2)
    axes=axes.flat
    fig.set_size_inches((10,15))
    for ii,m in enumerate(maps[:-1]):
        for i in np.arange(0, 256, 1):
            light = np.sum(m(i)[:3])/3
            axes[ii].plot([i], [light], 'o', markersize=30, color=m(i))
        axes[ii].set_xlabel('Colorvalue')
        axes[ii].set_ylabel('Brightness')
        axes[ii].title.set_text(mapnames[ii])
    for i in np.arange(0, 6, 1):
        light = np.sum(maps[-1](i)[:3])/3
        axes[-1].plot([i], [light], 'o', markersize=30, color=maps[-1](i))
    axes[-1].set_xlabel('Colorvalue')
    axes[-1].set_ylabel('Brightness')
    axes[-1].title.set_text(mapnames[-1])
    plt.tight_layout(pad=3)
    plt.savefig('maps.png')
    plt.show()


'''
import seaborn as sns

#generate testdata
y1 = 23+np.random.randn(100)
y2 = 23.5 + np.random.randn(100)
y = y1.tolist()+y2.tolist()
x1 = np.ones_like(y1)
x2 = np.ones_like(y1)*2
x = x1.tolist()+x2.tolist()


sns.boxplot(x=x, y=y, palette=sns.color_palette([colors.green1, colors.blue1]))
sns.swarmplot(x=x, y=y,color='k')
plt.xlabel('Group')
plt.ylabel('Eta /%')
plt.tight_layout()
plt.savefig('Boxplot_Eta.png')
plt.show()
'''
