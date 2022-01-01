%% requirements

% safely add current folder to the python search
% if count(py.sys.path, '') == 0
%     insert(py.sys.path,int32(0), '');
% end

% % reload custom module and generate particle set
% clear classes
% mod = py.importlib.import_module('python.mstm_particles');
% py.importlib.reload(mod);
% py.python.mstm_particles.test(0, 1)

% import CELES
addpath(genpath('../celes/src'))

% import generated file with particles data
data = dlmread('./particles.txt');

% ----------------------------------------------------------------------- %
%% main code

coords = euler(data(:, 1:3), 0, 8, 0);

% initialize particles and field
particles = celes_particles('positionArray',        coords, ...
                            'refractiveIndexArray', data(:, 5) + 1i*data(:, 6), ...
                            'radiusArray',          data(:, 4) ...
                            );

initialField = celes_initialField('polarAngle',     0, ...
                                  'azimuthalAngle', 0, ...
                                  'polarization',   'TE', ...
                                  'beamWidth',      300, ...
                                  'focalPoint',     [0, 0, 0] ...
                                  );

% celes input and preconditioner setup
input = celes_input('wavelength',                   83, ...
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
numerics = celes_numerics('lmax',                       3, ...
                          'polarAnglesArray',           0:pi/5e3:pi, ...
                          'azimuthalAnglesArray',       0:pi/1e2:2*pi, ...
                          'gpuFlag',                    true, ...
                          'particleDistanceResolution', 1, ...
                          'solver',                     solver);

% define a grid of points where the field will be evaulated (need to
% optimize)
scale = 1;
bnd = 5000 / scale;
stp = 4.2 / scale;
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
%% plot results

% display particles
% figure('Name','Particle positions','NumberTitle','off');
% plot_spheres(gca,simul.input.particles.positionArray, ...
%                  simul.input.particles.radiusArray, ...
%                  simul.input.particles.refractiveIndexArray)

% plot near field
h1 = figure('Name', 'Near-field cross-cut', 'NumberTitle', 'off');
plot_field(gca, simul, 'abs E', 'scattered field');
figure(h1)
ax = gca; hold on;
viscircles( ...
    ax, ...
    coords(:, [1, 3]), ...
    data(:, 4), ...
    'Color', 'black', ...
    'LineWidth', 1., ...
    'EnhanceVisibility', false);
xlabel('x, nm');
ylabel('z, nm');
fig = gcf;

axObjs = fig.Children;
cxdata = axObjs(2).Children(1).Children.XData;
cydata = axObjs(2).Children(1).Children.YData;
cydata = cydata.';
cxdata = cxdata.';
cxdata = cxdata(~isnan(cxdata));
cydata = cydata(~isnan(cydata));

particles_xy = [cxdata cydata];
heatmap = axObjs(2).Children(2).CData;
grid_max = bnd;
grid_step = stp;
filename = 'mstm_output.mat';

save(filename, 'particles_xy', 'heatmap', 'grid_max', 'grid_step');


% caxis([0,2])

% ----------------------------------------------------------------------- %
%% custom functions

function grid = euler(xyz, a, b, y)
    s = xyz;
    for i = 1:length(s)
        s(i, :) = s(i, :) * rotz(y) * roty(b) * rotx(a);
    end
    grid = s;
end