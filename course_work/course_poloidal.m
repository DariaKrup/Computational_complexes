% Poloidal point rotation
filename = 'C:\Users\Daria\Documents\MATLAB\L256216.txt';
L256216 = importdata(filename);

close all;
n_phi = 6;
nz = 3;  % center point
nr = 3;  % center point
rads = 0.5:0.5:2;
orients = {'west', 'south', 'east', 'north'};


% W-S-E-N
for j=1:size(rads, 2)
    rad_rot = rads(j);
    nz_s = [nz, nz - rad_rot, nz, nz + rad_rot];
    nr_s = [nr - rad_rot, nr, nr + rad_rot, nr];
    ind_W = ind666(nz, nr-rad_rot, n_phi); % west
    ind_S = ind666(nz-rad_rot, nr, n_phi); % south
    ind_E = ind666(nz, nr+rad_rot, n_phi); % east
    ind_N = ind666(nz+rad_rot, nr, n_phi); % north
    ind_rzph = [ind_W, ind_S, ind_E, ind_N];
    for i=1:size(orients, 2)
        orient = orients(i);
        ind_rzphi = ind_rzph(i);
        test_sol216 = zeros(216,1);
        test_sol216(ind_rzphi)=1;
        bsol216=L256216*test_sol216;
        
        % Save right parts
        matr_name = strcat({'b_'}, orient, {'_rad_'}, num2str(rad_rot), {'.txt'}); 
        matr_name = char(matr_name);
        save(matr_name, 'bsol216', '-ascii');
        
        bsol216sq=reshape(bsol216,16,16);
        
        % Save model solution
        sol_name = strcat({'x_'}, orient, {'_rad_'}, num2str(rad_rot), {'.txt'}); 
        sol_name = char(sol_name);
        save(sol_name, 'test_sol216', '-ascii');
        
        % Plot projection of detector matrix
        figure
        pcolor(bsol216sq')
        colorbar
        xlabel('\it col')
        ylabel('\it row')
        title_str = strcat({'Detector Matrix. CIRCLE '}, orient, {' nr ='}, num2str(nr_s(i)), {' nz ='}, num2str(nz_s(i)), {' rad ='}, num2str(rad_rot), {' nphi ='}, num2str(n_phi));
        title(title_str)
        fpath = 'C:\Users\Daria\Documents\MATLAB';
        saveas(gcf, fullfile(fpath, char(strcat(title_str, '.png'))), 'png');
        
        
        % Plot dependency number of variable - variable
        nums = 1:1:216;
        figure 
        grid on
        hold on
        xlim([1 216])
        plot(nums, test_sol216, 'b')
        xlabel('\it number of variable')
        ylabel('\it variable')
        title_str = strcat({'Model solution '}, orient, {' nr ='}, num2str(nr_s(i)), {' nz ='}, num2str(nz_s(i)), {' rad ='}, num2str(rad_rot), {' nphi ='}, num2str(n_phi));
        title(title_str)
        fpath = 'C:\Users\Daria\Documents\MATLAB';
        saveas(gcf, fullfile(fpath, char(strcat(title_str, '.png'))), 'png');
    end

    % Plot summary projection for radius
    solution = zeros(16, 16);
    for i=1:size(orients, 2)
        test_sol216 = zeros(216,1);
        orient = orients(i);
        ind_rzphi = ind_rzph(i);
        test_sol216(ind_rzphi)=1;
        bsol216=L256216*test_sol216;
        matr_name = strcat({'b_'}, orient, {'_rad_'}, num2str(rad_rot), {'.txt'}); 
        matr_name = char(matr_name);
        save(matr_name, 'bsol216', '-ascii');
        bsol216sq=reshape(bsol216,16,16);
        solution = solution +  bsol216sq;
    end
    
    % Save summary right part
    matr_name = strcat({'b'}, {'_rad_'}, num2str(rad_rot), {'.txt'}); 
    matr_name = char(matr_name);
    save(matr_name, 'bsol216', '-ascii');
    
    % Save summary solution
    sol_name = strcat({'x'},{'_rad_'}, num2str(rad_rot), {'.txt'}); 
    sol_name = char(sol_name);
    save(sol_name, 'test_sol216', '-ascii');
        
        
    figure
    pcolor(solution')
    colorbar
    xlabel('\it col')
    ylabel('\it row')
    title_str = strcat({'Detector Matrix. CIRCLE '}, {' nr ='}, num2str(3), {' nz ='}, num2str(3), {' rad ='}, num2str(rad_rot), {' nphi ='}, num2str(n_phi));
    title(title_str)
    figure_name = strcat(title_str,'.png');
    fpath = 'C:\Users\Daria\Documents\MATLAB';
    saveas(gcf, fullfile(fpath, char(strcat(title_str, '.png'))), 'png');
end