% submodules
addpath(genpath('../celes/src'))
addpath(genpath('./yaml'))

config = ReadYaml('./config.yml');
disp(config);

% ----------------------------------------------------------------------- %

for datafile = split(config.datafiles, ' ')
    for ang = config.initialAngles
        for wav = config.initialWavelength
            
            df = char(datafile);
            data = dlmread(df);
            coords = euler(data(:, 1:3), 0, ang, 0);

            basename = split(df, ".");
            basename = basename(1, 1);
            mat_fname = './output/' + string(basename) + '_' +...
                        string(ang) + 'deg_' + ...
                        config.initialPolarization +'pol_' + ...
                        string(wav) + 'wav_' + ...
                        string(config.initialBeamWidth) + 'bw.mat';
            
            % initialize particles and field
            particles = celes_particles('positionArray',        coords, ...
                                        'refractiveIndexArray', data(:, 5) + 1i*data(:, 6), ...
                                        'radiusArray',          data(:, 4) ...
                                        );
            
            initialField = celes_initialField('polarAngle',     0, ...
                                              'azimuthalAngle', 0, ...
                                              'polarization',   config.initialPolarization, ...
                                              'beamWidth',      config.initialBeamWidth, ...
                                              'focalPoint',     [0, 0, 0] ...
                                              );
            
            % celes input and preconditioner setup
            input = celes_input('wavelength',                   wav, ...
                                'mediumRefractiveIndex',        1, ...
                                'particles',                    particles, ...
                                'initialField',                 initialField ...
                                );
            
            precnd = celes_preconditioner('type',               'blockdiagonal', ...
                                          'partitionEdgeSizes', [1200, 1200, 1200] ...
                                          );
            
            % solver configuration
            solver = celes_solver('type',                       'GMRES', ...
                                  'tolerance',                  5e-4, ...
                                  'maxIter',                    1000, ...
                                  'restart',                    200, ...
                                  'preconditioner',             precnd);
            
            %
            numerics = celes_numerics('lmax',                       config.lmax, ...
                                      'polarAnglesArray',           0:pi/5e3:pi, ...
                                      'azimuthalAnglesArray',       0:pi/1e2:2*pi, ...
                                      'gpuFlag',                    config.gpu, ...
                                      'particleDistanceResolution', 1, ...
                                      'solver',                     solver);
            
            scale = config.GridScale;
            bnd = config.GridSize / scale;
            stp = config.GridStep / scale;
    
            [x, z] = meshgrid(-bnd:stp:bnd, -bnd:stp:bnd); y = zeros(size(x));
            
            output = celes_output('fieldPoints',                [x(:),y(:),z(:)], ...
                                  'fieldPointsArrayDims',       size(x));
            
            % initialize simulation class instance
            simul = celes_simulation('input',                   input, ...
                                     'numerics',                numerics, ...
                                     'output',                  output);
            
            % run simulation
            simul.run;
            
            % evaluate field at output.fieldPoints
            simul.evaluateFields;
            
            % ----------------------------------------------------------------------- %
            
            % plot near field
            h1 = figure('Name', 'Near-field cross-cut', 'NumberTitle', 'off');
            plot_field(gca, simul, 'abs E', 'scattered field');
            figure(h1)
            ax = gca; hold on;
            fig = gcf;
            
            axObjs = fig.Children;
            particles_xy = [coords data(:, 4)];
            heatmap = axObjs(2).Children.CData;
            grid_max = bnd;
            grid_step = stp;
            
            save(mat_fname, 'particles_xy', 'heatmap', 'grid_max', 'grid_step');
        end
    end
end

% ----------------------------------------------------------------------- %
%% custom functions

function grid = euler(xyz, a, b, y)
    s = xyz;
    for i = 1:length(s)
        s(i, :) = s(i, :) * rotz(y) * roty(b) * rotx(a);
    end
    grid = s;
end