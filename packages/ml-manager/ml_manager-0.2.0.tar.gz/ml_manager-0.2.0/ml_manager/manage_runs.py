import os
import shutil
from matplotlib import pyplot as plt
import torch
import numpy as np
import pandas as pd
import requests


class MANAGE_RUN:
    def __init__(self, parent_dir: str, exp_prefix: str = None, exp: str = None,
                 early_stopping: dict = None, patience: int = None, metrics: list = None, chat_id: str = None, token: str = None):
        assert not((exp_prefix == None and exp==None) or (exp_prefix != None and exp!=None))

        self.url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text="
        self.parent_dir = parent_dir
        check  = os.path.exists(self.parent_dir + "/runs")
        self.metrics = metrics
        if not check:
            os.mkdir(self.parent_dir+"/runs")
        if exp is None:
            exp = exp_prefix+"_exp_"+str(len(os.listdir(self.parent_dir+"/runs"))+1)
            os.mkdir(self.parent_dir+"/runs/"+exp)

        self.exp = exp
        self.run_dir = os.path.join(self.parent_dir, "runs",exp)
        self.losses = {
            "train": [],
            "valid":[]
        }
        if self.metrics  is not None:
            self.add_metrics_tracking_dictionary()

        self.fig_num = 0
        if early_stopping is not None:
            stop_on = early_stopping["stop_on"]
            self.patience = patience
            stop_on_1, self.stop_on_2 = stop_on.split("_")
            if self.stop_on_2 == "loss":
                self.early_stopping_guide = self.losses[stop_on_1]
            else:
                self.early_stopping_guide = self.metric_dictionaries[self.stop_on_2][stop_on_1]
            self.mode = early_stopping["mode"]
        self.improvements = []

    def send_message(self, message):
        try:
            _ = requests.get(self.url+message).json()
        except Exception as e:
            print(e)


    def add_metrics_tracking_dictionary(self,):
        self.metric_dictionaries = {}
        for m in self.metrics:
            self.metric_dictionaries[m] = {
                "train": [],
                "valid":[]
            }
        
    def save_artifacts(self, file_names):
        os.mkdir(os.path.join(self.run_dir, "artifacts"))
        for f in file_names:
            shutil.copy(os.path.join(self.parent_dir, f), os.path.join(self.run_dir, "artifacts", f))

        
    def save_weights(self, dictionary, which = "train"): 
        last = self.losses[which][-1]
        if len(self.losses[which])>1:
            past_best = min(self.losses[which][:-1])
        else:
            past_best = float("inf")
        if last<past_best:
            torch.save(dictionary, self.run_dir+"/best_run.pt")
            print(f"saved weights at loss = {last}")
    
    def check_early_stopping(self, ):
        if len(self.early_stopping_guide)>self.patience:
            if self.mode == "min":
                self.improvements.append(min(self.early_stopping_guide[:-1])-self.early_stopping_guide[-1])
            elif self.mode == "max":
                self.improvements.append(self.early_stopping_guide[-1]-max(self.early_stopping_guide[:-1]))
            else:
                raise Exception(f"Unknow mode {self.mode}")
            return not (np.asarray(self.improvements[-self.patience:])>0).any()

        return False

    def save_history(self,):
        history = {}
        history.update(self.losses)
        if self.metrics is not None:
            for m in self.metric_dictionaries.keys():
                history.update(
                    {
                        f"train_{m}": self.metric_dictionaries[m]["train"],
                        f"valid_{m}": self.metric_dictionaries[m]["valid"]
                    }
                )
        pd.DataFrame({key:pd.Series(value, dtype="float64") for key, value in history.items()}).to_csv(self.run_dir+"/history.csv")


    def track_loss(self, loss, which = "train"):
        self.losses[which].append(loss)
        

    def track_metrics(self, metric_values, which = "train"):
        for m, value in zip(self.metrics,metric_values):
            self.metric_dictionaries[m][which].append(value)


    def plot_loss(self):
        plt.figure(self.fig_num)
        plt.plot(list(range(len(self.losses["train"]))), self.losses["train"], label = "train_loss")
        plt.plot(list(range(len(self.losses["valid"]))), self.losses["valid"], label = "valid_loss")
        plt.title("loss curve")
        plt.xlabel("Epochs")
        plt.ylabel("loss")
        plt.savefig(self.run_dir+"/loss curve.png")
        self.fig_num+=1

    def plot_metrics(self):
        if len(self.metric_dictionaries.keys())==0:
            return
        for m in self.metric_dictionaries.keys():
            plt.figure(self.fig_num)
            _=self.metric_dictionaries[m]
            plt.plot(list(range(len(_["train"]))), _["train"], label = f"train_{m}")
            plt.plot(list(range(len(_["valid"]))), _["valid"], label = f"test_{m}")
            plt.title(f"{m} curve")
            plt.xlabel("Epochs")
            plt.ylabel(f"{m}")
            plt.savefig(self.run_dir+f"/{m}_curve.png")
            self.fig_num+=1
    def plot_all(self, ):
        self.plot_loss()
        self.plot_metrics()

    def delete_exp(self,):
        shutil.rmtree(self.run_dir)

    def save_dataframe(self, df, name):
        if type(df) == dict:
            pd.DataFrame(df).to_csv(self.run_dir + f"/{name}.csv")
            return
        df.to_csv(self.run_dir + f"/{name}.csv")
