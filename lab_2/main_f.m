% bar for solution
X = intval([infsup(-5, 5), infsup(-5, 5)]);
% rasstrigin function
[Z, WorkList, diams] = globopt0(X);
iter = 1:1:length(diams);
plot(iter, diams);
hold on;
xlim([0, length(diams)]);
xlabel('Iterations');
ylabel('Diameter of area');
title('Constriction of area');
path = 'C:\Users\Daria\Documents\MATLAB';
full_title = 'Rasstrigin';
saveas(gcf, fullfile(path, char(full_title)), 'png'); 

for i = 1:30
    disp(WorkList(i).Box);
    s = ['f(y) = ', num2str(WorkList(i).Estim)];
    disp(s);
end

% cross-in-tray
X = intval([infsup(-10, 10), infsup(-10, 10)]);
[Z, WorkList, diams] = globopt0(X);
solution = -2.0626;

answer = [];
for i = 1 : length(WorkList)
    answer(i) = WorkList(i).Estim;
end

for i = 1:length(answer)
    diff(i) = abs(answer(i) - solution);
end

iter = 1:1:length(answer);
plot(iter, diff);

semilogx(iter, diff);
hold on;
xlim([0, length(answer)]);
xlabel('Iterations');
ylabel('Absolute difference');
title('Convergence of method');
path = 'C:\Users\Daria\Documents\MATLAB';
full_title = 'Cross_in_tray';
saveas(gcf, fullfile(path, char(full_title)), 'png'); 

% Bar's center
centers_x= [];
centers_y = [];
for i = 1 : length(WorkList)
    centers_x(i) = WorkList(i).Box(1).mid;
    centers_y(i) = WorkList(i).Box(2).mid;
end
plot(centers_x(900:1001), centers_y(900:1001)); 
xlabel('Center X');
ylabel('Center Y');
title('Trajectory of bar center');
full_title = 'Trajectory_center';
saveas(gcf, fullfile(path, char(full_title)), 'png'); 