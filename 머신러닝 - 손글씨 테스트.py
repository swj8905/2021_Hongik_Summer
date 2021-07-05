import imageio
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import ImageDraw
from scipy import ndimage
import numpy as np
from PIL import Image
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pickle



#Load from file
with open("./mnist_model.pkl", 'rb') as file:
    model = pickle.load(file)

def crop_img(img_ndarray):
    first_row = np.nonzero(img_ndarray)[0].min()
    last_row = np.nonzero(img_ndarray)[0].max()
    middle_row = np.mean([last_row, first_row])
    # Across cols
    first_col = np.nonzero(img_ndarray)[1].min()
    last_col = np.nonzero(img_ndarray)[1].max()
    middle_col = np.mean([last_col, first_col])
    # Crop by longest non-zero to make sure all is kept
    row_length = last_row - first_row
    col_length = last_col - first_col
    length = max(row_length, col_length)
    # Minimum size of 28x28
    length = max(length, 28)
    # Get half length to add to middle point (add some padding: 1px)
    half_length = (length / 2) + 1
    # Make sure even the shorter dimension is centered
    first_row = int(middle_row - half_length)
    last_row = int(middle_row + half_length)
    first_col = int(middle_col - half_length)
    last_col = int(middle_col + half_length)
    # Crop image
    return img_ndarray[first_row:last_row, first_col:last_col]

def center_img(img_ndarray):
    com = ndimage.measurements.center_of_mass(img_ndarray)
    center = len(img_ndarray) / 2
    row_diff = int(com[0] - center)
    col_diff = int(com[1] - center)
    rows = np.zeros((abs(row_diff), img_ndarray.shape[1]))
    if row_diff > 0:
        img_ndarray = np.vstack((img_ndarray, rows))
    elif row_diff < 0:
        img_ndarray = np.vstack((rows, img_ndarray))
    cols = np.zeros((img_ndarray.shape[0], abs(col_diff)))
    if col_diff > 0:
        img_ndarray = np.hstack((img_ndarray, cols))
    elif col_diff < 0:
        img_ndarray = np.hstack((cols, img_ndarray))
    dim_diff = img_ndarray.shape[0] - img_ndarray.shape[1]
    half_A = half_B = abs(int(dim_diff / 2))
    if dim_diff % 2 != 0:
        half_B += 1
    if half_A == 0:  # 1 line off from exactly centered
        if dim_diff > 0:
            half_B = np.zeros((img_ndarray.shape[0], half_B))
            img_ndarray = np.hstack((half_B, img_ndarray))
        else:
            half_B = np.zeros((half_B, img_ndarray.shape[1]))
            img_ndarray = np.vstack((half_B, img_ndarray))
    elif dim_diff > 0:
        half_A = np.zeros((img_ndarray.shape[0], half_A))
        half_B = np.zeros((img_ndarray.shape[0], half_B))
        img_ndarray = np.hstack((img_ndarray, half_A))
        img_ndarray = np.hstack((half_B, img_ndarray))
    else:
        half_A = np.zeros((half_A, img_ndarray.shape[1]))
        half_B = np.zeros((half_B, img_ndarray.shape[1]))
        img_ndarray = np.vstack((img_ndarray, half_A))
        img_ndarray = np.vstack((half_B, img_ndarray))
    # Add padding all around (15px of zeros)
    return np.lib.pad(img_ndarray, 15, 'constant', constant_values=(0))


def resize_img(img_ndarray):
    img = Image.fromarray(img_ndarray)
    img.thumbnail((28, 28), Image.ANTIALIAS)
    return np.array(img)


def min_max_scaler(img_ndarray, final_range=(0, 1)):
    px_min = final_range[0]
    px_max = final_range[1]
    # Hard code pixel value range
    img_std = img_ndarray
    return img_std * (px_max - px_min) + px_min


def plot_digit(digit, show=True, file_name=None):
    plt.imshow(digit, cmap = 'Greys', interpolation = 'none')
    plt.tick_params(axis='both', which='both', bottom='off', top='off',
                    labelbottom='off', right='off', left='off', labelleft='off')
    if file_name is not None:
        plt.savefig(file_name)
    if show:
        plt.show()
def conver2black(x):
    return 255-x

def imageprepare(argv):
    eg_2 = imageio.imread(argv, pilmode="1")
    index = 0
    for i in eg_2:
        eg_2[index] = list(map(conver2black, i))
        index += 1
    eg_2 = crop_img(eg_2)
    eg_2 = center_img(eg_2)
    eg_2 = resize_img(eg_2)
    eg_2 = min_max_scaler(eg_2, final_range=(0, 1))
    # plot_digit(eg_2)
    eg_2 = eg_2.ravel().tolist()
    return eg_2

class ImageGenerator:
    def __init__(self, parent, posx, posy, *kwargs):
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 250
        self.sizey = 250
        self.b1 = "up"
        self.xold = None
        self.yold = None
        self.drawing_area = tk.Canvas(self.parent, width=self.sizex, height=self.sizey + 10)
        self.drawing_area.place(x=self.posx, y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.save)
        self.drawing_area.place(x=self.sizex / 7, y=self.sizex / 7)




        self.button1 = tk.Button(self.parent, text="Clear!", width=8, command=self.clear)
        self.button1.place(x=300, y=self.sizey - 40)

        self.text = tk.Text(self.parent, width=15, height=1)
        self.text.insert(tk.INSERT, "예상숫자 : ")
        self.text.pack()
        self.text.place(x=90, y=4)

        self.image = Image.new("1", (250, 250), (255))
        self.draw = ImageDraw.Draw(self.image)

    # def train(self, number):
    #     x = [imageprepare('./img.png')]
    #     newArr = []
    #     for i in range(784):
    #         newArr.append(x[0][i])
    #     newArr2 = []
    #     newArr2.append(newArr)
    #     newArr2.append(newArr)
    #
    #     clf.fit(newArr2, [number, number])
    #     with open('mnist_classifier.pkl', 'wb') as fid:
    #         pickle.dump(clf, fid)


    def save(self,event):
        self.b1 = "up"
        self.xold = None
        self.yold = None
        filename = "img.png"
        self.image.save(filename)
        print("예상숫자 : " + str(checkgo()))
        a = "예상숫자 : " + str(checkgo())
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.INSERT, a)

    def clear(self):
        self.drawing_area.delete("all")
        self.image = Image.new("1", (250, 250), (255))
        self.draw = ImageDraw.Draw(self.image)

    def b1down(self, event):
        self.b1 = "down"

    def b1up(self, event):
        self.b1 = "up"
        self.xold = None
        self.yold = None

    def motion(self, event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold, self.yold, event.x, event.y, smooth='true', width=3, fill='blue')
                self.draw.line(((self.xold, self.yold), (event.x, event.y)), (0), width=10)

        self.xold = event.x
        self.yold = event.y


def check():
    x = [imageprepare('./img.png')]
    newArr = []
    for i in range(784):
        newArr.append(x[0][i])
    newArr2 = []
    newArr2.append(newArr)
    test_data = newArr2

    result = model.predict(test_data)  # 숫자 예측시키기

    return result[0]


def checkgo():
    # try:
    a = check()
    return a
    # except:
    #     checkgo()

if __name__ == "__main__":
    root = tk.Tk()
    root.wm_geometry("%dx%d+%d+%d" % (400, 400, 10, 10))
    root.config(bg='gray')
    ImageGenerator(root, 10, 10)
    root.mainloop()
