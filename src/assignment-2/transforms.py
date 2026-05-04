"""
Image transformations and preprocessing utilities
"""
from torchvision import transforms


def get_transform(best_params):
    # Si recibe un objeto Optuna study, extrae .best_params
    if hasattr(best_params, "best_params"):
        best_params = best_params.best_params

    image_size = best_params["image_size"]
    rot_degrees = best_params["rot_degrees"]
    h_flip = best_params["h_flip"]
    brightness = best_params["brightness"]
    crop_scale = best_params["crop_scale"]
    norm_strategy = best_params["norm_strategy"]

    if norm_strategy == "imagenet":
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]

    elif norm_strategy == "custom":
        m = best_params["m_custom"]
        s = best_params["s_custom"]
        mean, std = [m, m , m ], [s, s , s]

    else :
        mean, std = [0.0, 0.0, 0.0], [1.0, 1.0, 1.0]

    return transforms.Compose([
            transforms.RandomRotation(degrees=rot_degrees),
            transforms.RandomResizedCrop(size=(image_size,image_size),scale=(crop_scale,crop_scale,1)),
            transforms.RandomHorizontalFlip(p=h_flip),
            transforms.ColorJitter(brightness=brightness),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std)
        ])


