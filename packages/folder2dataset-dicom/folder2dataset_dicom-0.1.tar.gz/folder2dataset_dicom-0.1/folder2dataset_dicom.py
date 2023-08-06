import os
import pydicom
import matplotlib.pyplot as plt
import albumentations as A
from albumentations.pytorch import ToTensorV2
from torch.utils.data import Dataset
import  numpy as np


class My_Dataset(Dataset):
    def __init__(self,path,ToGray_value=0.01,
                 HorizontalFlip_value=0.5,
                 VerticalFlip_value=0.5,
                 Resize_value=512,
                 ToTensorV2_value=1.0):
        
        self.path = path
        self.images = os.listdir(path)
        self.ToGray=A.ToGray(p=ToGray_value)
        self.HorizontalFlip=A.HorizontalFlip(p=HorizontalFlip_value)
        self.VerticalFlip=A.VerticalFlip(p=HorizontalFlip_value)
        self.Resize=A.Resize(height=Resize_value,width=Resize_value,p=1)
        self.ToTensorV2=ToTensorV2(p=ToTensorV2_value)


    def get_train_transform(self):
        return A.Compose(
            [
                self.ToGray,
                self.HorizontalFlip,
                self.VerticalFlip,
                self.Resize,
                self.ToTensorV2,
            ],
        )


    def __getitem__(self, item):
        
        image=  (pydicom.dcmread(os.path.join(self.path,self.images[item])).pixel_array).astype('float32')
        image= self.get_train_transform()(image=image)
        return image


    def __len__(self):
        return len(self.images)

    def image_show(self,index):
        dic_tensor= self.__getitem__(index)
        plt.figure(figsize=(8,8))
        plt.imshow(np.squeeze(dic_tensor['image'].numpy()),cmap='gray')

