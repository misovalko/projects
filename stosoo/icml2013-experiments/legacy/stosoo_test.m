s = RandStream('mt19937ar','Seed',1);
RandStream.setGlobalStream(s);


sin1 = @(value) (sin(13 * value) * sin(27 * value) / 2.0 + 0.5);
difficult =  @(x) 1-sqrt(x) + (-x*x +sqrt(x) )*(sin(1/(x*x*x))+1)/2;
guirland =  @(x) 4*x*(1-x)*(0.75+0.25*(1-sqrt(abs(sin(60.0*x)))));

myfun = guirland;


varparam = 50:50:300;
% varparam = 1e3;
numtrials = 10;

results = zeros(2,numel(varparam),numtrials);
runtimes = results;

myfun_minus = @(value) -myfun(value);
myfun_noise = @(value) myfun(value) + randn()/10;
myfun_noise_minus = @(value) -myfun_noise(value);

settings = [];
settings.plotf = myfun;
settings.verbose = 0;

%%


for v=1:numel(varparam)
    settings.nb_iter = varparam(v);
    
    for t = 1:numtrials
        tic;
        [x y tr] = oo(myfun_noise,settings);
        runtimes(1,v,t) = toc;
        results(1,v,t) = myfun(x);
        fprintf(1,'[%d %d] Maximum found: f(%f) = %f [%f] (%f seconds)\n', v,t,x,y,results(1,v,t),runtimes(1,v,t));
        
        
        options = optimset('MaxFunEvals',settings.nb_iter,'MaxIter',1000000,'Display','off');
        tic;
        [xm,ym] = fminbnd(myfun_noise_minus,0,1,options);
        runtimes(2,v,t) = toc;
        results(2,v,t) = myfun(xm);
        fprintf(1,'[%d %d] Fminbnd found: f(%f) = %f [%f] (%f seconds)\n', v,t,xm,-ym,results(2,v,t),runtimes(2,v,t));
        
    end
    
end

%%

if numel(varparam) > 1
    
    close all
    hold on
    box on
    avgresults = mean(results,3);
    stdresults = std(results,[],3);
%     plot(avgresults','d-','Linewidth',3,'MarkerSize',10,'MarkerFaceColor','auto')
%     plot(avgresults(1,:)','d-','Linewidth',3,'MarkerSize',15,'MarkerFaceColor','auto','Color',[0 0 0])
%     plot(avgresults(2,:)','o--','Linewidth',3,'MarkerSize',15,'MarkerFaceColor','auto','Color',0.6*[1 1 1])
%     % errorbar(avgresults',stdresults','Linewidth',3)
            errorbar(avgresults(1,:),stdresults(1,:),'d-','Color',[0 0 0],'LineWidth',3,'MarkerFaceColor','auto','MarkerSize',10)
            errorbar(avgresults(2,:),stdresults(2,:),'o--','Color',0.6*[1 1 1],'LineWidth',3,'MarkerFaceColor','auto','MarkerSize',10)
    ylim([min(avgresults(:))-0.01 max(avgresults(:))+0.01]);    
    set(gca,'XTick',1:numel(varparam))
    set(gca,'XTickLabel',cellstr(int2str(varparam')))
    ylabel('soution value','FontSize',12);
    xlabel('number of function evaluations','FontSize',12);
%     legend('StoSOO','Matlab fminbnd','Location','Best');
%     legend('boxoff')
    make_this_figure_tight
    saveas(gcf,'current.pdf');
    
end

% settings.type = 'det';
% [x y t] = stosoo(sin1,settings);
% fprintf(1,'StoSOO found: f(%f) = %f [%f]\n', x,y,sin1(x));
%
% options = optimset('MaxFunEvals',settings.nb_iter,'MaxIter',1000000,'Display','off');
% [xm,ym] = fminbnd(sin1_minus,0,1,options);
% fprintf(1,'Matlab found: f(%f) = %f [%f]\n', xm,-ym,sin1(xm));