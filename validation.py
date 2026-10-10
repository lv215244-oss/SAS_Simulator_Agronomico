import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

def metrics(obs, sim):
    obs=np.asarray(obs,float); sim=np.asarray(sim,float)
    rmse=float(np.sqrt(mean_squared_error(obs,sim)))
    r2=float(r2_score(obs,sim)) if len(obs)>1 else float('nan')
    den=float(np.sum((obs-np.mean(obs))**2))
    nse=float(1-np.sum((obs-sim)**2)/den) if den else float('nan')
    bias=float(np.mean(sim-obs))
    return {'RMSE':rmse,'R2':r2,'NSE':nse,'Bias':bias}
