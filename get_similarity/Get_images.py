import numpy as np
import networkx as nx
import torch
import torchvision

import warnings

warnings.filterwarnings("ignore")


# transforms = torch.nn.Sequential(
#     torchvision.transforms.CenterCrop((960,50)),
#     torchvision.transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
# )
# scripted_transforms = torch.jit.script(transforms)


def process_images():
    file_path = {}
    file_path['class'] = ["../video/class.mp4", "../video/class_1.mp4", "../video/class_2.mp4"]
    file_path['halway_1'] = ["../video/halway_1.mp4", "../video/halway_1_1.mp4"]
    file_path['halway_2'] = ["../video/halway_2.mp4"]
    file_path['halway_3'] = ["../video/halway_3.mp4", "../video/halway_3_1.mp4"]
    file_path['halway_4'] = ["../video/halway_4.mp4"]
    file_path['outdoor'] = ["../video/outdoor.mp4"]
    file_path['lecture_center'] = ["../video/lecture_center.mp4"]
    file_path['lecture_alley'] = ["../video/lecture_alley.mp4"]
    file_path['out_office'] = ["../video/out_office.mp4", "../video/out_office_1.mp4"]
    file_path['ERF_alley'] = ["../video/ERF_alley.mp4", "../video/ERF_alley_1.mp4", "../video/ERF_alley_2.mp4", "../video/ERF_alley_3.mp4"]


    database = {}

    for key in file_path.keys():
        data_store = []
        for i,file in enumerate(file_path[key]):
            data = torchvision.io.read_video(file)
            video = data[0]
            metadata = data[2]
            data_store.append(video.numpy())
            print(metadata, file)
        data_store = np.concatenate(data_store, axis=0)
        np.save(f"../data/{key}.npy", data_store)
        




if __name__ == "__main__":
    process_images()