function draw_partition(x,x_min,x_max,leaf,new,y,sums, ks,h_max,settings)

nb_iter = 1000;
for h=1:h_max
    for i=1:numel(x{h})
        if (leaf{h}(i) == 1)
%             ag_set_pen_color(AG_BLACK);
%             ag_line(dyv_ref(x_min[h],i),0.02,dyv_ref(x_min[h],i),-0.02);
%             ag_line(dyv_ref(x_max[h],i),0.02,dyv_ref(x_max[h],i),-0.02);
            %         ag_set_pen_color(AG_BLUE);
            plot(x{h}(i),y{h}(i),'sr','MarkerSize',10);
            meanF = sums{h}(i)/ks{h}(i);
            if (ks{h}(i) > 0)
                b_hi =  meanF + sqrt(log(nb_iter*nb_iter/settings.delta)/(2*ks{h}(i)));
            else
                b_hi = inf;
            end
            
%             ag_set_pen_color(AG_BLACK);
            plot(x{h}(i),meanF);
            plot(x{h}(i),b_hi);
%             ag_set_pen_color(AG_GREEN);
            plot(x{h}(i),b_hi);
            c = sprintf('%d',ks{h}(i));
%             ag_set_pen_color(AG_BLACK);
            text(x{h}(i)+0.005,b_hi+0.005,c);
            % 	printf("i: %f, b_hi: %f, y_hi: %f, mean: %f, ks: %d \n",...
%             dyv_ref(x[h],i),b_hi,dyv_ref(y[h],i),meanF, ivec_ref(ks[h],i));            
        end
    end
end
drawnow