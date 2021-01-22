import os
import subprocess
import sys
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class FullProf:

    def __init__(self, path: str = os.environ['FullProf']):
        self.fullprof_path = path

    def run_pcr(self, pcr_file: str):
        args = [os.path.join(self.fullprof_path, 'fp2k'), pcr_file]
        process = subprocess.Popen(args, shell=True)
        time.sleep(1)
        fig, ax, line = self.plot_prf(pcr_file[:-3] + 'prf')
        while process.poll() is None:
            self.plot_prf(pcr_file[:-3] + 'prf', fig=fig, ax=ax, line=line)

    def read_prf(self, prf_file: str):
        return pd.read_csv(prf_file, delimiter='\t', skiprows=3)

    def plot_prf(self, prf_file: str, fig=None, ax=None, line=None):
        data = self.read_prf(prf_file)
        if fig is None:
            fig, ax = plt.subplots()
            ax.plot(data[' 2Theta'], data['Yobs'])
            line = ax.plot(data[' 2Theta'], data['Ycal'])
            plt.draw()
        else:
            line[0].set_ydata(data['Ycal'])
            plt.draw()
        return fig, ax, line


if __name__ == "__main__":
    fp = FullProf()
    fp.run_pcr(sys.argv[1])
