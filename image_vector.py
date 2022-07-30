from __future__ import annotations
from typing import Tuple, Dict
import copy
import cv2
import numpy as np
from matplotlib import pyplot as plt

class ImageVector:
    def __init__(self,
                title:str = "untitled",
                file_name:str = None, 
                 image_array:np.ndarray = None, 
                ) -> None:
        if (file_name is not None) and (image_array is not None):
            raise ValueError("'file_name' and 'image_array' are both specified...")
        
        if file_name:
            self.image_array = cv2.imread(file_name)
        if image_array is not None:
            self.image_array = image_array
        
        self.title = title
        
    @property
    def shape(self) -> Tuple[int]:
        return self.image_array.shape
    
    @property
    def height(self) -> int:
        return self.image_array.shape[0]
    
    @property
    def width(self) -> int:
        return self.image_array.shape[1]
    
    @property
    def color_depth(self) -> int:
        return self.image_array.shape[2]
    
    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height
    
    def to_array(self) -> np.ndarray:
        return copy.deepcopy(self.image_array)

    def transpose(self) -> ImageVector:

        return self._get_self_with_image_array(
            cv2.transpose(self.image_array)
        )
    
    def flip_vertically(self) -> ImageVector:
        return self._get_self_with_image_array(
            cv2.flip(self.image_array, 0) # 如果要垂直翻轉或者是上下翻轉的話，就在 cv2.flip() 第二個參數帶入 0 即可
        )
    
    def flip_horizontally(self) -> ImageVector:
        return self._get_self_with_image_array(
            cv2.flip(self.image_array, 1) # 如果要水平翻轉或者是左右翻轉的話，就在 cv2.flip() 第二個參數帶入 1 即可
        )

    def scale(self, scale_rate:float = 1.0, interpolation:int = cv2.INTER_LINEAR) -> ImageVector:
        scaled_image = cv2.resize(
            self.image_array, 
            dsize = None, 
            fx= scale_rate, fy=scale_rate, 
            interpolation= interpolation
        )
        return self._get_self_with_image_array(scaled_image)
    
    def resize(self, dimension_size:Tuple[int, int], interpolation:int = cv2.INTER_LINEAR):
        resized_image = cv2.resize(
            self.image_array, 
            dsize = dimension_size, 
            interpolation= interpolation
        )
        return self._get_self_with_image_array(resized_image)

    def rotate(self, center:Tuple[float, float] = None, angle:float = 0.0, scale:float = 1.0) -> ImageVector:
        if center is None:
            center = (self.width // 2, self.height // 2) # 找到圖片中心
        
        # 第一個參數旋轉中心，第二個參數旋轉角度(-順時針/+逆時針)，第三個參數縮放比例
        rotated_maxtrix = cv2.getRotationMatrix2D(center, angle, scale)
        # 第三個參數變化後的圖片大小
        rotated_img_array = cv2.warpAffine(self.image_array, rotated_maxtrix, (self.width, self.height))

        return self._get_self_with_image_array(rotated_img_array)

    def convert_to_gray_scale(self) -> ImageVector:
        gray_image = cv2.cvtColor(self.image_array, cv2.COLOR_BGR2GRAY)

        return self._get_self_with_image_array(gray_image)

    def crop(self, start_point_x_y:Tuple[int, int], height:int, width:int) -> ImageVector:
        x, y = start_point_x_y
        cropped_image = self.image_array[y:y+height, x:x+width]

        return self._get_self_with_image_array(cropped_image)
    
    def display(self, size:int = 10) -> None:
        width = size * self.aspect_ratio
        plt.figure(figsize=(width, size))
        plt.imshow(
            cv2.cvtColor(self.image_array, cv2.COLOR_BGR2RGB)
        )
        plt.title(self.title)
        plt.show()
        
    def split_into_BGR_channels(self) -> Dict[str, ImageVector]:
        blue, green, red = cv2.split(self.image_array)
        
        return {
            "blue":self._get_self_with_image_array(blue),
            "green":self._get_self_with_image_array(green),
            "red":self._get_self_with_image_array(red)
        }
    
    def save_to_file(self, file_name:str) -> None:
        cv2.imwrite(file_name, self.image_array)

    def __repr__(self) -> str:
        self.display()
        return ""

    def __add__(self, value:float = 0.0) -> ImageVector:
        if value > 255:
            raise ValueError(f"operand greater than 255, entering {value}")

        matrix = np.ones(self.image_array.shape, dtype = "uint8") * value
        brighter_image_array = cv2.add(self.image_array, matrix)

        return self._get_self_with_image_array(brighter_image_array)

    def __sub__(self, value:float = 0.0) -> ImageVector:
        if value > 255:
            raise ValueError(f"operand greater than 255, entering {value}")

        matrix = np.ones(self.image_array.shape, dtype = "uint8") * value
        darker_image_array = cv2.subtract(self.image_array, matrix)
        
        return self._get_self_with_image_array(darker_image_array)
    

    def _get_self_with_image_array(self, new_image_array) -> ImageVector:

        return type(self)(
            title = self.title, image_array= new_image_array
        )
    
    