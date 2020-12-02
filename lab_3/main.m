Aconst=[13 15;18 19;23 12];
A=[infsup(11,15) infsup(13,17);infsup(15,21) infsup(17,21);infsup(21,25) infsup(10, 14)];

x = [0.5; 0.2];
b=[infsup(7,12);infsup(10.8,14.8);infsup(11.9, 15.9)];

% solution with tolsolvty
% 3 x 2 matrix
inf_A = [11 13; 15 17; 21 10];
sup_A = [15 17; 21 21; 25 14];
inf_b = [7; 10.8; 11.9];
sup_b = [12; 14.8; 15.9];
[maxTol,argmaxTol,envs,ccode]=tolsolvty(inf_A,sup_A,inf_b,sup_b);
%Cminim = cond(inf_A);
b1=inf(A);
Cminim = condd(A, inf_A, sup_A, b1, 1);

b = 0.5 * (abs(sup_b)-abs(inf_b));
ive=sqrt(2)* Cminim * maxTol * norm(argmaxTol)/ norm(b);
disp('For the first task:');
disp('Ive_2D = ' + ive);
disp('Max tol = ' + maxTol);
disp('Cond = ' + Cminim);
[V,P1,P2,P3,P4]=EqnTol2D(inf_A,sup_A,inf_b,sup_b);
rectangle('Position',[argmaxTol(1) argmaxTol(2) 0.001 0.001 ],'EdgeColor','r');
text(argmaxTol(1)+0.005,argmaxTol(2),'argmaxTol','FontSize',8);
title_str='3 x 2 task'; 
title(title_str);
xlabel('x_1');
ylabel('x_2');
title_str_name=strcat(title_str);
figure_name_out=strcat(title_str_name,'.png');
print('-dpng', '-r300', figure_name_out), pwd




% 2 x 3 matrix
c = [infsup(10.4, 14.4); infsup(10, 15)];
inf_c = [10.4; 10];
sup_c = [14.4; 15];
[maxTol2,argmaxTol2,envs,ccode] = tolsolvty(inf_A', sup_A', inf_c, sup_c);
b1 = inf(A');
Cminim2 = condd(A',inf_A', sup_A', b1, -1);
c = 0.5 * (abs(sup_c)-abs(inf_c));
ive2 = sqrt(2) * maxTol2 * norm(argmaxTol2) / norm(c) * Cminim2;
disp('For the second task:');
disp('Ive_2D = ' + ive2);
disp('Max tol = ' + maxTol2);
disp('Cond = ' + Cminim2);
[V] = EqnTol3D(inf_A', sup_A', inf_c, sup_c, 1, 1);
title_str='2 x 3 task';
title(title_str);
xlabel('x_1');
ylabel('x_2');
title_str_name=strcat(title_str);
figure_name_out=strcat(title_str_name,'.png');
print('-dpng', '-r300', figure_name_out), pwd



Xsolv=[argmaxTol2-ive2/2,argmaxTol2+ive2/2];
A_c = [infsup(11,15) infsup(21,25); infsup(13,17) infsup(10, 14)];
[V,P1,P2,P3,P4]=EqnTol2D(inf(A_c),sup(A_c),inf_c,sup_c);
rectangle('Position', [
Xsolv(1,1) Xsolv(3,1) Xsolv(1,2)-Xsolv(1,1) Xsolv(3,2)-Xsolv(3,1)]);
rectangle('Position',[argmaxTol2(1) argmaxTol2(3) 0.001 0.001 ],'EdgeColor','r');
title_str='Bar and tolerant set';
title(title_str);
xlabel('x_1');
ylabel('x_3');
xlim([0.6 1])
ylim([0 0.4])

title_str_name=strcat(title_str);
figure_name_out=strcat(title_str_name,'.png');
print('-dpng', '-r300', figure_name_out), pwd
