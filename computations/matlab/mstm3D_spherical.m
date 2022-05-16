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
        for theta0 = config.theta0

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
                        string(config.initialBeamWidth) + 'bw_spherical.mat';

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
            


            % spherical meshg
            rMax = config.radMax;
            rMin = config.radMin;
            rStep = config.radStep;
            angleStep = pi/180;

            r = rMin:rStep:rMax;
            phi = 0:angleStep:2*pi-angleStep;
            theta = 0:angleStep:pi-angleStep;

            [R, Phi, Theta] = meshgrid(r, phi, theta);

            x = R .* cos(Phi) .* sin(Theta);
            y = R .* sin(Phi) .* sin(Theta);
            z = R .* cos(Theta);

            coordinates = [x(:), y(:), z(:)];
            unique_coord = unique(coordinates, 'rows');
            fieldDims = size(unique_coord);
            
            output = celes_output('fieldPoints',                unique_coord, ...
                                  'fieldPointsArrayDims',       fieldDims);
            
            % initialize simulation class instance
            simul = celes_simulation('input',                   input, ...
                                     'numerics',                numerics, ...
                                     'output',                  output);
            
            % run simulation and evaluate field at output.fieldPoints
            simul.run;
            simul.evaluateFields;
            
            particles = [coords data(:, 4)];
            
            eField = simul.output.scatteredField + simul.output.internalField;
            eField3DAbs = gather(sqrt(sum(abs(eField).^2, 2)));
            
            save(mat_fname, 'particles', 'eField3DAbs', 'unique_coord');
            
        end
    end
end

% ----------------------------------------------------------------------- %
%% custom functions

function grid = euler(xyz, a, b, y)
    s = xyz;
    for i = 1:length(s)
        s(i, :) = rotx(a) * (roty(b) * (rotz(y) * s(i, :).')); % R * s.T, with transpose !!!
    end
    grid = s;
end