function [m,W]=pca(X)
  %% 1. Calcular vector medias de las muestras X por filas
  m = mean(X);
  %% Restar la media a todos los datos para obtener Xm
  Xm = X - m;
  %% Calcular covarianza (Xm' * Xm): Lo mismo con cov(Xt, 1) la verdad
  covarianza = (Xm' * Xm)/rows(X);
  %% Calcular valores y vectores propios de la matriz de covarianzas
  [vec, val] = eig(covarianza);
  %% Ordenar los vectores propios
  [S I] = sort(diag(val), "descend");
  W = vec(:,I);
end
