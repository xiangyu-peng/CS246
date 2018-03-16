load patches;
T1=lsh('lsh',10,24,size(patches,1),patches,'range',255);
%Compute average search time for LSH
tic;
for i = 100 : 100 : 1000
    lshlookup(patches(:,i),patches,T1,'k',4,'distfun','lpnorm','distargs',{1});
end
t1 = toc;
display(t1 / 10);

%Linear Serach A is the sum of d() of every figure to the column 100бн1000
A=zeros(10,59500)
i=100
while( i<1100)
    h=1;
    while(h<59501)
        j=1;
        sum=0;
        while(j<401)
            sum=sum+abs(patches(j,i)-patches(j,h));
            j=j+1 ;      
        end
        A(i/100,h)=sum;
        h=h+1;
    end
    i=i+100   
end

% X is the 10 nearest neighbors of these 10 columns
i=1
X=zeros(10,11)
AA=A
while i<11
    j=1
    while j<12
        [row,column]=find(AA(i,:)==min(AA(i,:)))
        AA(i,column)=1000000
        X(i,j)=column
        j=j+1
    end
    i=i+1
end

%%Compute average search time for Linear search
AAA=A
tic;
load linear;
xx=zeros(10,4)
i=1
while i<11
    j=1
    while j<5
        [row,column]=find(AAA(i,:)==min(AAA(i,:)))
        AAA(i,column)=1000000
        xx(i,j)=column
        j=j+1
    end
    i=i+1
end
t2 = toc;
display(t2 / 10);

% plot the figure of the column100

figure(1);imagesc(reshape(patches(:,100),20,20));colormap gray;axis image

% plot the figure of the 10 nearest neighbors of column100 of LSH
nnlsh = [];
while length(nnlsh) < 11
    [nnlsh,numcand]=lshlookup(patches(:,100),patches,T1,'k',11,'distfun','lpnorm','distargs',{1});
end
figure(2);clf;
for k=1:10, subplot(2,5,k);imagesc(reshape(patches(:,nnlsh(k+1)),20,20)); colormap gray;axis image; end

% plot the figure of the 10 nearest neighbors of column100 of Linear Search
figure(3);clf;
for k=1:10, subplot(2,5,k);imagesc(reshape(patches(:,X(1,k+1)),20,20)); colormap gray;axis image; end

% Calculate the errors
% For L
load patches;
i=3;
while (i<7)
T=lsh('lsh',(10+2*(i-1)),24,size(patches,1),patches,'range',255);
    j=1
    while (j<11)
        nnlsh=[]
        while (size(nnlsh)<4) 
            [nnlsh,numcand]=lshlookup(patches(:,100*j),patches,T,'k',11,'distfun','lpnorm','distargs',{1});
        end
        neighbor=[neighbor;nnlsh];
        j=j+1
    end
    i=i+1
end

load patches;
h=1
errors=zeros(1,6);
while (h<7)
    i=1
    sum2=0
    while (i<11)
        sum=0
        index1=neighbor((10*(h-1)+i),2)
        j=1
        while(j<401)
             sum=sum+abs(patches(j,100*i)-patches(j,index1));
            j=j+1 ;      
        end
        index2=neighbor((10*(h-1)+i),3)
        j=1
        while(j<401)
            sum=sum+abs(patches(j,100*i)-patches(j,index2));
            j=j+1 ;      
        end
        index3=neighbor((10*(h-1)+i),4)
        j=1
        while(j<401)
            sum=sum+abs(patches(j,100*i)-patches(j,index3));
            j=j+1 ;      
        end
        sum=sum/(A(i,X(i,2))+A(i,X(i,3))+A(i,X(i,4)));
        sum2=sum2+sum
        i=i+1
    end
    error=sum2/10;
    errors(1,h)=error;
    h=h+1
end
plot(errors)

% Calculate the errors
% For k
i=1;
while (i<6)
T=lsh('lsh',10,(14+2*i),size(patches,1),patches,'range',255);
    j=1
    while (j<11)
        [nnlsh,numcand]=lshlookup(patches(:,100*j),patches,T,'k',4,'distfun','lpnorm','distargs',{1});
        neighbor2=[neighbor2;nnlsh];
        j=j+1
    end
    i=i+1
end

h=1
errors2=zeros(1,5);
while (h<6)
    i=1
    sum2=0
    while (i<11)
        sum=0
        index1=neighbor2((10*(h-1)+i),2)
        j=1
        while(j<401)
             sum=sum+abs(patches(j,100*i)-patches(j,index1));
            j=j+1 ;      
        end
        index2=neighbor2((10*(h-1)+i),3)
        j=1
        while(j<401)
            sum=sum+abs(patches(j,100*i)-patches(j,index2));
            j=j+1 ;      
        end
        index3=neighbor2((10*(h-1)+i),4)
        j=1
        while(j<401)
            sum=sum+abs(patches(j,100*i)-patches(j,index3));
            j=j+1 ;      
        end
        sum=sum/(A(i,X(i,2))+A(i,X(i,3))+A(i,X(i,4)));
        sum2=sum2+sum
        i=i+1
    end
    error=sum2/10;
    errors2(1,h)=error;
    h=h+1
end
plot(errors2)
