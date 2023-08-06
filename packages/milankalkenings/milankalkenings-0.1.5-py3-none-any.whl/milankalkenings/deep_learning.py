from abc import ABC, abstractmethod
import random
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import Optimizer
import matplotlib.pyplot as plt


class Module(ABC, nn.Module):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def freeze_pretrained(self):
        pass

    @abstractmethod
    def unfreeze_pretrained(self):
        pass

    @abstractmethod
    def forward(self, x, y):
        """
        :return: dict {"loss": , "scores", ...}
        """
        pass


def make_reproducible(seed: int = 1):
    """
    ensures reproducibility over multiple script runs and after restarting the local machine
    """
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.cuda.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    torch.set_printoptions(sci_mode=False)
    torch.set_printoptions(threshold=100_000)
    np.set_printoptions(suppress=True)


class Setup:
    def __init__(self,
                 loader_train: DataLoader,
                 loader_val: DataLoader,
                 loader_test: DataLoader,
                 device: str = "cpu",
                 monitor_n_losses: int = 50,
                 checkpoint_initial: str = "../monitoring/checkpoint_initial.pkl",
                 checkpoint_running: str = "../monitoring/checkpoint_running.pkl",
                 checkpoint_final: str = "../monitoring/checkpoint_final.pkl",
                 lrrt_n_batches: int = 49,
                 lrrt_slope_desired: float = 0,
                 lrrt_max_decays: int = 0,
                 lrrt_decay: float = 0.9,
                 lrrt_initial_candidates: np.ndarray = np.array([1e-3, 1e-4, 1e-6]),
                 es_max_violations: int = 2,
                 optimizer_class=torch.optim.Adam):
        self.loader_train = loader_train
        self.loader_val = loader_val
        self.loader_test = loader_test
        self.device = device
        self.monitor_n_losses = monitor_n_losses  # prints loss slope after this amount of training steps
        self.checkpoint_initial = checkpoint_initial
        self.checkpoint_running = checkpoint_running
        self.checkpoint_final = checkpoint_final
        self.lrrt_n_batches = lrrt_n_batches  # batches used in lrrt for learning rate determination
        self.lrrt_slope_desired = lrrt_slope_desired  # exclusive border
        self.lrrt_max_decays = lrrt_max_decays  # max number of candidate decays performed in lrrt
        self.lrrt_decay = lrrt_decay
        self.lrrt_initial_candidates = lrrt_initial_candidates
        self.es_max_violations = es_max_violations  # max number of early stopping violations
        self.optimizer_class = optimizer_class


class BatchHandler:
    def __init__(self, setup: Setup):
        self.setup = setup

    def forward_batch(self, module: Module, batch: list):
        x, y = batch
        x = x.to(self.setup.device)
        y = y.to(self.setup.device)
        return module(x=x, y=y)

    def train_batch(self, module: Module, optimizer: Optimizer, batch: list, freeze_pretrained: bool = False):
        # freeze/unfreeze here: longer runtime, better encapsulation
        if freeze_pretrained:
            module.freeze_pretrained()
        else:
            module.freeze_pretrained()
        module.train()
        module.zero_grad()
        loss = self.forward_batch(module=module, batch=batch)["loss"]
        loss.backward()
        optimizer.step()
        return float(loss)

    def loss_batch_eval(self, module: Module, batch: list):
        module.eval()
        with torch.no_grad():
            return float(self.forward_batch(module=module, batch=batch)["loss"])

    def predict_class_labels_batch(self, module: Module, batch: list):
        scores = self.forward_batch(module=module, batch=batch)["scores"]
        return torch.argmax(scores, dim=1)

    def train_n_batches(self, module: Module,
                        optimizer: Optimizer,
                        n_batches: int,
                        loader: DataLoader,
                        freeze_pretrained: bool):
        losses = []
        for train_iter, batch in enumerate(loader):
            if train_iter == n_batches:
                break

            losses.append(
                self.train_batch(module=module, optimizer=optimizer, batch=batch, freeze_pretrained=freeze_pretrained))
            if (len(losses) % self.setup.monitor_n_losses) == 0:
                losses_last = np.array(losses[-self.setup.monitor_n_losses:])
                slope_last, _ = np.polyfit(x=np.arange(len(losses_last)), y=losses_last, deg=1)
                print("iter", train_iter + 1, "mean loss", losses_last.mean(), "loss slope", slope_last)
        slope_total, bias_total = np.polyfit(x=np.arange(len(losses)), y=losses, deg=1)
        return losses, slope_total, bias_total

    def lrrt(self, loader: DataLoader, freeze_pretrained: bool = False):
        """
        Learning Rate Range Test; basic idea:
        for each learning rate in a set of learning rate candidates:
            load a checkpoint
            train from the checkpoint on a small amount of batches
            determine the slope of the batch losses
            return the learning rate that creates the steepest negative slope

        modified to rerun with a decayed set of learning rate candidates
        until a max number of iterations or a certain slope is reached.

        :return: best learning rate, best loss slope
        """
        print("lr search using lrrt")
        slope_desired_found = False
        candidate_lrs = self.setup.lrrt_initial_candidates
        lr_best_total = np.inf
        slope_best_total = np.inf
        for decay_it in range(self.setup.lrrt_max_decays + 1):
            candidate_slopes = np.zeros(shape=len(candidate_lrs))
            for i, lr_candidate in enumerate(candidate_lrs):
                module = torch.load(self.setup.checkpoint_running)
                optimizer = self.setup.optimizer_class(params=module.parameters(), lr=lr_candidate)
                candidate_slopes[i] = self.train_n_batches(module=module,
                                                           optimizer=optimizer,
                                                           n_batches=self.setup.lrrt_n_batches,
                                                           freeze_pretrained=freeze_pretrained,
                                                           loader=loader)[1]
            best_candidate_slope_id = np.argmin(candidate_slopes)
            best_candidate_slope = candidate_slopes[best_candidate_slope_id]
            best_candidate_lr = candidate_lrs[best_candidate_slope_id]
            if best_candidate_slope < slope_best_total:
                slope_best_total = best_candidate_slope
                lr_best_total = best_candidate_lr
            if slope_best_total < self.setup.lrrt_slope_desired:
                slope_desired_found = True
                break
            else:
                candidate_lrs = candidate_lrs * self.setup.lrrt_decay
        if not slope_desired_found:
            print("lr with desired loss slope", self.setup.lrrt_slope_desired, "not found. using approx best lr")
        print("best loss slope", slope_best_total, "best lr", lr_best_total)
        return lr_best_total, slope_best_total


class Debugger(BatchHandler):
    def __init__(self, setup: Setup):
        super(Debugger, self).__init__(setup=setup)

    def overfit_one_batch(self, module: Module,
                          batch_debug: list,
                          n_iters: int,
                          lrrt_loader: DataLoader = None,
                          lr: float = 1e-5,
                          freeze_pretrained: bool = False):
        if lrrt_loader is not None:
            lr, _ = self.lrrt(loader=lrrt_loader, freeze_pretrained=freeze_pretrained)
        optimizer = self.setup.optimizer_class(params=module.parameters(), lr=lr)

        module.train()
        losses = []
        for _ in range(n_iters):
            losses.append(self.train_batch(module=module, optimizer=optimizer, batch=batch_debug,
                                           freeze_pretrained=freeze_pretrained))
        return module, losses


class Visualizer:
    def __init__(self):
        pass

    @staticmethod
    def largest_divisor(n: int):
        i = n // 2
        while i > 1:
            if n % i == 0:
                return i
            i -= 1
        return 1

    def lines_multiplot(self, lines: list, title: str, multiplot_titles: list, y_label: str, x_label: str, file_name: str):
        """
        creates multiple lines in the same subplot
        :param lines:
        :param title:
        :param multiplot_titles:
        :param y_label:
        :param x_label:
        :param file_name:
        :return:
        """
        plt.figure(figsize=(4, 4))
        for i, line in enumerate(lines):
            plt.plot(range(len(line)), line, label=multiplot_titles[i])
        plt.ylabel = y_label
        plt.xlabel = x_label
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"../monitoring/{file_name}.png")

    def lines_subplot(self, lines: list, title: str, subplot_titles: list, y_label: str, x_label: str, file_name: str):
        """
        creates multiple lines in individual subplots

        :param lines:
        :param title:
        :param subplot_titles:
        :param y_label:
        :param x_label:
        :param file_name:
        :return:
        """
        n_lines = len(lines)
        n_cols = self.largest_divisor(n=n_lines)
        n_rows = n_lines // n_cols
        plt.figure(figsize=(n_cols*4, n_rows*4))
        plt.suptitle(title)
        for i in range(n_lines):
            plt.subplot(n_rows, n_cols, i + 1)
            plt.title(subplot_titles[i])
            plt.ylabel = y_label
            plt.xlabel = x_label
            plt.plot(range(len(lines[i])), lines[i])
        plt.tight_layout()
        plt.savefig(f"../monitoring/{file_name}.png")


class Trainer(BatchHandler):
    def __init__(self, setup: Setup):
        super(Trainer, self).__init__(setup=setup)

    def loss_epoch_eval(self, module: Module, loader_eval: DataLoader):
        batch_losses = np.zeros(len(loader_eval))
        for batch_nr, batch in enumerate(loader_eval):
            batch_losses[batch_nr] = self.loss_batch_eval(module=module, batch=batch)
        return float(batch_losses.mean())

    def losses_epoch_eval(self, module: Module):
        loss_epoch_train = self.loss_epoch_eval(module=module, loader_eval=self.setup.loader_train)
        loss_epoch_val = self.loss_epoch_eval(module=module, loader_eval=self.setup.loader_val)
        return loss_epoch_train, loss_epoch_val

    def train_n_epochs_initial_lrrt(self, n_epochs: int, freeze_pretrained: bool = False):
        """
        determines the initial learning rate per epoch using lrrt.

        :param int n_epochs: #training epochs after determining the initial learning rate with lrrt
        :param bool freeze_pretrained:
        :return: trained module
        """
        module = torch.load(self.setup.checkpoint_running)
        loss_train, loss_val_last = self.losses_epoch_eval(module=module)
        print("initial eval loss val", loss_val_last, "initial eval loss train", loss_train)
        for epoch in range(1, n_epochs + 1):
            print("training epoch", epoch)
            lr_best, _ = self.lrrt(freeze_pretrained=freeze_pretrained, loader=self.setup.loader_train)
            module = torch.load(self.setup.checkpoint_running).to(self.setup.device)
            optimizer = self.setup.optimizer_class(params=module.parameters(), lr=lr_best)
            self.train_n_batches(module=module, optimizer=optimizer, n_batches=len(self.setup.loader_train),
                                 freeze_pretrained=freeze_pretrained, loader=self.setup.loader_train)

            loss_train, loss_val = self.losses_epoch_eval(module=module)
            print("eval loss val", loss_val, "eval loss train", loss_train)
            torch.save(module, self.setup.checkpoint_running)
            torch.save(module, self.setup.checkpoint_final)
        return torch.load(self.setup.checkpoint_final)

    def train_n_epochs_early_stop_initial_lrrt(self, max_epochs: int, freeze_pretrained: bool = False):
        """
        determines the initial learning rate per epoch using lrrt.
        early stops (naively after one early stop violation)

        :param int max_epochs: max #training epochs after determining the initial learning rate with lrrt
        :param bool freeze_pretrained:
        :return: early stopped trained module, lrrt chosen learning rates, epoch train losses, epoch val losses
        """
        es_violations = 0
        losses_train = []
        losses_val = []
        best_lrs = []

        module = torch.load(self.setup.checkpoint_running)
        loss_train, loss_val_last = self.losses_epoch_eval(module=module)
        print("initial eval loss val", loss_val_last, "initial eval loss train", loss_train)
        losses_train.append(loss_train)
        losses_val.append(loss_val_last)
        best_lrs.append(0)

        for epoch in range(1, max_epochs + 1):
            print("training epoch", epoch)

            # lrrt
            lr_best, _ = self.lrrt(freeze_pretrained=freeze_pretrained,
                                   loader=self.setup.loader_train)

            # epoch training
            module = torch.load(self.setup.checkpoint_running).to(self.setup.device)
            optimizer = self.setup.optimizer_class(params=module.parameters(), lr=lr_best)
            self.train_n_batches(module=module,
                                 optimizer=optimizer,
                                 n_batches=len(self.setup.loader_train),
                                 freeze_pretrained=freeze_pretrained,
                                 loader=self.setup.loader_train)

            # epoch evaluation
            loss_train, loss_val = self.losses_epoch_eval(module=module)
            print("eval loss val", loss_val, "eval loss train", loss_train)
            losses_train.append(loss_train)
            losses_val.append(loss_val)
            best_lrs.append(lr_best)

            # early stopping checkpointing
            if loss_val < loss_val_last:
                torch.save(module, self.setup.checkpoint_running)
                torch.save(module, self.setup.checkpoint_final)
                print("loss improvement achieved, final checkpoint updated")
                loss_val_last = loss_val
                es_violations = 0
            else:
                es_violations += 1
                torch.save(module, self.setup.checkpoint_running)
                print("no loss improvement, es violations:", es_violations, "of", self.setup.es_max_violations)
                if es_violations == self.setup.es_max_violations:
                    print("early stopping")
                    break
        return torch.load(self.setup.checkpoint_final), best_lrs, losses_train, losses_val
