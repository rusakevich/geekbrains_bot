#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sts
#get_ipython().magic('matplotlib inline')


# # Обернутая непрерывная случайная величина Коши

# In[2]:


cauchy = sts.wrapcauchy(0.3)
#генерируем выборку объемом 1000
sample = cauchy.rvs(size=1000)


# Строим график плотности распределения и гистограмму выборки объемом 1000

# In[3]:


x = np.linspace(-1,7,100)
pdf = cauchy.pdf(x)
plt.plot(x, pdf)
plt.hist(sample,density=True)
plt.ylabel('$f(x)$')
plt.xlabel('$x$')
plt.title("histogram and theoretical distribution density")
plt.show()


# In[4]:


#считаем значения параметров нормального распределения используя ЦПТ
EX = cauchy.mean() #мат. ожидание
sigma5 = cauchy.std()/5**0.5 #стандартное отклонение выборки объемом 5
sigma10 = cauchy.std()/10**0.5 #стандартное отклонение выборки объемом 10 
sigma50 = cauchy.std()/50**0.5 #стандартное отклонение выборки объемом 50
#находим выборочные средние выборок объемов 5, 10 и 50
average5 = []
average10 = []
average50 = []
i = 0
while i<1000:
    g5 = cauchy.rvs(size=5)
    g10 = cauchy.rvs(size=10)
    g50 = cauchy.rvs(size=50)
    average5.append(sum(g5)/len(g5))
    average10.append(sum(g10)/len(g10))
    average50.append(sum(g50)/len(g50))
    i+=1
    


# Строим графики нормальных распределений и гистограммы выборочных средних (5,10 и 50)

# In[5]:


x = np.linspace(0,5,100)
norm_5 = sts.norm(EX, sigma5)
pdf = norm_5.pdf(x)
plt.plot(x, pdf)
plt.hist(average5,density=True)
plt.ylabel('$f(x)$')
plt.xlabel('$x$')
plt.title("n=5")
plt.show()

# In[6]:


x = np.linspace(0,5,100)
norm_10 = sts.norm(EX, sigma10)
pdf = norm_10.pdf(x)
plt.plot(x, pdf)
plt.hist(average10,density=True)
plt.ylabel('$f(x)$')
plt.xlabel('$x$')
plt.title("n=10")
plt.show()

# In[7]:


x = np.linspace(0,5,100)
norm_50 = sts.norm(EX, sigma50)
pdf = norm_50.pdf(x)
plt.plot(x, pdf)
plt.hist(average50,density=True)
plt.ylabel('$f(x)$')
plt.xlabel('$x$')
plt.title("n=50")
plt.show()
