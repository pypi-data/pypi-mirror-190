from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
import io

def MyFun():
    print(':)')
    return '?'

def nonzero(im):
    r = np.ravel(im)
    return r[r>0]

def report(str):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(current_time, "  ", str)

def axisoff():
    plt.tick_params(axis='both', which='both', top=False,
                    bottom=False, left=False, right=False,
                    labelbottom=False, labelleft=False)

def newfig(figsize=[12,12], facecolor=[1,1,1]):
    plt.figure(figsize=figsize, facecolor=facecolor)



def M2E(M, nonzero=True):
    '''
    Convert an adjacency matrix to an edge list.
    '''
    df = pd.DataFrame(M)
    df = df.stack().reset_index()
    if nonzero:
        return df.loc[df.iloc[:,2]>0, :].values
    else:
        return df.values

def E2M(E, v = None, padding=0, dtype=None, return_base = False):
    if v is None and E.shape[1] == 3:
        v = E[:, 2]
    if dtype is None:
        if v is None:
            dtype=bool
        else:
            dtype = v.dtype
    x = E[:, 0].astype(int)
    y = E[:, 1].astype(int)
    xmin = x.min() - padding
    ymin = y.min() - padding
    x_shifted = x - xmin
    y_shifted = y - ymin
    xmax = x_shifted.max() + padding + 1
    ymax = y_shifted.max() + padding + 1
    if v is None:
        nn = np.zeros((xmax, ymax), dtype=bool)
        nn[x_shifted, y_shifted] = 1
    else:
        nn = np.zeros((xmax, ymax), dtype=dtype)
        nn[x_shifted, y_shifted] = v
    if return_base:
        return nn, np.array([xmin, ymin])
    else:
        return nn
        
    

def maskcrop(im, mask=None, padding=None, return_range=False):
    mask = mask.copy()
    im_size = im.shape
    if type(mask)==type(None):
        mask = (im>0)
    mask = mask*1
    
    xleft = np.argwhere(np.any(mask, axis=0))[0][0]
    xright = np.argwhere(np.any(mask, axis=0))[-1][0]

    ytop = np.argwhere(np.any(mask, axis=1))[0][0]
    ybot = np.argwhere(np.any(mask, axis=1))[-1][0]

    if padding == None:
        padding = int(0.05*max(xright-xleft, ybot-ytop))
    xleft = int(max(xleft - padding, 0))
    xright = int(min(xright + padding, im_size[1]))
    ytop = int(max(ytop - padding, 0))
    ybot = int(min(ybot + padding, im_size[0]))
    if len(im.shape) == 3:
        im_new = im[ytop:ybot,xleft:xright,:]
    else:
        im_new = im[ytop:ybot,xleft:xright]
    if return_range:
        return im_new, [ytop,ybot,xleft,xright]
    else:
        return im_new

def imshow(im, cmap='gray'):
    if len(im.shape)==2:
        plt.imshow(im, cmap=cmap)
    else:
        plt.imshow(im)
    plt.axis('off')
    
def splitmask(masks, cell_df, target_col = 'Class'):
    masks_new = {c:np.zeros_like(masks) for c in cell_df[target_col].unique()}

    for cell_id in tqdm(cell_df.Cell):
        c = cell_df.loc[cell_df.Cell == cell_id, target_col].values[0]
        masks_new[c] = np.logical_or(masks_new[c], masks==cell_id)
    return masks_new


def readchannel(data, fn, m, p=99, k='im'):
    ''''Read a channel and cap at p percentile'''
    im = data[fn][k][m]
    im = np.where(im > np.percentile(nonzero(im) , p), np.percentile(nonzero(im) , p), im)
    return im


def uint8(im):
    return (im/max(0.001, np.max(im))*255).astype('uint8')

def dist(a,b):
    return np.sqrt(np.sum(np.square(b-a)))

import seaborn as sns
def paired_palette():
    cp = sns.color_palette('Paired')
    colornames = [a+b  for b in ['b','g','r','o','p','y']for a in ['b','d']]
    cd = {colornames[i]: tuple((np.array(cp[i])*255).astype(int)) for i in range(len(cp))}
    for a in ['b','g','r','o','p','y']:
        cd['m'+a] = tuple(((np.array(cd['b'+a]) + np.array(cd['d' + a]))*0.5).astype(int))
    return cd


import matplotlib.gridspec as gridspec
def hist2d(x=None, y=None, df=None, c1='V1', c2='V2', t1=None, t2=None, bins=128, includezero=True,cmap='inferno', title='histgram', p=75, xmin=None, xmax=None, ymin=None, ymax=None, figsize=(7,7), t1_color = (1,0,0), t2_color = (1, 0,0)):
    '''
    Use either x and y, or df with m1 and m2.
    '''
    plt.figure(facecolor=(1,1,1), figsize = figsize)
    gs = gridspec.GridSpec(5, 5) # ( 10, 12)
    if df is None:
        if x is None or y is None:
            raise SyntaxError('Invalid input data.')
        df = pd.DataFrame({c1:x, c2:y})
    if not includezero:
        df = df.loc[np.logical_and(df[c1]>0, df[c2]>0), :]
    d1 = df[c1]
    d2 = df[c2]
    
    ax0 = plt.subplot(gs[1:, 0:4]) # [6:10, 5:9]
    cc,_,_ = np.histogram2d(d1, d2, bins=bins)
    p = np.percentile(nonzero(cc), p)
    plt.hist2d(d1, d2, bins = bins, cmap = cmap, vmax=p)
    plt.xlabel(c1)
    plt.ylabel(c2)
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])

    axx = plt.subplot(gs[:1, 0:4]) # [5:6, 5:9]
    plt.hist(d1, bins=bins)
    plt.xlim(ax0.get_xlim())
    plt.tick_params(
        axis='both',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,  
        left=False,
        top=False,        
        right=False,
        labelbottom=False,
        labelleft=False) 
    if t1 is not None:
        ax0.axvline(t1, color=t1_color)
        axx.axvline(t1, color=t1_color)

    axy = plt.subplot(gs[1:, 4:]) # [6:10, 9:10]
    _ = plt.hist(d2, bins=bins, orientation="horizontal")
    plt.ylim(ax0.get_ylim())
    plt.tick_params(
        axis='both',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,  
        left=False,
        top=False,        
        right=False,
        labelbottom=False,        
        labelleft=False) 
    if t2 is not None:
        ax0.axhline(t2, color=t2_color)
        axy.axhline(t2, color=t2_color)

    axx.set_title(title)
    return

def Im2Bytes(Im):
    img_byte_arr = io.BytesIO()
    Im.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr