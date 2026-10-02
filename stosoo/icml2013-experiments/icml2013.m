sin1 = @(value) (sin(13 * value) * sin(27 * value) / 2.0 + 0.5);
difficult =  @(x) 1-sqrt(x) + (-x*x +sqrt(x) )*(sin(1/(x*x*x))+1)/2;
guirland =  @(x) 4*x*(1-x)*(0.75+0.25*(1-sqrt(abs(sin(60*x)))));

myfun = sin1; fmax = 0.975599143811574975870826165191829204559326171875;
% myfun = guirland; fmax = 0.997772313413222;

delta1 = @(h) 14*2^(-h);
delta2 = @(h) 222*2^(-2*h);

% varparam = 100:100:1000;
% varparam = 500;
% varparam = [200];
% varparam = [50 100 150];
% varparam = [30:30:500];
% varparam = 50:50:500;
% varparam = [100 500 1000];
% varparam = [500 1000 5000 10000 50000 100000 500000 1000000];
% varparam = 1000:1000:5000;
varparam = [50 100 150 500];
% varparam = [10 50 100 500 1000];
% varparam = [1e-5 1e-4 1e-3 1e-2 1e-1 1 1e2 1e3];
% varparam = [0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1];
% varparam = [5:5:45 50:50:300 10000 ];
varparam = 1e5;
numtrials = 1;

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

% s = RandStream('mt19937ar','Seed',1);
% RandStream.setGlobalStream(s);

for v=1:numel(varparam)
    nb_iter = varparam(v);
    varparam(v)
    %     settings.nb_iter = 100;
    %     myfun_noise = @(value) myfun(value) + randn()*varparam(v);
    %     myfun_noise_minus = @(value) -myfun_noise(value);
    
    
    for t = 1:numtrials
        tic;
        nrow = 1;
        settings.k_max = 3*ceil(nb_iter/(log(nb_iter)^3));
        [x y tr1] = oo(myfun_noise,nb_iter,settings);
        runtimes(nrow,v,t) = toc;
        results(nrow,v,t) = myfun(x);
        fprintf(1,'[%d %d] StoSOO found: f(%f) = [%f] (%f seconds)\n', v,t,x,results(nrow,v,t),runtimes(nrow,v,t));
        %%
        
%         tic
%         nrow = nrow + 1;
%         settings.deltafunction = delta1;
%         [x2 y2 tr2] = stoo(myfun_noise,nb_iter,settings);
%         runtimes(nrow,v,t) = toc;
%         results(nrow,v,t) = myfun(x2);
%         fprintf(1,'[%d %d]  StOO1 found: f(%f) = [%f] (%f seconds)\n', v,t,x2,results(nrow,v,t),runtimes(nrow,v,t));
%         
%         %%
%         tic
%         nrow = nrow + 1;
%         settings.deltafunction = delta2;
%         settings.verbose = 0;
%         [x3 y3 tr3] = stoo(myfun_noise,nb_iter,settings);
%         settings.verbose = 0;
%         runtimes(nrow,v,t) = toc;
%         results(nrow,v,t) = myfun(x3);
%         fprintf(1,'[%d %d]  StOO2 found: f(%f) = [%f] (%f seconds)\n', v,t,x3,results(nrow,v,t),runtimes(nrow,v,t));
%         
%         %%
%         tic
%         options = optimset('MaxFunEvals',settings.nb_iter,'MaxIter',1000000,'Display','off');
%         [xm,ym] = fminbnd(myfun_noise_minus,0,1,options);
%         nrow = nrow + 1;
%         runtimes(nrow,v,t) = toc;
%         results(nrow,v,t) = myfun(xm);
%         fprintf(1,'[%d %d] Fminb found: f(%f) = [%f] (%f seconds)\n', v,t,xm,results(nrow,v,t),runtimes(nrow,v,t));
        %
    end
    
end
%%
results(nrow+1:end,:,:) = [];
results =  fmax - results;

%%
%  close all
%  draw_function(0,1,myfun,'plot.pdf');
%  close all
%  draw_function(0,1,myfun_noise,'plot_unnoised.pdf');

if numel(varparam) > 1
    
    close all
    hold on
    box on
    avgresults = mean(results,3);
    stdresults = std(results,[],3);
    %     plot(avgresults','d-','Linewidth',3,'MarkerSize',15,'MarkerFaceColor','auto')
    %       plot(avgresults(1,:)','d-','Linewidth',3,'MarkerSize',12,'MarkerFaceColor','auto','Color',[0 0 0])
    %       plot(avgresults(2,:)','o--','Linewidth',3,'MarkerSize',12,'MarkerFaceColor','auto','Color',0.6*[1 1 1])
    %       plot(avgresults(3,:)','o-.','Linewidth',3,'MarkerSize',12,'MarkerFaceColor','auto','Color',0.8*[1 1 1])
%     errorbar(avgresults',stdresults','d-','LineWidth',3,'MarkerFaceColor','auto','MarkerSize',15)
         errorbar(avgresults(1,:)',stdresults(1,:)','d-','Color',[0 0 0],'LineWidth',3,'MarkerFaceColor','auto','MarkerSize',12)
         errorbar(avgresults(2,:)',stdresults(2,:)','o--','Color',0.6*[1 1 1],'LineWidth',3,'MarkerFaceColor','auto','MarkerSize',12)
         errorbar(avgresults(3,:)',stdresults(3,:)','s-.','Color',0.8*[1 1 1],'LineWidth',3,'MarkerFaceColor','auto','MarkerSize',12)
        
    %      ylim([min(avgresults(:))-0.01 max(avgresults(:))+0.01]);
    
    %        ylim([0 max(avgresults(:))+0.01]);
    %        ylim([0 0.3]);
    %     xlim([0 21]);
    %     set(gca,'XTick',1:2:numel(varparam))
    %     set(gca,'XTickLabel',cellstr(num2str(varparam(1:2:numel(varparam))')))
    set(gca,'XTick',1:numel(varparam))
    set(gca,'XTickLabel',cellstr(num2str(varparam')))
    ylabel('regret (loss)','FontSize',12);
    xlabel('number of function evaluations','FontSize',12);
    %      legend('StoSOO','Matlab fminbnd','StoOO','Location','Best');
%     legend('StoSOO','StOO l1','StOO l2','Matlab fminbnd','Location','Best');
%     legend('StoSOO','StOO l1','StOO l2','Location','Best');
    %      legend('StoSOO','Matlab fminbnd','StoOO1','StoOO2','Location','Best');
    %      legend('boxoff')
    make_this_figure_tight
    saveas(gcf,'results.pdf');
end



