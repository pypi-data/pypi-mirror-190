import Organic.Organic as org
import os
import matplotlib.pyplot as plt


def main():
    # Loading the generators and discriminators
    dis = os.path.expandvars('/Users/jacques/Work/Organic/theGANextended2/saved_models/discriminatorfinalModel.h5')
    gen = os.path.expandvars('/Users/jacques/Work/Organic/theGANextended2/saved_models/generatorfinalModel.h5')

    #test = org.GAN(dis=dis, gen=gen, resetOpt=True, amsgrad = True, Adam_lr=0.0001, Adam_beta_1=0.91)

    # Data folder and files
    datafolder = 'my/folder/'
    datafiles = 'mydata.fits'
    # setting SPARCO
    sparco = org.SPARCO(wave0=1.65e-6, fstar = 0.32, denv = 1.0, dsec = -2, xsec = 0, ysec = 0, fsec = 0.0, UDstar = 0.5)

    # Launching image reconstruction


    test = org.GAN(dis=dis, gen=gen, resetOpt=True, amsgrad = True)
    test.ImageReconstruction(datafiles, sparco, data_dir = datafolder, mu=[1], ps=[0.6 ], diagnostics=True, epochs=[80], nrestart=[50], name='Nameofmyrun')



if __name__ == '__main__':
    main()
