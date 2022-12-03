%Irregular pattern recognition
clear
close all
% clc
%---------macierz obrazu-----------------------------------------
tic
[I0,map]=imread('flames','jpg');
colormap(map);
I0=double(I0);
Input_source_image=I0;
input_image=I0; %macierz na ktorej pracujemy
%conversion to grayscale
input_image(:,:,1)=(I0(:,:,1)+I0(:,:,2)+I0(:,:,3))/3;
input_image(:,:,2)=input_image(:,:,1);
input_image(:,:,3)=input_image(:,:,1);
 %input
%--- macierz wzorca----------------------------------------------
[I1,map]=imread('pt','bmp');
colormap(map);
I1=double(I1);
[row, col, deep]=size(I1);
Pattern_image=I1;
%conversion to grayscale
Pattern_image(:,:,1)=(I1(:,:,1)+I1(:,:,2)+I1(:,:,3))/3;
Pattern_image(:,:,2)=Pattern_image(:,:,1);
Pattern_image(:,:,3)=Pattern_image(:,:,1);
%-----------------------------------------------------------------
%co ile stopni obrót wzorca
beta = 45;
point = 360/beta;
%wymiary kolejno macierzy obrazu i macierzy wzorca
[M,N]=size(input_image(:,:,1));
[K,L]=size(Pattern_image(:,:,1));
%Accuumulator
max_A=0;
r = min(K,L)/2;
Rotated_patterns_matrix = zeros(row,col,point);
[K,L,m] = size(Rotated_patterns_matrix);
A=zeros(M-K+1,N-L+1,point); 
circle_mask=zeros(K,L);
for a=1:K
    for b=1:L
        if sqrt((a-r-0.5)^2+(b-r-0.5)^2) < r
            circle_mask(a,b)=1;
        end
    end
end

% Zbiór obróconych wzorców
for z=1:point
        IG4 = Pattern_image(:,:,1);
            alfa = z*beta;
        alfa = mod(alfa,360);
        a1 = alfa;
        while a1 > 0   
            a = 90;
            if a1 < 90
                a = a1;
            end    
            IG3 = IG4;
            [row, col, deep]=size(IG3);
            R = [cosd(a) -sind(a); sind(a) cosd(a)];
            x_p = row * cosd(90 - a) + col * cosd(a);
            y_p = row * sind(90 - a) + col * sind(a);
            xp = row;
            yp = col;
            xp = round(xp);
            yp = round(yp);
            x2 = col * cosd(90 - a);
            parfor x1=1:xp
                 for y1=1:yp
                     rotpoint = R^(-1) * [x1-x2;y1];
                     x =  [1,0] * rotpoint;
                     y = [0,1] * rotpoint;
                     x = round(x + (x_p - row)/2);
                     y = round(y+1);
                if x <= 0 || x > col || y <= 0 || y > row
                     IG4(y1,x1,1) = 0;
                else
                     IG4(y1,x1,1) = IG3(y,x,1);
                end
                 end
             end     
                 a1 = a1 - 90;
        end
        
        [p1,p2,p3] = size(Rotated_patterns_matrix);
        [g1,g2,g3] = size(IG4);

        i1 = round((p1-g1+1)/2);
        j1 = round((p2-g2+1)/2);
        Rotated_patterns_matrix(i1:i1+g1-1,j1:j1+g1-1,z) = IG4(:,:,1);
end

%sprawdzanie jak dobre sa punkty na obrazie

    parfor i=1:M-K+1 %image rows
        for j=1:N-L+1 %image columns
            s=0;
            %pattern
            for z = 1: point
                for p_i=1:K
                    for p_j=1:L
                        if circle_mask(p_i,p_j)
                            A(i,j,z) = A(i,j,z) + 255 - abs(input_image(i+p_i-1,j+p_j-1,1)- Rotated_patterns_matrix(p_i,p_j,z));      
                        end
                    end
                end     

            end
        end
    end  

    A1 = A; %macierz bez wyciec
    
   
   %wyszukiwanie najlepszych punktow z akumulatora 
   max_i = 0;
   max_j = 0;
   max_z = 0;
   r = round(r);
for a = 1 : 18
     max_A = 0;
     for z =1:point
         for i=1:M-K+1 %image rows
                for j=1:N-L+1 %image columns
                        if max_A < A(i,j,z)
                            max_A = A(i,j,z);
                            max_i = i;
                            max_j = j;
                            max_z = z;
                        end
                end        
         end  
     end
         for i=1:K
             for j=1:L

                c = round((i-r)^2) + (j-r)^2;
                g = 1;

                 if (c >= (r - g)^2 && c <= (r + g)^2)
                       I0(i+max_i -1,j+max_j -1,1) = 255;
                       I0(i+max_i -1,j+max_j -1,2) = 0;
                       I0(i+max_i -1,j+max_j -1,3) = 0;
                 end
                 

                 
             end
         end

                for g=0:ceil(K/1.5)
                    for h=0:ceil(L/1.5)
                       if(max_i + g <= M-K+1 && max_j + h <= N-L+1)
                         A(max_i + g,max_j + h,:) = 0;

                       end                   
                       if(max_i + g <= M-K+1 && max_j - h > 0 )
                         A(max_i + g,max_j - h,:) = 0;

                       end                   
                       if(max_i - g > 0 &&  max_j + h <= N-L+1) 
                         A(max_i - g,max_j + h,:) = 0;

                       end                   
                       if(max_i - g > 0 && max_j - h > 0 )
                         A(max_i - g,max_j - h,:) = 0;

                       end
                    end
                end
end


I1=uint8(I1);
figure(1);
image(I1);
title('Pattern');

Input_source_image=uint8(Input_source_image);
figure(2);
image(Input_source_image);
title('INPUT IMAGE');

I0=uint8(I0);
figure(3);
image(I0);
title('OUTPUT IMAGE');
toc