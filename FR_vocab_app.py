#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#%reset


# In[3]:


import pandas as pd
import numpy as np
from random import sample, shuffle
from tkinter import*
from tkinter import messagebox
import csv
pd.options.mode.chained_assignment = None
import tkinter.font as font


# In[4]:


file_name = 'FR_vocab.csv'
deja_connu_niveau = 4
n_per_group = 20


# In[55]:


mots = pd.read_csv(file_name, sep=';')


# In[56]:


mots.tail(10)


# In[57]:


mots.loc[np.isnan(mots['stage']), 'stage'] = 0
mots.loc[pd.isna(mots['type']), 'type'] = 'mot regulier'
mots = mots[(mots['stage']<deja_connu_niveau) & (mots['type'] != "n'importe")]
mots_connu = mots[(mots['stage']>=deja_connu_niveau) | (mots['type'] == "n'importe")].copy()
if len(mots_connu)>0:
    mots_connu.to_csv(f"mots_revise_{datetime.now().date()}_{str(datetime.now().hour).zfill(2)}_{str(datetime.now().minute).zfill(2)}.csv", index=False, encoding='utf-8-sig',sep=';')
mots = mots.sort_values(by = 'stage').reset_index(drop=True) 
mots['group'] = mots.index//n_per_group


# In[58]:


class App(Tk):
    def __init__(self, dictionary, n):
        super().__init__()
        self.group_num = 0
        self.vocab_num = 0
        self.dictionary = dictionary    
        
        self.verify_button = Button(self, text="OK!", command=self.verify, font = font.Font(size=25))
        self.verify_button.grid(row=2, column=11, columnspan=1)
        
        
        self.term_button = Button(self, text="N'importe", command=self.term, font = font.Font(size=25))
        self.term_button.grid(row=1, column=10, columnspan=1)
        
        self.conjunction_button = Button(self, text="Conjunction", command=self.conjunction, font = font.Font(size=25))
        self.conjunction_button.grid(row=1, column=11, columnspan=1)
        
        self.grammaire_button = Button(self, text="Grammaire", command=self.grammaire, font = font.Font(size=25))
        self.grammaire_button.grid(row=1, column=12, columnspan=1)
        
        self.label = None
        self.group = None
        self.choice_box = None
        self.n_per_group = n
        self.updatequestion()


    def get_choices(self):
        vocab_list = self.dictionary[self.dictionary['group']==self.group_num]['FR'].reset_index(drop=True) 
        vocab_list_EN = self.dictionary[self.dictionary['group']==self.group_num]['EN'].reset_index(drop=True)
        cs = sample([i for i in list(vocab_list_EN) if i != vocab_list_EN[self.vocab_num]], 4)
        cs.append(vocab_list_EN[self.vocab_num])
        shuffle(cs)

        return [vocab_list[self.vocab_num],vocab_list_EN[self.vocab_num],cs]
    
    def updatequestion(self):
        self.group = Label(self,
              text = '|  ' + str(self.group_num*self.n_per_group + self.vocab_num + 1) + 'e mot / '+ str(len(self.dictionary)),
              font = ("Times New Roman", 12), 
              padx = 10, pady = 10)
        self.group.grid(row=0, column=7, columnspan=6)
        
        self.label = Label(self,
              text = self.get_choices()[0],
              font = ("Times New Roman", 20), 
              padx = 10, pady = 10)
        self.label.grid(row=0, column=0, columnspan=2)

        #Create choices
        self.choice_box = Listbox(self, selectmode = "single", font = ("Times New Roman", 20),
                                  width=50, height=20)
        for col, var in enumerate(self.get_choices()[2]):
            self.choice_box.insert(col, var)
            self.choice_box.grid(row=1, column=0, columnspan=8)

    def term(self):
        self.dictionary['type'].iloc[self.group_num*self.n_per_group+self.vocab_num] = "n'importe"
    def grammaire(self):
        self.dictionary['type'].iloc[self.group_num*self.n_per_group+self.vocab_num] = "grammaire"
    def conjunction(self):
        self.dictionary['type'].iloc[self.group_num*self.n_per_group+self.vocab_num] = "conjunction"
        
    def verify(self):

        if self.choice_box.get(ACTIVE) == self.get_choices()[1]:
      
            self.dictionary['stage'].iloc[self.group_num*self.n_per_group+self.vocab_num] += 1
          
            messagebox.showinfo("Correct") 
        else:
            if self.dictionary['stage'].iloc[self.group_num*self.n_per_group+self.vocab_num] >=1:
                self.dictionary['stage'].iloc[self.group_num*self.n_per_group+self.vocab_num] -= 1     
            messagebox.showinfo(title="False", message = "It's "+self.get_choices()[1])

        self.choice_box.grid_remove()
        self.label.grid_remove()

        self.vocab_num += 1
        if self.vocab_num == len(self.dictionary[self.dictionary['group']==self.group_num]):
            self.dictionary.to_csv(file_name, index=False, encoding='utf-8-sig',sep=';')
            self.group_num += 1
            self.vocab_num =0
        if self.group_num ==len(self.dictionary['group'].unique()):
            self.group_num =0

        self.updatequestion()
    def save(self):
        self.dictionary['group'] = np.nan
        self.dictionary.to_csv(file_name, index=False, encoding='utf-8-sig',sep=';')


# In[59]:


if __name__ == "__main__":
    app = App(mots, n= n_per_group)
    app.iconbitmap(r'C:\\Users\\Admin\\Desktop\\FR_learning\\icon.ico')
    app.title('FR learning app')
    app.geometry("1200x500")
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            app.save()
            app.destroy()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()


# In[ ]:




