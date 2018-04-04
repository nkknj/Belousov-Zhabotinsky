import numpy as np
import matplotlib.pyplot as plt

#setting
connection=np.loadtxt('data.txt', delimiter=' ')
#connection[connection<(np.sum(connection)/np.sum(connection>0))]=0
connection+=connection.T	#undirected
connection=(connection>0)	#unweighted
for i in range(connection.shape[0]):
	connection[i, i]=0	#delete loop

n=50		#number of states (NOT THE NUMBER OF NODES!)
steps=250	#number of steps
g=0
k1=10
k2=5

sigma_n=1

#initialize
state=np.random.rand(connection.shape[0]).reshape(-1, 1)*n
post=np.zeros(connection.shape[0])

for t in range(steps):
	pre=np.zeros((connection.shape))
	pre+=state[:, -1]
	neigh_state=pre*connection	#i-th row means neighbor states around i-th node
	for i in range(connection.shape[0]):
		if state[i, -1]==0:
			b=np.sum(neigh_state[i]>=n)
			a=np.sum(neigh_state[i]>0)-b
			post[i]=a/k1+b/k2+np.random.randn(1)*sigma_n
		elif state[i, -1]>=n:
			post[i]=0
		else:
			b=np.sum(neigh_state[i]>=n)
			a=np.sum(neigh_state[i]>0)-b
			s=np.sum(neigh_state[i])
			if a>0:
				post[i]=s/a+b+1+g+np.random.randn(1)*sigma_n
			else:
				post[i]=n
			#if a>0:
			#	post[i]=s/a+b+1+g+state[i, -1]
			#else:
			#	post[i]=n
	post[post>n]=n
	state=np.c_[state, post]

plt.plot(state.T)
plt.show()
