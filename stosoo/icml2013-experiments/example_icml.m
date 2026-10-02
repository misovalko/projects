sin1 = @(value) (sin(13 * value) * sin(27 * value) / 2.0 + 0.5);
difficult =  @(x) 1-sqrt(x) + (-x*x +sqrt(x) )*(sin(1/(x*x*x))+1)/2;
guirland =  @(x) 4*x*(1-x)*(0.75+0.25*(1-sqrt(abs(sin(60*x)))));

myfun = sin1; fmax = 0.975599143811574975870826165191829204559326171875;
% myfun = guirland; fmax = 0.997772313413222;

delta1 = @(h) 14*2^(-h);
delta2 = @(h) 222*2^(-2*h);

varparam = [10 50 100 500 1000];
numtrials = 10;

results = zeros(4,numel(varparam),numtrials);
runtimes = results;

myfun_minus = @(value) -myfun(value);
myfun_noise = @(value) myfun(value) + randn()/10;
myfun_noise_minus = @(value) -myfun_noise(value);

options = [];
settings = [];
settings.plotf = myfun;
settings.verbose = 0;
settings.type = 'sto';

%%

s = RandStream('mt19937ar','Seed',1);
RandStream.setGlobalStream(s);

for v=1:numel(varparam)
    nb_iter = varparam(v);
    varparam(v);
    
    for t = 1:numtrials
        tic;
        nrow = 1;
        settings.k_max = 3*ceil(nb_iter/(log(nb_iter)^3));
        [x y tr1] = oo(myfun_noise,nb_iter, settings);
        runtimes(nrow,v,t) = toc;
        results(nrow,v,t) = myfun(x);
        fprintf(1,'[%d %d] StoSOO found: f(%f) = [%f] (%f seconds)\n', v,t,x,results(nrow,v,t),runtimes(nrow,v,t));
        %%
        
        tic
        nrow = nrow + 1;
        settings.deltafunction = delta1;
        [x2 y2 tr2] = stoo(myfun_noise,nb_iter,settings);
        runtimes(nrow,v,t) = toc;
        results(nrow,v,t) = myfun(x2);
        fprintf(1,'[%d %d]  StOO1 found: f(%f) = [%f] (%f seconds)\n', v,t,x2,results(nrow,v,t),runtimes(nrow,v,t));
        
        %%
        tic
        nrow = nrow + 1;
        settings.deltafunction = delta2;
        settings.verbose = 0;
        [x3 y3 tr3] = stoo(myfun_noise,nb_iter,settings);
        settings.verbose = 0;
        runtimes(nrow,v,t) = toc;
        results(nrow,v,t) = myfun(x3);
        fprintf(1,'[%d %d]  StOO2 found: f(%f) = [%f] (%f seconds)\n', v,t,x3,results(nrow,v,t),runtimes(nrow,v,t));
        %
    end
    
end
%%
results(nrow+1:end,:,:) = [];
results =  fmax - results;




