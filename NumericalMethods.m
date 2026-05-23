function NumericalMethodsApp()

clc;
clear;

%% =========================================
% MAIN WINDOW
%% =========================================

fig = uifigure( ...
    'Name','Numerical Methods MATLAB', ...
    'Position',[100 50 1600 900]);

tg = uitabgroup(fig,'Position',[10 10 1580 880]);

rootTab = uitab(tg,'Title','Root Finding Methods');
matrixTab = uitab(tg,'Title','Matrix Operations');

%% =========================================
% ROOT FINDING TAB
%% =========================================

uilabel(rootTab,'Text','Equation f(x):', ...
    'Position',[20 820 120 22]);

eqField = uieditfield(rootTab,'text', ...
    'Position',[140 820 320 22], ...
    'Value','x^3 + 3*x^2 - 4*x - 12');

uilabel(rootTab,'Text','Method:', ...
    'Position',[500 820 60 22]);

methodDrop = uidropdown(rootTab, ...
    'Items',{'Incremental','Bisection','Regula Falsi', ...
              'Newton-Raphson','Secant'}, ...
    'Position',[570 820 180 22], ...
    'Value','Bisection');

uilabel(rootTab,'Text','XL:', ...
    'Position',[20 780 40 22]);

xlField = uieditfield(rootTab,'numeric', ...
    'Position',[60 780 100 22], ...
    'Value',1);

uilabel(rootTab,'Text','XU:', ...
    'Position',[180 780 40 22]);

xuField = uieditfield(rootTab,'numeric', ...
    'Position',[220 780 100 22], ...
    'Value',2);

uilabel(rootTab,'Text','Tolerance:', ...
    'Position',[350 780 80 22]);

tolField = uieditfield(rootTab,'numeric', ...
    'Position',[430 780 120 22], ...
    'Value',0.0001);

uibutton(rootTab,'push', ...
    'Text','Solve', ...
    'Position',[580 780 100 30], ...
    'ButtonPushedFcn',@(btn,event) solveRoot());

uibutton(rootTab,'push', ...
    'Text','Clear', ...
    'Position',[700 780 100 30], ...
    'ButtonPushedFcn',@(btn,event) clearRoot());

cols = {'i','XL','XR','XU','f(XL)','f(XR)','Error %','Product','Status'};

rootTable = uitable(rootTab, ...
    'Position',[20 40 900 700], ...
    'ColumnName',cols);

ax = uiaxes(rootTab, ...
    'Position',[950 40 600 700]);

title(ax,'Function Visualization');
grid(ax,'on');

%% =========================================
% MATRIX TAB
%% =========================================

uilabel(matrixTab,'Text','Operation:', ...
    'Position',[20 820 100 22]);

matrixDrop = uidropdown(matrixTab, ...
    'Items',{'Addition','Multiplication','Transpose', ...
              'Determinant','Inverse','Adjoint', ...
              'Power','Equation'}, ...
    'Position',[120 820 220 22]);

uilabel(matrixTab,'Text','Matrix A:', ...
    'Position',[20 760 100 22]);

matrixA = uitextarea(matrixTab, ...
    'Position',[20 450 350 280], ...
    'Value',{'1 2';'3 4'});

uilabel(matrixTab,'Text','Matrix B:', ...
    'Position',[420 760 100 22]);

matrixB = uitextarea(matrixTab, ...
    'Position',[420 450 350 280], ...
    'Value',{'5 6';'7 8'});

uibutton(matrixTab,'push', ...
    'Text','Compute', ...
    'Position',[20 390 120 30], ...
    'ButtonPushedFcn',@(btn,event) computeMatrix());

uibutton(matrixTab,'push', ...
    'Text','Clear', ...
    'Position',[160 390 120 30], ...
    'ButtonPushedFcn',@(btn,event) clearMatrix());

matrixResult = uitextarea(matrixTab, ...
    'Position',[820 300 600 450]);

%% =========================================
% FUNCTION PARSER
%% =========================================

function f = parseFunction(expr)

    expr = lower(expr);

    expr = strrep(expr,' ','');
    expr = strrep(expr,'^','.^');

    expr = regexprep(expr,'(\d)(x)','${1}.*${2}');
    expr = regexprep(expr,'(x)(\d)','${1}.*${2}');
    expr = regexprep(expr,'(\))(x)','${1}.*${2}');
    expr = regexprep(expr,'(x)(\()','${1}.*${2}');

    f = str2func(['@(x) ' expr]);

end

%% =========================================
% SOLVE ROOT
%% =========================================

function solveRoot()

    try

        rootTable.Data = {};

        f = parseFunction(eqField.Value);

        xl = xlField.Value;
        xu = xuField.Value;
        tol = tolField.Value;

        method = methodDrop.Value;

        switch method

            case 'Incremental'
                data = incrementalMethod(f,xl,xu);

            case 'Bisection'
                data = bisectionMethod(f,xl,xu,tol);

            case 'Regula Falsi'
                data = regulaFalsiMethod(f,xl,xu,tol);

            case 'Newton-Raphson'
                data = newtonMethod(f,xl,tol);

            case 'Secant'
                data = secantMethod(f,xl,xu,tol);

        end

        rootTable.Data = data;

        plotGraph(f,xl,xu,NaN);

    catch ME

        uialert(fig,ME.message,'Root Finding Error');

    end

end

%% =========================================
% CLEAR ROOT
%% =========================================

function clearRoot()

    rootTable.Data = {};
    cla(ax);

end

%% =========================================
% PLOT GRAPH
%% =========================================

function plotGraph(f,xl,xu,xr)

    cla(ax);

    x = linspace(xl-5,xu+5,1000);

    y = zeros(size(x));

    for i = 1:length(x)
        y(i) = f(x(i));
    end

    plot(ax,x,y,'LineWidth',2);

    hold(ax,'on');

    yline(ax,0);

    xline(ax,xl,'--g','XL');

    xline(ax,xu,'--r','XU');

    if ~isnan(xr)
        scatter(ax,xr,0,120,'filled','g');
    end

    hold(ax,'off');

    grid(ax,'on');

end

%% =========================================
% INCREMENTAL METHOD
%% =========================================

function data = incrementalMethod(f,xl,xu)

    step = 0.1;

    k = 1;

    data = {};

    for x = xl:step:(xu-step)

        fx = f(x);

        fx2 = f(x+step);

        prod = fx * fx2;

        if prod < 0
            status = 'Possible Root';
        else
            status = 'Next';
        end

        data(k,:) = { ...
            k, x, x+step, '-', ...
            fx, fx2, '-', ...
            prod, status};

        k = k + 1;

    end

end

%% =========================================
% BISECTION METHOD
%% =========================================

function data = bisectionMethod(f,xl,xu,tol)

    data = {};

    xr_old = xl;

    for i = 1:100

        xr = (xl + xu)/2;

        fxl = f(xl);

        fxr = f(xr);

        prod = fxl * fxr;

        if i == 1
            ea = inf;
        else
            ea = abs((xr - xr_old)/xr) * 100;
        end

        if prod < 0
            xu = xr;
            status = 'LEFT';
        else
            xl = xr;
            status = 'RIGHT';
        end

        data(i,:) = { ...
            i, xl, xr, xu, ...
            fxl, fxr, ea, ...
            prod, status};

        plotGraph(f,xl,xu,xr);

        drawnow;

        if ea < tol
            break;
        end

        xr_old = xr;

    end

end

%% =========================================
% REGULA FALSI
%% =========================================

function data = regulaFalsiMethod(f,xl,xu,tol)

    data = {};

    xr_old = xl;

    for i = 1:100

        fxl = f(xl);

        fxu = f(xu);

        xr = xu - (fxu * (xl - xu)) / (fxl - fxu);

        fxr = f(xr);

        prod = fxl * fxr;

        if i == 1
            ea = inf;
        else
            ea = abs((xr - xr_old)/xr) * 100;
        end

        if prod < 0
            xu = xr;
        else
            xl = xr;
        end

        data(i,:) = { ...
            i, xl, xr, xu, ...
            fxl, fxr, ea, ...
            prod, 'Iterating'};

        plotGraph(f,xl,xu,xr);

        drawnow;

        if ea < tol
            break;
        end

        xr_old = xr;

    end

end

%% =========================================
% NEWTON RAPHSON
%% =========================================

function data = newtonMethod(f,x0,tol)

    h = 1e-6;

    data = {};

    for i = 1:100

        df = (f(x0+h)-f(x0))/h;

        x1 = x0 - f(x0)/df;

        ea = abs((x1-x0)/x1) * 100;

        data(i,:) = { ...
            i, x0, x1, '-', ...
            f(x0), f(x1), ...
            ea, '-', 'Newton'};

        plotGraph(f,x0,x1,x1);

        drawnow;

        if ea < tol
            break;
        end

        x0 = x1;

    end

end

%% =========================================
% SECANT METHOD
%% =========================================

function data = secantMethod(f,x0,x1,tol)

    data = {};

    for i = 1:100

        fx0 = f(x0);

        fx1 = f(x1);

        x2 = x1 - (fx1 * (x1 - x0)) / (fx1 - fx0);

        ea = abs((x2 - x1)/x2) * 100;

        data(i,:) = { ...
            i, x0, x1, x2, ...
            fx0, fx1, ea, ...
            '-', 'Secant'};

        plotGraph(f,x0,x1,x2);

        drawnow;

        if ea < tol
            break;
        end

        x0 = x1;
        x1 = x2;

    end

end

%% =========================================
% MATRIX OPERATIONS
%% =========================================

function computeMatrix()

    try

        A = str2num(strjoin(matrixA.Value,newline));

        B = str2num(strjoin(matrixB.Value,newline));

        op = matrixDrop.Value;

        switch op

            case 'Addition'
                R = A + B;

            case 'Multiplication'
                R = A * B;

            case 'Transpose'
                R = A';

            case 'Determinant'
                R = det(A);

            case 'Inverse'
                R = inv(A);

            case 'Adjoint'
                R = det(A) * inv(A);

            case 'Power'
                R = A^2;

            case 'Equation'
                R = A \ B;

        end

        matrixResult.Value = splitlines(evalc('disp(R)'));

    catch ME

        uialert(fig,ME.message,'Matrix Error');

    end

end

%% =========================================
% CLEAR MATRIX
%% =========================================

function clearMatrix()

    matrixA.Value = {'1 2';'3 4'};
    matrixB.Value = {'5 6';'7 8'};
    matrixResult.Value = {''};

end

end
