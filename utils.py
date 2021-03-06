
import numpy as np
import torch
from matplotlib import pyplot
import datetime
import os
import shutil
import global_variables as gv
import argparse

def plot_stroke(stroke, save_name=None):
    # Plot a single example.
    f, ax = pyplot.subplots()

    x = np.cumsum(stroke[:, 1])
    y = np.cumsum(stroke[:, 2])

    size_x = x.max() - x.min() + 1.
    size_y = y.max() - y.min() + 1.
    # lets limit it to size 2000,500
    

    f.set_size_inches(2. * size_x / size_y, 2.)
    

    cuts = np.where(stroke[:, 0] == 1)[0]
    start = 0
    if cuts.shape[0] ==0:
        cuts = [stroke.shape[0]]
    for cut_value in cuts:
        ax.plot(x[start:cut_value], y[start:cut_value],
                'k-', linewidth=3)
        start = cut_value + 1
    ax.axis('equal')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    if save_name is None:
        pyplot.show()
    else:
        try:
            pyplot.savefig(
                save_name,
                bbox_inches='tight',
                pad_inches=0.5)
        except Exception:
            print "Error building image!: " + save_name

    pyplot.close()
    
def plot_stroke_numpy(stroke, save_name=None):
    # Plot a single example.
    f, ax = pyplot.subplots()
    x = np.cumsum(stroke[:, 1])
    y = np.cumsum(stroke[:, 2])

    size_x = x.max() - x.min() + 1.
    size_y = y.max() - y.min() + 1.

    f.set_size_inches(5. * size_x / size_y, 5.)

    cuts = np.where(stroke[:, 0] == 1)[0]
    if cuts.shape[0] ==0:
        cuts = [stroke.shape[0]]
    start = 0
    for cut_value in cuts:
        ax.plot(x[start:cut_value], y[start:cut_value],
                'k-', linewidth=3)
        start = cut_value + 1
    ax.axis('equal')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    f.tight_layout(pad=0)
    f.canvas.draw()
    data = np.fromstring(f.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(f.canvas.get_width_height()[::-1]+(3,)).astype('float32')
    pyplot.close()
    return data

def save_checkpoint(state,best_name=gv.exp_name, is_best=False, filename='checkpoint.pth'):
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, 'weights/best_'+best_name+'.pth')
        
        
        

def adjust_learning_rate(optimizer, epoch,orig_lr):
    """Sets the learning rate to the initial LR decayed by 10 every 3 epochs"""
    lr = orig_lr * (0.1 ** (epoch//gv.reduction_epoch))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr
        
        
def save_exp_information(exp_name=gv.exp_name):
    all_files = os.listdir('.')
    files = [x for x in all_files if x[-3:]=='.py']
    folders = [x for x in all_files if not '.' in x]
    
    ## For Folders
    for folder in folders:
        inner_files = os.listdir(folder)
        add_files = [os.path.join(folder,x) for x in inner_files if x[-3:]=='.py']
        files.extend(add_files)
        
    fmt='%m-%d-%H-%M_{fname}'
    dir_name = datetime.datetime.now().strftime(fmt).format(fname=exp_name)
    new_dir = os.path.join(gv.experiment_code_log_folder,dir_name)
    os.system('mkdir '+new_dir)
    
    for folder in folders:
        inner_files = os.system('mkdir ' + os.path.join(new_dir,folder))
    for cur_file in files:
        os.system('cp ' + cur_file+ ' '+ os.path.join(new_dir,cur_file))
        
# for saving summaries without disgust:
def write_summaries(name_list,value_list,type_list, writer, jter):
    for iter, name in enumerate(name_list):
        if type_list[iter] ==0:
            # 0 is scalar (link 1D)
            writer.add_scalar(name, value_list[iter], jter)
        elif type_list[iter] ==1:
            # 1 is for images
            writer.add_image(name, value_list[iter], jter)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_exp', default='True', help='The dataset the class to processed')
    args = parser.parse_args()
    
    if args.save_exp == 'True':
        save_exp_information()
    
        