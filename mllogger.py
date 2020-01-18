import os
import csv
import pickle
import matplotlib.pyplot as plt

# Directory structure
"""
#program
|__main.py
|__mllogger.py
|
|__dataset
|   |_train
|   |   |_class0
|   |   |_class1
|   |
|   |_test
|
|__log
|   |_modellog
|       |_log.csv
|
|__model
    |_modelsave.pkl.tar
"""

class Logger():
    def __init__(self, logger_name, allow_duplicate=False, save_inside=False):
        """
        logger_name : String. Name logger's directory
        allow_duplicate : Boolean. If False, log/model will be saved as its version. Defualt is False. 
        save_inside : Boolean. If True, log/model will be saved in current directory. 
                      If False, log/model will be saved in previous directory. Defualt is False. 
        """
        # set save path
        global log_path
        log_path = "./log"
        global model_path
        model_path = "./model/"

        if not save_inside:
            log_path = "../log"
            model_path = "../model/"

        self.logger_name = logger_name
        self.allow_duplicate = allow_duplicate
        logger_path = log_path+"/"+logger_name
        try:
            os.makedirs(logger_path)
            print("Make a new directory at "+log_path)
        except FileExistsError:
            # directory already exists
            print("The directory already exists.")
        
        print("#"*50)

    def model_log(self, root, model):
        # safty make a directory only use for Python 3.2 or above.
        os.makedirs(model_path, exist_ok=True)
        # save a model as model.pkl.tar
        save_path = model_path+root+".pkl.tar"
        if not self.allow_duplicate:
            count = 1
            while os.path.exists(save_path):
                count += 1
                save_path = model_path+root+"_ver_"+str(count)+".pkl.tar"

        pickle.dump(model, open(save_path,'wb'))

    def make(self, log_name):
        if type(log_name)==str:
            str_name = log_name
            log_name = []
            log_name.append(str_name)

        def make_sheet(log_name):
            log_root = log_path+"/"+self.logger_name
            log = Log_sheet(sheet_name=log_name, 
                            sheet_root=log_root)
            log.allow_duplicate = self.allow_duplicate
            print("The log file, %s, is ready." %(log_name))
            print("#"*50)

            return log
            
        return {name:make_sheet(name) for name in log_name}
    
    def plot_compare(self, a_log, b_log, x_label="Epoches", y_label=None, line_label_a=None, line_label_b=None, title=None):
        x, y_a = a_log.read()
        _, y_b = b_log.read()

        plt.plot(x, y_a, label=line_label)
        plt.plot(x, y_b, label=line_label)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        if line_label:
            plt.legend()

        if a_log.sheet_name and b_log.sheet_name:
            save_name = a_log.sheet_name + "_and_" + b_log.sheet_name
        else:
            save_name = "thisandthat"

        plt.savefig(log_path+"/"+self.logger_name+"/compare_"+save_name+".png")
        plt.show()


class Log_sheet:
    def __init__(self, sheet_name=None, sheet_root=None, sheet_path=None):
        self.log = []
        self.sheet_name = sheet_name
        self.sheet_root = sheet_root
        if sheet_path:
            self.save_path = sheet_path

    def record(self, value):
        self.log.append(value)

    def save(self):
        list_values = self.log
        if self.sheet_name and self.sheet_root:
            save_path = self.sheet_root+"/"+self.sheet_name+".csv"
            count = 1
            if not self.allow_duplicate:
                while os.path.exists(save_path):
                    count += 1
                    save_path = self.sheet_root+"/"+self.sheet_name+"_ver_"+str(count)+".csv"
        
            writer = csv.writer(open(save_path, 'w'), delimiter=',', lineterminator='\n')
            writer.writerow(list_values)
            print("A log file, %s, has been saved at %s" %(self.sheet_name+"_ver_"+str(count), self.sheet_root))
            print("#"*50)
            self.save_path = save_path
        
        else:
            print("ERROR!, you have to name and specify directory for the log file.")

    def get(self, all=False):
        if self.save_path:
            save_path = self.save_path
            _, values = self.read()
            if all:
                print("This is all data contained in "+save_path)
                return values
            else:
                print("This is the final datum contained in "+save_path)
                return values[-1]
        
        else:
            print("ERROR!, you must locate the save path")

    def plot(self, x_label="Epoches", y_label=None, line_label=None, title=None):
        if self.save_path:
            save_path = self.save_path
            x, y = self.read()

            plt.plot(x, y, label=line_label)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(title)
            if line_label:
                plt.legend()

            plt.savefig(save_path[:-4]+".png")
            print("The graph has been saved.")

            plt.show()
            print("This is the graph from "+save_path)
        
        else:
            print("ERROR!, you must locate the save path")

    def read(self):
        if self.save_path:
            save_path = self.save_path
            x = []
            y = []
            with open(save_path, 'r') as csvfile:
                count = 1
                reader= csv.reader(csvfile, delimiter=',')
                for row in list(reader)[0]:
                    x.append(count)
                    y.append(float(row))
                    count += 1

            return x, y

        else:
            print("ERROR!, you must locate the save path")
