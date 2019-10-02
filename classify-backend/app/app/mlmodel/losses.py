
import torch.nn as nn
import torch.nn.functional as F

# https://github.com/adambielski/siamese-triplet/blob/master/losses.py
class ContrastiveLoss(nn.Module):
    """Takes embeddings of two samples and a target label == 1 if samples are from the same class and label == 0 otherwise
    """
    def __init__(self, margin=1.):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin
        self.eps = 1e-9

    def forward(self, ops, target, size_average=True):
        op1, op2 = ops[0], ops[1]
        dist = F.pairwise_distance(op1, op2)
        losses = 0.5 * (target.float() * dist +
                (1 + -1 * target).float() * F.relu(self.margin - (dist + self.eps).sqrt()).pow(2))
        return losses.mean() if size_average else losses.sum()
