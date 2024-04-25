import torchvision
from nn import Conv2D, ReLU, MeanSquaredErrorLoss
from transforms import PIL2numpy, Normalize, OneHot
import numpy as np
from tqdm import tqdm


class Autoencoder:
    def __init__(self):
        self.layers = []
        self.layers.append(Conv2D((1, 28, 28), 3, 1))
        self.layers.append(ReLU())
        self.layers.append(Conv2D((1, 26, 26), 3, 1, transposed=True))
        self.layers.append(ReLU())

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

    def backward(self, x, learning_rate=0.01):
        for layer in self.layers[::-1]:
            if isinstance(layer, Conv2D):
                x = layer.backward(x, learning_rate)
            else:
                x = layer.backward(x)


def get_class_dict(train=True):
    transforms = torchvision.transforms.Compose([
        PIL2numpy(),
        Normalize(),
    ])
    target_transform = torchvision.transforms.Compose([
        OneHot()
    ])

    dataset = torchvision.datasets.MNIST(
        # dataset = torchvision.datasets.FashionMNIST(
        root='./data',
        train=train,
        download=True,
        transform=transforms,
        target_transform=target_transform
    )

    class_dict = {}

    for _, target in dataset:
        target = np.argmax(target).item()
        if target not in class_dict:
            class_dict[target] = []
        class_dict[target].append(_)

    return class_dict


def train_loop(dataset, model, criterion, learning_rate):
    for idx, image in enumerate(tqdm(dataset, desc="Processing Images")):
        pred = model([image])
        loss = criterion(image, pred)
        x = criterion.backward()
        model.backward(x, learning_rate)


def main(num_epochs=1, learning_rate=0.01):
    train_class_dict = get_class_dict(train=True)
    models = [Autoencoder() for _ in range(len(train_class_dict.keys()))]

    criterion = MeanSquaredErrorLoss()
    for model, cls in zip(models, sorted(train_class_dict.keys())):
        for epoch in range(num_epochs):
            train_loop(train_class_dict[cls], model, criterion, learning_rate)

    test_class_dict = get_class_dict(train=False)
    true = 0
    false = 0
    for cls in sorted(test_class_dict.keys()):
        for image in test_class_dict[cls]:
            loss = []
            for idx, model in enumerate(models):
                pred = model([image])
                loss.append(criterion(image, pred).sum())
            if np.argmin(loss) == cls:
                true += 1
            else:
                false += 1
    print(f"true: {true}, false: {false}")


if __name__ == '__main__':
    main(num_epochs=1, learning_rate=0.3)
