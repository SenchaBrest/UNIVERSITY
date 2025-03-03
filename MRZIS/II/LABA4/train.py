import torchvision
import argparse
import time

from torch.utils.data import Subset

from cnn.transforms import PIL2numpy, Normalize, OneHot
from cnn.model import (
    Conv2d, ReLU, Sigmoid, Softmax, Maxpool2d, Flatten, Linear,
    CrossEntropyLoss
)


class Cnn:
    def __init__(self):
        self.conv1 = Conv2d(1, 2, 3, 1)
        self.conv2 = Conv2d(2, 5, 2, 2, padding=1)
        self.max_pool = Maxpool2d(2, 2, padding=1)
        self.fc1 = Linear(320, 100)
        self.fc2 = Linear(100, 10)
        self.flatten = Flatten()
        self.relu = ReLU()
        self.sigmoid1 = Sigmoid()
        self.sigmoid2 = Sigmoid()
        self.softmax = Softmax()

    def load_weights(self, load_path):
        self.conv1.load_weights('conv_w_1', 'conv_b_1', load_path)
        self.conv2.load_weights('conv_w_2', 'conv_b_2', load_path)
        self.fc1.load_weights('fc_w_1', 'fc_b_1', load_path)
        self.fc2.load_weights('fc_w_2', 'fc_b_2', load_path)

    def __call__(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.max_pool(x)
        x = self.conv2(x)
        x = self.sigmoid1(x)
        x = self.flatten.matrices2vector(x)
        x = self.fc1(x)
        x = self.sigmoid2(x)
        x = self.fc2(x)
        x = self.softmax(x)
        return x

    def backprop(self, x, lr=0.01):
        x = self.softmax.backprop(x)
        x = self.fc2.backprop(x, lr)
        x = self.sigmoid2.backprop(x)
        x = self.fc1.backprop(x, lr)
        x = self.flatten.vector2matrices(x)
        x = self.sigmoid1.backprop(x)
        x = self.conv2.backprop(x, lr)
        x = self.max_pool.backprop(x)
        x = self.relu.backprop(x)
        x = self.conv1.backprop(x, lr)


def get_train_dataset(num_classes=3, max_images_per_class=100):
    # Define transformations
    transforms = torchvision.transforms.Compose([
        PIL2numpy(),
        Normalize(),
    ])
    target_transform = torchvision.transforms.Compose([
        OneHot()
    ])

    # Load MNIST dataset
    train_dataset = torchvision.datasets.MNIST(
        root='./data',
        train=True,
        download=True,
        transform=transforms,
        target_transform=target_transform
    )

    # Filter out classes
    train_dataset.data = train_dataset.data[train_dataset.targets < num_classes]
    train_dataset.targets = [t for t in train_dataset.targets if t < num_classes]

    # Apply max_images_per_class limit
    if max_images_per_class is not None:
        class_counts = [0] * num_classes
        filtered_indices = []
        for i, label in enumerate(train_dataset.targets):
            if class_counts[label] < max_images_per_class:
                class_counts[label] += 1
                filtered_indices.append(i)
        train_dataset = Subset(train_dataset, filtered_indices)

    # Load test dataset
    test_dataset = torchvision.datasets.MNIST(
        root='./data',
        train=False,
        download=True,
        transform=transforms,
        target_transform=target_transform
    )

    # Filter out classes in test dataset
    test_dataset.data = test_dataset.data[test_dataset.targets < num_classes]
    test_dataset.targets = [t for t in test_dataset.targets if t < num_classes]

    return train_dataset, test_dataset

# def get_train_dataset(num_classes=3, max_images_per_class=100):
#     # Define transformations
#     transforms = torchvision.transforms.Compose([
#         PIL2numpy(),
#         Normalize(),
#     ])
#     target_transform = torchvision.transforms.Compose([
#         OneHot()
#     ])
#
#     # Load FashionMNIST dataset
#     train_dataset = torchvision.datasets.FashionMNIST(
#         root='./data',
#         train=True,
#         download=True,
#         transform=transforms,
#         target_transform=target_transform
#     )
#
#     # Filter out classes
#     train_dataset.data = train_dataset.data[train_dataset.targets < num_classes]
#     train_dataset.targets = [t for t in train_dataset.targets if t < num_classes]
#
#     # Apply max_images_per_class limit
#     if max_images_per_class is not None:
#         class_counts = [0] * num_classes
#         filtered_indices = []
#         for i, label in enumerate(train_dataset.targets):
#             if class_counts[label] < max_images_per_class:
#                 class_counts[label] += 1
#                 filtered_indices.append(i)
#         train_dataset = Subset(train_dataset, filtered_indices)
#
#     # Load test dataset
#     test_dataset = torchvision.datasets.FashionMNIST(
#         root='./data',
#         train=False,
#         download=True,
#         transform=transforms,
#         target_transform=target_transform
#     )
#
#     # Filter out classes in test dataset
#     test_dataset.data = test_dataset.data[test_dataset.targets < num_classes]
#     test_dataset.targets = [t for t in test_dataset.targets if t < num_classes]
#
#     return train_dataset, test_dataset


def train_loop(dataset, model, criterion, print_log_freq, lr):
    loss_log = []
    acc_log = []
    start_time = time.time()
    for idx, (image, target) in enumerate(dataset):
        pred = model([image])
        loss = criterion(target, pred)
        x = criterion.backprop(target, pred)
        model.backprop(x, lr=lr)

        loss_log.append(loss.sum())
        acc_log.append(pred.argmax() == target.argmax())
        if idx % print_log_freq == 0:
            loss_avg = sum(loss_log[-print_log_freq:]) / print_log_freq
            acc_avg = sum(acc_log[-print_log_freq:]) / print_log_freq
            loop_time = time.time() - start_time
            start_time = time.time()
            print(f'Train step {idx}, Loss: {loss_avg:.5f}, '
                  f'Acc: {acc_avg:.4f}, time: {loop_time:.1f}')


def val_loop(dataset, model, criterion):
    loss_log = []
    acc_log = []
    start_time = time.time()
    for idx, (image, target) in enumerate(dataset):
        pred = model([image])
        loss = criterion(target, pred)
        loss_log.append(loss.sum())
        acc_log.append(pred.argmax() == target.argmax())

    loss_avg = sum(loss_log) / len(loss_log)
    acc_avg = sum(acc_log) / len(acc_log)
    loop_time = time.time() - start_time
    print(f'Val step, Loss: {loss_avg:.5f}, '
          f'Acc: {acc_avg:.4f}, time: {loop_time:.1f}')


def main(args):
    train_dataset, test_dataset = get_train_dataset()
    model = Cnn()
    if args.load_path:
        model.load_weights(args.load_path)
        print('Numpy model weights were loaded')

    criterion = CrossEntropyLoss()
    for epoch in range(args.num_epochs):
        train_loop(train_dataset, model, criterion,
                   args.print_log_freq, args.lr)
        val_loop(test_dataset, model, criterion)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--print_log_freq', type=int, default=100,
                        help='Frequency of printing of training logs')
    parser.add_argument('--load_path', type=str, default='',
                        help='Path to model weights to start training with')
    parser.add_argument('--num_epochs', type=int, default=1,
                        help='Total number of epochs')
    parser.add_argument('--lr', type=float, default=0.01,
                        help='learning rate')
    args = parser.parse_args()

    main(args)
