import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def defs(k1, k2, g, n, nei):
    def BZreaction(plate):
        padded=zeropad(plate)
        output=np.zeros(padded.shape)
        i=nei
        while i<padded.shape[0]-nei:
            j=nei
            while j<padded.shape[0]-nei:
                if padded[i, j]==0:
                    b=np.sum(padded[i-nei:i+nei+1, j-nei:j+nei+1]>=n)
                    a=np.sum(padded[i-nei:i+nei+1, j-nei:j+nei+1]>0)-b
                    output[i, j]=a/k1+b/k2
                elif padded[i, j]>=n:
                    output[i, j]=0
                else:
                    s=np.sum(padded[i-nei:i+nei+1, j-nei:j+nei+1])
                    b=np.sum(padded[i-nei:i+nei+1, j-nei:j+nei+1]>=n)
                    a=np.sum(padded[i-nei:i+nei+1, j-nei:j+nei+1]>0)-b
                    output[i, j]=s/a+b+1+g
                j+=1
            i+=1
        
        return output[nei:-1*nei, nei:-1*nei]

    def zeropad(plate):
        padded=np.zeros((plate.shape[0]+2*nei, plate.shape[0]+2*nei))
        padded[nei:plate.shape[0]+nei, nei:plate.shape[1]+nei]=plate
        return padded
    
    return BZreaction, zeropad

if __name__=='__main__':
	#setting
	k1=2
	k2=1
	g=10
	n=20
	l=100
	nei=1
	steps=250

	#preparation
	plate=np.random.rand(l*l).reshape(l, l)*n
	BZreaction, zeropad=defs(k1, k2, g, n, nei)
	fig=plt.figure()
	ims=[]

	#simulation
	for a in range(steps):
		plate=BZreaction(plate)
		plate[plate>n]=n
		im=plt.imshow(plate, animated=True)
		ims.append([im])

	ani=animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
	#ani.save('BZ.gif', writer='imagemagick')
	plt.show()
