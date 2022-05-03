% submodules
addpath(genpath('../celes/src'))
addpath(genpath('./yaml'))

% read and display config
config = ReadYaml('./config.yml');
disp(config);

% filter input files
filePattern = fullfile(config.inputDir, "*.txt");
dataFiles = dir(filePattern);

% evaluate for all datafiles, angles and wavelengths passed
for k = 1:length(dataFiles)
    for wav = config.initialWavelength

        theta0 = config.theta0;
        phi0 = config.phi0;
        
        % extract mesh and rotate as specified
        df = fullfile(config.inputDir, dataFiles(k).name);
        data = readmatrix(df);
        coords = euler(data(:, 1:3), 0, theta0, phi0);
        
        % build output fname according to config
        basename = split(dataFiles(k).name, ".txt");
        basename = basename(1, 1);
        out_fname = string(basename) + '_' +...
                    string(theta0) + 'deg_theta0_' + ...
                    string(phi0) + 'deg_phi0_' + ...
                    config.initialPolarization +'pol_' + ...
                    string(wav) + 'wav_' + ...
                    string(config.initialBeamWidth) + 'bw.mat';

        mat_fname = fullfile(config.outputDir, out_fname);
        
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
        
        numerics = celes_numerics('lmax',                       config.lmax, ...
                                    'polarAnglesArray',           0:pi/5e3:pi, ...
                                    'azimuthalAnglesArray',       0:pi/1e2:2*pi, ...
                                    'gpuFlag',                    config.gpu, ...
                                    'particleDistanceResolution', 1, ...
                                    'solver',                     solver);
        
        % build solution mesh
        scale = config.GridScale;
        bnd = config.GridSize / scale;
        stp = config.GridStep / scale;

        [x, y, z] = meshgrid(-bnd:stp:bnd, -bnd:stp:bnd, -bnd:stp:bnd);
        
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
        
        % plot near field
        %h1 = figure('Name', 'Near-field cross-cut', 'NumberTitle', 'off');
        %plot_field(gca, simul, 'abs E', 'scattered field');
        %figure(h1)
        %ax = gca; hold on;
        %fig = gcf;
        
        %axObjs = fig.Children;
        particles_xy = [coords data(:, 4)];
        %heatmap = axObjs(2).Children.CData;
        grid_max = bnd;
        grid_step = stp;
        
        eField = simul.output.scatteredField + simul.output.internalField;
        dims = simul.output.fieldPointsArrayDims;
        eField3DAbs = reshape(gather(sqrt(sum(abs(eField).^2,2))), dims);
        
        save(mat_fname, 'particles_xy', 'eField3DAbs', 'grid_max', 'grid_step');
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