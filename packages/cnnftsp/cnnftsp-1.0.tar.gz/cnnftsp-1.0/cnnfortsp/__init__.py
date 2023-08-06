import numpy as np
import torch
from scipy.integrate import odeint
from tqdm.notebook import tqdm
from numpy import tan,arctan,exp,sqrt,arcsin,sin,pi
import matplotlib.pyplot as plt
import random
import time
def Inoue_Nagayoshi(d,totaln,x0=0,y0=0,s=50,A=50,A_B=10,theta=-0.5,nin=4,a=4,b=3.995,eps=.002,best=[0],init_model='rand',N_freeze_limit=8): 
    def activation(xvh,yvh):
        return np.where(abs(xvh-yvh) <eps, 1, 0)
    def f(xv):
        return a*xv*(1-xv)
    def g(yv):
        return b*yv*(1-yv)
    def eom(xv,yv,I):
        if (2*I+1)==0:
            print("Noooooo")
        return ((f(xv)*(1+I)+I*g(yv))/(2*I+1),(g(yv)*(1+I)+I*f(xv))/(2*I+1))
    def delta(ii,jj):
        return int(ii==jj)
    def init():
        if init_model == 'rand':
            xj=(np.random.random((N,N)))
            yj=xj+(np.random.random((N,N))-0.5)/100
            return (xj,yj,activation(xj,yj))
        if init_model == 'given':
            return (x0,y0,activation(x0,y0))
    def Energy1(uv,wv):
        Ev = -np.einsum('ijkl,ij,kl', wv, uv, uv) / 2
        return Ev
    def Energy2(uv,wv):
        Ev = -np.einsum('ijkl,ij,kl', wv, uv, uv) / 2 - s * np.sum(uv)+N*A
        return Ev
    tt=time.time()
    B=A/A_B
    N=len(d)
    xs,ys,u=init()
    I=np.zeros((N,N))
    ar=np.arange(N)
    # Es2=np.zeros(totaln)
    w=np.zeros((N,N,N,N))
    for i in ar:
        for k in ar:
            for j in ar:
                for l in ar:
                    w[i,k,j,l]=-A*(delta(i,j)*(1-delta(k,l))+delta(k,l)*(1-delta(i,j)))-B*d[i,j]*(delta(l,(k+1)%N)+delta(l,(k-1)%N))
    w1=np.zeros((N,N,N,N))
    for i in ar:
            for k in ar:
                for j in ar:
                     for l in ar:
                        w1[i,k,j,l]=-A*(delta(i,j)*(1-delta(k,l))+delta(k,l)*(1-delta(i,j)))
    N_valid=0

    Emin_best=0
    Step=totaln
    if len(best)>1:
        Emin_best = Energy2(best,w)
    Emin = Energy2(u,w)
    ubest=u
    u_freeze = u
    N_freeze = 0
    Ns=np.arange(totaln)
    # print(len(Ns))
    # print(u)
    for n in tqdm(Ns[1:],total=totaln-1,leave=False): 
    # for n in Ns[1:]:
        I.fill(0)
        I=np.einsum('ijkl,kl->ij', w, u)+s-theta
        # print(xs)
        I=np.where(I>0,I,0)
        for inter in range(nin):
            for i in ar:
                for j in ar:
                    xs[i,j],ys[i,j]=eom(xs[i,j],ys[i,j],I[i,j])
        # print('After',xs,ys)
        u = activation(xs,ys)
        if np.array_equal(u,u_freeze):
            N_freeze+=1
        else:
            if Energy1(u,w1)==0:
                N_valid+=1
        if N_freeze_limit>8:
            xs,ys,u=init()
            N_freeze_limit=0
        u_freeze=u
        # Es2[n]=Energy2(u,w)
        Ecan = Energy2(u,w)
        
            
        if Ecan<Emin:
            Emin=Ecan
            ubest=u
            Step = n
            Time = time.time()-tt
            if Ecan<=Emin_best:
                break
    # plt.plot(Ns[1:],Es2[1:])
    return (ubest,Emin,Emin_best,Step,Time,N_valid)
def random_cities(N):
    cities=np.array([[0,0]])
    for ii in range(N):
        cities=np.append(cities,[np.random.random(2)],axis=0)
    cities=np.delete(cities,0,axis=0)
    d=np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            x1,y1=cities[i]
            x2,y2=cities[j]
            d[i,j]=sqrt((x1-x2)**2+(y1-y2)**2)
    return (d,cities)
def plot_road(ud,cities,axs = plt,labels=''):
    cold = np.argmax(ud[:,0])
    axs.plot(cities[:,0],cities[:,1],'o',markersize=10)
    for j in range(len(cities)-1):
        cnew = np.argmax(ud[:,j+1])
        x1,y1=cities[cold]
        x2,y2=cities[cnew]
        axs.plot([x1,x2],[y1,y2])
        cold=cnew
    cnew = np.argmax(ud[:,0])
    x1,y1=cities[cold]
    x2,y2=cities[cnew]
    axs.plot([x1,x2],[y1,y2])
    # axs.legend()
    axs.show()
def analyze(nni,ii,fld):
    print(fld)
    print('Number of cities: %i'%num_cities)
    print("Number of seeds: %i"%seeds)
    print('Max steps: %i'%num_steps_1)
    for st,t,nin in zip(steps[nni,ii],times[nni,ii],ninm):
        print('Nin = %i: %f steps, %f times'%(nin,np.mean(st),np.mean(t)))
    plt.plot(ninm,np.mean(steps[nni,ii],axis=1)/max(np.mean(steps[nni,ii],axis=1)),label = 'Steps')
    plt.plot(ninm,np.mean(times[nni,ii],axis=1)/max(np.mean(times[nni,ii],axis=1)),label = 'Times')
    if min(np.mean(energies[0,0],axis=1))!=max(np.mean(energies[0,0],axis=1)):
        plt.plot(ninm,(np.mean(energies[nni,ii],axis=1)-min(np.mean(energies[nni,ii],axis=1)))/(max(np.mean(energies[nni,ii],axis=1))-min(np.mean(energies[nni,ii],axis=1))),label = 'Energies')
    
    plt.ylabel('Normalized number of steps/time:')
    plt.xlabel('Nin parameter')
    plt.legend()
    plt.ylim(0,1.1)
    # plt.yscale('log')
    plt.savefig(fld+str(num_cities)+'.png')
    plt.show()
def analyze2(ii,jj,jjj):
    print('Number of cities: %i'%num_cities)
    print("Number of seeds: %i"%seeds)
    print("Number of nin: %i"%jjj)
    print('Max steps: %i'%num_steps_1)
    print('        ',NNS)
    for seed in range(seeds):
            print('Seed %i:  '%seed,end='') 
            for nnn in np.arange(len(NNS)):
                print('%i steps'%int(steps[nnn,ii,jj,seed]),end='  ')
            print('')
    print('        ',NNS)
    for seed in range(seeds):
            print('Seed %i:  '%seed,end='')
            for nnn in np.arange(len(NNS)):
                print('%.2f sec'%times[nnn,ii,jj,seed],end='  ')
            print('')
    print('        ',NNS)
    for seed in range(seeds):
            print('Seed %i:  '%seed,end='')
            for nnn in np.arange(len(NNS)):
                print('%.2f     '%energies[nnn,ii,jj,seed],end='  ')
            print('')
    for nni,NN in enumerate(NNS):
        for st,t,nin in zip(steps[nni,ii],times[nni,ii],ninm):
            print('%s: %f steps, %f times'%(NN,np.mean(st),np.mean(t)))
def rand_init(N,model='rand',T=0):
    if model=='rand':
        xj=np.random.random((N,N))-0.5
    if model=='sym':
        if T==0:
            T=1/50000
        # xj  = T*np.log[-(u/(-1 + u))]
        u00 = 1/N
        u=((np.random.random((N,N))-0.5)*0.2+1)*u00
        xj = T*np.log(-(u/(-1 + u)))
    return (xj)


def Duffing(d,totaln,x0=0,s=50,A=50,A_B=10,theta=0,nin=4,eta=100,best=[0],T=0,init_model='rand',Lambda=0.25,ddt=0.01): 
    def activation(xvh):
        if T==0:
            return np.where(xvh >= 0, 1, 0)
        else:
            return 1/(1+exp(-xvh/T))
    def delta(ii,jj):
        return int(ii==jj)
        
    def init():
        if init_model == 'rand':
            xj=np.random.random((N,N))-0.5
            yj=np.random.random((N,N))-0.5
            return (xj,yj,activation(xj))
        if init_model == 'given':
            return (x0,activation(x0))
    def model_disipative(u, t,ee,eb):
        return (u[1], ee-u[1]*alpha + beta*u[0] -gamma*(u[0])**3 + f*np.cos(omega*t))
    def xn(Tend,e,dt,xold,yold):
        NN = 1
        tT = np.linspace((Tend-1)*dt, Tend*dt, int(NN+1))
        x0=xold
        y0=yold
        z1 = odeint(model_disipative, [x0, y0], tT,args=(e,e))
        return (z1[-1,0],z1[-1,1])
    def Energy1(uv,wv):
        Ev = -np.einsum('ijkl,ij,kl', wv, uv, uv) / 2 
        return Ev
    def Energy2(uv,wv):
        Ev = -np.einsum('ijkl,ij,kl', wv, uv, uv) / 2 - s * np.sum(uv)+N*A
        return Ev
    tt=time.time()
    f=1
    alpha=1
    beta=10
    gamma=100
    omega=3.5
    B=A/A_B
    N=len(d)
    xs,ys,u=init()
    I=np.zeros((N,N))
    ar=np.arange(N)
    # Es2=np.zeros(totaln)
    w=np.zeros((N,N,N,N))
    w1=np.zeros((N,N,N,N))
    for i in ar:
            for k in ar:
                for j in ar:
                     for l in ar:
                        w1[i,k,j,l]=-A*(delta(i,j)*(1-delta(k,l))+delta(k,l)*(1-delta(i,j)))
    N_valid=0
    u_freeze=u

    for i in ar:
        for k in ar:
            for j in ar:
                for l in ar:
                    w[i,k,j,l]=-A*(delta(i,j)*(1-delta(k,l))+delta(k,l)*(1-delta(i,j)))-B*d[i,j]*(delta(l,(k+1)%N)+delta(l,(k-1)%N))

    Emin_best=0
    Step=totaln
    if len(best)>1:
        Emin_best = Energy2(best,w)
    Emin = Energy2(u,w)
    Time = time.time()-tt
    ubest=u
    Ns=np.arange(totaln)+60
    for n in tqdm(Ns[1:],total=totaln-1,leave=False): 
    # for n in Ns[1:]:
        I.fill(0)
        I=np.einsum('ijkl,kl->ij', w, u)+s+theta
        eps=Lambda*arctan(I)
        vec_g = np.vectorize(xn)
        xs,ys = vec_g(n,eps,ddt,xs,ys)
        u = activation(xs)
        if np.array_equal(u,u_freeze) ^ True:
            if Energy1(u,w1)==0:
                N_valid+=1
        u_freeze=u
        # Es2[n]=Energy2(u,w)
        Ecan = Energy2(u,w)
        if Ecan<Emin:
            Emin=Ecan
            ubest=u
            Step = n-60
            Time = time.time()-tt
            if Ecan<=Emin_best:
                break
    # plt.plot(Ns[1:],Es2[1:])
    return (ubest,Emin,Emin_best,Step,Time,N_valid)
def SinMap(d,totaln,x0=0,s=50,A=50,A_B=10,theta=0,nin=1,eta=100,best=[0],T=0,init_model='rand'): 
    def activation(xvh):
        if T==0:
            return np.where(xvh >= 0, 1, 0)
        else:
            return 1/(1+np.exp(-xvh/T))
    def g(xv,I):
        e = 0.25/(1+eta*I**2)
        if xv<0:
            if I>0:
                e=0.5-e
            return 0.5*sin(2*xv*(pi+arcsin(2*e)))
        else:
            if I<0:
                e=0.5-e
            return 0.5*sin(2*xv*(pi+arcsin(2*e)))
    def delta(ii,jj):
        return int(ii==jj)
    def init():
        if init_model == 'rand':
            xj=np.random.random((N,N))-0.5
            return (xj,activation(xj))
        if init_model == 'given':
            return (x0,activation(x0))
    def Energy1(uv,wv):
        Ev = -np.einsum('ijkl,ij,kl', wv, uv, uv) / 2
        return Ev
            
    def Energy2(uv,wv):
        Ev = -np.einsum('ijkl,ij,kl', wv, uv, uv) / 2 - s * np.sum(uv)+N*A
        return Ev
    B=A/A_B
    N=len(d)
    xs,u=init()
    I=np.zeros((N,N))
    ar=np.arange(N)
    # Es2=np.zeros(totaln)
    w=np.zeros((N,N,N,N))
    w1=np.zeros((N,N,N,N))
    for i in ar:
        for k in ar:
            for j in ar:
                for l in ar:
                    w[i,k,j,l]=-A*(delta(i,j)*(1-delta(k,l))+delta(k,l)*(1-delta(i,j)))-B*d[i,j]*(delta(l,(k+1)%N)+delta(l,(k-1)%N))
    for i in ar:
        for k in ar:
            for j in ar:
                 for l in ar:
                    w1[i,k,j,l]=-A*(delta(i,j)*(1-delta(k,l))+delta(k,l)*(1-delta(i,j)))
    Emin_best=0
    Step=totaln
    if len(best)>1:
        Emin_best = Energy2(best,w)
    Emin = Energy2(u,w)
    ubest=u
    N_valid=0
    Ns=np.arange(totaln)
    u_freeze=u
    Earray = np.zeros(len(Ns))
    Time=0
    tt=time.time()
    for n in tqdm(Ns[1:],total=totaln-1,leave=False): 
    # for n in Ns[1:]:
        I=np.einsum('ijkl,kl->ij', w, u)+s+theta
        vec_g = np.vectorize(g)
        for it in range(nin):
            xs = vec_g(xs, I)
            u = activation(xs)
        Ecan = Energy2(u,w)
        if np.array_equal(u,u_freeze) ^ True:
            if Energy1(u,w1)==0:
                N_valid+=1
            u_freeze=u
        Earray[n]=Ecan
        if Ecan<Emin:
            Emin=Ecan
            ubest=u
            Step = n
            Time = time.time()-tt
            # if Ecan<=Emin_best:
            #     break
    # plt.plot(Earray[1:])
    # plt.xlim(0,200)
    # plt.show()
    return (ubest,Emin,Emin_best,Step,Time,N_valid)