load ../../MNIST/train-images-idx3-ubyte.mat.gz
[m, W]=pca(X);
for i=1:5
  xr = reshape(W(:,i),28,28);imshow((xr)',[]);pause(1);
end
