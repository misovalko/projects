function [finalx finaly t] = stosoo1d(f,settings)

% implementation of SOO (stochastic and deterministic (todo)) algorithm
% potential problems: sample at least once when expanding?

%% settings
k_max = ceil(settings.nb_iter/(log(settings.nb_iter)^3));
% k_max = 10;

if ~isfield(settings,'type')
    settings.type = 'sto';
end

if ~isfield(settings,'plotf')
    settings.plotf = @(x) 0;
end

if ~isfield(settings,'axis')
    settings.axis = [0 1 -3 3];
end

if ~isfield(settings,'delta')
    settings.delta = 1/sqrt(settings.nb_iter);
    % settings.delta = 0.01;
end

if ~isfield(settings,'verbose')
    verbose = 2;
else
    verbose = settings.verbose;
end

if strcmp(settings.type,'det')
    k_max = 1;
    settings.h_max = ceil(sqrt(settings.nb_iter));
end

if ~isfield(settings,'h_max')
    settings.h_max = ceil(sqrt(settings.nb_iter/k_max));
end


%% initilisation of the tree
t = cell(settings.h_max,1);

for i = 1:settings.h_max
    t{i}.x_max = [];
    t{i}.x_min = [];
    t{i}.x = [];
    t{i}.leaf = [];
    t{i}.new = [];
    t{i}.y = [];
    t{i}.sums = [];
    t{i}.ks = [];
    t{i}.values = {};
end

t{1}.x_min = 0;
t{1}.x_max = 1;
t{1}.x = 0.5;
t{1}.leaf = 1;
t{1}.new = 0;
t{1}.sums = f(t{1}.x);
t{1}.ks = 1;
t{1}.values = {[]};

UCBK = log((settings.nb_iter)^2/settings.delta)/2;

%% execution
finaly = -inf; % for deterministic case
at_least_one = 1;
n = 1;
while n<settings.nb_iter
    if (at_least_one~=1), break, end
    if (verbose > 1), fprintf(1,'----- new pass %d of %d evaluations used ..\n',n,settings.nb_iter); end
    v_max = -inf;
    
    if (verbose >1), draw_function(0,1,settings.plotf); draw_partition_tree(t,settings); end
    
    at_least_one=0;
    for h=1:settings.h_max
        if n>=settings.nb_iter, break, end
%         if (verbose > 2), fprintf(1,'Depth: %d.. \n',h); end;
        i_max = -1;
        b_hi_max = -inf;
        for i=1:numel(t{h}.x)
%             if (verbose > 2), fprintf('Node: %d..',i); end;
            if ((t{h}.leaf(i) == 1) && (t{h}.new(i)==0))
                b_hi = inf;
                if (t{h}.ks(i) > 0)
                    meanF = t{h}.sums(i)/t{h}.ks(i);
                    switch settings.type
                        case 'sto',  b_hi = meanF + sqrt(UCBK/t{h}.ks(i));
                        otherwise,  b_hi = meanF;
                    end
                end
%                 if (verbose > 2), fprintf(1,'b-value: %f..\n',b_hi); end
                if (b_hi > b_hi_max)
                    b_hi_max= b_hi;
                    i_max = i;
                end
            end
        end
        if (i_max > -1)  % we found a maximum open the leaf (h,i_max)
            if (verbose > 2), fprintf(1,'max b-value for: %f (%d of %d)..\n',b_hi_max,i_max,numel(t{h}.x)); end;
            
            if (verbose >1), 
                plot([t{h}.x_min(i_max) t{h}.x_max(i_max)],[settings.axis(3)+0.7 settings.axis(3)+0.7],'-k','LineWidth',4);
            end
            
            if (h+1>settings.h_max)
                fprintf(1,'Attempt to go beyond maximum depth refused. \n');
            elseif (b_hi_max >= v_max)
                % sample the state and collect the reward
                x_g = (5 * t{h}.x_min(i_max) + t{h}.x_max(i_max))/6.0;
                x_d = (t{h}.x_min(i_max) + 5 * t{h}.x_max(i_max))/6.0;
                xx = t{h}.x(i_max);
                sampled_value = f(xx);
                if sampled_value > finaly
                    finalx = xx;
                    finaly = sampled_value;
                end                
                t{h}.values{i_max} = [t{h}.values{i_max} sampled_value]; %just for debugging
                t{h}.sums(i_max) = t{h}.sums(i_max) + sampled_value; %sample the function at xx
                t{h}.ks(i_max) = t{h}.ks(i_max) + 1;  %increment the count
                n = n+1;
                if (verbose > 0),
                    fprintf(1,'%d: sampling (%d,%d), for the %d. time (max=%d) f(%f) = %f\n', ...
                        n,h,i_max,t{h}.ks(i_max),k_max,xx,sampled_value);
                end
                
                at_least_one = 1;
                if (t{h}.ks(i_max) >= k_max)
                    t{h}.leaf(i_max) = 0;  % the leaf becomes an inner node
                    % left node
                    t{h+1}.x = [t{h+1}.x x_g];
                    switch settings.type
                        case {'det' 'sto'} 
                            sampled_value = f(x_g);
                            t{h+1}.ks = [t{h+1}.ks 1]; % not sampled yet
                            t{h+1}.sums = [t{h+1}.sums sampled_value];
                            t{h+1}.values{numel(t{h+1}.values)+1} =  sampled_value;
                            n = n+1;                                                        
                        otherwise
                            t{h+1}.ks = [t{h+1}.ks 0]; % not sampled yet
                            t{h+1}.sums = [t{h+1}.sums 0];
                            t{h+1}.values{numel(t{h+1}.values)+1} =  [];
                    end
                    t{h+1}.x_min = [t{h+1}.x_min t{h}.x_min(i_max)];
                    t{h+1}.x_max = [t{h+1}.x_max (2*t{h}.x_min(i_max)+t{h}.x_max(i_max))/3.0];
                    t{h+1}.leaf = [t{h+1}.leaf 1];
                    t{h+1}.new = [t{h+1}.new 1];                    
                    %  right node
                    t{h+1}.x = [t{h+1}.x x_d];
                    switch settings.type
                        case {'det' 'sto'} 
                            sampled_value = f(x_d);
                            t{h+1}.ks = [t{h+1}.ks 1]; % not sampled yet
                            t{h+1}.sums = [t{h+1}.sums sampled_value];
                            t{h+1}.values{numel(t{h+1}.values)+1} =  sampled_value;
                            n = n+1;
                        otherwise
%                         case 'sto'
                            t{h+1}.ks = [t{h+1}.ks 0]; % not sampled yet
                            t{h+1}.sums = [t{h+1}.sums 0];
                            t{h+1}.values{numel(t{h+1}.values)+1} =  [];
                    end
                    t{h+1}.x_min = [t{h+1}.x_min (t{h}.x_min(i_max)+2*t{h}.x_max(i_max))/3.0];
                    t{h+1}.x_max = [t{h+1}.x_max t{h}.x_max(i_max)];
                    t{h+1}.leaf = [t{h+1}.leaf 1];
                    t{h+1}.new = [t{h+1}.new 1];                    
                    %  central node
                    t{h+1}.x = [t{h+1}.x xx];
                    t{h+1}.ks = [t{h+1}.ks t{h}.ks(i_max)];
                    t{h+1}.sums = [t{h+1}.sums t{h}.sums(i_max)];
                    t{h+1}.x_min = [t{h+1}.x_min (2*t{h}.x_min(i_max)+t{h}.x_max(i_max))/3.0];
                    t{h+1}.x_max= [t{h+1}.x_max (t{h}.x_min(i_max)+2*t{h}.x_max(i_max))/3.0];
                    t{h+1}.leaf = [t{h+1}.leaf 1];
                    t{h+1}.new = [t{h+1}.new 1];
                    t{h+1}.values{numel(t{h+1}.values)+1} =  t{h}.values{i_max};
                    % set the max Bvalue and increment the number of iteration
                    v_max = b_hi_max;
                end
            end
        end
    end
    drawnow
    for h=1:settings.h_max
        %         t{h}.new = zeros(1,numel(t{h}.x));
        for i=1:numel(t{h}.x)
            t{h}.new(i) = 0;
        end
    end
end

%% get the deepest unexpanded node (and among all of those, pick a maximum)

switch settings.type
    case 'sto'
        for h=settings.h_max:-1:1
            if isempty(t{h}.leaf), continue; end;
            final_idx = find(~t{h}.leaf);
            if ~isempty(final_idx),
                [~,final_idx] = max(t{h}.sums(final_idx));
                finalx = t{h}.x(final_idx);
                finaly = t{h}.sums(final_idx)/t{h}.ks(final_idx);
                break;
            end;
        end    
end

%% final drawing
if (verbose >0),
    draw_function(0,1,settings.plotf);
    draw_partition_tree(t,settings);
    drawnow
end