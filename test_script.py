from datasets import load_dataset
d = load_dataset('./datasets/cifar100')
print(d)
print(d['train'][0])

# import pickle as pkl
# train_path = '../../../Downloads/cifar-100-python/train'
# test_path = '../../../Downloads/cifar-100-python/test'
# with open(train_path,'rb') as f:
#     train = pkl.load(f,encoding="bytes")

# train_dict = {}
# train_dict[b"data"] = train[b"data"][:5]
# train_dict[b"fine_labels"] = train[b"fine_labels"][:5]
# train_dict[b"coarse_labels"] = train[b"coarse_labels"][:5]
# with open('./datasets/cifar100/dummy/cifar100/1.0.0/dummy_data/cifar-100-python.tar.gz/cifar-100-python/train','wb') as f:
#     pkl.dump(train_dict,f)

# with open(test_path, 'rb') as f:
#     test = pkl.load(f, encoding="bytes")

# test_dict = {}
# test_dict[b"data"] = test[b"data"][:5]
# test_dict[b"fine_labels"] = test[b"fine_labels"][:5]
# test_dict[b"coarse_labels"] = test[b"coarse_labels"][:5]
# with open('./datasets/cifar100/dummy/cifar100/1.0.0/dummy_data/cifar-100-python.tar.gz/cifar-100-python/test', 'wb') as f:
#     pkl.dump(test_dict, f)
