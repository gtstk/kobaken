#(111)plane,(110)dilection strain
import numpy as np
import pandas as pd
import time

#parameter
L = 100
l = 2*L-1
splane = 100

#init spin
spin_twi = np.empty((l, l+2, l+2, 3))
for k in range(l):
    k_real = k/2
    for j in range(l+2):
        j_real =j/2
        for i in range(l+2):
            i_real = i/2
            flag = i_real.is_integer() and j_real.is_integer() and k_real.is_integer()
            if flag:
                if (i_real+j_real)%2==0:
                    spin_twi[k, j, i, :] = np.array([0, 0, -1])
                else:
                    spin_twi[k, j, i, :] = np.array([0, 0, 1])
            else:
                spin_twi[k, j, i, :] = np.array([0, 0, 0])
print(spin_twi)
spinmap = np.empty((l**3, 6))
for k in range(l):
    k_real = k/2
    for j in range(l):
        j_real = j/2
        for i in range(l):
            i_real = i/2
            id = l**2*k + l*j + i
            spinmap[id, :] = [i_real, j_real, k_real, spin_twi[k, j+2, i, 0], spin_twi[k, j+2, i, 1], spin_twi[k, j+2, i, 2]]
print("init spinmap:", spinmap)
f = pd.DataFrame(spinmap, columns=['rx', 'ry', 'rz', 'Sx', 'Sy', 'Sz'])
f.to_csv('init_spinmap_L{}.csv'.format(L), index=False, sep=' ')

strained_spin_twi = np.empty((l, l, l, 3))
#(111)plane, (110)direction strain
for k in range(l):
    k_real = k/2
    for j in range(l+2):
        j_real = (j-2)/2 #基準+2
        for i in range(l+2):
            i_real = i/2
            if (2<=j) and (i<=l-1):
                print("i,j,k:", i_real, j_real, k_real)
                strained_spin_twi[k, j-2, i, :] = spin_twi[k, j, i, :]
                sum_ijk = i_real+j_real+k_real
                flag = sum_ijk.is_integer()
                if flag and (splane <= sum_ijk):
                    #(110)direction movement
                    print("before:", spin_twi[k, j, i, :])
                    strained_spin_twi[k, j-2, i, :] = spin_twi[k, j-1, i+1, :]
                    print("after:", strained_spin_twi[k, j-2, i, :])
print("strained_spinmap:", strained_spin_twi)

spinmap = np.empty((l**3, 6))
for k in range(l):
    k_real = k/2
    for j in range(l):
        j_real = j/2
        for i in range(l):
            i_real = i/2
            id = l**2*k + l*j + i
            spinmap[id, :] = [i_real, j_real, k_real, strained_spin_twi[k, j, i, 0], strained_spin_twi[k, j, i, 1], strained_spin_twi[k, j, i, 2]]
print("strained spinmap:", spinmap)
f = pd.DataFrame(spinmap, columns=['rx', 'ry', 'rz', 'Sx', 'Sy', 'Sz'])
f.to_csv('strained_spinmap_L{}.csv'.format(L), index=False, sep=' ')

#main calc
for qz in np.arange(4.1):
    qz_real = qz/4
    for qy in np.arange(4.1):
        qy_real = qy/4
        print("qx_scan,qy,qz:", qy_real, qz_real)
        #time
        start = time.time()
        for qx in np.arange(L+0.1):
            qx_real = qx/L
            Q = np.array([qx_real, qy_real, qz_real])
            print("Q:", Q)

            sum_fq = 0
            for k in range(l):
                k_real = k/2
                for j in range(l):
                    j_real = j/2
                    for i in range(l):
                        i_real = i/2
                        sum_ijk = i_real+j_real+k_real
                        if flag:
                            Sz = int(strained_spin_twi[k, j, i, 2]) #spin
                            r = np.array([i_real, j_real, k_real]) #r
                            sum_fq += Sz * np.exp(2 * np.pi * 1j * np.dot(Q, r))
            Fq = abs(sum_fq)
            qmap = np.array([qx_real, qy_real, qz_real, Fq])
            print(qmap)
            id = int((L+1)**2 * qz + (L+1)*qy + qx)

            #save
            if id==0:
                f = pd.DataFrame([[qx_real, qy_real, qz_real, Fq]], columns=['qx', 'qy', 'qz', 'Fq'])
                f.to_csv('calc_strained_qmap_L100.csv', index=False, sep=' ', mode='w')
            else:
                f = pd.DataFrame([[qx_real, qy_real, qz_real, Fq]])
                f.to_csv('calc_strained_qmap_L100.csv', index=False, header=False, sep=' ', mode='a')
        print(time.time()-start)